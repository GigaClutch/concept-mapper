"""Recall proxy (D6, promised since Phase 2): compare the graph against SEP's
own "Related Entries".

For every cached article, the entries SEP's editors list as related are a
free, human-curated hint of what a good graph should connect. This report
answers, per article: of the related entries that resolve to registry nodes,
how many are linked (directly, or one hop via the article's own grounded
nodes) in our graph? Zero API cost — everything comes from cache/ and data/.

  python pipeline/recall_proxy.py [--verbose]

Writes data/recall_proxy.json and prints a per-article summary. The number is
a coverage *proxy*, not a target to game: SEP relates entries for reasons
beyond our edge taxonomy (biography, history, methodology), so 100% is not
expected — watch the trend across pipeline changes, not the absolute value.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from common import atomic_write, load_registry

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
ARTICLE_CACHE = ROOT / "cache" / "sep" / "articles"


def extract_related(text: str) -> list[str]:
    i = text.rfind("Related Entries")
    if i == -1:
        return []
    tail = text[i + len("Related Entries"):]
    m = re.search(r"Copyright\s*©", tail)
    if m:
        tail = tail[:m.start()]
    return [t.strip() for t in tail.split("|") if t.strip()]


def title_variants(title: str) -> list[str]:
    """SEP styles: 'Kant, Immanuel' (person), 'ethics: deontological' (topic)."""
    out = [title]
    if ":" in title:
        head, sub = title.split(":", 1)
        out += [head.strip(), f"{sub.strip()} {head.strip()}"]
    elif ", " in title:
        parts = [p.strip() for p in title.split(",")]
        if len(parts) == 2:
            out.append(f"{parts[1]} {parts[0]}")  # 'Kant, Immanuel' -> 'Immanuel Kant'
    return out


def main() -> None:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--verbose", action="store_true",
                    help="list unresolved and unlinked entries per article")
    args = ap.parse_args()

    _, _, _, resolve = load_registry()
    graph = json.loads((DATA / "graph.json").read_text(encoding="utf-8"))
    neighbors: dict[str, set] = {}
    for e in graph["edges"]:
        neighbors.setdefault(e["source"], set()).add(e["target"])
        neighbors.setdefault(e["target"], set()).add(e["source"])
    # nodes each article grounds: endpoints of edges carrying its evidence
    grounded_by: dict[str, set] = {}
    for e in graph["edges"]:
        for ev in e["evidence"]:
            grounded_by.setdefault(ev["article_id"], set()).update(
                (e["source"], e["target"]))

    report, tot_rel, tot_res, tot_cov = [], 0, 0, 0
    for txt_file in sorted(ARTICLE_CACHE.glob("*.txt")):
        aid = txt_file.stem
        related = extract_related(txt_file.read_text(encoding="utf-8"))
        if not related:
            continue
        anchor = grounded_by.get(aid, set())
        resolved, covered, missing = [], [], []
        for title in related:
            rid = next((resolve[v.casefold()] for v in title_variants(title)
                        if v.casefold() in resolve), None)
            if rid is None:
                missing.append(title)
                continue
            resolved.append(rid)
            # linked = in the article's own grounded set, or one hop from it
            if rid in anchor or (neighbors.get(rid, set()) & anchor):
                covered.append(rid)
        report.append({
            "article_id": aid, "related_entries": len(related),
            "resolved": len(resolved), "linked": len(covered),
            "unlinked": sorted(set(resolved) - set(covered)),
            "unresolved": missing,
        })
        tot_rel += len(related)
        tot_res += len(resolved)
        tot_cov += len(covered)
        line = (f"{aid}: {len(covered)}/{len(resolved)} resolved entries linked "
                f"({len(related)} related, {len(missing)} outside registry)")
        print(line)
        if args.verbose and set(resolved) - set(covered):
            print(f"   unlinked: {', '.join(sorted(set(resolved) - set(covered)))}")

    pct = 100 * tot_cov / tot_res if tot_res else 0.0
    print(f"\nTOTAL: {tot_cov}/{tot_res} resolved related-entries linked "
          f"({pct:.0f}%); {tot_rel - tot_res} of {tot_rel} lie outside the "
          f"registry (expected — bounded domain)")
    atomic_write(DATA / "recall_proxy.json", {
        "meta": {"linked": tot_cov, "resolved": tot_res,
                 "related_total": tot_rel, "linked_pct": round(pct, 1)},
        "articles": report})
    print(f"wrote data/recall_proxy.json")


if __name__ == "__main__":
    main()

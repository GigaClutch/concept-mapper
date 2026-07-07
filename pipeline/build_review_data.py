"""Bundle the review queue into viewer/review.data.js (for file:// loading).

Inputs: data/verification_sample.json, data/quarantine/proposed_edges.json,
data/quarantine/proposed_nodes.json, and the live provisional content in
data/graph.json that browse-time research (D7) added — provisional nodes and
research-origin edges that have not been human-confirmed yet. Items that
already carry a verdict are included (the page shows them as already decided).
Re-run after any of the inputs change.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from common import atomic_write

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def load(path: Path, fallback):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else fallback


def main() -> None:
    registry = json.loads((DATA / "registry.json").read_text(encoding="utf-8"))
    corpus = json.loads((DATA / "corpus.json").read_text(encoding="utf-8"))
    graph = json.loads((DATA / "graph.json").read_text(encoding="utf-8"))
    sample = load(DATA / "verification_sample.json", {"sample": []})
    pedges = load(DATA / "quarantine" / "proposed_edges.json", {"proposals": []})
    pnodes = load(DATA / "quarantine" / "proposed_nodes.json", {"proposed_nodes": []})
    assist = load(DATA / "review_assist.json", {"items": {}}).get("items", {})

    def with_assist(section, items, keyfn):
        for it in items:
            a = assist.get(f"{section}|{keyfn(it)}")
            if a:
                it["assist"] = {"verdict": a["verdict"], "quote_check": a["quote_check"],
                                "reason": a["reason"], "model": a["model"]}
        return items

    ek = lambda it: f"{it['source']}|{it['type']}|{it['target']}"

    # browse-time research (D7) writes provisional content straight into the
    # graph so it shows live; surface it here so it is still governed by review.
    researched_edges = [
        {"source": e["source"], "type": e["type"], "target": e["target"],
         "quote": e["evidence"][0]["quote"] if e.get("evidence") else "",
         "article_id": e["evidence"][0]["article_id"] if e.get("evidence") else ""}
        for e in graph["edges"]
        if e.get("origin") == "research" and e.get("status") == "unverified"]
    researched_nodes = [
        {"id": n["id"], "label": n["label"], "type": n["type"],
         "definition": n.get("definition", ""),
         "reason": n.get("definition", "")}
        for n in graph["nodes"] if n.get("status") == "provisional"]

    # decided items leave the queue: applied sample verdicts, accepted/rejected
    # proposals, and ruled-on node suggestions stay in their data files as the
    # audit trail but are no longer review work
    sections = {
        "sample": with_assist("sample", [s for s in sample["sample"]
                                         if not s.get("verdict")], ek),
        "proposed_edges": with_assist("proposed_edges", [
            p for p in pedges["proposals"]
            if p.get("status", "quarantined") == "quarantined"], ek),
        "proposed_nodes": with_assist("proposed_nodes", [
            p for p in pnodes["proposed_nodes"] if not p.get("status")],
            lambda it: it["label"]),
        "researched_edges": with_assist("researched_edges", researched_edges, ek),
        "researched_nodes": with_assist("researched_nodes", researched_nodes, lambda it: it["id"]),
    }
    # every item carries a stable identity key: review.html stores verdicts by
    # it (never by array position, which shifts whenever the queue is rebuilt);
    # proposed_edges include the article because one triple can be proposed by
    # several articles
    for name, items in sections.items():
        for it in items:
            it["key"] = (it["label"] if name == "proposed_nodes"
                         else it["id"] if name == "researched_nodes"
                         else ek(it) + (f"|{it.get('article_id', '')}"
                                        if name == "proposed_edges" else ""))

    bundle = {
        # deterministic: same queue -> same bundle bytes (no wall-clock stamp);
        # the page uses this to detect that saved decisions predate a rebuild
        "fingerprint": hashlib.sha256(json.dumps(
            {n: [it["key"] for it in items] for n, items in sections.items()},
            sort_keys=True).encode("utf-8")).hexdigest()[:16],
        "labels": {r["id"]: {"label": r["label"], "type": r["type"]}
                   for r in registry["nodes"]},
        "articles": {a["id"]: {"title": a["title"], "url": a["url"]}
                     for a in corpus["articles"]},
        **sections,
    }
    out = ROOT / "viewer" / "review.data.js"
    atomic_write(out, "window.REVIEW = " + json.dumps(bundle, indent=1, ensure_ascii=False)
                 + ";\n")
    print(f"wrote {out.relative_to(ROOT)}: {len(bundle['sample'])} sampled edges, "
          f"{len(bundle['proposed_edges'])} proposed edges, "
          f"{len(bundle['proposed_nodes'])} proposed nodes, "
          f"{len(researched_edges)} researched edges, "
          f"{len(researched_nodes)} researched nodes")


if __name__ == "__main__":
    main()

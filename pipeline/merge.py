"""Merge seeds + Wikidata enrichment + SEP contents -> data/registry.json + data/corpus.json.

The registry is the closed world (D3): every node in any generated graph must
have a row here. Rows carry the curated label/aliases plus Wikidata QID,
description, aliases and dates where resolved. corpus.json is the bounded
Ethics article list (curated ids verified against the scraped SEP contents).
Provisional rows added by browse-time research (D7) are carried forward from
the existing registry; every check runs before anything is written.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from common import atomic_write, preserve_built

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

SEP_BASE = "https://plato.stanford.edu/entries"


def fmt_year(y: int | None) -> str:
    if y is None:
        return ""
    return f"{-y} BCE" if y < 0 else str(y)


def time_period(etype: str, enr: dict, seed: dict) -> str:
    if etype == "person":
        b, d = enr.get("birth_year"), enr.get("death_year")
        if b is not None:
            return f"{fmt_year(b)}–{fmt_year(d)}" if d is not None else fmt_year(b)
        return ""
    if etype == "work":
        y = enr.get("pub_year") or seed.get("year")
        return fmt_year(y)
    return ""


def merge_aliases(seed: dict, enr: dict) -> list[str]:
    seen = {seed["label"].casefold()}
    out: list[str] = []
    for a in seed.get("aliases", []) + enr.get("wd_aliases", []):
        if a.casefold() not in seen:
            seen.add(a.casefold())
            out.append(a)
    return out


def main() -> None:
    seeds = json.loads((DATA / "seeds.json").read_text(encoding="utf-8"))
    enrichment = {e["id"]: e for e in json.loads(
        (DATA / "wikidata_enrichment.json").read_text(encoding="utf-8"))["entries"]}
    contents = {e["id"]: e["title"] for e in json.loads(
        (DATA / "sep_contents.json").read_text(encoding="utf-8"))["entries"]}

    groups = [("concept", seeds["concepts"]), ("person", seeds["persons"]),
              ("school", seeds["schools"]), ("work", seeds["works"])]
    rows = []
    for etype, entries in groups:
        for seed in entries:
            enr = enrichment.get(seed["id"])
            if enr is None:
                sys.exit(f"no enrichment for seed {seed['id']} — rerun wikidata_bootstrap.py")
            rows.append({
                "id": seed["id"],
                "label": seed["label"],
                "type": etype,
                "aliases": merge_aliases(seed, enr),
                "domain": seeds["meta"]["domain"],
                "time_period": time_period(etype, enr, seed),
                "wikidata_qid": enr["wikidata_qid"],
                "qid_source": enr["qid_source"],
                "wd_description": enr["wd_description"],
                "note": seed.get("note", ""),
                "author_id": seed.get("author_id", ""),
                "status": "registry",
            })

    dup = {r["id"] for r in rows if sum(x["id"] == r["id"] for x in rows) > 1}
    if dup:
        sys.exit(f"duplicate registry ids: {sorted(dup)}")

    # carry forward provisional rows added by browse-time research (D7): they
    # are absent from seeds.json but graph nodes depend on them (D3)
    out = DATA / "registry.json"
    ids = {r["id"] for r in rows}
    if out.exists():
        for r in json.loads(out.read_text(encoding="utf-8"))["nodes"]:
            if r.get("status") == "provisional" and r["id"] not in ids:
                rows.append(r)
                ids.add(r["id"])
                print(f"carried forward provisional row: {r['id']}")

    registry = {
        "meta": {
            "version": seeds["meta"]["version"],
            "built": time.strftime("%Y-%m-%d"),
            "domain": seeds["meta"]["domain"],
            "count": len(rows),
            "qid_sources": {
                s: sum(1 for r in rows if r["qid_source"] == s)
                for s in sorted({r["qid_source"] for r in rows})},
        },
        "nodes": rows,
    }

    # carry forward per-article bookkeeping (retrieved date, grounding counters)
    # so a registry re-run never resets what ground.py apply recorded
    out_corpus = DATA / "corpus.json"
    prev_articles = {}
    if out_corpus.exists():
        prev_articles = {a["id"]: a for a in json.loads(
            out_corpus.read_text(encoding="utf-8"))["articles"]}
    corpus_rows = []
    for c in seeds["sep_corpus"]:
        if c["id"] not in contents:
            sys.exit(f"corpus id {c['id']} not in SEP contents — fix seeds.json")
        prev = prev_articles.get(c["id"], {})
        corpus_rows.append({
            "id": c["id"], "title": contents[c["id"]],
            "url": f"{SEP_BASE}/{c['id']}/", "priority": c["priority"],
            "retrieved": prev.get("retrieved", ""),
            "grounded_edges": prev.get("grounded_edges", 0),
            "proposed_edges": prev.get("proposed_edges", 0),
        })
    corpus = {"meta": {"built": time.strftime("%Y-%m-%d"), "count": len(corpus_rows)},
              "articles": corpus_rows}

    # closed-world check (D3), BEFORE any write: every node already in the
    # graph must be registered — on failure nothing on disk changes
    graph = json.loads((DATA / "graph.json").read_text(encoding="utf-8"))
    missing = [n["id"] for n in graph["nodes"] if n["id"] not in ids]
    if missing:
        sys.exit(f"graph nodes missing from registry: {missing}")

    atomic_write(out, preserve_built(out, registry))
    print(f"wrote {out.relative_to(ROOT)} ({len(rows)} rows)")
    print(json.dumps(registry["meta"]["qid_sources"], indent=2))
    atomic_write(out_corpus, preserve_built(out_corpus, corpus))
    print(f"wrote {out_corpus.relative_to(ROOT)} ({len(corpus_rows)} articles)")
    print("all graph nodes covered by registry")


if __name__ == "__main__":
    main()

"""Bundle the review queue into viewer/review.data.js (for file:// loading).

Inputs: data/verification_sample.json, data/quarantine/proposed_edges.json,
data/quarantine/proposed_nodes.json, and the live provisional content in
data/graph.json that browse-time research (D7) added — provisional nodes and
research-origin edges that have not been human-confirmed yet. Items that
already carry a verdict are included (the page shows them as already decided).
Re-run after any of the inputs change.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

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

    bundle = {
        "built": time.strftime("%Y-%m-%d"),
        "labels": {r["id"]: {"label": r["label"], "type": r["type"]}
                   for r in registry["nodes"]},
        "articles": {a["id"]: {"title": a["title"], "url": a["url"]}
                     for a in corpus["articles"]},
        "sample": with_assist("sample", sample["sample"], ek),
        "proposed_edges": with_assist("proposed_edges", pedges["proposals"], ek),
        "proposed_nodes": with_assist("proposed_nodes", pnodes["proposed_nodes"], lambda it: it["label"]),
        "researched_edges": with_assist("researched_edges", researched_edges, ek),
        "researched_nodes": with_assist("researched_nodes", researched_nodes, lambda it: it["id"]),
    }
    out = ROOT / "viewer" / "review.data.js"
    out.write_text("window.REVIEW = " + json.dumps(bundle, indent=1, ensure_ascii=False)
                   + ";\n", encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)}: {len(bundle['sample'])} sampled edges, "
          f"{len(bundle['proposed_edges'])} proposed edges, "
          f"{len(bundle['proposed_nodes'])} proposed nodes, "
          f"{len(researched_edges)} researched edges, "
          f"{len(researched_nodes)} researched nodes")


if __name__ == "__main__":
    main()

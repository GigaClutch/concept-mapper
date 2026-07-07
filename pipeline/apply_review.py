"""Apply exported review decisions (Phase 5) to the graph and quarantine files.

Reads data/review_decisions.json (downloaded from viewer/review.html):
  - spot-check sample: accept -> edge status "confirmed";
    reject -> edge removed (and any node it orphans removed with it)
  - proposed edges: accept -> merged into graph.json with its evidence quote
    (origin "grounding", domain/range + closed-world checked);
    reject -> recorded in quarantine with status "rejected"
  - proposed nodes: verdicts recorded in quarantine; accepted ones are flagged
    for seeds.json at the next registry expansion (never auto-added — D3)

Weights are recomputed for every edge, verdicts are written back into
data/verification_sample.json, and decided proposals keep an audit trail.
Afterwards run: metrics.py, validate.py, evaluate.py --graph,
build_viewer_data.py, build_review_data.py.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from backbone import DOMAIN_RANGE, node_from_registry
from common import atomic_write, recompute_weights
from validate import edge_key

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DECISIONS = DATA / "review_decisions.json"
QUAR_EDGES = DATA / "quarantine" / "proposed_edges.json"
QUAR_NODES = DATA / "quarantine" / "proposed_nodes.json"
SAMPLE = DATA / "verification_sample.json"

TODAY = time.strftime("%Y-%m-%d")


def main() -> None:
    if not DECISIONS.exists():
        sys.exit(f"no {DECISIONS.relative_to(ROOT)} — export from viewer/review.html "
                 "and save the download there first")
    dec = json.loads(DECISIONS.read_text(encoding="utf-8"))["decisions"]
    graph = json.loads((DATA / "graph.json").read_text(encoding="utf-8"))
    registry = json.loads((DATA / "registry.json").read_text(encoding="utf-8"))
    nodes = {r["id"]: r for r in registry["nodes"]}
    by_key = {edge_key(e["source"], e["target"], e["type"]): e for e in graph["edges"]}

    # --- spot-check sample -------------------------------------------------
    sample_doc = json.loads(SAMPLE.read_text(encoding="utf-8"))
    sample_by_key = {edge_key(s["source"], s["target"], s["type"]): s
                     for s in sample_doc["sample"]}
    confirmed = removed = 0
    for d in dec.get("sample", []):
        if d["verdict"] not in ("accept", "reject"):
            continue
        k = edge_key(d["source"], d["target"], d["type"])
        if k in sample_by_key:
            sample_by_key[k]["verdict"] = d["verdict"]
            sample_by_key[k]["notes"] = d.get("note", "")
        e = by_key.get(k)
        if e is None:
            continue
        if d["verdict"] == "accept":
            if e["status"] in ("unverified", "grounded"):
                e["status"] = "confirmed"
            confirmed += 1
        else:
            graph["edges"].remove(e)
            del by_key[k]
            removed += 1
            print(f"removed: {d['source']} -{d['type']}-> {d['target']}"
                  f"{' — ' + d['note'] if d.get('note') else ''}")

    # --- auto-researched provisional content, live in the graph (D7) -------
    drop_node_ids = {d.get("id") for d in dec.get("researched_nodes", [])
                     if d.get("verdict") == "reject" and d.get("id")}
    accept_node_ids = {d.get("id") for d in dec.get("researched_nodes", [])
                       if d.get("verdict") == "accept" and d.get("id")}
    res_confirmed = res_removed = 0
    for d in dec.get("researched_edges", []):
        if d["verdict"] not in ("accept", "reject"):
            continue
        e = by_key.get(edge_key(d["source"], d["target"], d["type"]))
        if e is None:
            continue
        if d["verdict"] == "reject":
            graph["edges"].remove(e)
            del by_key[edge_key(d["source"], d["target"], d["type"])]
            res_removed += 1
        else:
            e["status"] = "confirmed"
            res_confirmed += 1
    # rejecting a provisional node takes any remaining edges that need it
    for e in list(graph["edges"]):
        if e["source"] in drop_node_ids or e["target"] in drop_node_ids:
            graph["edges"].remove(e)
            by_key.pop(edge_key(e["source"], e["target"], e["type"]), None)
    graph["nodes"] = [n for n in graph["nodes"] if n["id"] not in drop_node_ids]

    # --- proposed edges ----------------------------------------------------
    quar = json.loads(QUAR_EDGES.read_text(encoding="utf-8"))
    prop_by_key = {}
    for p in quar["proposals"]:
        prop_by_key.setdefault(
            (p["source"], p["type"], p["target"], p.get("article_id")), p)
    merged = declined = 0
    for d in dec.get("proposed_edges", []):
        if d["verdict"] not in ("accept", "reject"):
            continue
        p = prop_by_key.get((d["source"], d["type"], d["target"], d.get("article_id")))
        if p is None:
            print(f"WARN: decision for unknown proposal "
                  f"{d['source']} -{d['type']}-> {d['target']}")
            continue
        p["status"] = "accepted" if d["verdict"] == "accept" else "rejected"
        p["decided"] = TODAY
        if d.get("note"):
            p["note"] = d["note"]
        if d["verdict"] == "reject":
            declined += 1
            continue
        k = edge_key(d["source"], d["target"], d["type"])
        if k in by_key:  # another article's copy already merged
            e = by_key[k]
            if not any(ev["article_id"] == p["article_id"] for ev in e["evidence"]):
                e["evidence"].append({"article_id": p["article_id"],
                                      "quote": p["quote"]})
            continue
        dom, rng = DOMAIN_RANGE[d["type"]]
        if nodes[d["source"]]["type"] not in dom or nodes[d["target"]]["type"] not in rng:
            print(f"WARN: accepted proposal violates domain/range, skipped: "
                  f"{d['source']} -{d['type']}-> {d['target']}")
            continue
        e = {"source": d["source"], "target": d["target"], "type": d["type"],
             "weight": 0.5, "origin": "grounding",
             "extractor": {"model": "claude-haiku-4-5", "prompt_version": "gr-v2",
                           "date": TODAY},
             "evidence": [{"article_id": p["article_id"], "quote": p["quote"]}],
             "status": "confirmed"}
        graph["edges"].append(e)
        by_key[k] = e
        merged += 1
        node_ids = {n["id"] for n in graph["nodes"]}
        for end in (d["source"], d["target"]):
            if end not in node_ids:
                graph["nodes"].append(node_from_registry(nodes[end]))

    # --- proposed nodes ----------------------------------------------------
    qn = json.loads(QUAR_NODES.read_text(encoding="utf-8"))
    pn_by_label = {p["label"].casefold(): p for p in qn["proposed_nodes"]}
    flagged = 0
    for d in dec.get("proposed_nodes", []):
        if d["verdict"] not in ("accept", "reject"):
            continue
        p = pn_by_label.get(d["label"].casefold())
        if p is None:
            continue
        p["status"] = ("approved — add to seeds.json at next registry expansion"
                       if d["verdict"] == "accept" else "rejected")
        p["decided"] = TODAY
        if d.get("note"):
            p["note"] = d["note"]
        flagged += d["verdict"] == "accept"

    # --- weights, orphans, write-out ---------------------------------------
    recompute_weights(graph["edges"])
    linked = set()
    for e in graph["edges"]:
        linked.add(e["source"])
        linked.add(e["target"])
    orphans = [n for n in graph["nodes"] if n["id"] not in linked]
    for n in orphans:
        graph["nodes"].remove(n)
        print(f"removed orphaned node: {n['id']}")

    # promote accepted provisional nodes that survived; prune provisional
    # registry rows whose graph node is gone (rejected or orphaned out)
    graph_ids = {n["id"] for n in graph["nodes"]}
    res_kept = 0
    for n in graph["nodes"]:
        if n["id"] in accept_node_ids and n.get("status") == "provisional":
            n["status"] = "curated"
            res_kept += 1
    for r in registry["nodes"]:
        if r["id"] in accept_node_ids and r.get("status") == "provisional":
            r["status"] = "curated"
    registry["nodes"] = [r for r in registry["nodes"]
                         if r.get("status") != "provisional" or r["id"] in graph_ids]
    registry["meta"]["count"] = len(registry["nodes"])

    graph["meta"]["built"] = TODAY
    atomic_write(DATA / "graph.json", graph)
    atomic_write(DATA / "registry.json", registry)
    atomic_write(SAMPLE, sample_doc)
    atomic_write(QUAR_EDGES, quar)
    atomic_write(QUAR_NODES, qn)
    print(f"sample: {confirmed} confirmed, {removed} removed; "
          f"researched: {res_confirmed} confirmed, {res_removed} removed, "
          f"{res_kept} provisional entries kept; proposals: {merged} merged, "
          f"{declined} rejected; {flagged} new entries flagged "
          f"(+{len(orphans)} orphaned nodes dropped)")
    print("now run: metrics.py, validate.py, evaluate.py --graph, "
          "build_viewer_data.py, build_review_data.py")


if __name__ == "__main__":
    main()

"""On-demand node research (D7): expand the graph around one node, lazily.

research_node(node_id) is the unit the browse-time researcher runs when the
viewer lands on a node whose research status is not yet "researched":

  1. find the node's SEP entry via data/sep_contents.json (label/alias/surname
     match), fetch + cache it politely (scrape_sep machinery)
  2. one claude-haiku-4-5 call (structured outputs, rs-v1):
       - grounded_edges between EXISTING registry ids, each with a verbatim quote
       - up to 8 provisional new_nodes central to the focus node
       - new_edges wiring every new node in, each with a verbatim quote
  3. validate everything mechanically: quotes verbatim against the cached
     source, closed-world resolution (a "new" node that is really an existing
     row gets resolved to it), edge types + domain/range, dedupe, no orphans
  4. apply with provenance: registry rows status "provisional" (qid unresolved,
     for the next Wikidata pass), graph nodes status "provisional", edges
     origin "research" + evidence; the focus node gets a research stamp so it
     is never re-researched; weights recomputed; metrics refreshed

Every write goes through apply() which returns the delta the viewer merges
live. The caller (serve.py) runs validate.py afterwards and rolls back on any
failure, so the graph on disk is never left red. Provisional material is
reviewable in review.html like any other quarantined claim.
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path

import metrics as metrics_mod
import networkx  # noqa: F401  (fail fast here, not mid-apply, if missing)
from backbone import DOMAIN_RANGE, node_from_registry
from common import (PRICES, atomic_write, call_cost, load_key, load_registry,
                    recompute_weights, registry_index, retry_messages_create)
from ground import MAX_QUOTE_CHARS, find_verbatim
from scrape_sep import fetch_article
from validate import EDGE_TYPES, edge_key

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
ARTICLE_CACHE = ROOT / "cache" / "sep" / "articles"
SEP_BASE = "https://plato.stanford.edu/entries"

# spend of the most recent research_node call, even when it later raised —
# serve.py adds this to its session meter on the failure path
LAST_COST = 0.0

PROMPT_VERSION = "rs-v1"
MODEL = "claude-haiku-4-5"
MAX_NEW_NODES = 8
# the org tier rejects single requests beyond ~50K input tokens/minute, and
# the longest SEP entries exceed that — cap the source text we send
MAX_SOURCE_CHARS = 120_000

SCHEMA = {
    "type": "object",
    "properties": {
        "grounded_edges": {"type": "array", "items": {
            "type": "object",
            "properties": {"source": {"type": "string"}, "type": {"type": "string"},
                           "target": {"type": "string"}, "quote": {"type": "string"}},
            "required": ["source", "type", "target", "quote"],
            "additionalProperties": False}},
        "new_nodes": {"type": "array", "items": {
            "type": "object",
            "properties": {"label": {"type": "string"}, "type": {"type": "string"},
                           "definition": {"type": "string"},
                           "aliases": {"type": "array", "items": {"type": "string"}}},
            "required": ["label", "type", "definition", "aliases"],
            "additionalProperties": False}},
        "new_edges": {"type": "array", "items": {
            "type": "object",
            "properties": {"source": {"type": "string"}, "type": {"type": "string"},
                           "target": {"type": "string"}, "quote": {"type": "string"}},
            "required": ["source", "type", "target", "quote"],
            "additionalProperties": False}},
    },
    "required": ["grounded_edges", "new_nodes", "new_edges"],
    "additionalProperties": False,
}


def slugify(label: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "_", label.casefold()).strip("_")
    return s or "node"


def find_sep_sources(node: dict, contents: list[dict], limit: int = 2) -> list[dict]:
    """Match SEP entries to a node: exact-ish title hits first, then looser."""
    names = [node["label"]] + node.get("aliases", [])
    if node["type"] == "person":
        names.append(node["label"].split()[-1])  # SEP titles persons "Surname, First"
    names = [n.casefold() for n in names if len(n) >= 4]
    scored = []
    for e in contents:
        title = e["title"].casefold()
        head = title.split(":")[0]
        for n in names:
            if head == n or head.startswith(n + ",") or head.startswith(n + " ("):
                scored.append((0, e))
                break
            if re.search(rf"\b{re.escape(n)}\b", title):
                scored.append((1, e))
                break
    scored.sort(key=lambda t: (t[0], len(t[1]["title"])))
    return [e for _, e in scored[:limit]]


TYPE_GLOSS = """\
IS_A: X is a kind of Y | PART_OF: X is a constituent of Y | SUBCATEGORY_OF: X is \
the narrower category | DEVELOPED_BY: concept/school developed by person | \
EXTENDED_BY: concept/school extended by later person | DERIVED_FROM: X grew out \
of Y | INFLUENCED_BY: later thinker influenced by earlier | CONTRASTS_WITH: \
standard opposition (symmetric) | CRITIQUES: X argues against Y | RESPONDS_TO: \
X reacts to Y | AUTHORED_BY: work written by person | INTRODUCED_IN: concept \
first stated in work"""


def build_prompt(node: dict, rows: list[dict], article_id: str, text: str) -> str:
    return (
        f"You are expanding a typed knowledge graph of academic philosophy around "
        f"one focus node, using the Stanford Encyclopedia of Philosophy entry "
        f"'{article_id}'.\n\n"
        f"FOCUS NODE: {node['label']} (id: {node['id']}, type: {node['type']})\n\n"
        f"Relationship types: {TYPE_GLOSS}\n\n"
        "Produce three things:\n"
        "1. grounded_edges — relationships between EXISTING registry ids (below) "
        "that this article clearly states, ideally involving the focus node. "
        f"Each needs a quote copied EXACTLY, character for character, from the "
        f"article text (single contiguous span, <= {MAX_QUOTE_CHARS} chars) that "
        "explicitly names or unmistakably refers to BOTH endpoints and supports "
        "the SPECIFIC relationship and direction. A tangential quote is worse "
        "than none — omit when in doubt. At most 15.\n"
        f"2. new_nodes — up to {MAX_NEW_NODES} entities (concept|person|school|"
        "work) that are textbook-central to the focus node's thought and MISSING "
        "from the registry. No minor figures, no near-duplicates of existing "
        "rows. definition: <= 220 chars IN YOUR OWN WORDS (never copied text). "
        "aliases: alternative names, may be empty.\n"
        "3. new_edges — relationships involving at least one new node (use the "
        "new node's label as its id), same strict quote rules. EVERY new node "
        "must appear in at least one new edge; a new node you cannot connect "
        "with a quoted edge must be dropped.\n\n"
        "Direction reminders: persons are never the source of DEVELOPED_BY/"
        "EXTENDED_BY/AUTHORED_BY; the earlier thinker is never INFLUENCED_BY "
        "the later.\n\n"
        f"## Existing registry ids (closed world)\n\n{registry_index(rows, rich=False)}\n\n"
        f"## Article text ({article_id})\n\n{text[:MAX_SOURCE_CHARS]}\n"
    )


def research_node(node_id: str, max_cost: float = 0.30) -> dict:
    """Run one research pass; returns the delta dict (also applied to disk)."""
    import anthropic

    global LAST_COST
    LAST_COST = 0.0
    graph = json.loads((DATA / "graph.json").read_text(encoding="utf-8"))
    registry, rows, by_id, resolve = load_registry()
    gnode = next((n for n in graph["nodes"] if n["id"] == node_id), None)
    if gnode is None or node_id not in by_id:
        return {"error": f"unknown node '{node_id}'"}
    if (gnode.get("research") or {}).get("status") == "researched":
        return {"error": "already researched", "already": True}

    contents = json.loads((DATA / "sep_contents.json").read_text(encoding="utf-8"))
    sources = find_sep_sources(by_id[node_id], contents["entries"])
    if not sources:
        gnode["research"] = {"status": "no_source", "date": time.strftime("%Y-%m-%d"),
                             "sources": []}
        _write(graph, registry)
        return {"researched": False, "reason": "no SEP entry found for this node",
                "focus": gnode, "cost": 0.0, "new_nodes": [], "new_edges": [],
                "grounded": 0, "articles": [], "metrics": _metrics_map()}

    art = sources[0]
    txt_file = ARTICLE_CACHE / f"{art['id']}.txt"
    if not txt_file.exists():
        fetch_article(art["id"], refresh=False)
    text = txt_file.read_text(encoding="utf-8")

    client = anthropic.Anthropic(api_key=load_key())
    prompt = build_prompt(by_id[node_id], rows, art["id"], text)
    # enforce max_cost BEFORE spending: a conservative input-token estimate
    # (~4 chars/token) already dominates the cost of one Haiku call
    in_p, _ = PRICES[MODEL]
    est = len(prompt) / 4 * in_p / 1e6
    if est > max_cost:
        return {"error": f"estimated call cost ${est:.2f} exceeds the "
                         f"${max_cost:.2f} per-call cap"}
    resp = retry_messages_create(
        client, attempts=3, min_wait=20, model=MODEL, max_tokens=16000,
        messages=[{"role": "user", "content": prompt}],
        output_config={"format": {"type": "json_schema", "schema": SCHEMA}},
    )
    if resp is None:
        return {"error": "rate-limited, try again in a minute"}
    cost = call_cost(MODEL, resp.usage)
    LAST_COST = cost
    if resp.stop_reason == "max_tokens":
        return {"error": "model response truncated; try again", "cost": cost}
    raw = json.loads(next(b.text for b in resp.content if b.type == "text"))

    existing_keys = {edge_key(e["source"], e["target"], e["type"])
                     for e in graph["edges"]}
    node_ids_in_graph = {n["id"] for n in graph["nodes"]}
    today = time.strftime("%Y-%m-%d")
    extractor = {"model": MODEL, "prompt_version": PROMPT_VERSION, "date": today}

    # --- provisional new nodes (resolve duplicates back to existing rows) ----
    accepted_nodes: dict[str, dict] = {}   # prompt-label.casefold() -> registry row
    for p in raw.get("new_nodes", [])[:MAX_NEW_NODES]:
        label = (p.get("label") or "").strip()
        ntype = p.get("type")
        if not label or ntype not in {"concept", "person", "school", "work"}:
            continue
        if label.casefold() in resolve:
            continue  # already exists — edges naming it resolve to the old id
        nid = slugify(label)
        if nid in by_id or nid in accepted_nodes:
            continue
        row = {"id": nid, "label": label, "type": ntype,
               "aliases": [a for a in p.get("aliases", []) if a and a.casefold() != label.casefold()][:4],
               "domain": by_id[node_id].get("domain", ""),
               "time_period": "", "wikidata_qid": "", "qid_source": "unresolved",
               "wd_description": "", "note": f"auto-research around {node_id} ({art['id']})",
               "author_id": "", "status": "provisional",
               "definition": (p.get("definition") or "")[:220]}
        accepted_nodes[label.casefold()] = row

    def endpoint(raw_id: str) -> str | None:
        rid = resolve.get(str(raw_id).casefold())
        if rid:
            return rid
        row = accepted_nodes.get(str(raw_id).casefold())
        if row:
            return row["id"]
        return slugify(str(raw_id)) if slugify(str(raw_id)) in {r["id"] for r in accepted_nodes.values()} else None

    new_edges, used_new = [], set()
    for kind in ("grounded_edges", "new_edges"):
        for e in raw.get(kind, []):
            etype = e.get("type")
            if etype not in EDGE_TYPES:
                continue
            s, t = endpoint(e.get("source")), endpoint(e.get("target"))
            if s is None or t is None or s == t:
                continue
            vq = find_verbatim(e.get("quote", ""), text)
            if vq is None:
                continue
            stype = (by_id.get(s) or next(r for r in accepted_nodes.values() if r["id"] == s))["type"]
            ttype = (by_id.get(t) or next(r for r in accepted_nodes.values() if r["id"] == t))["type"]
            dom, rng = DOMAIN_RANGE[etype]
            if stype not in dom or ttype not in rng:
                continue
            k = edge_key(s, t, etype)
            if k in existing_keys:
                edge = next(x for x in graph["edges"]
                            if edge_key(x["source"], x["target"], x["type"]) == k)
                if not any(ev["article_id"] == art["id"] for ev in edge["evidence"]):
                    edge["evidence"].append({"article_id": art["id"], "quote": vq})
                continue
            existing_keys.add(k)
            new_edges.append({"source": s, "target": t, "type": etype, "weight": 0.5,
                              "origin": "research", "extractor": extractor,
                              "evidence": [{"article_id": art["id"], "quote": vq}],
                              "status": "unverified"})
            used_new.update(x for x in (s, t) if any(r["id"] == x for r in accepted_nodes.values()))

    kept_rows = [r for r in accepted_nodes.values() if r["id"] in used_new]
    added_nodes = []
    for row in kept_rows:
        definition = row.pop("definition")
        rows.append(row)
        gn = node_from_registry(row)
        gn["definition"] = definition
        gn["status"] = "provisional"
        graph["nodes"].append(gn)
        node_ids_in_graph.add(row["id"])
        added_nodes.append(gn)
    # drop edges that pointed at a new node we did not keep
    new_edges = [e for e in new_edges
                 if e["source"] in node_ids_in_graph and e["target"] in node_ids_in_graph]
    graph["edges"].extend(new_edges)

    recompute_weights(graph["edges"])

    art_entry = None
    if not any(a["id"] == art["id"] for a in graph.get("articles", [])):
        art_entry = {"id": art["id"], "title": art["title"],
                     "url": f"{SEP_BASE}/{art['id']}/", "retrieved": today,
                     "grounded_edges": len(new_edges), "proposed_edges": 0}
        graph.setdefault("articles", []).append(art_entry)

    gnode["research"] = {"status": "researched", "date": today,
                         "sources": [art["id"]], "model": MODEL}
    registry["meta"]["count"] = len(rows)
    _write(graph, registry)
    metrics_mod.main()

    return {"researched": True, "focus": gnode, "cost": round(cost, 4),
            "source": {"id": art["id"], "title": art["title"]},
            "new_nodes": added_nodes, "new_edges": new_edges,
            "grounded": sum(1 for _ in new_edges),
            "articles": [art_entry] if art_entry else [],
            "metrics": _metrics_map()}


def _metrics_map() -> dict:
    graph = json.loads((DATA / "graph.json").read_text(encoding="utf-8"))
    return {n["id"]: n["metrics"] for n in graph["nodes"]}


def _write(graph: dict, registry: dict) -> None:
    atomic_write(DATA / "graph.json", graph)
    atomic_write(DATA / "registry.json", registry)


if __name__ == "__main__":
    import argparse
    import sys
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("node_id")
    ap.add_argument("--max-cost", type=float, default=0.30)
    args = ap.parse_args()
    try:
        delta = research_node(args.node_id, args.max_cost)
    except RuntimeError as e:
        sys.exit(str(e))
    delta.pop("metrics", None)
    print(json.dumps(delta, indent=1, ensure_ascii=False))

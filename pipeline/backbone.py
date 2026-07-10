"""Backbone generation (Phase 3): typed edges over the closed-world registry.

The LLM never writes to the graph directly. The flow is:

  prompts  -> cache/backbone/prompts/<pass>.md     (versioned, deterministic)
  <LLM answers each prompt; responses are saved to data/backbone/responses/<pass>.json
   by whatever driver runs the model: an API script, or a Claude Code session>
  ingest   -> data/backbone/candidates.json        (schema + closed-world + domain/range
                                                    checks; unknown nodes -> quarantine)
  merge    -> data/graph.json                      (existing edges win; weights/extractor
                                                    stamped; nodes pulled from registry)
  sample   -> data/verification_sample.json        (deterministic draw for human review)

Per CLAUDE.md D3/D4/D6: registry ids only, typed edges only, no confidence numbers,
every generated edge carries extractor {model, prompt_version, date}, and every
candidate set must pass pipeline/evaluate.py against the gold sets before merge.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
import time
from pathlib import Path

from common import atomic_write, load_registry, registry_index
from validate import EDGE_TYPES, edge_key

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
PROMPT_DIR = ROOT / "cache" / "backbone" / "prompts"
RESPONSE_DIR = DATA / "backbone" / "responses"
CANDIDATES = DATA / "backbone" / "candidates.json"
QUARANTINE = DATA / "quarantine" / "proposed_nodes.json"
SAMPLE = DATA / "verification_sample.json"

PROMPT_VERSION = "bb-v1"

# Allowed (source type, target type) pairs per edge type. Directional traps like
# person-DEVELOPED_BY-concept or person-AUTHORED_BY-work are rejected here
# mechanically, before any human review.
DOMAIN_RANGE = {
    "IS_A":           ({"concept", "school"}, {"concept", "school"}),
    "PART_OF":        ({"concept"}, {"concept", "school"}),
    "SUBCATEGORY_OF": ({"concept"}, {"concept"}),
    "DEVELOPED_BY":   ({"concept", "school"}, {"person"}),
    "EXTENDED_BY":    ({"concept", "school"}, {"person"}),
    "DERIVED_FROM":   ({"concept", "school"}, {"concept", "person", "school", "work"}),
    "INFLUENCED_BY":  ({"person", "school"}, {"person", "school", "work"}),
    "CONTRASTS_WITH": ({"concept", "school"}, {"concept", "school"}),
    "CRITIQUES":      ({"concept", "person", "school", "work"},
                       {"concept", "person", "school", "work"}),
    "RESPONDS_TO":    ({"concept", "person", "school", "work"},
                       {"concept", "person", "school", "work"}),
    "AUTHORED_BY":    ({"work"}, {"person"}),
    "INTRODUCED_IN":  ({"concept"}, {"work"}),
}

def load_passes(domain: str) -> tuple[dict, dict]:
    """Pass definitions are data (Phase 11): data/passes/<domain>.json holds
    {meta: {domain, ...}, passes: {...}} — adding a domain is a JSON file,
    not a code change."""
    f = DATA / "passes" / f"{domain}.json"
    if not f.exists():
        sys.exit(f"no pass definitions for domain '{domain}' — create "
                 f"{f.relative_to(ROOT)} (see data/passes/ethics.json)")
    doc = json.loads(f.read_text(encoding="utf-8"))
    return doc["meta"], doc["passes"]


# default domain, also what the test suite exercises
PASSES_META, PASSES = load_passes("ethics")

EDGE_DIRECTION_GUIDE = """\
| type | direction reads as | example |
|---|---|---|
| IS_A | X IS_A Y: X is a kind/conception of Y | `justice IS_A virtue` |
| PART_OF | X PART_OF Y: X is a constituent of theory/tradition Y | `duty PART_OF deontology` |
| SUBCATEGORY_OF | X SUBCATEGORY_OF Y: X is the narrower category | `deontology SUBCATEGORY_OF normative_ethics` |
| DEVELOPED_BY | concept/school DEVELOPED_BY person | `utilitarianism DEVELOPED_BY jeremy_bentham` |
| EXTENDED_BY | concept/school EXTENDED_BY later person | `utilitarianism EXTENDED_BY john_stuart_mill` |
| DERIVED_FROM | X DERIVED_FROM Y: X grew out of Y | `german_idealism DERIVED_FROM immanuel_kant` |
| INFLUENCED_BY | later thinker INFLUENCED_BY earlier thinker/school | `immanuel_kant INFLUENCED_BY david_hume` |
| CONTRASTS_WITH | standard opposition; symmetric, assert once | `deontology CONTRASTS_WITH consequentialism` |
| CRITIQUES | X CRITIQUES Y: X argues against Y | `bernard_williams CRITIQUES utilitarianism` |
| RESPONDS_TO | X RESPONDS_TO Y: X is a reaction to problem/position Y | `compatibilism RESPONDS_TO determinism` |
| AUTHORED_BY | work AUTHORED_BY person (never the reverse) | `leviathan AUTHORED_BY thomas_hobbes` |
| INTRODUCED_IN | concept INTRODUCED_IN work (first/canonical statement) | `categorical_imperative INTRODUCED_IN groundwork_metaphysics_of_morals` |
"""

PROMPT_RULES = """\
Rules — read carefully:
1. CLOSED WORLD: `source` and `target` MUST be ids from the registry index below,
   verbatim. If a philosophically important neighbor is missing from the registry,
   list it under `proposed_nodes` instead of inventing an id.
2. Use ONLY the 12 edge types above. There is no RELATED_TO; if no typed relation
   fits, assert nothing.
3. Direction matters. Re-check every edge against the direction column. Persons are
   never the source of DEVELOPED_BY/EXTENDED_BY/AUTHORED_BY edges.
4. Precision over recall: assert only mainstream, textbook-defensible claims of
   academic philosophy. If you are unsure who developed a doctrine, WHICH work first
   stated a concept, or which direction an influence runs — omit the edge.
5. Classic failure modes to avoid: reversed directions; anachronistic influence
   (the earlier figure cannot be influenced by the later); conflating similarly
   named or adjacent doctrines (e.g. 18th-century sentimentalism is not 20th-century
   emotivism; ethical intuitionism is a form of realism); attributing a concept to a
   thinker's most famous book when it actually appears in another.
6. No numeric confidence scores. `rationale` is one short factual sentence
   (<= 140 chars) that a human reviewer can check.
7. CONTRASTS_WITH is symmetric: assert each pair once.
8. Output a single JSON object, no markdown fences, matching exactly:

{
  "meta": {"pass_id": "<pass id>", "prompt_version": "<version>",
           "model": "<your model id>", "date": "<YYYY-MM-DD>"},
  "edges": [
    {"source": "<registry id>", "type": "<EDGE_TYPE>", "target": "<registry id>",
     "rationale": "<short check-able justification>"}
  ],
  "proposed_nodes": [
    {"label": "<name>", "type": "concept|person|school|work",
     "reason": "<why it belongs in the graph>"}
  ]
}
"""


def build_prompt(pass_id: str, spec: dict, rows: list[dict], by_id: dict,
                 domain_label: str) -> str:
    focus = "\n".join(f"- {i}  ({by_id[i]['type']}) {by_id[i]['label']}"
                      for i in spec["focus"])
    return (
        f"# Concept Mapper backbone pass: {spec['title']}\n\n"
        f"pass_id: {pass_id}\nprompt_version: {PROMPT_VERSION}\n\n"
        "You are building the backbone of a typed knowledge graph of academic\n"
        f"philosophy (domain: {domain_label}) from your own knowledge. Output edges between\n"
        "registry nodes only; evidence quotes are attached in a later stage.\n\n"
        f"## Edge types\n\n{EDGE_DIRECTION_GUIDE}\n"
        f"## {spec['title']}\n\n{spec['guidance']}\n\n"
        f"Focus nodes (relate these to each other and to any other registry node):\n"
        f"{focus}\n\n"
        f"## Registry index (closed world — the only legal ids)\n\n"
        f"{registry_index(rows)}\n\n"
        f"## Output\n\n{PROMPT_RULES}"
    )


def cmd_prompts(args) -> None:
    meta, passes = load_passes(args.domain)
    _, rows, by_id, _ = load_registry()
    for pass_id, spec in passes.items():
        unknown = [i for i in spec["focus"] if i not in by_id]
        if unknown:
            sys.exit(f"pass {pass_id}: focus ids not in registry: {unknown}")
    PROMPT_DIR.mkdir(parents=True, exist_ok=True)
    for pass_id, spec in passes.items():
        out = PROMPT_DIR / f"{pass_id}.md"
        out.write_text(build_prompt(pass_id, spec, rows, by_id, meta["domain"]),
                       encoding="utf-8")
        print(f"wrote {out.relative_to(ROOT)}")
    print(f"{len(passes)} prompts, prompt_version {PROMPT_VERSION}")


def cmd_ingest(args) -> None:
    _, passes = load_passes(args.domain)
    _, _, by_id, resolve = load_registry()
    edges: list[dict] = []
    rejects: list[dict] = []
    warnings: list[str] = []
    proposals: dict[str, dict] = {}
    passes_meta: dict[str, dict] = {}
    seen: set[tuple] = set()

    files = sorted(RESPONSE_DIR.glob("*.json"))
    if not files:
        sys.exit(f"no responses in {RESPONSE_DIR.relative_to(ROOT)} — answer the "
                 f"prompts in {PROMPT_DIR.relative_to(ROOT)} first")
    for f in files:
        resp = json.loads(f.read_text(encoding="utf-8"))
        meta = resp.get("meta", {})
        pass_id = meta.get("pass_id", f.stem)
        if pass_id != f.stem:
            warnings.append(f"{f.name}: meta.pass_id '{pass_id}' != filename")
        if pass_id not in passes:
            warnings.append(f"{f.name}: unknown pass_id '{pass_id}'")
        if meta.get("prompt_version") != PROMPT_VERSION:
            warnings.append(f"{f.name}: prompt_version {meta.get('prompt_version')} "
                            f"!= current {PROMPT_VERSION}")
        passes_meta[pass_id] = {"model": meta.get("model", ""),
                                "date": meta.get("date", ""),
                                "raw_edges": len(resp.get("edges", []))}

        for p in resp.get("proposed_nodes", []):
            key = p.get("label", "").casefold()
            proposals.setdefault(key, {**p, "pass_id": pass_id, "edges": []})

        for e in resp.get("edges", []):
            tag = f"{pass_id}: {e.get('source')} -{e.get('type')}-> {e.get('target')}"
            etype = e.get("type")
            if etype not in EDGE_TYPES:
                rejects.append({**e, "pass_id": pass_id, "reason": "unknown edge type"})
                continue
            endpoints = []
            unknown = None
            for end in ("source", "target"):
                raw = str(e.get(end, ""))
                rid = resolve.get(raw.casefold())
                if rid is None:
                    unknown = raw
                    break
                if rid != raw:
                    warnings.append(f"{tag}: resolved {end} '{raw}' -> '{rid}'")
                endpoints.append(rid)
            if unknown is not None:
                key = unknown.casefold()
                proposals.setdefault(key, {
                    "label": unknown, "type": "", "reason": "referenced by extractor",
                    "pass_id": pass_id, "edges": []})
                proposals[key]["edges"].append(
                    {k: e.get(k) for k in ("source", "type", "target", "rationale")})
                continue
            src, tgt = endpoints
            if src == tgt:
                rejects.append({**e, "pass_id": pass_id, "reason": "self-loop"})
                continue
            dom, rng = DOMAIN_RANGE[etype]
            if by_id[src]["type"] not in dom or by_id[tgt]["type"] not in rng:
                rejects.append({**e, "pass_id": pass_id, "reason":
                                f"domain/range: {by_id[src]['type']} -{etype}-> "
                                f"{by_id[tgt]['type']} not allowed"})
                continue
            k = edge_key(src, tgt, etype)
            if k in seen:
                rejects.append({**e, "pass_id": pass_id, "reason": "duplicate"})
                continue
            seen.add(k)
            edges.append({"source": src, "type": etype, "target": tgt,
                          "rationale": e.get("rationale", ""), "pass_id": pass_id,
                          "model": meta.get("model", ""), "date": meta.get("date", "")})

    CANDIDATES.parent.mkdir(parents=True, exist_ok=True)
    atomic_write(CANDIDATES, {
        "meta": {"built": time.strftime("%Y-%m-%d"), "prompt_version": PROMPT_VERSION,
                 "passes": passes_meta, "candidate_count": len(edges),
                 "reject_count": len(rejects), "rejects": rejects,
                 "warnings": warnings},
        "edges": edges})
    print(f"wrote {CANDIDATES.relative_to(ROOT)}: {len(edges)} candidates, "
          f"{len(rejects)} rejected, {len(warnings)} warnings")
    for w in warnings:
        print(f"  WARN  {w}")
    for r in rejects:
        print(f"  REJECT  {r['source']} -{r['type']}-> {r['target']}: {r['reason']}")

    QUARANTINE.parent.mkdir(parents=True, exist_ok=True)
    atomic_write(QUARANTINE, {
        "meta": {"built": time.strftime("%Y-%m-%d"),
                 "source": f"backbone {PROMPT_VERSION}", "count": len(proposals)},
        "proposed_nodes": sorted(proposals.values(), key=lambda p: p["label"])})
    print(f"wrote {QUARANTINE.relative_to(ROOT)}: {len(proposals)} proposed nodes")


def node_from_registry(row: dict) -> dict:
    return {
        "id": row["id"], "label": row["label"], "type": row["type"],
        "definition": row.get("wd_description", ""),
        "aliases": row.get("aliases", []), "domain": row.get("domain", ""),
        "tradition": "", "time_period": row.get("time_period", ""),
        "wikidata_qid": row.get("wikidata_qid", ""), "status": "generated",
        "metrics": {"degree": 0, "betweenness": 0.0, "community": 0},
    }


def cmd_merge(args) -> None:
    _, _, by_id, _ = load_registry()
    cand = json.loads(CANDIDATES.read_text(encoding="utf-8"))
    graph = json.loads((DATA / "graph.json").read_text(encoding="utf-8"))

    existing = {edge_key(e["source"], e["target"], e["type"]) for e in graph["edges"]}
    node_ids = {n["id"] for n in graph["nodes"]}
    added_edges = added_nodes = 0
    for e in cand["edges"]:
        k = edge_key(e["source"], e["target"], e["type"])
        if k in existing:
            continue
        existing.add(k)
        graph["edges"].append({
            "source": e["source"], "target": e["target"], "type": e["type"],
            "weight": 0.5,  # n = 1: backbone assertion, no evidence yet
            "origin": "backbone",
            "extractor": {"model": e["model"],
                          "prompt_version": cand["meta"]["prompt_version"],
                          "date": e["date"]},
            "evidence": [], "status": "unverified"})
        added_edges += 1
        for end in (e["source"], e["target"]):
            if end not in node_ids:
                graph["nodes"].append(node_from_registry(by_id[end]))
                node_ids.add(end)
                added_nodes += 1

    graph["meta"]["built"] = time.strftime("%Y-%m-%d")
    domains = sorted({n.get("domain", "") for n in graph["nodes"]} - {""})
    graph["meta"]["description"] = (
        "hand-built seed cluster + backbone "
        f"({cand['meta']['prompt_version']}) over the "
        f"{' + '.join(domains) or 'full'} registry")
    out = DATA / "graph.json"
    atomic_write(out, graph)
    print(f"wrote {out.relative_to(ROOT)}: +{added_edges} edges, +{added_nodes} nodes "
          f"-> {len(graph['nodes'])} nodes, {len(graph['edges'])} edges")
    print("now run: validate.py, evaluate.py --graph, build_viewer_data.py")


def cmd_sample(args) -> None:
    graph = json.loads((DATA / "graph.json").read_text(encoding="utf-8"))
    rationale = {}
    if CANDIDATES.exists():
        cand = json.loads(CANDIDATES.read_text(encoding="utf-8"))
        rationale = {edge_key(e["source"], e["target"], e["type"]): e["rationale"]
                     for e in cand["edges"]}
    pool = [e for e in graph["edges"]
            if e.get("origin") == "backbone" and e.get("status") == "unverified"]
    pool.sort(key=lambda e: (e["source"], e["type"], e["target"]))
    n = min(args.n, len(pool))
    picked = random.Random(args.seed).sample(pool, n)
    SAMPLE.write_text(json.dumps({
        "meta": {"built": time.strftime("%Y-%m-%d"), "seed": args.seed,
                 "drawn": n, "pool": len(pool),
                 "instructions": "human review: set verdict to accept|reject and "
                                 "add notes; feeds the Phase 5 review loop"},
        "sample": [{"source": e["source"], "type": e["type"], "target": e["target"],
                    "rationale": rationale.get(
                        edge_key(e["source"], e["target"], e["type"]), ""),
                    "verdict": "", "notes": ""}
                   for e in picked]}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
    print(f"wrote {SAMPLE.relative_to(ROOT)}: {n} of {len(pool)} unverified "
          f"backbone edges (seed {args.seed})")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    dom = argparse.ArgumentParser(add_help=False)
    dom.add_argument("--domain", default="ethics",
                     help="pass definitions to use: data/passes/<domain>.json")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("prompts", parents=[dom],
                   help="emit per-pass prompts to cache/backbone/prompts/")
    sub.add_parser("ingest", parents=[dom],
                   help="validate responses -> candidates + quarantine")
    sub.add_parser("merge", parents=[dom],
                   help="merge candidates into data/graph.json")
    sp = sub.add_parser("sample", help="draw verification sample from merged edges")
    sp.add_argument("-n", type=int, default=25)
    sp.add_argument("--seed", type=int, default=20260611)
    args = ap.parse_args()
    {"prompts": cmd_prompts, "ingest": cmd_ingest,
     "merge": cmd_merge, "sample": cmd_sample}[args.cmd](args)


if __name__ == "__main__":
    main()

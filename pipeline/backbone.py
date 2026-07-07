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

PASSES = {
    "normative_theories": {
        "title": "Normative ethical theories",
        "guidance": (
            "Map the normative-ethics families: the consequentialism/utilitarianism "
            "tree, deontology and the Kantian apparatus (imperatives, autonomy, maxims, "
            "good will, kingdom of ends), the virtue-ethics tree and its Aristotelian "
            "concepts, contract theories, egoisms, hedonism, divine command, natural "
            "law, and care/feminist ethics. Assert the taxonomy (SUBCATEGORY_OF), the "
            "classic oppositions (CONTRASTS_WITH), and developer/extender attributions."),
        "focus": [
            "normative_ethics", "consequentialism", "utilitarianism",
            "act_utilitarianism", "rule_utilitarianism", "greatest_happiness_principle",
            "deontology", "duty", "categorical_imperative", "hypothetical_imperative",
            "autonomy", "heteronomy", "good_will", "maxim", "kingdom_of_ends",
            "universalizability", "virtue_ethics", "virtue", "eudaimonia",
            "golden_mean", "practical_wisdom", "akrasia", "contractarianism",
            "contractualism", "social_contract", "ethical_egoism",
            "psychological_egoism", "hedonism", "divine_command_theory", "natural_law",
            "care_ethics", "feminist_ethics", "altruism",
        ],
    },
    "metaethics": {
        "title": "Metaethical positions",
        "guidance": (
            "Map the metaethics tree: realism vs anti-realism, cognitivism vs "
            "non-cognitivism, the non-cognitivisms (emotivism, prescriptivism, "
            "expressivism, quasi-realism), error theory, naturalism vs non-naturalism, "
            "intuitionism, relativism/subjectivism/nihilism, sentimentalism, and the "
            "classic arguments (open question, naturalistic fallacy, is/ought). Take "
            "special care to attribute each doctrine to its actual proponent and each "
            "argument to the work that actually introduced it."),
        "focus": [
            "metaethics", "moral_realism", "moral_anti_realism", "moral_cognitivism",
            "non_cognitivism", "emotivism", "prescriptivism", "expressivism",
            "quasi_realism", "error_theory", "moral_naturalism", "moral_non_naturalism",
            "moral_intuitionism", "moral_relativism", "moral_subjectivism",
            "moral_nihilism", "moral_sentimentalism", "open_question_argument",
            "naturalistic_fallacy", "is_ought_problem", "prima_facie_duty",
            "moral_particularism",
        ],
    },
    "agency_value": {
        "title": "Moral agency, freedom, and value",
        "guidance": (
            "Map moral psychology and value concepts: free will / determinism / "
            "compatibilism, moral responsibility and moral luck, moral agency and "
            "moral status, dilemmas and the trolley problem, double effect, "
            "supererogation, practical reason, well-being, justice and rights, "
            "and applied ethics."),
        "focus": [
            "free_will", "determinism", "compatibilism", "moral_responsibility",
            "moral_luck", "moral_agency", "moral_status", "moral_dilemma",
            "trolley_problem", "doctrine_of_double_effect", "supererogation",
            "practical_reason", "well_being", "justice", "rights", "applied_ethics",
            "altruism", "psychological_egoism", "eudaimonia",
        ],
    },
    "works_bibliography": {
        "title": "Works: authorship and first introductions",
        "guidance": (
            "For every work in the registry, assert AUTHORED_BY (direction: work -> "
            "person). Add INTRODUCED_IN edges (concept -> work) only where a concept "
            "was genuinely first introduced or canonically stated in that work — "
            "getting the right work matters more than coverage; many famous "
            "attributions name the wrong book. Add work-level CRITIQUES / RESPONDS_TO "
            "where a work's central target is itself a registry node."),
        "focus": [
            "a_theory_of_justice", "after_virtue", "critique_of_practical_reason",
            "critique_of_pure_reason", "enquiry_principles_of_morals",
            "ethics_inventing_right_and_wrong", "groundwork_metaphysics_of_morals",
            "language_truth_and_logic", "leviathan", "metaphysics_of_morals",
            "methods_of_ethics", "modern_moral_philosophy", "nicomachean_ethics",
            "on_liberty", "on_the_genealogy_of_morality", "principia_ethica",
            "principles_of_morals_and_legislation", "reasons_and_persons",
            "republic_plato", "the_right_and_the_good", "treatise_of_human_nature",
            "utilitarianism_mill", "what_we_owe_to_each_other",
        ],
    },
    "persons_schools": {
        "title": "Influence network and schools",
        "guidance": (
            "Map INFLUENCED_BY among persons (direction: the later thinker is "
            "INFLUENCED_BY the earlier; check the dates), person <-> school links, "
            "school founders (school DEVELOPED_BY person), school oppositions, and "
            "famous person-level CRITIQUES of registry doctrines. Only assert "
            "influence that is standard, documented intellectual history."),
        "focus": [
            "a_j_ayer", "alasdair_macintyre", "allan_gibbard", "aristotle",
            "arthur_schopenhauer", "bernard_williams", "carol_gilligan",
            "charles_stevenson", "christine_korsgaard", "david_hume", "derek_parfit",
            "elizabeth_anscombe", "epicurus", "francis_hutcheson",
            "friedrich_nietzsche", "g_e_moore", "h_a_prichard", "henry_sidgwick",
            "immanuel_kant", "j_l_mackie", "jeremy_bentham", "john_rawls",
            "john_stuart_mill", "joseph_butler", "nel_noddings", "peter_singer",
            "philippa_foot", "plato", "r_m_hare", "rosalind_hursthouse",
            "simon_blackburn", "socrates", "t_m_scanlon", "thomas_aquinas",
            "thomas_hobbes", "w_d_ross", "zeno_of_citium", "empiricism",
            "epicureanism", "german_idealism", "rationalism", "scholasticism",
            "stoicism",
        ],
    },
    "cross_boundary": {
        "title": "Cross-cluster boundary concepts",
        "guidance": (
            "Explicit cross-domain pass: connect concepts that bridge the clusters "
            "covered by the other passes — branch-level distinctions (metaethics vs "
            "normative ethics), arguments that target doctrines in another cluster, "
            "concepts that are constituents of theories mapped elsewhere, and "
            "oppositions that cross family lines. Do not repeat edges that obviously "
            "belong inside a single cluster; look for the seams."),
        "focus": [
            "metaethics", "normative_ethics", "applied_ethics", "is_ought_problem",
            "naturalistic_fallacy", "universalizability", "maxim", "kingdom_of_ends",
            "duty", "virtue", "justice", "rights", "well_being", "eudaimonia",
            "practical_reason", "moral_sentimentalism", "moral_particularism",
            "prima_facie_duty", "contractualism", "consequentialism",
            "moral_dilemma", "trolley_problem", "akrasia", "free_will",
            "moral_responsibility",
        ],
    },
}

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


def build_prompt(pass_id: str, spec: dict, rows: list[dict], by_id: dict) -> str:
    focus = "\n".join(f"- {i}  ({by_id[i]['type']}) {by_id[i]['label']}"
                      for i in spec["focus"])
    return (
        f"# Concept Mapper backbone pass: {spec['title']}\n\n"
        f"pass_id: {pass_id}\nprompt_version: {PROMPT_VERSION}\n\n"
        "You are building the backbone of a typed knowledge graph of academic\n"
        "philosophy (domain: Ethics) from your own knowledge. Output edges between\n"
        "registry nodes only; evidence quotes are attached in a later stage.\n\n"
        f"## Edge types\n\n{EDGE_DIRECTION_GUIDE}\n"
        f"## {spec['title']}\n\n{spec['guidance']}\n\n"
        f"Focus nodes (relate these to each other and to any other registry node):\n"
        f"{focus}\n\n"
        f"## Registry index (closed world — the only legal ids)\n\n"
        f"{registry_index(rows)}\n\n"
        f"## Output\n\n{PROMPT_RULES}"
    )


def cmd_prompts(_args) -> None:
    _, rows, by_id, _ = load_registry()
    for pass_id, spec in PASSES.items():
        unknown = [i for i in spec["focus"] if i not in by_id]
        if unknown:
            sys.exit(f"pass {pass_id}: focus ids not in registry: {unknown}")
    PROMPT_DIR.mkdir(parents=True, exist_ok=True)
    for pass_id, spec in PASSES.items():
        out = PROMPT_DIR / f"{pass_id}.md"
        out.write_text(build_prompt(pass_id, spec, rows, by_id), encoding="utf-8")
        print(f"wrote {out.relative_to(ROOT)}")
    print(f"{len(PASSES)} prompts, prompt_version {PROMPT_VERSION}")


def cmd_ingest(_args) -> None:
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
        if pass_id not in PASSES:
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


def cmd_merge(_args) -> None:
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
    graph["meta"]["description"] = (
        "Phase 1 hand-built Kant cluster + Phase 3 backbone "
        f"({cand['meta']['prompt_version']}) over the full Ethics registry")
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
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("prompts", help="emit per-pass prompts to cache/backbone/prompts/")
    sub.add_parser("ingest", help="validate responses -> candidates + quarantine")
    sub.add_parser("merge", help="merge candidates into data/graph.json")
    sp = sub.add_parser("sample", help="draw verification sample from merged edges")
    sp.add_argument("-n", type=int, default=25)
    sp.add_argument("--seed", type=int, default=20260611)
    args = ap.parse_args()
    {"prompts": cmd_prompts, "ingest": cmd_ingest,
     "merge": cmd_merge, "sample": cmd_sample}[args.cmd](args)


if __name__ == "__main__":
    main()

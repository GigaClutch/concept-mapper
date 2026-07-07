"""Validate graph.json (and the gold sets) against the registry and cached sources.

Checks (per CLAUDE.md, run on every graph build):
  - node ids unique, node types allowed, every node id exists in registry.json
  - edge endpoints exist in the graph AND in the registry (closed world)
  - edge types in the allowed taxonomy (no RELATED_TO)
  - weights follow w = 1 - 0.5^n, n = 1 backbone assertion + 1 per evidence item
  - no duplicate (source, target, type); CONTRASTS_WITH compared unordered
  - no orphan nodes
  - every evidence quote is a verbatim substring (whitespace-normalized) of the
    cached article text in cache/sep/articles/<article_id>.txt
  - gold sets: endpoints in registry, types allowed, no duplicates, and no edge
    appears in both the canonical and the adversarial set
Exits non-zero if anything fails.
"""

from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
ARTICLE_CACHE = ROOT / "cache" / "sep" / "articles"

# --allow-missing-cache (CI: cache/ is gitignored) downgrades a missing cached
# article from error to a summary warning; the quote check still runs against
# every cache file that IS present. Locally this stays a hard error.
ALLOW_MISSING_CACHE = False

NODE_TYPES = {"concept", "person", "school", "work"}
EDGE_TYPES = {
    "IS_A", "PART_OF", "SUBCATEGORY_OF",                          # hierarchical
    "DEVELOPED_BY", "EXTENDED_BY", "DERIVED_FROM", "INFLUENCED_BY",  # developmental
    "CONTRASTS_WITH", "CRITIQUES", "RESPONDS_TO",                 # oppositional
    "AUTHORED_BY", "INTRODUCED_IN",                               # bibliographic
}
SYMMETRIC = {"CONTRASTS_WITH"}

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace(" ", " ")).strip()


def edge_key(source: str, target: str, etype: str) -> tuple:
    if etype in SYMMETRIC:
        return (*sorted((source, target)), etype)
    return (source, target, etype)


def check_edge_list(edges: list[dict], registry_ids: set[str], ctx: str) -> set[tuple]:
    keys: set[tuple] = set()
    for e in edges:
        tag = f"{ctx}: {e.get('source')} -{e.get('type')}-> {e.get('target')}"
        for end in ("source", "target"):
            if e.get(end) not in registry_ids:
                err(f"{tag}: {end} '{e.get(end)}' not in registry")
        if e.get("type") not in EDGE_TYPES:
            err(f"{tag}: type not allowed")
        k = edge_key(e.get("source", ""), e.get("target", ""), e.get("type", ""))
        if k in keys:
            err(f"{tag}: duplicate edge")
        keys.add(k)
    return keys


def check_graph(registry_ids: set[str], registry_qids: dict[str, str]) -> None:
    g = json.loads((DATA / "graph.json").read_text(encoding="utf-8"))
    nodes, edges = g["nodes"], g["edges"]
    articles = {a["id"] for a in g.get("articles", [])}

    ids = [n["id"] for n in nodes]
    for i in ids:
        if ids.count(i) > 1:
            err(f"graph: duplicate node id '{i}'")
    for n in nodes:
        if n["type"] not in NODE_TYPES:
            err(f"graph node {n['id']}: bad type '{n['type']}'")
        if n["id"] not in registry_ids:
            err(f"graph node {n['id']}: not in registry (closed world violated)")
        rq = registry_qids.get(n["id"], "")
        if rq and n.get("wikidata_qid") != rq:
            err(f"graph node {n['id']}: wikidata_qid '{n.get('wikidata_qid')}' "
                f"!= registry '{rq}' (identity drift)")

    id_set = set(ids)
    degree = {i: 0 for i in id_set}
    for e in edges:
        for end in ("source", "target"):
            if e[end] in degree:
                degree[e[end]] += 1
    check_edge_list(edges, registry_ids, "graph")

    missing_cache: set[str] = set()
    for e in edges:
        if e["source"] not in id_set or e["target"] not in id_set:
            err(f"graph edge {e['source']}->{e['target']}: endpoint missing from graph nodes")
        n = (1 if e.get("origin") == "backbone" else 0) + \
            sum(1 for ev in e.get("evidence", []) if ev.get("support") != "no")
        expected = 1 - 0.5 ** max(n, 1)
        if not math.isclose(e.get("weight", -1), expected, abs_tol=1e-9):
            err(f"graph edge {e['source']}-{e['type']}->{e['target']}: "
                f"weight {e.get('weight')} != {expected} (n={n})")
        for ev in e.get("evidence", []):
            if ev["article_id"] not in articles:
                err(f"graph edge {e['source']}->{e['target']}: evidence article "
                    f"'{ev['article_id']}' not in graph articles list")
            cached = ARTICLE_CACHE / f"{ev['article_id']}.txt"
            if not cached.exists():
                if ALLOW_MISSING_CACHE:
                    missing_cache.add(ev["article_id"])
                else:
                    err(f"graph edge {e['source']}->{e['target']}: no cached source for "
                        f"'{ev['article_id']}' — run pipeline/scrape_sep.py --article {ev['article_id']}")
            elif norm(ev["quote"]) not in norm(cached.read_text(encoding="utf-8")):
                err(f"graph edge {e['source']}->{e['target']}: quote is NOT a verbatim "
                    f"substring of cached '{ev['article_id']}'")
    if missing_cache:
        warn(f"quote verbatim check SKIPPED for {len(missing_cache)} uncached "
             f"article(s) (--allow-missing-cache): {sorted(missing_cache)}")

    for i, d in degree.items():
        if d == 0:
            err(f"graph: orphan node '{i}'")
    print(f"graph: {len(nodes)} nodes, {len(edges)} edges checked")


def check_gold(registry_ids: set[str]) -> None:
    canon = json.loads((DATA / "gold" / "canonical_edges.json").read_text(encoding="utf-8"))
    adv = json.loads((DATA / "gold" / "adversarial.json").read_text(encoding="utf-8"))
    ck = check_edge_list(canon["edges"], registry_ids, "gold/canonical")
    ak = check_edge_list(adv["traps"], registry_ids, "gold/adversarial")
    for k in ck & ak:
        err(f"gold: edge {k} appears in BOTH canonical and adversarial sets")
    if canon["meta"].get("edge_count") != len(canon["edges"]):
        warn(f"gold/canonical meta edge_count {canon['meta'].get('edge_count')} "
             f"!= actual {len(canon['edges'])}")
    if adv["meta"].get("trap_count") != len(adv["traps"]):
        warn(f"gold/adversarial meta trap_count {adv['meta'].get('trap_count')} "
             f"!= actual {len(adv['traps'])}")
    for t in adv["traps"]:
        if t.get("trap_type") not in {"direction_error", "polysemy", "plausible_but_false"}:
            err(f"gold/adversarial {t['source']}->{t['target']}: bad trap_type")
    print(f"gold: {len(canon['edges'])} canonical edges, {len(adv['traps'])} traps checked")


REGISTRY_REQUIRED = ("id", "label", "type", "aliases", "domain", "status")


def main() -> None:
    global ALLOW_MISSING_CACHE
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--allow-missing-cache", action="store_true",
                    help="warn instead of fail when a cached article is absent "
                         "(for CI, where cache/ is not checked out)")
    ALLOW_MISSING_CACHE = ap.parse_args().allow_missing_cache

    registry = json.loads((DATA / "registry.json").read_text(encoding="utf-8"))
    registry_ids = {r["id"] for r in registry["nodes"]}
    print(f"registry: {len(registry_ids)} rows")

    # row schema + search identity: labels unique, no alias claimed twice or
    # shadowing another row's label — an ambiguous name breaks search and the
    # closed-world resolve map (utilitarianism_mill's old label did exactly this)
    labels: dict[str, str] = {}
    for r in registry["nodes"]:
        for f in REGISTRY_REQUIRED:
            if f not in r:
                err(f"registry {r.get('id', '?')}: missing field '{f}'")
        if r.get("type") not in NODE_TYPES:
            err(f"registry {r.get('id', '?')}: bad type '{r.get('type')}'")
        lk = r["label"].casefold()
        if lk in labels:
            err(f"registry: label '{r['label']}' on both {labels[lk]} and {r['id']}")
        labels[lk] = r["id"]
    alias_owner: dict[str, str] = {}
    for r in registry["nodes"]:
        for a in r.get("aliases", []):
            ak = a.casefold()
            if ak in labels and labels[ak] != r["id"]:
                err(f"registry {r['id']}: alias '{a}' is the label of {labels[ak]}")
            if ak in alias_owner and alias_owner[ak] != r["id"]:
                err(f"registry: alias '{a}' on both {alias_owner[ak]} and {r['id']}")
            alias_owner.setdefault(ak, r["id"])

    by_qid: dict[str, list[str]] = {}
    for r in registry["nodes"]:
        if r.get("wikidata_qid"):
            by_qid.setdefault(r["wikidata_qid"], []).append(r["id"])
    for qid, rids in by_qid.items():
        if len(rids) > 1:
            err(f"registry: QID {qid} shared by {rids} — two rows, one entity")
    unreviewed = [r["id"] for r in registry["nodes"]
                  if r.get("qid_source") == "unresolved"]
    if unreviewed:
        warn(f"registry: {len(unreviewed)} rows with unresolved QID "
             f"(not yet human-reviewed): {unreviewed}")

    check_graph(registry_ids,
                {r["id"]: r.get("wikidata_qid", "") for r in registry["nodes"]})
    check_gold(registry_ids)

    for w in warnings:
        print(f"  WARN  {w}")
    if errors:
        print(f"\n{len(errors)} ERROR(S):")
        for e in errors:
            print(f"  FAIL  {e}")
        sys.exit(1)
    print("\nvalidation PASSED")


if __name__ == "__main__":
    main()

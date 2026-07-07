"""Semantic evidence check (Phase 9): does each quote actually support its claim?

For every evidence item on every edge, one cheap structured-output call asks
whether the quote, on its own, states or clearly supports the SPECIFIC claim
(right entities, right direction). The verdict is stored on the evidence item
as support: "yes" | "no". Items with support "no" stay attached — the passage
is still context a reader may want — but they stop counting toward the edge
weight (see common.edge_weight) and the viewer labels them "contextual".

Verdicts are cached in data/quote_check/cache.json keyed by the claim+quote,
so re-runs are free and only new evidence costs anything. Run as a script to
check the whole graph:

  python pipeline/quote_check.py [--max-cost 0.50]

research.py calls check_one() inline so browse-time evidence is labelled the
moment it lands.
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

from common import (atomic_write, call_cost, load_key, recompute_weights,
                    retry_messages_create)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CACHE = DATA / "quote_check" / "cache.json"

MODEL = "claude-haiku-4-5"
PROMPT_VERSION = "qc-v1"

SENTENCE = {
    "IS_A": "is a kind of", "PART_OF": "is part of",
    "SUBCATEGORY_OF": "is a subcategory of", "DEVELOPED_BY": "was developed by",
    "EXTENDED_BY": "was extended by", "DERIVED_FROM": "grew out of",
    "INFLUENCED_BY": "was influenced by", "CONTRASTS_WITH": "contrasts with",
    "CRITIQUES": "argues against", "RESPONDS_TO": "responds to",
    "AUTHORED_BY": "was written by", "INTRODUCED_IN": "was introduced in",
}

SCHEMA = {
    "type": "object",
    "properties": {"support": {"type": "string", "enum": ["yes", "no"]}},
    "required": ["support"],
    "additionalProperties": False,
}


def _key(claim: str, quote: str) -> str:
    return hashlib.sha256(f"{claim}|{quote}".encode("utf-8")).hexdigest()[:24]


def _claim(edge: dict, labels: dict) -> str:
    s = labels.get(edge["source"], edge["source"])
    t = labels.get(edge["target"], edge["target"])
    return f"{s} {SENTENCE.get(edge['type'], edge['type'])} {t}"


def _prompt(claim: str, quote: str) -> str:
    return (
        "You are checking evidence in a knowledge graph of academic philosophy.\n\n"
        f"CLAIM: {claim}\n\n"
        f"QUOTE (from the Stanford Encyclopedia of Philosophy):\n\"{quote}\"\n\n"
        "Does the quote, ON ITS OWN, state or clearly support this SPECIFIC claim "
        "— the right entities, in the right direction/role? A quote that merely "
        "mentions the entities, discusses a related point, or supports a different "
        "or reversed relationship does not count. Answer strictly yes or no."
    )


def load_cache() -> dict:
    return json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}


def check_one(edge: dict, ev: dict, labels: dict, client, cache: dict) -> float:
    """Set ev['support'] from cache or one API call; returns USD spent."""
    claim = _claim(edge, labels)
    k = _key(claim, ev["quote"])
    hit = cache.get(k)
    if hit:
        ev["support"] = hit["support"]
        return 0.0
    resp = retry_messages_create(
        client, model=MODEL, max_tokens=16,
        messages=[{"role": "user", "content": _prompt(claim, ev["quote"])}],
        output_config={"format": {"type": "json_schema", "schema": SCHEMA}})
    if resp is None:
        return 0.0  # still rate-limited; leave unchecked (counts as supporting)
    verdict = json.loads(next(b.text for b in resp.content if b.type == "text"))
    ev["support"] = verdict["support"]
    cache[k] = {"support": verdict["support"], "model": MODEL,
                "prompt_version": PROMPT_VERSION, "date": time.strftime("%Y-%m-%d")}
    atomic_write(CACHE, cache)
    return call_cost(MODEL, resp.usage)


def main() -> None:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--max-cost", type=float, default=0.50)
    ap.add_argument("--pace", type=float, default=0.3,
                    help="seconds between API calls")
    args = ap.parse_args()

    try:
        key = load_key()
    except RuntimeError as e:
        sys.exit(f"error: {e}")
    import anthropic
    client = anthropic.Anthropic(api_key=key)

    graph = json.loads((DATA / "graph.json").read_text(encoding="utf-8"))
    labels = {n["id"]: n["label"] for n in graph["nodes"]}
    cache = load_cache()

    todo = [(e, ev) for e in graph["edges"] for ev in e["evidence"]
            if "support" not in ev]
    print(f"{len(todo)} evidence items to check "
          f"({sum(len(e['evidence']) for e in graph['edges'])} total)")
    spent, checked = 0.0, 0
    for e, ev in todo:
        if spent >= args.max_cost:
            print(f"STOP: cost ${spent:.3f} >= cap ${args.max_cost:.2f}")
            break
        cost = check_one(e, ev, labels, client, cache)
        spent += cost
        checked += 1
        if cost and args.pace:
            time.sleep(args.pace)
        if checked % 25 == 0:
            print(f"  {checked}/{len(todo)} checked, ${spent:.3f}")

    recompute_weights(graph["edges"])
    atomic_write(DATA / "graph.json", graph)
    tally = {}
    for e in graph["edges"]:
        for ev in e["evidence"]:
            tally[ev.get("support", "unchecked")] = \
                tally.get(ev.get("support", "unchecked"), 0) + 1
    print(f"done: {checked} checked this run, ${spent:.4f} | verdicts: {tally}")
    print("now run: validate.py, evaluate.py --graph, build_viewer_data.py, "
          "build_review_data.py")


if __name__ == "__main__":
    main()

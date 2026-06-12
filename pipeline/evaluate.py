"""Score an edge set against the gold sets (Phase 3+, CLAUDE.md D6).

Metrics:
  - canonical recall: fraction of data/gold/canonical_edges.json recovered
  - adversarial hits: traps from data/gold/adversarial.json that were asserted
    (each one is a precision failure)
  - reversed canonicals: directed gold edges asserted backwards

Run against the backbone candidates before merging (the gate), and against
data/graph.json after merging (the regression check). Exits non-zero when any
threshold is violated; every prompt/pipeline change must keep this green
before it is adopted.

Usage:
  python pipeline/evaluate.py                       # data/backbone/candidates.json
  python pipeline/evaluate.py --graph               # data/graph.json
  python pipeline/evaluate.py --min-recall 0.8 --max-traps 0 --max-reversed 0
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from validate import SYMMETRIC, edge_key

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def load_keys(path: Path, field: str) -> tuple[set, list[dict]]:
    doc = json.loads(path.read_text(encoding="utf-8"))
    edges = doc[field] if field in doc else doc["edges"]
    return {edge_key(e["source"], e["target"], e["type"]) for e in edges}, edges


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--graph", action="store_true",
                    help="score data/graph.json instead of the backbone candidates")
    ap.add_argument("--edges", type=Path, default=None,
                    help="explicit edges file (any JSON with an 'edges' list)")
    ap.add_argument("--min-recall", type=float, default=0.8)
    ap.add_argument("--max-traps", type=int, default=0)
    ap.add_argument("--max-reversed", type=int, default=0)
    args = ap.parse_args()

    target = (args.edges if args.edges
              else DATA / "graph.json" if args.graph
              else DATA / "backbone" / "candidates.json")
    keys, _ = load_keys(target, "edges")
    _, canon = load_keys(DATA / "gold" / "canonical_edges.json", "edges")
    _, traps = load_keys(DATA / "gold" / "adversarial.json", "traps")
    print(f"scoring {target.relative_to(ROOT)} ({len(keys)} edges) against gold\n")

    hit, missed = [], []
    for e in canon:
        (hit if edge_key(e["source"], e["target"], e["type"]) in keys
         else missed).append(e)
    recall = len(hit) / len(canon)
    by_type = Counter(e["type"] for e in canon)
    hit_type = Counter(e["type"] for e in hit)
    print(f"canonical recall: {len(hit)}/{len(canon)} = {recall:.2%}")
    for t in sorted(by_type):
        print(f"  {t:<15} {hit_type[t]}/{by_type[t]}")
    for e in missed:
        print(f"  MISS  {e['source']} -{e['type']}-> {e['target']}  ({e['note']})")

    trap_hits = [t for t in traps
                 if edge_key(t["source"], t["target"], t["type"]) in keys]
    print(f"\nadversarial hits: {len(trap_hits)}/{len(traps)}")
    for t in trap_hits:
        print(f"  TRAP  {t['source']} -{t['type']}-> {t['target']} "
              f"[{t['trap_type']}] {t['reason']}")

    reversed_hits = [e for e in canon if e["type"] not in SYMMETRIC
                     and edge_key(e["target"], e["source"], e["type"]) in keys]
    print(f"\nreversed canonicals asserted: {len(reversed_hits)}")
    for e in reversed_hits:
        print(f"  REV   {e['target']} -{e['type']}-> {e['source']} (gold direction is "
              f"{e['source']} -> {e['target']})")

    failures = []
    if recall < args.min_recall:
        failures.append(f"recall {recall:.2%} < {args.min_recall:.2%}")
    if len(trap_hits) > args.max_traps:
        failures.append(f"{len(trap_hits)} trap hits > {args.max_traps}")
    if len(reversed_hits) > args.max_reversed:
        failures.append(f"{len(reversed_hits)} reversed canonicals > {args.max_reversed}")
    if failures:
        print("\nevaluation FAILED: " + "; ".join(failures))
        sys.exit(1)
    print("\nevaluation PASSED")


if __name__ == "__main__":
    main()

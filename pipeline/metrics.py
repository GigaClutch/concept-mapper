"""Network metrics (Phase 5): degree, betweenness, community -> node metrics.

Centrality and community detection treat the graph as undirected (edge types
carry the direction semantics; connectivity is what matters here). Communities
come from greedy modularity maximisation and are numbered by size (0 = the
largest), so ids are stable across runs on the same graph. Re-run after any
graph change, then build_viewer_data.py.
"""

from __future__ import annotations

import json
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def main() -> None:
    graph = json.loads((DATA / "graph.json").read_text(encoding="utf-8"))

    g = nx.Graph()
    g.add_nodes_from(n["id"] for n in graph["nodes"])
    for e in graph["edges"]:
        # parallel typed edges collapse; keep the max weight as tie strength
        w = max(e["weight"], g.edges[e["source"], e["target"]]["weight"]) \
            if g.has_edge(e["source"], e["target"]) else e["weight"]
        g.add_edge(e["source"], e["target"], weight=w)

    betweenness = nx.betweenness_centrality(g, weight=None, normalized=True)
    communities = sorted(nx.community.greedy_modularity_communities(g),
                         key=lambda c: (-len(c), sorted(c)[0]))
    community_of = {nid: i for i, c in enumerate(communities) for nid in c}

    for n in graph["nodes"]:
        n["metrics"] = {
            "degree": g.degree[n["id"]],
            "betweenness": round(betweenness[n["id"]], 6),
            "community": community_of[n["id"]],
        }

    out = DATA / "graph.json"
    out.write_text(json.dumps(graph, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8")
    top = sorted(graph["nodes"], key=lambda n: -n["metrics"]["betweenness"])[:8]
    print(f"wrote {out.relative_to(ROOT)}: {len(communities)} communities; "
          f"most central: " + ", ".join(
              f"{n['label']} ({n['metrics']['betweenness']:.3f})" for n in top))


if __name__ == "__main__":
    main()

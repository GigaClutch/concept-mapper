"""Regenerate viewer/graph.data.js from data/graph.json (for file:// loading)."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

graph = json.loads((ROOT / "data" / "graph.json").read_text(encoding="utf-8"))
out = ROOT / "viewer" / "graph.data.js"
out.write_text("window.GRAPH = " + json.dumps(graph, indent=1, ensure_ascii=False) + ";\n",
               encoding="utf-8")
print(f"wrote {out.relative_to(ROOT)}")

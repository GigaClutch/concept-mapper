"""Regenerate viewer/graph.data.js from data/graph.json (for file:// loading).

Presentation-layer only: edges the independent checker disputes (assist verdict
"incorrect" on a still-undecided spot-check item) get a `disputed` note in the
bundle so visitors see the claim is contested — data/graph.json stays clean,
and the note disappears once the human rules on the item."""

import json
from pathlib import Path

from common import atomic_write

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def load(path, fallback):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else fallback


graph = json.loads((DATA / "graph.json").read_text(encoding="utf-8"))

# the registry knows which domains the map covers; the viewer titles itself
# from this (never from per-node subject fields)
registry_meta = json.loads((DATA / "registry.json").read_text(encoding="utf-8"))["meta"]
graph["meta"]["domains"] = registry_meta.get(
    "domains", [registry_meta.get("domain", "")])

assist = load(DATA / "review_assist.json", {"items": {}}).get("items", {})
sample = load(DATA / "verification_sample.json", {"sample": []})["sample"]
undecided = {(s["source"], s["type"], s["target"])
             for s in sample if not s.get("verdict")}
disputed = 0
for e in graph["edges"]:
    a = assist.get(f"sample|{e['source']}|{e['type']}|{e['target']}")
    if (e["source"], e["type"], e["target"]) in undecided \
            and a and a.get("verdict") == "incorrect":
        e["disputed"] = a.get("reason", "an automated check disputes this claim")
        disputed += 1

out = ROOT / "viewer" / "graph.data.js"
atomic_write(out, "window.GRAPH = " + json.dumps(graph, indent=1, ensure_ascii=False) + ";\n")
print(f"wrote {out.relative_to(ROOT)}"
      + (f" ({disputed} disputed edges flagged)" if disputed else ""))

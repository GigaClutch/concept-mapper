"""Bundle the review queue into viewer/review.data.js (for file:// loading).

Inputs: data/verification_sample.json, data/quarantine/proposed_edges.json,
data/quarantine/proposed_nodes.json. Items that already carry a verdict are
included (the page shows them as already decided). Re-run after any of the
inputs change.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def load(path: Path, fallback):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else fallback


def main() -> None:
    registry = json.loads((DATA / "registry.json").read_text(encoding="utf-8"))
    corpus = json.loads((DATA / "corpus.json").read_text(encoding="utf-8"))
    sample = load(DATA / "verification_sample.json", {"sample": []})
    pedges = load(DATA / "quarantine" / "proposed_edges.json", {"proposals": []})
    pnodes = load(DATA / "quarantine" / "proposed_nodes.json", {"proposed_nodes": []})

    bundle = {
        "built": time.strftime("%Y-%m-%d"),
        "labels": {r["id"]: {"label": r["label"], "type": r["type"]}
                   for r in registry["nodes"]},
        "articles": {a["id"]: {"title": a["title"], "url": a["url"]}
                     for a in corpus["articles"]},
        "sample": sample["sample"],
        "proposed_edges": pedges["proposals"],
        "proposed_nodes": pnodes["proposed_nodes"],
    }
    out = ROOT / "viewer" / "review.data.js"
    out.write_text("window.REVIEW = " + json.dumps(bundle, indent=1, ensure_ascii=False)
                   + ";\n", encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)}: {len(bundle['sample'])} sampled edges, "
          f"{len(bundle['proposed_edges'])} proposed edges, "
          f"{len(bundle['proposed_nodes'])} proposed nodes")


if __name__ == "__main__":
    main()

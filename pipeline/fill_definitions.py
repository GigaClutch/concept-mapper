"""Fill empty/stub node definitions from cached SEP articles (Phase 9).

Targets every graph node whose definition is under 45 characters (empty or a
Wikidata stub like "moral theory"). For each target that matches a CACHED
article (never fetches), one Haiku call reads the article opening and writes a
1-2 sentence neutral definition in its own words. Responses are cached in
data/definitions/responses.json so re-runs are free; nodes without a cached
matching article are reported and skipped. Also normalizes NBSP characters in
all existing definitions.

  python pipeline/fill_definitions.py [--max-cost 0.25]
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from common import (atomic_write, call_cost, load_key, retry_messages_create)
from research import find_sep_sources

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
ARTICLE_CACHE = ROOT / "cache" / "sep" / "articles"
RESPONSES = DATA / "definitions" / "responses.json"

MODEL = "claude-haiku-4-5"
PROMPT_VERSION = "df-v1"
STUB_CHARS = 45
EXCERPT_CHARS = 7000

SCHEMA = {
    "type": "object",
    "properties": {"definition": {"type": "string"}},
    "required": ["definition"],
    "additionalProperties": False,
}


def evidence_article(node_id: str, graph: dict) -> str | None:
    """Fallback source: the article most often cited as evidence on this
    node's edges — the entry that discusses it, even without a title match
    (good_will, maxim etc. are defined inside kant-moral)."""
    counts: dict[str, int] = {}
    for e in graph["edges"]:
        if node_id in (e["source"], e["target"]):
            for ev in e["evidence"]:
                counts[ev["article_id"]] = counts.get(ev["article_id"], 0) + 1
    for aid, _ in sorted(counts.items(), key=lambda kv: -kv[1]):
        if (ARTICLE_CACHE / f"{aid}.txt").exists():
            return aid
    return None


def focused_excerpt(text: str, node: dict) -> str:
    """Article opening plus a window around the first mention of the label,
    so the model sees where the entry actually discusses this node."""
    head = text[:3000]
    import re
    m = re.search(rf"\b{re.escape(node['label'])}\b", text[3000:], re.IGNORECASE)
    if m:
        start = 3000 + max(0, m.start() - 500)
        return head + " […] " + text[start:start + 3500]
    return text[:EXCERPT_CHARS]


def clip(definition: str, limit: int = 300) -> str:
    """Cut at the last sentence end within the limit — never mid-word."""
    d = definition.strip()
    if len(d) <= limit:
        return d
    cut = d[:limit]
    dot = cut.rfind(". ")
    if dot >= 60:
        return cut[:dot + 1]
    return cut[:cut.rfind(" ")] + "…"


def build_prompt(node: dict, article_id: str, excerpt: str) -> str:
    return (
        f"Write a definition of the philosophical entry below for a general "
        f"reader, based on this Stanford Encyclopedia of Philosophy excerpt.\n\n"
        f"ENTRY: {node['label']} ({node['type']})\n\n"
        "Rules: 1-2 sentences, at most 300 characters, IN YOUR OWN WORDS (never "
        "copy the text), neutral encyclopedic tone, no 'According to...', no "
        "mention of the article itself. State what it is, not why it matters.\n\n"
        f"## Excerpt ({article_id})\n\n{excerpt}\n"
    )


def main() -> None:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--max-cost", type=float, default=0.25)
    ap.add_argument("--pace", type=float, default=0.3)
    args = ap.parse_args()

    graph = json.loads((DATA / "graph.json").read_text(encoding="utf-8"))
    contents = json.loads((DATA / "sep_contents.json").read_text(encoding="utf-8"))
    done = json.loads(RESPONSES.read_text(encoding="utf-8")) if RESPONSES.exists() else {}

    # NBSP normalization across every definition (they broke text rendering)
    for n in graph["nodes"]:
        if " " in (n.get("definition") or ""):
            n["definition"] = n["definition"].replace(" ", " ")

    targets = [n for n in graph["nodes"]
               if len((n.get("definition") or "").strip()) < STUB_CHARS]
    print(f"{len(targets)} nodes with empty/stub definitions")

    client = None
    spent, filled, skipped = 0.0, 0, []
    for n in targets:
        if n["id"] in done:
            n["definition"] = done[n["id"]]["definition"]
            filled += 1
            continue
        sources = [s for s in find_sep_sources(n, contents["entries"])
                   if (ARTICLE_CACHE / f"{s['id']}.txt").exists()]
        aid = sources[0]["id"] if sources else evidence_article(n["id"], graph)
        if aid is None:
            skipped.append(n["id"])
            continue
        if spent >= args.max_cost:
            print(f"STOP: cost ${spent:.3f} >= cap ${args.max_cost:.2f}")
            break
        if client is None:
            try:
                key = load_key()
            except RuntimeError as e:
                sys.exit(f"error: {e}")
            import anthropic
            client = anthropic.Anthropic(api_key=key)
        text = (ARTICLE_CACHE / f"{aid}.txt").read_text(encoding="utf-8")
        excerpt = focused_excerpt(text, n)
        resp = retry_messages_create(
            client, model=MODEL, max_tokens=200,
            messages=[{"role": "user", "content": build_prompt(n, aid, excerpt)}],
            output_config={"format": {"type": "json_schema", "schema": SCHEMA}})
        if resp is None:
            print("still rate-limited, stopping run")
            break
        spent += call_cost(MODEL, resp.usage)
        definition = clip(json.loads(
            next(b.text for b in resp.content if b.type == "text"))["definition"])
        done[n["id"]] = {"definition": definition, "article_id": aid,
                         "model": MODEL, "prompt_version": PROMPT_VERSION,
                         "date": time.strftime("%Y-%m-%d")}
        atomic_write(RESPONSES, done)
        n["definition"] = definition
        filled += 1
        print(f"  {n['id']} <- {aid} (${spent:.3f})")
        time.sleep(args.pace)

    atomic_write(DATA / "graph.json", graph)
    print(f"filled {filled} definitions this run (${spent:.4f}); "
          f"{len(skipped)} skipped, no cached article: {skipped}")
    print("now run: validate.py, build_viewer_data.py")


if __name__ == "__main__":
    main()

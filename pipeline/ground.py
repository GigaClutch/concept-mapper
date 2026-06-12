"""Evidence grounding (Phase 4): attach verbatim SEP quotes to backbone edges.

  extract  -> data/ground/responses/<article>.json   one LLM call per cached
              corpus article: which graph edges does this article support, and
              with exactly which sentence? Responses are cached on disk, so
              re-runs never re-spend API credit. A running cost meter enforces
              --max-cost (default $2.00) as a hard stop.
  apply    -> data/graph.json + data/corpus.json + data/quarantine/proposed_edges.json
              attaches quotes that survived verbatim verification, recomputes
              weights (w = 1 - 0.5^n, n = backbone + distinct grounding
              articles), updates article bookkeeping, quarantines proposed
              new edges (never merged directly — D3).

Every quote is verified to be a verbatim substring of the cached article text
(whitespace-normalized, with a punctuation-variant rescue that always stores
the article's own characters). Quotes that fail are dropped, never repaired by
hand — validate.py re-checks them on every build.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

from validate import EDGE_TYPES, edge_key, norm

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
ARTICLE_CACHE = ROOT / "cache" / "sep" / "articles"
RESPONSE_DIR = DATA / "ground" / "responses"
PROPOSED_EDGES = DATA / "quarantine" / "proposed_edges.json"

PROMPT_VERSION = "gr-v2"
DEFAULT_MODEL = "claude-haiku-4-5"
PRICES = {  # USD per million tokens (input, output)
    "claude-haiku-4-5": (1.00, 5.00),
    "claude-sonnet-4-6": (3.00, 15.00),
}
MAX_QUOTE_CHARS = 300

# straight/curly punctuation variants; 1:1 so indices survive translation and
# the stored quote can be recovered from the article's own characters
TRANS = str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"',
                       "–": "-", "—": "-", " ": " "})

TYPE_GLOSS = """\
IS_A: X is a kind/conception of Y | PART_OF: X is a constituent of Y | \
SUBCATEGORY_OF: X is the narrower category | DEVELOPED_BY: concept developed by person | \
EXTENDED_BY: concept extended by later person | DERIVED_FROM: X grew out of Y | \
INFLUENCED_BY: later thinker influenced by earlier | CONTRASTS_WITH: standard opposition | \
CRITIQUES: X argues against Y | RESPONDS_TO: X is a reaction to Y | \
AUTHORED_BY: work written by person | INTRODUCED_IN: concept first/canonically stated in work"""

SCHEMA = {
    "type": "object",
    "properties": {
        "groundings": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "edge_index": {"type": "integer"},
                    "quote": {"type": "string"},
                },
                "required": ["edge_index", "quote"],
                "additionalProperties": False,
            },
        },
        "proposed_edges": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "source": {"type": "string"},
                    "type": {"type": "string"},
                    "target": {"type": "string"},
                    "quote": {"type": "string"},
                },
                "required": ["source", "type", "target", "quote"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["groundings", "proposed_edges"],
    "additionalProperties": False,
}


def load_key() -> str:
    import os
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    env_file = ROOT / ".env"
    if not key and env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            if line.startswith("ANTHROPIC_API_KEY="):
                key = line.split("=", 1)[1].strip()
    if not key:
        sys.exit("no ANTHROPIC_API_KEY in environment or .env")
    return key


def find_verbatim(quote: str, text: str) -> str | None:
    """Return the article's own substring matching the quote, or None."""
    q = re.sub(r"\s+", " ", quote).strip()
    if not q or len(q) > MAX_QUOTE_CHARS:
        return None
    if norm(q) in norm(text):
        return q  # exactly the containment validate.py re-checks on every build
    qt, tt = q.translate(TRANS), text.translate(TRANS)
    i = tt.find(qt)
    if i >= 0:
        return text[i:i + len(qt)]
    return None


def mentions(node: dict, text: str) -> bool:
    names = [node["label"]] + [a for a in node.get("aliases", []) if len(a) >= 4]
    if node["type"] == "person":
        names.append(node["label"].split()[-1])
    return any(re.search(rf"\b{re.escape(n)}\b", text, re.IGNORECASE) for n in names)


def candidate_edges(graph: dict, nodes: dict, text: str) -> list[dict]:
    hit = {nid for nid, n in nodes.items() if mentions(n, text)}
    return [e for e in graph["edges"] if e["source"] in hit and e["target"] in hit]


def build_prompt(article_id: str, text: str, cands: list[dict], nodes: dict) -> str:
    lines = []
    for i, e in enumerate(cands):
        s, t = nodes[e["source"]], nodes[e["target"]]
        lines.append(f"{i}. {s['label']} ({e['source']}) -{e['type']}-> "
                     f"{t['label']} ({e['target']})")
    return (
        "You are grounding a typed knowledge graph of academic philosophy in the "
        f"Stanford Encyclopedia of Philosophy entry '{article_id}'.\n\n"
        "For each numbered relationship below, find ONE short passage in the "
        "article that states or clearly supports that specific relationship. "
        "Rules:\n"
        f"- The quote must be copied EXACTLY, character for character, from the "
        f"article text below — a single contiguous span, at most {MAX_QUOTE_CHARS} "
        "characters. Do not paraphrase, abbreviate with '...', fix typos, or "
        "change punctuation.\n"
        "- The passage must support the SPECIFIC relationship (its direction and "
        "type), not merely mention both items.\n"
        "- The passage must explicitly name, or unmistakably refer to, BOTH "
        "endpoints of the relationship. If an endpoint never appears in the "
        "article's prose (e.g. it occurs only in the bibliography or the "
        "related-entries list), omit every relationship involving it.\n"
        "- A tangential or wrong quote is WORSE than no quote: when in doubt, "
        "omit. Never attach a passage about one endpoint to a relationship "
        "just because no better passage exists.\n"
        "- If the article contains no such passage for a relationship, omit it. "
        "Most relationships will have no quote in any given article; that is "
        "expected. Quality over coverage.\n"
        "- Additionally, you may propose up to 5 NEW relationships this article "
        "clearly states between the listed entities (use the ids in parentheses "
        "and the types from the glossary), each with a supporting quote under "
        "the same rules. Only propose textbook-defensible claims.\n\n"
        f"Relationship types: {TYPE_GLOSS}\n\n"
        f"## Relationships to ground\n\n" + "\n".join(lines) + "\n\n"
        f"## Article text ({article_id})\n\n{text}\n"
    )


def cmd_extract(args) -> None:
    import anthropic

    client = anthropic.Anthropic(api_key=load_key())
    in_price, out_price = PRICES[args.model]
    graph = json.loads((DATA / "graph.json").read_text(encoding="utf-8"))
    registry = json.loads((DATA / "registry.json").read_text(encoding="utf-8"))
    nodes = {r["id"]: r for r in registry["nodes"]}
    corpus = json.loads((DATA / "corpus.json").read_text(encoding="utf-8"))
    only = set(args.articles.split(",")) if args.articles else None

    RESPONSE_DIR.mkdir(parents=True, exist_ok=True)
    spent = 0.0
    last_call = 0.0
    for art in corpus["articles"]:
        aid = art["id"]
        if only and aid not in only:
            continue
        out = RESPONSE_DIR / f"{aid}.json"
        if out.exists():
            print(f"{aid}: cached, skipping")
            continue
        txt_file = ARTICLE_CACHE / f"{aid}.txt"
        if not txt_file.exists():
            print(f"{aid}: no cached text — run scrape_sep.py --article {aid}")
            continue
        if spent >= args.max_cost:
            print(f"STOP: cost meter ${spent:.2f} >= cap ${args.max_cost:.2f}")
            break
        gap = args.pace - (time.monotonic() - last_call)
        if gap > 0:
            time.sleep(gap)
        text = txt_file.read_text(encoding="utf-8")
        cands = candidate_edges(graph, nodes, text)
        if not cands:
            out.write_text(json.dumps({
                "meta": {"article_id": aid, "model": "", "prompt_version": PROMPT_VERSION,
                         "date": time.strftime("%Y-%m-%d"), "skipped": "no candidate edges",
                         "cost_usd": 0.0},
                "groundings": [], "proposed_edges": []}, indent=2) + "\n",
                encoding="utf-8")
            print(f"{aid}: no candidate edges, skipped (no API call)")
            continue

        # the org tier allows ~50K input tokens/minute and one article is most
        # of that, so pace calls and honor retry-after on 429s
        for attempt in range(5):
            try:
                resp = client.messages.create(
                    model=args.model,
                    max_tokens=16000,
                    messages=[{"role": "user",
                               "content": build_prompt(aid, text, cands, nodes)}],
                    output_config={"format": {"type": "json_schema", "schema": SCHEMA}},
                )
                break
            except anthropic.RateLimitError as e:
                wait = 60
                if e.response is not None:
                    wait = max(int(e.response.headers.get("retry-after", "60")), 30)
                print(f"{aid}: rate-limited, waiting {wait}s (attempt {attempt + 1}/5)")
                time.sleep(wait)
        else:
            print(f"{aid}: still rate-limited after 5 attempts, stopping run")
            break
        last_call = time.monotonic()
        cost = (resp.usage.input_tokens * in_price
                + resp.usage.output_tokens * out_price) / 1e6
        spent += cost
        if resp.stop_reason == "max_tokens":
            print(f"{aid}: response truncated at max_tokens — rerun later with a "
                  f"higher cap | ${cost:.4f} (total ${spent:.4f})")
            continue  # no response file written, so a rerun retries this article
        try:
            raw = json.loads(next(b.text for b in resp.content if b.type == "text"))
        except (StopIteration, json.JSONDecodeError) as exc:
            print(f"{aid}: unparseable response ({exc}) — skipping, rerun retries "
                  f"| ${cost:.4f} (total ${spent:.4f})")
            continue

        groundings, dropped = [], 0
        for g in raw.get("groundings", []):
            i = g.get("edge_index", -1)
            if not (0 <= i < len(cands)):
                dropped += 1
                continue
            vq = find_verbatim(g.get("quote", ""), text)
            if vq is None:
                dropped += 1
                continue
            e = cands[i]
            groundings.append({"source": e["source"], "type": e["type"],
                               "target": e["target"], "quote": vq})
        proposals = []
        for p in raw.get("proposed_edges", []):
            vq = find_verbatim(p.get("quote", ""), text)
            if vq is None or p.get("type") not in EDGE_TYPES \
                    or p.get("source") not in nodes or p.get("target") not in nodes:
                dropped += 1
                continue
            proposals.append({"source": p["source"], "type": p["type"],
                              "target": p["target"], "quote": vq})

        out.write_text(json.dumps({
            "meta": {"article_id": aid, "model": args.model,
                     "prompt_version": PROMPT_VERSION,
                     "date": time.strftime("%Y-%m-%d"),
                     "candidates": len(cands),
                     "input_tokens": resp.usage.input_tokens,
                     "output_tokens": resp.usage.output_tokens,
                     "cost_usd": round(cost, 6), "dropped_unverifiable": dropped},
            "groundings": groundings, "proposed_edges": proposals},
            indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"{aid}: {len(cands)} candidates -> {len(groundings)} verified quotes, "
              f"{len(proposals)} proposals, {dropped} dropped | ${cost:.4f} "
              f"(total ${spent:.4f})")
    print(f"extract done — this run spent ${spent:.4f}")


def cmd_apply(_args) -> None:
    graph = json.loads((DATA / "graph.json").read_text(encoding="utf-8"))
    corpus = json.loads((DATA / "corpus.json").read_text(encoding="utf-8"))
    by_key = {edge_key(e["source"], e["target"], e["type"]): e for e in graph["edges"]}
    grounded_per_article: dict[str, int] = {}
    proposed_per_article: dict[str, int] = {}
    proposals = []
    attached = 0

    for f in sorted(RESPONSE_DIR.glob("*.json")):
        doc = json.loads(f.read_text(encoding="utf-8"))
        aid = doc["meta"]["article_id"]
        grounded_per_article.setdefault(aid, 0)
        for g in doc["groundings"]:
            e = by_key.get(edge_key(g["source"], g["target"], g["type"]))
            if e is None:
                continue
            if any(ev["article_id"] == aid for ev in e["evidence"]):
                continue  # one quote per (edge, article): weight counts articles
            e["evidence"].append({"article_id": aid, "quote": g["quote"]})
            if e.get("status") == "unverified":
                e["status"] = "grounded"
            attached += 1
            grounded_per_article[aid] += 1
        existing = {edge_key(e["source"], e["target"], e["type"]) for e in graph["edges"]}
        for p in doc["proposed_edges"]:
            if edge_key(p["source"], p["target"], p["type"]) in existing:
                continue
            proposals.append({**p, "article_id": aid, "status": "quarantined"})
            proposed_per_article[aid] = proposed_per_article.get(aid, 0) + 1

    for e in graph["edges"]:
        n = 1 + len(e["evidence"])  # backbone assertion + distinct grounding articles
        e["weight"] = 1 - 0.5 ** n

    title_url = {a["id"]: a for a in corpus["articles"]}
    graph["articles"] = [
        {"id": aid, "title": title_url[aid]["title"], "url": title_url[aid]["url"],
         "retrieved": time.strftime("%Y-%m-%d"),
         "grounded_edges": cnt, "proposed_edges": proposed_per_article.get(aid, 0)}
        for aid, cnt in sorted(grounded_per_article.items()) if cnt > 0
    ]
    for a in corpus["articles"]:
        if (ARTICLE_CACHE / f"{a['id']}.txt").exists():
            a["retrieved"] = time.strftime("%Y-%m-%d")
        a["grounded_edges"] = grounded_per_article.get(a["id"], 0)
        a["proposed_edges"] = proposed_per_article.get(a["id"], 0)

    (DATA / "graph.json").write_text(
        json.dumps(graph, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (DATA / "corpus.json").write_text(
        json.dumps(corpus, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    PROPOSED_EDGES.write_text(json.dumps({
        "meta": {"built": time.strftime("%Y-%m-%d"), "source": f"ground {PROMPT_VERSION}",
                 "count": len(proposals),
                 "note": "evidence-backed edges proposed by the grounding pass; "
                         "await Phase 5 human review, never merged directly (D3)"},
        "proposals": proposals}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    grounded_edges = sum(1 for e in graph["edges"] if e["evidence"])
    print(f"attached {attached} quotes -> {grounded_edges}/{len(graph['edges'])} edges "
          f"have evidence; {len(proposals)} proposed edges quarantined")
    print("now run: validate.py, evaluate.py --graph, build_viewer_data.py")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    ex = sub.add_parser("extract", help="one grounding LLM call per cached article")
    ex.add_argument("--articles", help="comma-separated article ids (default: all)")
    ex.add_argument("--model", default=DEFAULT_MODEL, choices=sorted(PRICES))
    ex.add_argument("--max-cost", type=float, default=2.00,
                    help="hard stop for this run's estimated spend in USD")
    ex.add_argument("--pace", type=float, default=55.0,
                    help="minimum seconds between API calls (rate-limit pacing)")
    sub.add_parser("apply", help="attach verified quotes to graph.json")
    args = ap.parse_args()
    {"extract": cmd_extract, "apply": cmd_apply}[args.cmd](args)


if __name__ == "__main__":
    main()

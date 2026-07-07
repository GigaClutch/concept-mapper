"""Assisted review (Phase 5+): an independent model pre-checks each pending
review item so a non-specialist can supervise instead of judge from scratch.

For every undecided item in the review queue — spot-check sample edges,
quarantined proposed edges/nodes, and live provisional research edges/nodes —
this runs ONE call to an independent verifier model (default a different model
from the one that generated the map, for genuine second-opinion independence).
The verifier returns, in plain English:
  - verdict: correct | incorrect | unsure
  - quote_check: does the attached SEP quote actually support THIS specific
    claim (right entities, right direction)? yes | no | no_quote
  - reason: one short sentence a non-expert can sanity-check

Results are written to data/review_assist.json after every item (an
interrupted run keeps everything already paid for), keyed per item and cached,
so re-runs are free and only new items cost anything. A cost meter + --max-cost
hard stop bounds spend. build_review_data.py folds these verdicts into the
review page, which uses them to bulk-accept the clearly-correct items and flag
the rest. The human still makes the final call — this only triages the work.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from common import PRICES, atomic_write, call_cost, load_key, retry_messages_create
from validate import edge_key

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
ASSIST = DATA / "review_assist.json"
DEFAULT_MODEL = "claude-sonnet-4-6"

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
    "properties": {
        "verdict": {"type": "string", "enum": ["correct", "incorrect", "unsure"]},
        "quote_check": {"type": "string", "enum": ["yes", "no", "no_quote"]},
        "reason": {"type": "string"},
    },
    "required": ["verdict", "quote_check", "reason"],
    "additionalProperties": False,
}


def plain_edge(slabel, etype, tlabel):
    return f"{slabel} {SENTENCE.get(etype, etype.replace('_', ' ').lower())} {tlabel}."


def collect_items() -> list[dict]:
    registry = json.loads((DATA / "registry.json").read_text(encoding="utf-8"))
    labels = {r["id"]: r for r in registry["nodes"]}
    graph = json.loads((DATA / "graph.json").read_text(encoding="utf-8"))
    edge_by_key = {edge_key(e["source"], e["target"], e["type"]): e
                   for e in graph["edges"]}
    arts = {a["id"]: a for a in graph.get("articles", [])}

    def lab(i):
        return (labels.get(i) or {}).get("label", i)

    def quote_for(src, tgt, et):
        e = edge_by_key.get(edge_key(src, tgt, et))
        if e and e.get("evidence"):
            ev = e["evidence"][0]
            return ev["quote"], ev["article_id"]
        return "", ""

    items = []

    sample = json.loads((DATA / "verification_sample.json").read_text(encoding="utf-8"))
    for s in sample.get("sample", []):
        if s.get("verdict") in ("accept", "reject"):
            continue
        q, aid = quote_for(s["source"], s["target"], s["type"])
        items.append({
            "section": "sample", "key": f"{s['source']}|{s['type']}|{s['target']}",
            "kind": "edge", "claim": plain_edge(lab(s["source"]), s["type"], lab(s["target"])),
            "quote": q, "article_id": aid, "context": s.get("rationale", "")})

    pe = json.loads((DATA / "quarantine" / "proposed_edges.json").read_text(encoding="utf-8"))
    for p in pe.get("proposals", []):
        if p.get("status") not in (None, "quarantined"):
            continue
        items.append({
            "section": "proposed_edges",
            "key": f"{p['source']}|{p['type']}|{p['target']}",
            "kind": "edge", "claim": plain_edge(lab(p["source"]), p["type"], lab(p["target"])),
            "quote": p.get("quote", ""), "article_id": p.get("article_id", ""),
            "context": ""})

    pn = json.loads((DATA / "quarantine" / "proposed_nodes.json").read_text(encoding="utf-8"))
    for p in pn.get("proposed_nodes", []):
        if p.get("status") not in (None, "", "proposed"):
            continue
        items.append({
            "section": "proposed_nodes", "key": p["label"], "kind": "node",
            "claim": f"Add a new {p.get('type') or 'entry'} called “{p['label']}”.",
            "quote": "", "article_id": "", "context": p.get("reason", "")})

    for e in graph["edges"]:
        if e.get("origin") == "research" and e.get("status") == "unverified":
            ev = e["evidence"][0] if e.get("evidence") else {}
            items.append({
                "section": "researched_edges",
                "key": f"{e['source']}|{e['type']}|{e['target']}", "kind": "edge",
                "claim": plain_edge(lab(e["source"]), e["type"], lab(e["target"])),
                "quote": ev.get("quote", ""), "article_id": ev.get("article_id", ""),
                "context": ""})
    for n in graph["nodes"]:
        if n.get("status") == "provisional":
            items.append({
                "section": "researched_nodes", "key": n["id"], "kind": "node",
                "claim": f"Add a new {n['type']} called “{n['label']}”.",
                "quote": "", "article_id": "", "context": n.get("definition", "")})

    for it in items:
        it["src"] = arts.get(it["article_id"], {}).get("title", it["article_id"])
    return items


def build_prompt(it: dict) -> str:
    p = ("You are an academic philosophy fact-checker helping a NON-SPECIALIST decide "
         "whether to keep an entry in a philosophy reference map. Judge the claim below "
         "as mainstream academic philosophy.\n\n"
         f"CLAIM: {it['claim']}\n")
    if it["context"] and it["kind"] == "node":
        p += f"PROPOSED DESCRIPTION: {it['context']}\n"
    if it["quote"]:
        p += (f"\nSUPPORTING QUOTE (verbatim from the Stanford Encyclopedia entry "
              f"'{it['src']}'):\n“{it['quote']}”\n\n"
              "Decide TWO things: (1) is the claim correct? (2) does this quote actually "
              "support THIS SPECIFIC claim — naming or clearly referring to BOTH things "
              "and the right direction? A quote that only mentions the general topic, or "
              "supports a different relationship, does NOT support the claim (quote_check "
              "= no). Set quote_check to yes only if the quote genuinely backs the exact "
              "claim.\n")
    else:
        p += ("\nThere is no source quote for this item. Judge it from your own knowledge "
              "and set quote_check = no_quote.\n")
    p += ("\nBe skeptical: reversed direction, a wrong or conflated person/work, an "
          "anachronism, or a description that misstates the concept all mean verdict = "
          "incorrect. Use 'unsure' only when genuinely borderline. The reason must be ONE "
          "short plain-English sentence a non-expert can check, naming the decisive fact "
          "(e.g. who actually developed it, or which book it is really in). Keep it under "
          "200 characters.")
    return p


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--model", default=DEFAULT_MODEL, choices=sorted(PRICES))
    ap.add_argument("--limit", type=int, default=0, help="max items this run (0 = all)")
    ap.add_argument("--sections", help="comma-separated subset, e.g. proposed_edges,researched_nodes")
    ap.add_argument("--max-cost", type=float, default=1.50)
    args = ap.parse_args()

    try:
        key = load_key()
    except RuntimeError as e:
        sys.exit(f"error: {e}")
    import anthropic
    client = anthropic.Anthropic(api_key=key)

    done = {}
    if ASSIST.exists():
        done = json.loads(ASSIST.read_text(encoding="utf-8")).get("items", {})

    def save():
        atomic_write(ASSIST, {
            "meta": {"built": time.strftime("%Y-%m-%d"), "model": args.model,
                     "checked": len(done), "note": "independent verifier verdicts for the "
                     "review queue; verdict in {correct,incorrect,unsure}"},
            "items": done})

    items = collect_items()
    if args.sections:
        keep = set(args.sections.split(","))
        items = [it for it in items if it["section"] in keep]
    todo = [it for it in items if f"{it['section']}|{it['key']}" not in done]
    if args.limit:
        todo = todo[:args.limit]
    print(f"{len(items)} pending items, {len(done)} already checked, {len(todo)} to do now")

    spent = 0.0
    for i, it in enumerate(todo, 1):
        if spent >= args.max_cost:
            print(f"STOP: cost ${spent:.3f} >= cap ${args.max_cost:.2f}")
            break
        resp = retry_messages_create(
            client, model=args.model, max_tokens=400,
            messages=[{"role": "user", "content": build_prompt(it)}],
            output_config={"format": {"type": "json_schema", "schema": SCHEMA}})
        if resp is None:
            print(f"  [{i}/{len(todo)}] still rate-limited after retries, stopping run")
            break
        raw = json.loads(next(b.text for b in resp.content if b.type == "text"))
        spent += call_cost(args.model, resp.usage)
        done[f"{it['section']}|{it['key']}"] = {
            "verdict": raw["verdict"], "quote_check": raw["quote_check"],
            "reason": raw["reason"], "model": args.model, "date": time.strftime("%Y-%m-%d")}
        save()
        flag = {"correct": "OK ", "incorrect": "BAD", "unsure": "?? "}[raw["verdict"]]
        print(f"  [{i}/{len(todo)}] {flag} {it['claim'][:64]}")
        print(f"          quote_supports={raw['quote_check']} | {raw['reason'][:90]}")

    save()
    tally = {}
    for v in done.values():
        tally[v["verdict"]] = tally.get(v["verdict"], 0) + 1
    print(f"\nwrote {ASSIST.relative_to(ROOT)} | this run ${spent:.4f} | "
          f"totals: {tally}")


if __name__ == "__main__":
    main()

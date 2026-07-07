"""Shared pipeline helpers (Phase 7): one source of truth for the D4 weight
formula, atomic writes, registry loading, and the Anthropic call plumbing
(prices, cost, retries). The weight formula here reproduces validate.py's
reference check exactly — every writer must go through it.

anthropic is imported lazily inside the functions that need it, so the
offline stages (validate, build_*, merge, metrics) and CI can import this
module without anthropic installed.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

PRICES = {  # USD per million tokens (input, output)
    "claude-haiku-4-5": (1.00, 5.00),
    "claude-sonnet-4-6": (3.00, 15.00),
}


def edge_weight(edge: dict) -> float:
    """D4: w = 1 - 0.5^n, n = backbone assertion + supporting evidence items,
    min 1. Evidence the semantic check rejected (support == "no") stays
    attached as context but no longer counts toward the weight (Phase 9)."""
    n = (1 if edge.get("origin") == "backbone" else 0) + \
        sum(1 for ev in edge.get("evidence", []) if ev.get("support") != "no")
    return 1 - 0.5 ** max(n, 1)


def recompute_weights(edges: list[dict]) -> list[dict]:
    """Restamp every edge's weight in place; returns the same list."""
    for e in edges:
        e["weight"] = edge_weight(e)
    return edges


def atomic_write(path: Path, doc) -> None:
    """Write JSON (dict/list) or raw text via tmp + replace; never a torn file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    text = doc if isinstance(doc, str) else \
        json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
    tmp = path.with_suffix(".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def preserve_built(path: Path, doc: dict) -> dict:
    """Keep the existing meta.built stamp when the document is otherwise
    unchanged, so idempotent re-runs stay byte-identical."""
    path = Path(path)
    if path.exists() and "meta" in doc:
        try:
            old = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return doc
        old_built = old.get("meta", {}).get("built")
        if old_built:
            probe = json.loads(json.dumps(doc))
            probe["meta"]["built"] = old_built
            if probe == old:
                doc["meta"]["built"] = old_built
    return doc


def load_registry(path: Path | None = None) -> tuple[dict, list[dict], dict, dict]:
    """Load registry.json -> (doc, rows, by_id, resolve): the full document
    (mutate + write back), its nodes list, id -> row, and casefolded
    id/label/alias -> canonical id."""
    doc = json.loads(Path(path or DATA / "registry.json").read_text(encoding="utf-8"))
    rows = doc["nodes"]
    by_id = {r["id"]: r for r in rows}
    resolve: dict[str, str] = {}
    for r in rows:
        resolve[r["id"].casefold()] = r["id"]
        resolve.setdefault(r["label"].casefold(), r["id"])
        for a in r.get("aliases", []):
            resolve.setdefault(a.casefold(), r["id"])
    return doc, rows, by_id, resolve


def registry_index(rows: list[dict], rich: bool = True) -> str:
    """Closed-world id index for prompts. rich=True adds time period, aliases
    and description (backbone bb-v1 prompts); rich=False is the compact
    one-line form (research rs-v1 prompts)."""
    lines = []
    for r in sorted(rows, key=lambda r: (r["type"], r["id"])):
        if rich:
            alias = f" — aka: {', '.join(r['aliases'])}" if r.get("aliases") else ""
            desc = f" | {r['wd_description']}" if r.get("wd_description") else ""
            when = f" ({r['time_period']})" if r.get("time_period") else ""
            lines.append(f"{r['id']}  [{r['type']}]  {r['label']}{when}{alias}{desc}")
        else:
            lines.append(f"{r['id']}  [{r['type']}]  {r['label']}")
    return "\n".join(lines)


def load_key() -> str:
    """ANTHROPIC_API_KEY from the environment or .env; raises RuntimeError if
    absent — CLI entry points catch it and exit 1, serve.py survives it."""
    import os
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    env_file = ROOT / ".env"
    if not key and env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            if line.startswith("ANTHROPIC_API_KEY="):
                key = line.split("=", 1)[1].strip()
    if not key:
        raise RuntimeError("no ANTHROPIC_API_KEY in environment or .env")
    return key


def call_cost(model: str, usage) -> float:
    """USD for one API response, given resp.usage."""
    in_p, out_p = PRICES[model]
    return (usage.input_tokens * in_p + usage.output_tokens * out_p) / 1e6


def retry_messages_create(client, attempts: int = 5, min_wait: int = 30, **kwargs):
    """client.messages.create(**kwargs), honoring retry-after on 429s.
    Returns the response, or None if still rate-limited after all attempts."""
    import anthropic
    for attempt in range(attempts):
        try:
            return client.messages.create(**kwargs)
        except anthropic.RateLimitError as e:
            wait = 60
            if e.response is not None:
                wait = max(int(e.response.headers.get("retry-after", "60")), min_wait)
            print(f"rate-limited, waiting {wait}s (attempt {attempt + 1}/{attempts})")
            time.sleep(wait)
    return None

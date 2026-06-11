"""Resolve seed entries to Wikidata QIDs and enrich them -> data/wikidata_enrichment.json.

For every entry in data/seeds.json (concepts, persons, schools, works):
  1. search Wikidata (wbsearchentities, prefix-based) using the entry's
     search override, label, then aliases, until candidates appear;
  2. fetch claims for the top candidates in batches (wbgetentities, cached);
  3. pick a candidate by type-specific verification:
       person  -> P31 human AND birth year (P569) within +/-3 of expect_birth
       work    -> P50 author contains the resolved QID of author_id
       concept/school -> highest description/label keyword score, never a
                         disambiguation page; always flagged for human review
  4. record label / description / aliases / dates from Wikidata.

Hand-curated qids in seeds.json are verified the same way (qid_source
"curated-verified"; a failure is reported loudly, never silently kept).

qid_source values: curated-verified | auto-verified | auto-unverified | unresolved.
Idempotent: all API calls cached in cache/wikidata/api_cache.json.
"""

from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CACHE_DIR = ROOT / "cache" / "wikidata"
CACHE_FILE = CACHE_DIR / "api_cache.json"

API = "https://www.wikidata.org/w/api.php"
USER_AGENT = ("ConceptMapperBot/0.1 (personal research project; "
              "low-volume cached registry bootstrap)")
DELAY_S = 2.0
N_CANDIDATES = 5
MAX_RETRIES = 8

BAD_CLASSES = {
    "Q4167410",   # disambiguation page
    "Q4167836",   # Wikimedia category
    "Q13442814",  # scholarly article
    "Q101352",    # family name
    "Q202444",    # given name
    "Q11424",     # film
    "Q5398426",   # television series
    "Q482994",    # album
}
CONCEPT_KEYWORDS = re.compile(
    r"philosoph|ethic|moral|kant|aristot|hume|virtue|normative|metaethic|"
    r"epistemolog|metaphys|doctrine|theory|principle|school of|concept",
    re.I)

session = requests.Session()
session.headers["User-Agent"] = USER_AGENT

_cache: dict = {}
_cache_dirty = 0


def load_cache() -> None:
    global _cache
    if CACHE_FILE.exists():
        _cache = json.loads(CACHE_FILE.read_text(encoding="utf-8"))


def save_cache() -> None:
    global _cache_dirty
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(_cache), encoding="utf-8")
    _cache_dirty = 0


def api_get(params: dict) -> dict:
    """Cached, rate-limited GET against the Wikidata action API."""
    global _cache_dirty
    key = json.dumps(params, sort_keys=True)
    if key in _cache:
        return _cache[key]
    data = None
    for attempt in range(MAX_RETRIES):
        time.sleep(DELAY_S)
        resp = session.get(API, params={**params, "format": "json", "maxlag": 5},
                           timeout=30)
        if resp.status_code == 429:
            wait = int(resp.headers.get("Retry-After", 0) or 0) or 30 * (attempt + 1)
            print(f"    429 rate-limited, backing off {wait}s ...")
            time.sleep(wait)
            continue
        resp.raise_for_status()
        data = resp.json()
        if "error" in data and data["error"].get("code") == "maxlag":
            # Retry-After during lag spikes is often a too-optimistic 5s;
            # escalate so a multi-minute spike doesn't exhaust the retries
            wait = max(int(resp.headers.get("Retry-After", 0) or 0),
                       30 * (attempt + 1))
            print(f"    maxlag, backing off {wait}s ...")
            time.sleep(wait)
            continue
        break
    if data is None or "error" in data:
        save_cache()
        sys.exit(f"giving up after {MAX_RETRIES} attempts on {params.get('action')}")
    _cache[key] = data
    _cache_dirty += 1
    if _cache_dirty >= 20:
        save_cache()
    return data


def search_candidates(entry: dict) -> list[dict]:
    """Try search override, then label, then aliases; return top candidates."""
    queries = []
    if entry.get("search"):
        queries.append(entry["search"])
    queries.append(entry["label"])
    queries.extend(entry.get("aliases", []))
    for q in queries:
        data = api_get({"action": "wbsearchentities", "search": q,
                        "language": "en", "uselang": "en",
                        "type": "item", "limit": 20})
        hits = data.get("search", [])
        if hits:
            return hits[:N_CANDIDATES]
    return []


def fetch_entities(qids: list[str]) -> dict[str, dict]:
    """Batched wbgetentities for labels/aliases/descriptions/claims."""
    out: dict[str, dict] = {}
    qids = [q for q in dict.fromkeys(qids) if q]
    for i in range(0, len(qids), 50):
        batch = qids[i:i + 50]
        data = api_get({"action": "wbgetentities", "ids": "|".join(batch),
                        "props": "labels|aliases|descriptions|claims",
                        "languages": "en"})
        out.update(data.get("entities", {}))
    return out


# ---- claim helpers -------------------------------------------------------

def claim_ids(entity: dict, prop: str) -> list[str]:
    ids = []
    for c in entity.get("claims", {}).get(prop, []):
        v = c.get("mainsnak", {}).get("datavalue", {}).get("value")
        if isinstance(v, dict) and "id" in v:
            ids.append(v["id"])
    return ids


def claim_year(entity: dict, prop: str) -> int | None:
    for c in entity.get("claims", {}).get(prop, []):
        v = c.get("mainsnak", {}).get("datavalue", {}).get("value")
        if isinstance(v, dict) and "time" in v:
            m = re.match(r"^([+-]\d+)-", v["time"])
            if m:
                return int(m.group(1))
    return None


def en(entity: dict, field: str) -> str:
    return entity.get(field, {}).get("en", {}).get("value", "")


def en_aliases(entity: dict, cap: int = 8) -> list[str]:
    return [a["value"] for a in entity.get("aliases", {}).get("en", [])][:cap]


# ---- type-specific verification ------------------------------------------

def pick_person(entry: dict, cands: list[dict], ents: dict) -> tuple[str, str]:
    for c in cands:
        e = ents.get(c["id"], {})
        if "Q5" not in claim_ids(e, "P31"):
            continue
        born = claim_year(e, "P569")
        if born is None or abs(born - entry["expect_birth"]) > 3:
            continue
        return c["id"], "auto-verified"
    return "", "unresolved"


def pick_work(entry: dict, cands: list[dict], ents: dict,
              author_qid: str) -> tuple[str, str]:
    if author_qid:
        for c in cands:
            if author_qid in claim_ids(ents.get(c["id"], {}), "P50"):
                return c["id"], "auto-verified"
    return "", "unresolved"


def pick_concept(entry: dict, cands: list[dict], ents: dict) -> tuple[str, str]:
    best, best_score = "", 0
    for rank, c in enumerate(cands):
        e = ents.get(c["id"], {})
        if BAD_CLASSES & set(claim_ids(e, "P31")):
            continue
        score = 1 - 0.1 * rank
        desc = en(e, "descriptions")
        if CONCEPT_KEYWORDS.search(desc or ""):
            score += 2
        if en(e, "labels").lower() == entry["label"].lower():
            score += 1
        if score > best_score:
            best, best_score = c["id"], score
    if best and best_score >= 2:  # rank/label alone never suffices
        return best, "auto-unverified"
    return "", "unresolved"


def verify_curated(entry: dict, etype: str, ents: dict,
                   author_qid: str) -> str:
    e = ents.get(entry["qid"], {})
    if not e or "missing" in e:
        return "curated-FAILED"
    if etype == "person":
        born = claim_year(e, "P569")
        ok = ("Q5" in claim_ids(e, "P31") and born is not None
              and abs(born - entry["expect_birth"]) <= 3)
    elif etype == "work":
        ok = not author_qid or author_qid in claim_ids(e, "P50")
    else:
        ok = not (BAD_CLASSES & set(claim_ids(e, "P31")))
    return "curated-verified" if ok else "curated-FAILED"


# ---- main ----------------------------------------------------------------

def enrich(entry: dict, etype: str, qid: str, source: str, ents: dict) -> dict:
    rec = {"id": entry["id"], "type": etype, "label": entry["label"],
           "wikidata_qid": qid, "qid_source": source,
           "wd_label": "", "wd_description": "", "wd_aliases": []}
    e = ents.get(qid, {}) if qid else {}
    if e:
        rec["wd_label"] = en(e, "labels")
        rec["wd_description"] = en(e, "descriptions")
        rec["wd_aliases"] = en_aliases(e)
        if etype == "person":
            rec["birth_year"] = claim_year(e, "P569")
            rec["death_year"] = claim_year(e, "P570")
        if etype == "work":
            rec["pub_year"] = claim_year(e, "P577") or claim_year(e, "P571")
    return rec


def main() -> None:
    load_cache()
    seeds = json.loads((DATA / "seeds.json").read_text(encoding="utf-8"))
    groups = [("person", seeds["persons"]), ("concept", seeds["concepts"]),
              ("school", seeds["schools"]), ("work", seeds["works"])]

    # 1. search candidates for every non-curated entry
    cand_map: dict[str, list[dict]] = {}
    all_qids: list[str] = []
    for etype, entries in groups:
        for entry in entries:
            if entry.get("no_qid"):
                print(f"  no-qid   {entry['id']} (reviewed: no Wikidata item)")
            elif entry.get("qid"):
                all_qids.append(entry["qid"])
                print(f"  curated  {entry['id']} ({entry['qid']})")
            else:
                cands = search_candidates(entry)
                cand_map[entry["id"]] = cands
                all_qids.extend(c["id"] for c in cands)
                print(f"  searched {entry['id']}")

    # 2. one batched claims fetch for everything
    print(f"fetching claims for {len(set(all_qids))} candidate entities ...")
    ents = fetch_entities(all_qids)
    save_cache()

    # 3. resolve persons first (works need author QIDs), then the rest
    results: dict[str, dict] = {}
    person_qid: dict[str, str] = {}
    for etype, entries in groups:
        for entry in entries:
            author_qid = person_qid.get(entry.get("author_id", ""), "")
            if entry.get("no_qid"):
                qid, source = "", "curated-none"
            elif entry.get("qid"):
                qid, source = entry["qid"], verify_curated(entry, etype, ents,
                                                           author_qid)
            elif etype == "person":
                qid, source = pick_person(entry, cand_map[entry["id"]], ents)
            elif etype == "work":
                qid, source = pick_work(entry, cand_map[entry["id"]], ents,
                                        author_qid)
            else:
                qid, source = pick_concept(entry, cand_map[entry["id"]], ents)
            if etype == "person" and qid:
                person_qid[entry["id"]] = qid
            results[entry["id"]] = enrich(entry, etype, qid, source, ents)

    out = DATA / "wikidata_enrichment.json"
    out.write_text(json.dumps(
        {"retrieved": time.strftime("%Y-%m-%d"), "entries": list(results.values())},
        indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    counts: dict[str, int] = {}
    for r in results.values():
        counts[r["qid_source"]] = counts.get(r["qid_source"], 0) + 1
    print(f"\nwrote {out.relative_to(ROOT)} ({len(results)} entries)")
    print("qid_source counts:", json.dumps(counts, indent=2))
    problems = [r for r in results.values()
                if r["qid_source"] in ("unresolved", "curated-FAILED")]
    if problems:
        print("\nNEEDS ATTENTION:")
        for r in problems:
            print(f"  {r['qid_source']:>14}  {r['type']:<7} {r['id']}")
    if any(r["qid_source"] == "curated-FAILED" for r in problems):
        sys.exit(1)


if __name__ == "__main__":
    main()

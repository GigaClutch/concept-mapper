# Concept Mapper

Interactive concept map of philosophy: search a concept, see it situated in a typed, evidence-backed network of related concepts, philosophers, schools, and works. Goals: insight by association, relational context, disambiguation.

Full plan lives in the Obsidian vault at `C:\Users\gigac\My Drive\Comp-Sci Vault\Concept Mapper\`: `Concept Mapper - Master Plan.md` (operative roadmap) and `Concept Mapper - Ultimate Build.md` (end-state vision). This file is the distilled, binding version for coding sessions.

## Current state
- **Phase 1 complete:** hand-built Kant cluster (`data/graph.json`, 14 nodes / 17 edges) + static ego-view viewer (`viewer/index.html`, Cytoscape.js, no build step). Viewer reads `graph.data.js` — regenerate with `pipeline/build_viewer_data.py` after any graph.json change.
- **Phase 2 complete (2026-06-11):** `data/registry.json` (137 rows: 71 concepts / 37 persons / 6 schools / 23 works, cross-checked against the vault seed lists; QIDs hand- or claims-verified, auto-resolved rows human-reviewed, 5 reviewed-no-QID) built by `seeds.json → wikidata_bootstrap.py → merge.py`; `data/corpus.json` (30 SEP Ethics entries, ids verified against scraped contents); gold sets in `data/gold/` (32 canonical edges, 25 adversarial traps); `validate.py` green incl. verbatim-quote check against cached `kant-moral`. Note: Q221373 is *deontology*, not the categorical imperative (Q209681) — early plan docs had this wrong.
- **Phase 3 complete (2026-06-11):** backbone generated over the full registry by `pipeline/backbone.py` — six `bb-v1` passes (normative, metaethics, agency/value, works, persons/schools, cross-boundary) answered by `claude-fable-5`; prompts regenerable to `cache/backbone/prompts/`, raw responses committed under `data/backbone/responses/`. Ingest enforces closed world + per-edge-type domain/range (e.g. persons can never source DEVELOPED_BY/AUTHORED_BY — kills direction traps mechanically); unmappable mentions → `data/quarantine/proposed_nodes.json` (11 proposals, incl. Dancy, Thomson, Rousseau). `pipeline/evaluate.py` gates on gold BEFORE merge: 32/32 canonical recall, 0/25 traps, 0 reversed canonicals. Graph: 137 nodes / 195 edges (all registry rows connected, no orphans; Phase 1 hand-built edges kept; generated edges weight 0.5, status `unverified`, extractor-stamped). Human verification sample (25 edges, seed 20260611) awaiting verdicts in `data/verification_sample.json`. Viewer verified against the full graph; `.claude/launch.json` serves it for preview.
- **Phase 4 complete (2026-06-12):** all 30 corpus articles scraped + cached (`pipeline/scrape_corpus.ps1`); `pipeline/ground.py` (`extract` → `apply`) grounds edges via the Anthropic API — `claude-haiku-4-5`, structured outputs, prompt `gr-v2` (v1 attached tangential quotes ~25% of the time; v2 requires the passage to name BOTH endpoints — fixed it), one call per article, responses cached in `data/ground/responses/` (reruns free), cost meter + `--max-cost` hard stop, 55s pacing for the 50K-TPM tier limit. Result: 237 verbatim-verified quotes on 117/195 edges, weights recomputed (n = backbone + distinct grounding articles), 44 evidence-backed proposed edges in `data/quarantine/proposed_edges.json` (await review, D3). Whole phase cost ≈ $0.72 of API credit. `validate.py` green (re-checks all 237 quotes verbatim against cache); gold still 32/32, 0/25 traps. API key lives in gitignored `.env` (C:\Dev copy only — never in OneDrive, never committed).
- **Now doing Phase 5:** metrics + review loop (see Roadmap).

## Architecture decisions (do not silently revisit)
- **D1 — Demo-first:** bounded corpus (Ethics domain, ~20 SEP articles). JSON file storage. No Neo4j, no backend API, no frontend framework until the demo proves valuable. Schema stays migration-ready.
- **D2 — Backbone-first, evidence-second:** the graph is generated from a curated registry using LLM knowledge (backbone), then grounded with SEP evidence quotes. Not mined from scraped text first.
- **D3 — Closed world:** nodes come only from `registry.json` (types: concept | person | school | work). LLM output mapping to unknown concepts goes to `quarantine/proposed_nodes.json`, never straight into the graph. Registry rows carry `wikidata_qid` where available.
- **D4 — Edges:** typed only, no RELATED_TO. Families: hierarchical (IS_A, PART_OF, SUBCATEGORY_OF), developmental (DEVELOPED_BY, EXTENDED_BY, DERIVED_FROM, INFLUENCED_BY), oppositional (CONTRASTS_WITH, CRITIQUES, RESPONDS_TO), bibliographic (AUTHORED_BY, INTRODUCED_IN). CONTRASTS_WITH is symmetric (`meta.symmetric_types`; viewer renders no arrowhead). Weight = `1 − 0.5^n`, n = evidence items (backbone assertion = 1, +1 per distinct grounding article). Never store LLM confidence numbers. Every generated edge carries `extractor: {model, prompt_version, date}`.
- **D5 — Viewer:** ego-network view is primary (≤150 nodes ever shown); atlas mode secondary. Static HTML, no server.
- **D6 — Evaluation:** gold set = canonical seed (~30 hand-written edges) + adversarial set (~20 traps: direction errors, polysemy, plausible-but-false) + verification sample (randomly drawn from real output, human-verified). Recall proxy: compare per-article extraction against SEP "Related Entries". Score every prompt/pipeline change against the gold set before adopting it.

## Data schema (canonical)
```json
// Node
{ "id": "categorical_imperative", "label": "Categorical Imperative",
  "type": "concept", "definition": "...", "aliases": ["CI"],
  "domain": "Ethics", "tradition": "", "time_period": "18th century",
  "wikidata_qid": "Q209681", "status": "curated",
  "metrics": { "degree": 0, "betweenness": 0.0, "community": 0 } }
// Edge
{ "source": "categorical_imperative", "target": "immanuel_kant",
  "type": "DEVELOPED_BY", "weight": 0.75, "origin": "backbone",
  "extractor": { "model": "", "prompt_version": "", "date": "" },
  "evidence": [ { "article_id": "kant-moral", "quote": "..." } ],
  "status": "confirmed" }
// Article
{ "id": "kant-moral", "title": "...", "url": "https://plato.stanford.edu/entries/kant-moral/",
  "retrieved": "2026-06-11", "grounded_edges": 0, "proposed_edges": 0 }
```
Evidence quotes must be verbatim substrings of the cached source text — verify programmatically, reject otherwise.

## Roadmap
2. **Registry bootstrap + gold seed:** scrape SEP table of contents; Wikidata SPARQL for philosophers/concepts/schools/works (labels, aliases, dates, QIDs); cross-check against vault seed lists; prune/merge → `registry.json`. Hand-author gold canonical seed + adversarial set.
3. **Backbone generation:** per-domain LLM passes (JSON-schema-constrained, registry IDs only) + explicit cross-domain pass over boundary concepts. Sample output for human verification. Complete working product at end of this phase.
4. **Evidence grounding:** polite SEP scraper (~20 Ethics entries, cached); LLM grounding pass attaches verified quotes to existing edges, proposes new edges/nodes → quarantine. Recompute weights.
5. **Metrics + review loop:** NetworkX centrality/communities into node metrics; build `review.html` (accept/reject quarantined items, export decisions); re-score, tune, expand.
6. **Polish:** filters, path-finding, URL hash state, keyboard nav, deploy static.

## Suggested repo layout
```
concept-mapper/
  CLAUDE.md
  data/            registry.json, graph.json, gold/, quarantine/, backbone/ (responses + candidates), ground/ (responses)
  pipeline/        scrape_sep.py, wikidata_bootstrap.py, backbone.py, evaluate.py, ground.py, merge.py, metrics.py, validate.py
  viewer/          index.html, graph.data.js (generated), review.html (Phase 5)
  cache/           raw scraped HTML/text (gitignored)
  tests/
```

## Working practices
- Git from the start; commit per phase milestone. Code lives here, NOT in Google Drive (sync corrupts files mid-write — it has happened).
- Windows machine; venv: `.\venv\Scripts\Activate.ps1`.
- Every pipeline stage idempotent and re-runnable; cache scrapes, never re-hit SEP unnecessarily. Be polite: rate-limit, identify the client, respect robots.txt.
- Evidence quotes stay short with attribution + URL (SEP/IEP licensing).
- API spend is metered: LLM pipeline stages cache every response to disk (reruns free), default to `claude-haiku-4-5`, and take a `--max-cost` hard stop. The key sits in gitignored `.env`; keep it out of OneDrive and out of git.
- `validate.py` runs on every graph build: edge endpoints exist in registry, types allowed, weights in range, no duplicate (source,target,type), no orphan nodes, evidence quotes verbatim in cached source.
- When extraction quality is in question, the gold set decides — not vibes.

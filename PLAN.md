# Concept Mapper — Development Plan: Phases 7–12

Established 2026-07-06 from a five-part audit of the whole project (data quality, pipeline
code, viewer/UX, evaluation, product/deployment — 48 verified findings). This replaces the
completed Phase 1–6 roadmap. CLAUDE.md stays the binding architecture record (D1–D7);
this file is the operative work plan.

## Where the project stands

Phases 1–6 shipped: 139-entry Ethics graph, 198 typed connections, 237 verbatim SEP quotes,
gold-gated backbone, browse-time research (D7), assisted review, and a live site at
https://gigaclutch.github.io/concept-mapper/. The mechanical hygiene is genuinely strong:
zero duplicate edges, zero reversed pairs, every weight matches the formula, every quote is
verbatim.

## What the audit found (the honest version)

1. **Nothing the LLM generated has ever been human-confirmed.** 17/198 edges are confirmed —
   all of them the hand-built Phase-1 Kant edges. The 85-item review queue has sat since
   2026-06-12, and the independent verifier flags ~12–20% of sampled edges as wrong; five
   flagged edges are live on the public site today.
2. **The review tool would corrupt the reviewer's work.** `review.html` saves decisions keyed
   by array position, so regenerating the bundle silently shifts every saved verdict. This
   must be fixed *before* anyone clears the queue.
3. **Re-running the pipeline destroys data.** Since D7 shipped, a re-run of `ground.py apply`
   drops the researched `nietzsche` article and mis-weights research edges; a re-run of
   `merge.py` deletes the provisional registry rows (orphaning graph nodes). Most writers are
   non-atomic on a machine with a documented mid-write-corruption history.
4. **"Evidence-backed" leaks.** 45/242 quotes name neither endpoint of their edge; ~20 are bare
   citation fragments ("Rawls 1971") that still inflate weights. The only semantic sample says
   most attached quotes don't support their specific claim.
5. **The quality gates have holes.** The gold set is saturated (frozen at 2026-06-11 vintage,
   can't catch new errors); D7 research output is never gold-gated; the D6 recall proxy was
   never built; GitHub Pages deploys on every push with no validation or freshness gate.
6. **Visitor-facing gaps.** 8 central concepts have empty definitions (~25 more are stubs); a
   4-node care-ethics island and the 2-node Nietzsche island are unreachable from the main
   map; pipeline jargon ("unverified", "backbone") leaks into the UI; no mobile layout; search
   fails silently on non-exact matches; zero SEO/social metadata.

## The plan

Ordering logic: fix everything that can corrupt data or the reviewer's work first (7), then
make the one human-blocked task cheap and get it done (8), then make the evidence claim true
and measurable (9), then polish what visitors see (10), then — and only then — spend on
growth (11–12). Total new API spend across all phases ≈ $2.50 of the ~$5 budget.

### Phase 7 — Safety: nothing corrupts, nothing ships ungated  *(no human needed)*
Goal: every pipeline stage is safe to re-run, the server can't be killed or exploited, and a
broken graph can no longer deploy.
- Fix `viewer/review.html` decision storage: key by item identity (`source|type|target` /
  node id — the keys `assist_review` already uses), embed a bundle fingerprint,
  warn-and-reset on mismatch.
- Fix `ground.py apply` idempotency: union `graph.articles` with existing entries; use the
  origin-aware weight formula; preserve `status`/decision fields in
  `quarantine/proposed_edges.json` on rewrite.
- Fix `merge.py`: carry forward `status: "provisional"` registry rows; run the graph-coverage
  check *before* writing the registry.
- New `pipeline/common.py`: atomic write (tmp+replace), single shared weight function,
  registry loader, API retry + cost meter; adopt across all writers (formula is currently
  duplicated in 4 files, one already divergent).
- Harden `serve.py`: catch `SystemExit` in the research handler; localhost Origin/Host check
  on `POST /api/research` (any webpage can currently burn the budget via CSRF);
  timeout on robots check; count failed-call spend.
- `assist_review.py`: save incrementally so a crash at item 80/85 doesn't discard a paid run.
- Tests for the mutating paths (weight parity, merge preserves provisional, apply_review
  round-trip, serve rollback); add `networkx` to requirements.txt.
- Gate `.github/workflows/pages.yml`: run validate + evaluate + unittest + a bundle-freshness
  diff before upload; red or stale fails the deploy.
- Demo: re-run `ground.py apply` and `merge.py` on live data → validate green, zero loss.

### Phase 8 — Clear the review queue  *(one human session, made cheap first)*
Goal: queue at 0; the five verifier-flagged live edges ruled on; both islands connected or
removed; confirmed share rises from 8.6% toward ~70%.
- Before the human touches anything: land the Phase 7 review.html fix.
- Auto-flip the 13/44 quarantined proposals that are valid when direction-reversed (the D4
  domain/range check catches them mechanically); badge them in the queue.
- Cut friction: j/k + y/n/u keyboard verdicts, auto-advance, hide-decided, per-card links to
  the map and the SEP article (23 no-quote proposals currently give the reviewer nothing).
- `POST /api/decisions` on the existing local `serve.py`: receive the export, snapshot, run
  apply_review → metrics → validate → evaluate → rebuild bundles, roll back on red. Review
  becomes one click end-to-end instead of a 6-script chain.
- Interim safety until verdicts land: badge verifier-disputed edges in the public viewer
  (never auto-remove — the verifier is deliberately strict and has known false positives).
- **Human:** bulk-accept the 33 safe-tier items, work the ~52 rest with assist reasons,
  rule on the 5 flagged live edges.
- Connect the care-ethics island (e.g. `feminist_ethics SUBCATEGORY_OF normative_ethics`,
  grounded from the cached feminism-ethics article, gold-gated); resolve the Nietzsche island.

### Phase 9 — Make "evidence-backed" true and measurable  *(no human needed)*
Goal: every displayed quote demonstrably supports its claim; research output is gold-gated;
coverage has a number.
- Mechanical quote filter in `ground.py`: reject <~40-char quotes and quotes that name
  neither endpoint (label/alias match); recompute weights honestly. Cached responses make
  the re-apply free.
- Semantic pass: one cached Haiku `quote_check` per evidence item (<$1 for all 242); items
  failing it stop counting toward weight and render as "contextual" in the viewer; fold the
  same check into `ground.py` and `research.py` accept paths permanently.
- Add `evaluate.py --graph` to `serve.py`'s post-research snapshot check (research output is
  currently never gold-gated); adopt the growth-era gold policy — every newly researched
  region adds canonical + trap rows (start with Nietzsche direction traps).
- Build `pipeline/recall_proxy.py` (~100 lines, $0): parse Related Entries from cached SEP
  articles, resolve to registry ids, report per-article coverage — the D6 measure that was
  never implemented, and the KPI for all growth work.
- Definition fill: one batched Haiku pass over the 8 empty + ~25 stub definitions from the
  already-cached SEP articles (<$0.50); restore the 14 curated nodes' dropped QIDs; fix the
  duplicate "Utilitarianism" label and shared alias; extend `validate.py` (registry schema,
  label/alias uniqueness, corpus/article consistency).

### Phase 10 — Speak visitor, not pipeline  *(no human needed)*
Goal: a first-time, non-technical, possibly-mobile visitor understands what they're looking
at and trusts what they read.
- Plain language: "unverified" → "awaiting review", relationship labels in sentence form,
  legend explanations; an intro/onboarding hint on first load.
- Fix known UI bugs: node panel renders before the server health-check resolves (Research
  button hidden until you re-select); research error messages destroyed before readable.
- Search/path inputs: prefix + substring fallback and a visible "no entry matches X" state.
- Mobile-responsive layout; accessibility basics (focus, ARIA on controls, contrast);
  failure states for CDN/data load.
- Findability: meta description, OpenGraph/social tags, a static noscript summary.

### Phase 11 — Domain as data  *(no human needed)*
Goal: adding a domain means writing two JSON files, not editing Python — proven by
regenerating Ethics from config with identical gold scores.
- Move the six hand-written backbone passes to `data/passes/ethics.json` behind a
  `--domain` flag; per-domain seeds (`data/seeds_<domain>.json`) merged without touching
  other domains' rows; gold paths per-domain (`data/gold/<domain>/`).
- Move the Wikidata disambiguation keyword list into seeds meta; make `ground.py`'s corpus
  iteration domain-aware; template the viewer title/description from graph meta.
- Regression proof: regenerate the Ethics registry + re-ingest committed backbone responses
  from config; diff for equivalence; gold 32/32 and 0/25 unchanged (the D6 gate for a change
  this size).

### Phase 12 — Second domain: Epistemology pilot  *(human curates seeds + gold, then one review session)*
Goal: a live two-domain map with working cross-domain path-finding, produced through the
hardened loop for ≈ $1 of API spend.
- **Human (Claude-assisted):** curate `seeds_epistemology.json` (~100–140 rows;
  `sep_contents.json` already lists 34 epistemology titles) and a gold set (~30 canonical +
  ~20 traps).
- Bootstrap → merge → backbone passes from config **plus an explicit Ethics↔Epistemology
  boundary pass** (Hume, Kant, rationalism, empiricism already sit in the registry) →
  gold gate → scrape ~30 SEP entries politely → ground with Phase 9 gates (~$0.72) →
  assist_review (~$0.20) → one-click review session → gated deploy.
- Demo: "Path to…" traces a chain from an Ethics concept to an Epistemology concept through
  a boundary node.

## Deferred (explicitly not now)
Timeline/tour/comparison features, canvas performance work (matters past ~500 nodes),
auto-refresh publishing, IEP as a second source, Neo4j/backend anything (D1 stands until the
two-domain demo proves value).

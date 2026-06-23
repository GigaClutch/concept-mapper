# Concept Mapper

An interactive concept map of philosophy. Search a concept — say *categorical imperative* — and
see it situated in a typed, evidence-backed network of related concepts, philosophers, schools, and
works. Goals: insight by association, relational context, disambiguation. Current domain: **Ethics**
(139 entries, 198 typed connections, 237 verbatim quotes from the Stanford Encyclopedia of
Philosophy).

## View it

**No install, no server** — just open `viewer/index.html` in a browser. You get the full map:
search, ego/atlas views, importance sizing, filters, path-finding, sourced quotes, and shareable
links. (The one feature that needs the server below is live "research".)

**With live research** — run the local app server, which adds the browse-time researcher:

```powershell
.\venv\Scripts\Activate.ps1
python pipeline\serve.py            # then open http://localhost:8742/
```

### What you can do in the viewer

- **Search** any concept, philosopher, school, or work (top-left, or press `/`).
- **Ego view** centres an entry with its neighbourhood; **Atlas** shows the whole map (`e` / `a`).
- **Filters** — click any legend tag to show/hide that node type, relationship family, or
  unreviewed items.
- **Path to…** — trace the shortest chain of relationships between two entries.
- **Importance** — bigger circles are bigger "bridges" between topics; each entry shows its rank.
- **Evidence** — click a connection to read the quote(s) that back it, with links to the source.
- **Shareable links** — the address bar always reflects the current view; copy it to share or bookmark.
- **Research** (server only) — land on an un-researched entry and click *Research now* (or flip on
  *auto-research*) to have it read the matching encyclopedia article and grow the map. New entries
  appear dashed until you approve them in the review page.

### Review page

`viewer/review.html` is the accept/reject queue for anything awaiting human sign-off — spot-checks of
the generated map, suggested new connections, and the dashed auto-researched items. Decisions save in
your browser; *Export decisions* downloads `review_decisions.json`, which `pipeline/apply_review.py`
applies back to the map.

## Deploy it

The `viewer/` folder is a static site — host it anywhere (GitHub Pages, Netlify, any static host) and
the read-only map works as-is. Live research is intentionally *not* part of the static deploy: it needs
`serve.py` and an API key, so it stays a local tool.

## How the map is built (pipeline)

Each stage is a script in `pipeline/`, idempotent and re-runnable. See `CLAUDE.md` for the full design
record (decisions D1–D7) and per-phase detail.

| Stage | Script | What it does |
|---|---|---|
| Registry | `wikidata_bootstrap.py` → `merge.py` | the closed-world list of every allowed entry |
| Backbone | `backbone.py` | generates typed connections from LLM knowledge, gold-gated |
| Evidence | `scrape_sep.py`, `ground.py` | attaches verbatim encyclopedia quotes |
| Metrics | `metrics.py` | importance + clustering (NetworkX) |
| Review | `build_review_data.py`, `apply_review.py` | human accept/reject loop |
| Research | `research.py`, `serve.py` | browse-time, on-demand expansion |
| Quality gate | `validate.py`, `evaluate.py` | run on every build; quotes verbatim, gold set must pass |
| Viewer data | `build_viewer_data.py` | regenerates `viewer/graph.data.js` after any graph change |

## Trust & safety

- Every quote is verified to be a **verbatim** substring of the cached source — non-matches are
  dropped, never hand-patched.
- Connections obey a typed direction grammar (e.g. a person is never "developed by" a concept).
- Generated content is scored against a hand-written **gold set** (canonical facts + adversarial
  traps) before it is adopted.
- LLM pipeline stages cache every response (re-runs are free), default to a cheap model, and take a
  `--max-cost` hard stop. The API key lives only in a gitignored `.env`.

## Notes

- Windows + Python venv (`.\venv\Scripts\Activate.ps1`). Dependencies in `requirements.txt`.
- Be polite to the Stanford Encyclopedia: the scraper rate-limits, identifies itself, respects
  robots.txt, and caches everything.

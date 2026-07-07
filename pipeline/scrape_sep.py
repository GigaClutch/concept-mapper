"""Scrape the SEP table of contents (politely, cached) -> data/sep_contents.json.

Idempotent: uses cache/sep/contents.html if present; pass --refresh to refetch.
Also cross-checks the curated sep_corpus ids in data/seeds.json against the
scraped contents and reports any that don't exist.

--article <id> instead fetches a single entry and caches its HTML plus
extracted plain text under cache/sep/articles/ (used by validate.py to check
evidence quotes verbatim). Bulk corpus scraping is Phase 4; this exists so
already-attached evidence can be verified now.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.robotparser
from html.parser import HTMLParser
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "cache" / "sep"
DATA = ROOT / "data"

SEP_BASE = "https://plato.stanford.edu"
CONTENTS_URL = f"{SEP_BASE}/contents.html"
USER_AGENT = (
    "ConceptMapperBot/0.1 (personal research project, single cached fetch; "
    "+https://github.com/local/concept-mapper)"
)
REQUEST_DELAY_S = 3  # politeness gap between any two SEP requests


def robots_allows(url: str) -> bool:
    # fetched with a timeout: urllib's rp.read() has none and can hang the
    # single-threaded app server (serve.py) indefinitely
    resp = requests.get(f"{SEP_BASE}/robots.txt",
                        headers={"User-Agent": USER_AGENT}, timeout=30)
    resp.raise_for_status()
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(resp.text.splitlines())
    return rp.can_fetch(USER_AGENT, url)


def fetch_contents(refresh: bool) -> str:
    CACHE.mkdir(parents=True, exist_ok=True)
    cached = CACHE / "contents.html"
    if cached.exists() and not refresh:
        print(f"using cached {cached.relative_to(ROOT)}")
        return cached.read_text(encoding="utf-8")
    if not robots_allows(CONTENTS_URL):
        sys.exit("robots.txt disallows fetching the contents page; aborting")
    time.sleep(REQUEST_DELAY_S)
    resp = requests.get(CONTENTS_URL, headers={"User-Agent": USER_AGENT}, timeout=30)
    resp.raise_for_status()
    resp.encoding = resp.apparent_encoding or "utf-8"
    cached.write_text(resp.text, encoding="utf-8")
    print(f"fetched and cached {CONTENTS_URL}")
    return resp.text


class ContentsParser(HTMLParser):
    """Collect entries/<id>/ links and their anchor text."""

    LINK_RE = re.compile(r"^entries/([a-z0-9-]+)/?$")

    def __init__(self) -> None:
        super().__init__()
        self.entries: dict[str, str] = {}
        self._current_id: str | None = None
        self._text: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return
        href = dict(attrs).get("href", "")
        m = self.LINK_RE.match(href)
        if m:
            self._current_id = m.group(1)
            self._text = []

    def handle_data(self, data):
        if self._current_id is not None:
            self._text.append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self._current_id is not None:
            title = re.sub(r"\s+", " ", "".join(self._text)).strip()
            # contents page repeats ids under see-also lines; keep first (canonical) title
            if title and self._current_id not in self.entries:
                self.entries[self._current_id] = title
            self._current_id = None


class TextExtractor(HTMLParser):
    """Whole-page text, minus script/style — enough for verbatim-quote checks."""

    SKIP = {"script", "style"}

    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self._skip_depth += 1

    def handle_endtag(self, tag):
        if tag in self.SKIP and self._skip_depth:
            self._skip_depth -= 1

    def handle_data(self, data):
        if not self._skip_depth:
            self.parts.append(data)

    def text(self) -> str:
        # join with "" so inline tags (<em>, <a>) don't inject spurious spaces;
        # the source's own whitespace separates words
        return re.sub(r"\s+", " ", "".join(self.parts))


def fetch_article(article_id: str, refresh: bool) -> None:
    adir = CACHE / "articles"
    adir.mkdir(parents=True, exist_ok=True)
    html_file, txt_file = adir / f"{article_id}.html", adir / f"{article_id}.txt"
    url = f"{SEP_BASE}/entries/{article_id}/"
    if html_file.exists() and not refresh:
        print(f"using cached {html_file.relative_to(ROOT)}")
        html = html_file.read_text(encoding="utf-8")
    else:
        if not robots_allows(url):
            # raise, not sys.exit: SystemExit escapes serve.py's error handling
            # and would kill the app server (library callers catch RuntimeError)
            raise RuntimeError(f"robots.txt disallows {url}; aborting")
        time.sleep(REQUEST_DELAY_S)
        resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=30)
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding or "utf-8"
        html = resp.text
        html_file.write_text(html, encoding="utf-8")
        print(f"fetched and cached {url}")
    ex = TextExtractor()
    ex.feed(html)
    txt_file.write_text(ex.text(), encoding="utf-8")
    print(f"wrote {txt_file.relative_to(ROOT)} ({len(ex.text())} chars)")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true", help="refetch even if cached")
    ap.add_argument("--article", help="fetch a single entry by id instead of the contents page")
    args = ap.parse_args()

    if args.article:
        try:
            fetch_article(args.article, args.refresh)
        except RuntimeError as e:
            sys.exit(str(e))
        return

    html = fetch_contents(args.refresh)
    parser = ContentsParser()
    parser.feed(html)
    entries = [{"id": k, "title": v} for k, v in sorted(parser.entries.items())]
    if len(entries) < 1000:
        sys.exit(f"parsed only {len(entries)} entries — page layout may have changed")

    out = DATA / "sep_contents.json"
    out.write_text(
        json.dumps({"retrieved": time.strftime("%Y-%m-%d"), "source": CONTENTS_URL,
                    "count": len(entries), "entries": entries},
                   indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} ({len(entries)} entries)")

    seeds = json.loads((DATA / "seeds.json").read_text(encoding="utf-8"))
    known = set(parser.entries)
    missing = [c["id"] for c in seeds["sep_corpus"] if c["id"] not in known]
    if missing:
        print(f"WARNING: {len(missing)} curated corpus ids not in SEP contents: {missing}")
    else:
        print(f"all {len(seeds['sep_corpus'])} curated corpus ids verified against SEP contents")


if __name__ == "__main__":
    main()

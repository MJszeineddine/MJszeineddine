# Web Scraping & Browser Automation Lab

Public proof project showing the engineering patterns I use for reliable web-data extraction. It uses only public demo targets and synthetic output — no client code, private data, credentials, or production records.

## What this demonstrates

- Python extraction pipelines for static and JavaScript-rendered pages
- Playwright browser automation for dynamic pages and interaction-heavy flows
- HTTP-first extraction with `httpx` + BeautifulSoup when a browser is unnecessary
- pagination/infinite-scroll style collection boundaries
- retries, timeouts, structured validation, normalization and deduplication
- CSV/JSONL-ready records that can be persisted to PostgreSQL or exposed through FastAPI
- testable separation between fetching, parsing and pipeline logic

## Architecture

```text
Target
  ├─ HTTP path: httpx -> BeautifulSoup
  └─ Browser path: Playwright -> rendered DOM
                    |
                    v
               normalized records
                    |
          validation + deduplication
                    |
              JSONL / CSV / DB
```

## Example

The demo parser targets [Books to Scrape](https://books.toscrape.com/), a public website intentionally created for scraping practice.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
playwright install chromium

python -m scraping_lab.http
python -m scraping_lab.browser
pytest
```

## Production extension points

For real systems I normally add the pieces the target requires: authenticated session handling, API extraction, CSS/XPath selectors, rotating request identities/proxy infrastructure where appropriate, concurrency controls, checkpointing, scheduled runs, PostgreSQL persistence, monitoring, and FastAPI endpoints.

## Scope

This is intentionally a compact public engineering sample. My commercial scraping work spans 100+ websites since 2020, while client source and production data remain private.

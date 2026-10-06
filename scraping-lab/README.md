# Web Scraping & Browser Automation Lab

Public, client-safe proof of the engineering patterns I use for reliable web-data extraction and automation.

The repository uses only public demo targets and synthetic/test data. It contains **no client source code, credentials, private datasets, or production records**.

## What this demonstrates

- Python extraction for static and JavaScript-rendered pages
- Playwright browser automation for interaction-heavy workflows
- Scrapy crawling with domain limits, retry policy and pagination
- HTTP-first extraction with `httpx` + BeautifulSoup when a browser is unnecessary
- structured validation with Pydantic
- retries, timeouts, normalization and deterministic deduplication
- CSV and JSONL delivery
- a FastAPI layer around extraction
- Dockerized execution
- offline parser/unit tests and CI

## Architecture

```text
                         ┌─────────────────────┐
                         │   target website    │
                         └──────────┬──────────┘
                                    │
              ┌─────────────────────┼──────────────────────┐
              │                     │                      │
              ▼                     ▼                      ▼
      httpx + BeautifulSoup      Playwright              Scrapy
       HTTP-first path         browser path          crawler path
              │                     │                      │
              └──────────────┬──────┴──────────────┬──────┘
                             ▼                     ▼
                     normalized records      pagination/retries
                             │
                    validation + dedupe
                             │
            ┌────────────────┼──────────────────┐
            ▼                ▼                  ▼
          CSV/JSONL       PostgreSQL*        FastAPI
                                              │
                                              ▼
                                      consumer / workflow
```

`*` PostgreSQL is shown as a production extension point; this public demo does not require a database to run.

## Project structure

```text
scraping-lab/
├── Dockerfile
├── pyproject.toml
├── src/scraping_lab/
│   ├── api.py              # FastAPI wrapper
│   ├── browser.py          # Playwright extraction
│   ├── http.py             # httpx + BeautifulSoup extraction
│   ├── scrapy_spider.py    # Scrapy crawling example
│   ├── pipeline.py         # validation + deduplication
│   └── output.py           # CSV / JSONL delivery
└── tests/
    ├── test_api.py
    ├── test_parser.py
    └── test_pipeline.py
```

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Only needed for the browser path:
playwright install chromium
```

Run the HTTP path:

```bash
python -m scraping_lab.http
```

Run the browser path:

```bash
python -m scraping_lab.browser
```

Run the Scrapy crawler:

```bash
scrapy runspider src/scraping_lab/scrapy_spider.py -O output/books.json
```

Run the API:

```bash
uvicorn scraping_lab.api:app --reload
```

Then:

```bash
curl "http://127.0.0.1:8000/health"
curl "http://127.0.0.1:8000/demo/books?engine=http&limit=5"
```

Run tests and linting:

```bash
pytest -q
ruff check src tests
```

## Docker

```bash
docker build -t scraping-lab .
docker run --rm -p 8000:8000 scraping-lab
```

The container installs Chromium for the Playwright path and exposes the FastAPI service on port `8000`.

## Why three extraction paths?

A production scraper should not use a browser when ordinary HTTP is enough.

- **HTTP path:** lower cost and higher throughput for server-rendered/public HTML.
- **Playwright path:** dynamic JavaScript, interactions, browser state, or flows that genuinely need a browser.
- **Scrapy path:** crawling many pages with explicit concurrency, retry, pagination and domain policies.

That choice matters more than blindly using the heaviest tool.

## Production extension points

For real systems I add only what the target requires:

- authenticated session and cookie-state handling
- API discovery/extraction
- CSS/XPath selectors
- AJAX and infinite-scroll handling
- proxy/request-identity infrastructure where appropriate
- bounded concurrency and backpressure
- checkpointing and resumable jobs
- PostgreSQL persistence
- scheduled runs and change detection
- FastAPI endpoints
- observability, alerts and failure recovery
- Docker/CI deployment

## Scope and experience

This is intentionally a compact public proof project. My commercial scraping and automation work spans **100+ websites since 2020**. Client implementation details remain private.

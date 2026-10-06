from __future__ import annotations

from fastapi import FastAPI, Query

from .browser import scrape_browser
from .http import scrape_http

app = FastAPI(
    title="Web Scraping & Browser Automation Lab",
    version="0.2.0",
    description="Public demo API for safe HTTP and Playwright extraction patterns.",
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/demo/books")
async def demo_books(
    engine: str = Query(default="http", pattern="^(http|browser)$"),
    limit: int = Query(default=10, ge=1, le=20),
) -> dict[str, object]:
    records = await (scrape_browser() if engine == "browser" else scrape_http())
    return {
        "engine": engine,
        "count": min(limit, len(records)),
        "records": [record.model_dump(mode="json") for record in records[:limit]],
    }

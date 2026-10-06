from __future__ import annotations

from decimal import Decimal
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential

from .pipeline import ProductRecord, deduplicate

BASE_URL = "https://books.toscrape.com/"


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=0.5, min=0.5, max=4),
    reraise=True,
)
async def fetch_html(client: httpx.AsyncClient, url: str) -> str:
    response = await client.get(url, timeout=15)
    response.raise_for_status()
    return response.text


def parse_products(html: str, page_url: str) -> list[ProductRecord]:
    soup = BeautifulSoup(html, "html.parser")
    records: list[ProductRecord] = []

    for card in soup.select("article.product_pod"):
        anchor = card.select_one("h3 a")
        price = card.select_one(".price_color")
        availability = card.select_one(".availability")
        if not anchor or not price or not availability:
            continue

        href = anchor.get("href")
        title = anchor.get("title")
        if not href or not title:
            continue

        records.append(
            ProductRecord(
                source_url=urljoin(page_url, href),
                title=title,
                price_gbp=Decimal(price.get_text(strip=True).replace("£", "")),
                availability=availability.get_text(" ", strip=True),
            )
        )

    return records


async def scrape_http(url: str = BASE_URL) -> list[ProductRecord]:
    headers = {"user-agent": "JawadScrapingLab/0.1 public-demo"}
    async with httpx.AsyncClient(headers=headers, follow_redirects=True) as client:
        html = await fetch_html(client, url)
    return deduplicate(parse_products(html, url))


if __name__ == "__main__":
    import asyncio
    import json

    result = asyncio.run(scrape_http())
    print(json.dumps([r.model_dump(mode="json") for r in result[:5]], indent=2))

from __future__ import annotations

from decimal import Decimal
from urllib.parse import urljoin

from playwright.async_api import Page, async_playwright

from .pipeline import ProductRecord, deduplicate

BASE_URL = "https://books.toscrape.com/"


async def parse_rendered_page(page: Page) -> list[ProductRecord]:
    records: list[ProductRecord] = []

    for card in await page.locator("article.product_pod").all():
        anchor = card.locator("h3 a")
        href = await anchor.get_attribute("href")
        title = await anchor.get_attribute("title")
        price_text = await card.locator(".price_color").inner_text()
        availability = await card.locator(".availability").inner_text()

        if not href or not title:
            continue

        records.append(
            ProductRecord(
                source_url=urljoin(page.url, href),
                title=title,
                price_gbp=Decimal(price_text.strip().replace("£", "")),
                availability=availability,
            )
        )

    return records


async def scrape_browser(url: str = BASE_URL) -> list[ProductRecord]:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=30_000)
            await page.locator("article.product_pod").first.wait_for(timeout=10_000)
            return deduplicate(await parse_rendered_page(page))
        finally:
            await browser.close()


if __name__ == "__main__":
    import asyncio
    import json

    result = asyncio.run(scrape_browser())
    print(json.dumps([r.model_dump(mode="json") for r in result[:5]], indent=2))

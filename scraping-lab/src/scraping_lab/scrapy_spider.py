from __future__ import annotations

from decimal import Decimal
from typing import Any

import scrapy


class BooksSpider(scrapy.Spider):
    """Small public Scrapy example using a site built for scraping practice."""

    name = "books_demo"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    custom_settings = {
        "ROBOTSTXT_OBEY": True,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "DOWNLOAD_DELAY": 0.25,
        "RETRY_TIMES": 2,
        "USER_AGENT": "JawadScrapingLab/0.2 public-demo",
        "LOG_LEVEL": "WARNING",
    }

    def parse(self, response: scrapy.http.Response, **kwargs: Any):
        for card in response.css("article.product_pod"):
            title = card.css("h3 a::attr(title)").get()
            href = card.css("h3 a::attr(href)").get()
            price = card.css(".price_color::text").get()
            availability = " ".join(card.css(".availability *::text").getall()).strip()

            if not title or not href or not price:
                continue

            yield {
                "source_url": response.urljoin(href),
                "title": " ".join(title.split()),
                "price_gbp": str(Decimal(price.replace("£", ""))),
                "availability": " ".join(availability.split()),
            }

        next_href = response.css("li.next a::attr(href)").get()
        if next_href:
            yield response.follow(next_href, callback=self.parse)

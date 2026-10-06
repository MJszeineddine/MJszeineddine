from decimal import Decimal

from scraping_lab.pipeline import ProductRecord, deduplicate


def record(url: str, title: str = "Example") -> ProductRecord:
    return ProductRecord(
        source_url=url,
        title=title,
        price_gbp=Decimal("10.50"),
        availability="  In   stock  ",
    )


def test_text_normalization() -> None:
    item = record("https://example.com/a", "  A   useful   book ")
    assert item.title == "A useful book"
    assert item.availability == "In stock"


def test_deduplicate_by_source_url() -> None:
    first = record("https://example.com/a", "First")
    duplicate = record("https://example.com/a", "Duplicate")
    second = record("https://example.com/b", "Second")

    result = deduplicate([first, duplicate, second])

    assert [item.title for item in result] == ["First", "Second"]

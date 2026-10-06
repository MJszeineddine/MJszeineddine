from __future__ import annotations

from decimal import Decimal
from typing import Iterable

from pydantic import BaseModel, Field, HttpUrl, field_validator


class ProductRecord(BaseModel):
    source_url: HttpUrl
    title: str = Field(min_length=1)
    price_gbp: Decimal = Field(ge=0)
    availability: str = Field(min_length=1)

    @field_validator("title", "availability")
    @classmethod
    def normalize_text(cls, value: str) -> str:
        return " ".join(value.split())


def deduplicate(records: Iterable[ProductRecord]) -> list[ProductRecord]:
    """Keep the first normalized record for each source URL."""
    seen: set[str] = set()
    output: list[ProductRecord] = []

    for record in records:
        key = str(record.source_url)
        if key in seen:
            continue
        seen.add(key)
        output.append(record)

    return output

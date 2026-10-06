from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable

from .pipeline import ProductRecord


def write_jsonl(records: Iterable[ProductRecord], path: str | Path) -> Path:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    with destination.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record.model_dump(mode="json"), ensure_ascii=False) + "\n")

    return destination


def write_csv(records: Iterable[ProductRecord], path: str | Path) -> Path:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["source_url", "title", "price_gbp", "availability"],
        )
        writer.writeheader()
        for record in records:
            row = record.model_dump(mode="json")
            writer.writerow(row)

    return destination

from __future__ import annotations

from typing import Any


def example_detail(title: str, text: str = "", code: str = "") -> dict[str, Any]:
    return {
        "kind": "example",
        "title": title,
        "text": text.strip(),
        "code": code.strip(),
    }


def table_detail(title: str, headers: list[str], rows: list[list[str]], text: str = "") -> dict[str, Any]:
    return {
        "kind": "table",
        "title": title,
        "text": text.strip(),
        "table": {
            "headers": headers,
            "rows": rows,
        },
    }


def explanation_detail(title: str, text: str) -> dict[str, Any]:
    return {
        "kind": "explanation",
        "title": title,
        "text": text.strip(),
    }


def unique_detail_id(base_id: str, taken: set[str], index: int) -> str:
    candidate = f"{base_id}-d{index}"
    serial = index
    while candidate in taken:
        serial += 1
        candidate = f"{base_id}-d{serial}"
    taken.add(candidate)
    return candidate

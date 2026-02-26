from __future__ import annotations

from typing import TypeVar


T = TypeVar("T")


def chunked(seq: list[T], size: int) -> list[list[T]]:
    return [seq[i : i + size] for i in range(0, len(seq), size)]

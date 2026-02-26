from __future__ import annotations

import re


def compact_text(value: str, max_len: int) -> str:
    text = (value or "").strip()
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rstrip() + "…"


def trim_lines(value: str, max_lines: int) -> str:
    lines = (value or "").splitlines()
    if len(lines) <= max_lines:
        return "\n".join(lines)
    return "\n".join(lines[:max_lines]) + "\n# ..."


def normalize_newlines(text: str) -> str:
    return str(text or "").replace("\r\n", "\n").replace("\r", "\n")


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", str(text or "")).strip()

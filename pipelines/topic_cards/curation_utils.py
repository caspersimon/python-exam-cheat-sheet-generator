from __future__ import annotations

import re
from typing import Any


STOPWORDS = {
    "the",
    "a",
    "an",
    "and",
    "or",
    "to",
    "of",
    "for",
    "in",
    "on",
    "with",
    "this",
    "that",
    "what",
    "which",
    "should",
    "you",
    "use",
    "first",
    "question",
    "questions",
    "compact",
    "reference",
}


def safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def safe_str(value: Any) -> str:
    return str(value or "").strip()


def table_signature(table: dict[str, Any] | None) -> str:
    if not table:
        return ""
    headers = "|".join(" ".join(safe_str(cell).lower().split()) for cell in safe_list(table.get("headers")))
    rows = "||".join(
        "|".join(" ".join(safe_str(cell).lower().split()) for cell in safe_list(row))
        for row in safe_list(table.get("rows"))
    )
    return f"{headers}###{rows}"


def token_set(text: Any) -> set[str]:
    raw = re.sub(r"[^a-z0-9\s]+", " ", safe_str(text).lower())
    return {token for token in raw.split() if token and token not in STOPWORDS}


def overlap_score(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    return len(left & right) / min(len(left), len(right))


def structured_question_item(
    *,
    item_id: str,
    summary: str,
    detail: str = "",
    extra: str = "",
    code: str = "",
    table: dict[str, Any] | None = None,
    subtopic_id: str = "",
    subtopic_title: str = "",
) -> dict[str, Any]:
    item: dict[str, Any] = {
        "id": item_id,
        "summary": summary,
        "detail": detail,
        "extra": extra,
        "subtopic_id": subtopic_id,
        "subtopic_title": subtopic_title,
    }
    if code:
        item["code"] = code
    if table:
        item["table"] = table
    return item


def dedupe_section_overlap(sections: dict[str, Any]) -> dict[str, Any]:
    common = sections.get("ai_common_questions", {}) if isinstance(sections.get("ai_common_questions"), dict) else {}
    items = safe_list(common.get("items"))
    key_points = safe_list(sections.get("key_points_to_remember"))
    key_point_texts = [token_set(item.get("text")) for item in key_points if safe_str(item.get("text"))]
    detail_table_sigs = {
        table_signature(detail.get("table"))
        for item in key_points
        for detail in safe_list(item.get("details"))
        if isinstance(detail, dict) and detail.get("table")
    }

    deduped_bullets = []
    seen_bullet_keys: set[str] = set()
    for bullet in safe_list(common.get("bullets")):
        bullet_text = safe_str(bullet)
        if not bullet_text:
            continue
        bullet_key = " ".join(bullet_text.lower().split())
        if bullet_key in seen_bullet_keys:
            continue
        bullet_tokens = token_set(bullet_text)
        if bullet_tokens and any(overlap_score(bullet_tokens, kp_tokens) >= 0.6 for kp_tokens in key_point_texts if kp_tokens):
            continue
        seen_bullet_keys.add(bullet_key)
        deduped_bullets.append(bullet_text)

    deduped_items = []
    seen_item_keys: set[str] = set()
    for item in items:
        if not isinstance(item, dict):
            continue
        item_table_sig = table_signature(item.get("table"))
        if item_table_sig and item_table_sig in detail_table_sigs:
            continue

        item_tokens = token_set(f"{item.get('summary', '')} {item.get('detail', '')}")
        if item_tokens and not item.get("code") and not item.get("table"):
            if any(overlap_score(item_tokens, kp_tokens) >= 0.6 for kp_tokens in key_point_texts if kp_tokens):
                continue

        item_key = "||".join(
            [
                " ".join(safe_str(item.get("summary")).lower().split()),
                " ".join(safe_str(item.get("detail")).lower().split()),
                " ".join(safe_str(item.get("extra")).lower().split()),
                item_table_sig,
                " ".join(safe_str(item.get("code")).lower().split()),
            ]
        )
        if item_key in seen_item_keys:
            continue
        seen_item_keys.add(item_key)
        deduped_items.append(item)

    common["bullets"] = deduped_bullets
    common["items"] = deduped_items
    sections["ai_common_questions"] = common
    return sections

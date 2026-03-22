from __future__ import annotations

import ast
import re
from copy import deepcopy
from typing import Any

from pipelines.topic_cards.manual_curation_card_overrides import apply_card_specific_adjustments
from pipelines.topic_cards.manual_curation_data import CARD_SUMMARIES, TEXT_REWRITES, TITLE_REWRITES, TOPIC_EXCLUDES
from pipelines.topic_cards.study_text import infer_pattern_label

GENERIC_TRACE = "Work through the code in execution order and keep track of the exact value after each step."


def _safe_str(value: object) -> str:
    return str(value or "").strip()


def _clean_text(text: object) -> str:
    return re.sub(r"\s+", " ", _safe_str(text)).strip()


def _rewrite_text(text: object) -> str:
    value = _clean_text(text)
    return TEXT_REWRITES.get(value, value)


def _looks_invalid_python(code: str) -> bool:
    blob = _safe_str(code)
    if not blob:
        return False
    try:
        ast.parse(blob)
    except SyntaxError:
        return True
    return False


def _contains_any(text: str, terms: tuple[str, ...]) -> bool:
    lower = text.lower()
    return any(term in lower for term in terms)


def _match_topic(topic_id: str, *parts: object) -> bool:
    haystack = " \n".join(_safe_str(part) for part in parts if _safe_str(part)).lower()
    excludes = TOPIC_EXCLUDES.get(topic_id, ())
    if excludes and _contains_any(haystack, excludes):
        return False
    return True


def _example_note(topic_id: str, example: dict[str, Any]) -> str:
    why = _rewrite_text(example.get("why"))
    if why and why != GENERIC_TRACE:
        return why

    if topic_id == "w1-functions-and-imports":
        return "Keep track of which name is actually available after `import`, `from ... import ...`, or `as`."
    if topic_id == "w2-dictionaries-and-mappings":
        return "Check whether the code is looking up a key, iterating with `.items()`, or mutating the dictionary."
    if topic_id == "w3-defining-and-calling-functions":
        return "Use `()` to call a function and `[]` to index a sequence; mixing them causes a `TypeError`."
    if topic_id == "w4-string-fundamentals":
        return "Use matching quotes or escape the inner quote; remember string methods return a new string."
    if topic_id == "w4-oop-fundamentals":
        return "`self` is the current object, so instance data should be stored or read through `self.attr`."
    if topic_id == "w5-pandas-core-structures":
        return "Decide first whether the result should be a `Series` or a `DataFrame`, then pick the matching constructor or selection form."
    if topic_id == "w6-datetime":
        return "Keep the direction straight: parse text with `strptime`, format objects with `strftime`, and use `timedelta` for arithmetic."
    return ""


def _question_detail(topic_id: str, item: dict[str, Any]) -> str:
    detail = _rewrite_text(item.get("detail"))
    if detail and detail != GENERIC_TRACE:
        return detail

    code = _safe_str(item.get("code"))
    summary = _safe_str(item.get("summary"))
    if topic_id == "w1-sequences-and-access":
        return "Apply the slice or `range` rule first, then trace the resulting sequence or printed value."
    if topic_id == "w1-objects-and-names":
        return "Decide whether the code is rebinding a name or mutating a shared mutable object."
    if topic_id == "w2-dictionaries-and-mappings":
        return "Check whether membership is testing keys, and trace any lookup or mutation on the dictionary."
    if topic_id == "w3-arguments":
        return "Match arguments to parameters carefully, then ask whether the function mutates an existing object or returns a new one."
    if topic_id == "w4-string-fundamentals":
        return "Decide whether the code is building a new string, escaping characters, or trying an illegal in-place string update."
    if topic_id == "w5-pandas-core-structures":
        return "Identify whether the operation should return a `Series`, `DataFrame`, or scalar before checking the exact syntax."
    inferred = infer_pattern_label(summary, code)
    if inferred and inferred != summary:
        return inferred
    return ""


def _trim_question_meta(extra: object) -> str:
    value = _safe_str(extra)
    value = re.sub(r"\s*•\s*Answer shape:[\s\S]*$", "", value)
    value = re.sub(r"^Lecture question\s*•\s*", "", value)
    return _clean_text(value)


def apply_manual_curation(card: dict[str, Any]) -> dict[str, Any]:
    curated = deepcopy(card)
    topic_id = _safe_str(curated.get("id"))
    sections = curated.setdefault("sections", {})

    summary = CARD_SUMMARIES.get(topic_id)
    if summary:
        sections.setdefault("ai_summary", {})
        sections["ai_summary"]["content"] = summary

    for subtopic in curated.get("subtopics", []):
        subtopic["summary"] = CARD_SUMMARIES.get(topic_id, _rewrite_text(subtopic.get("summary")))

    question_items = []
    seen_question_keys: set[tuple[str, str, str]] = set()
    for item in sections.get("ai_common_questions", {}).get("items", []):
        next_item = deepcopy(item)
        next_item["summary"] = _rewrite_text(next_item.get("summary"))
        next_item["detail"] = _question_detail(topic_id, next_item)
        next_item["extra"] = _trim_question_meta(next_item.get("extra"))
        if not _match_topic(topic_id, next_item.get("summary"), next_item.get("detail"), next_item.get("code"), next_item.get("extra")):
            continue
        key = (_safe_str(next_item.get("summary")), _safe_str(next_item.get("detail")), _safe_str(next_item.get("code")))
        if key in seen_question_keys:
            continue
        seen_question_keys.add(key)
        question_items.append(next_item)
    if sections.get("ai_common_questions"):
        sections["ai_common_questions"]["items"] = question_items[:8]

    key_points = []
    seen_key_points: set[str] = set()
    for item in sections.get("key_points_to_remember", []):
        next_item = deepcopy(item)
        next_item["text"] = _rewrite_text(next_item.get("text"))
        if next_item["text"] in seen_key_points:
            continue
        seen_key_points.add(next_item["text"])
        key_points.append(next_item)
    sections["key_points_to_remember"] = key_points[:10]

    examples = []
    seen_examples: set[tuple[str, str]] = set()
    for item in sections.get("ai_examples", []):
        next_item = deepcopy(item)
        next_item["title"] = TITLE_REWRITES.get(_safe_str(next_item.get("title")), _safe_str(next_item.get("title")) or infer_pattern_label(next_item.get("code")))
        next_item["why"] = _example_note(topic_id, next_item)
        if next_item.get("kind") == "correct" and _looks_invalid_python(next_item.get("code", "")):
            continue
        if not _match_topic(topic_id, next_item.get("title"), next_item.get("why"), next_item.get("code"), next_item.get("output")):
            continue
        key = (_safe_str(next_item.get("title")), _safe_str(next_item.get("code")))
        if key in seen_examples:
            continue
        seen_examples.add(key)
        examples.append(next_item)
    sections["ai_examples"] = examples[:8]

    apply_card_specific_adjustments(
        curated,
        safe_str=_safe_str,
        rewrite_text=_rewrite_text,
        match_topic=_match_topic,
        looks_invalid_python=_looks_invalid_python,
    )

    valid_ids = {
        _safe_str(item.get("id"))
        for bucket in ("lecture_snippets", "exam_questions", "notebook_snippets", "ai_examples", "key_points_to_remember")
        for item in sections.get(bucket, [])
        if isinstance(item, dict) and _safe_str(item.get("id"))
    }
    for subtopic in curated.get("subtopics", []):
        item_ids = subtopic.get("item_ids", {})
        if not isinstance(item_ids, dict):
            continue
        for key, values in list(item_ids.items()):
            if isinstance(values, list):
                item_ids[key] = [value for value in values if _safe_str(value) in valid_ids]

    return curated

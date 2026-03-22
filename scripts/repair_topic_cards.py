#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TOPIC_CARDS_FILE = ROOT / "topic_cards.json"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.topic_cards.core import pretty_topic
SAFE_CARD_MERGES: tuple[tuple[str, str], ...] = (
    ("topic-f-string", "topic-debugging-f-string"),
    ("topic-argument-double-keyword-kwarg-star", "topic-args-double-keyword-kwarg-star"),
    ("topic-global-local-scope", "topic-scope-global"),
    ("topic-1-2-dictionary-manipulation", "topic-2-dictionary-manipulation"),
    ("topic-1-2-dictionary-slicing", "topic-2-dictionary-slicing"),
    ("topic-function", "topic-function-2"),
)


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip()).lower()


def _card_priority(card: dict[str, Any]) -> tuple[int, int, int, str]:
    exam_hits = int(card.get("exam_stats", {}).get("total_hits", 0))
    week_count = len(card.get("weeks") or [])
    source_count = sum(
        len(card.get("sections", {}).get(key, []))
        for key in ["lecture_snippets", "exam_questions", "notebook_snippets", "ai_examples", "key_points_to_remember"]
    )
    return (-exam_hits, -week_count, -source_count, str(card.get("canonical_topic") or card.get("topic") or ""))


def _item_text(item: dict[str, Any]) -> str:
    return str(item.get("text") or item.get("point") or "")


def _stable_union(items: list[Any], key_fn) -> list[Any]:
    seen: set[str] = set()
    merged: list[Any] = []
    for item in items:
        key = _norm(key_fn(item))
        if not key or key in seen:
            continue
        seen.add(key)
        merged.append(item)
    return merged


def _ensure_unique_ids(cards: list[dict[str, Any]]) -> int:
    used: dict[str, int] = {}
    changed = 0
    for card in cards:
        base_id = str(card.get("id") or "").strip()
        if not base_id:
            continue
        count = used.get(base_id, 0) + 1
        used[base_id] = count
        if count == 1:
            continue
        card["id"] = f"{base_id}-{count}"
        changed += 1
    return changed


def _dedupe_within_card(card: dict[str, Any]) -> tuple[int, int]:
    sections = card.get("sections", {})

    seen_points: set[str] = set()
    deduped_points = []
    removed_points = 0
    for item in sections.get("key_points_to_remember", []):
        key = _norm(str(item.get("text") or ""))
        if not key or key in seen_points:
            removed_points += 1
            continue
        seen_points.add(key)
        deduped_points.append(item)
    sections["key_points_to_remember"] = deduped_points

    seen_examples: set[str] = set()
    deduped_examples = []
    removed_examples = 0
    for item in sections.get("ai_examples", []):
        key = _norm(str(item.get("code") or ""))
        if not key or key in seen_examples:
            removed_examples += 1
            continue
        seen_examples.add(key)
        deduped_examples.append(item)
    sections["ai_examples"] = deduped_examples
    return removed_points, removed_examples


def _recompute_exam_stats(card: dict[str, Any]) -> None:
    exam_questions = card.get("sections", {}).get("exam_questions", [])
    by_exam: dict[str, int] = {}
    for item in exam_questions:
        exam_label = str(item.get("exam_label") or item.get("exam_source") or "").strip()
        if not exam_label:
            continue
        by_exam[exam_label] = by_exam.get(exam_label, 0) + 1
    card["exam_stats"] = {
        "total_hits": len(exam_questions),
        "by_exam": dict(sorted(by_exam.items(), key=lambda kv: (-kv[1], kv[0]))),
        "coverage_count": len(by_exam),
    }


def _merge_card_pair(primary: dict[str, Any], secondary: dict[str, Any]) -> None:
    primary["weeks"] = sorted({*(primary.get("weeks") or []), *(secondary.get("weeks") or [])})
    primary["related_topics"] = _stable_union(
        [*(primary.get("related_topics") or []), *(secondary.get("related_topics") or [])],
        lambda item: str(item),
    )
    primary["trap_patterns"] = _stable_union(
        [*(primary.get("trap_patterns") or []), *(secondary.get("trap_patterns") or [])],
        lambda item: "|".join(
            [
                str(item.get("pattern") or ""),
                str(item.get("trap") or ""),
                ",".join(str(week) for week in item.get("weeks") or []),
            ]
        ),
    )

    primary_sections = primary.setdefault("sections", {})
    secondary_sections = secondary.get("sections", {})
    source_buckets = ["lecture_snippets", "exam_questions", "notebook_snippets"]
    for key in source_buckets:
        primary_sections[key] = _stable_union(
            [*(primary_sections.get(key) or []), *(secondary_sections.get(key) or [])],
            lambda item: str(item.get("id") or ""),
        )

    primary_sections["ai_examples"] = _stable_union(
        [*(primary_sections.get("ai_examples") or []), *(secondary_sections.get("ai_examples") or [])],
        lambda item: str(item.get("code") or item.get("title") or item.get("id") or ""),
    )
    primary_sections["key_points_to_remember"] = _stable_union(
        [*(primary_sections.get("key_points_to_remember") or []), *(secondary_sections.get("key_points_to_remember") or [])],
        _item_text,
    )

    valid_ids = {
        item.get("id")
        for bucket in source_buckets
        for item in primary_sections.get(bucket, [])
        if isinstance(item, dict) and item.get("id")
    }
    primary_sections["recommended_ids"] = [
        item_id
        for item_id in _stable_union(
            [*(primary_sections.get("recommended_ids") or []), *(secondary_sections.get("recommended_ids") or [])],
            lambda item: str(item),
        )
        if item_id in valid_ids
    ]

    _recompute_exam_stats(primary)


def _apply_safe_merges(cards: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], int]:
    by_id = {card.get("id"): card for card in cards}
    merged_secondaries: set[str] = set()
    merges_applied = 0
    for primary_id, secondary_id in SAFE_CARD_MERGES:
        primary = by_id.get(primary_id)
        secondary = by_id.get(secondary_id)
        if not primary or not secondary or secondary_id in merged_secondaries:
            continue
        _merge_card_pair(primary, secondary)
        merged_secondaries.add(secondary_id)
        merges_applied += 1

    return [card for card in cards if card.get("id") not in merged_secondaries], merges_applied


def _dedupe_across_cards(cards: list[dict[str, Any]], *, section_key: str, field: str) -> int:
    occurrences: dict[str, list[tuple[int, int]]] = {}
    for card_index, card in enumerate(cards):
        section = card.get("sections", {}).get(section_key, [])
        for item_index, item in enumerate(section):
            value = _norm(str(item.get(field) or ""))
            if not value:
                continue
            occurrences.setdefault(value, []).append((card_index, item_index))

    removals: dict[int, set[int]] = {}
    for matches in occurrences.values():
        card_indexes = {card_index for card_index, _ in matches}
        if len(card_indexes) <= 1:
            continue
        keeper = min(card_indexes, key=lambda card_index: _card_priority(cards[card_index]))
        for card_index, item_index in matches:
            if card_index == keeper:
                continue
            removals.setdefault(card_index, set()).add(item_index)

    removed = 0
    for card_index, item_indexes in removals.items():
        section = cards[card_index].get("sections", {}).get(section_key, [])
        cards[card_index]["sections"][section_key] = [
            item for idx, item in enumerate(section) if idx not in item_indexes
        ]
        removed += len(item_indexes)
    return removed


def _rebuild_week_groups(cards: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups = []
    weeks = sorted({week for card in cards for week in card.get("weeks", []) if isinstance(week, int)})
    for week in weeks:
        topic_refs = []
        for card in cards:
            if week not in (card.get("weeks") or []):
                continue
            sections = card.get("sections", {})
            topic_refs.append(
                {
                    "card_id": card["id"],
                    "topic": card.get("topic", ""),
                    "canonical_topic": card.get("canonical_topic", ""),
                    "exam_hits": card.get("exam_stats", {}).get("total_hits", 0),
                    "related_topics": card.get("related_topics", []),
                    "item_counts": {
                        "lecture_snippets": len(sections.get("lecture_snippets", [])),
                        "exam_questions": len(sections.get("exam_questions", [])),
                        "notebook_snippets": len(sections.get("notebook_snippets", [])),
                        "ai_examples": len(sections.get("ai_examples", [])),
                        "key_points_to_remember": len(sections.get("key_points_to_remember", [])),
                        "recommended_ids": len(sections.get("recommended_ids", [])),
                    },
                }
            )
        topic_refs.sort(key=lambda item: (-item["exam_hits"], str(item["topic"]).lower()))
        groups.append({"id": f"week-{week}", "week": week, "title": f"Week {week}", "topic_refs": topic_refs})
    return groups


def _relabel_cards(cards: list[dict[str, Any]]) -> int:
    changed = 0
    for card in cards:
        new_label = pretty_topic(str(card.get("canonical_topic") or ""), str(card.get("topic") or ""))
        if new_label and new_label != card.get("topic"):
            card["topic"] = new_label
            changed += 1
    return changed


def repair_payload(payload: dict[str, Any]) -> dict[str, int]:
    cards = payload.get("cards", [])

    ids_changed = _ensure_unique_ids(cards)

    cards, merges_applied = _apply_safe_merges(cards)
    payload["cards"] = cards

    labels_changed = _relabel_cards(cards)

    within_points_removed = 0
    within_examples_removed = 0
    for card in cards:
        points_removed, examples_removed = _dedupe_within_card(card)
        within_points_removed += points_removed
        within_examples_removed += examples_removed

    cross_points_removed = _dedupe_across_cards(cards, section_key="key_points_to_remember", field="text")
    cross_examples_removed = _dedupe_across_cards(cards, section_key="ai_examples", field="code")

    payload["deck_groups"] = _rebuild_week_groups(cards)
    payload.setdefault("meta", {}).setdefault("notes", []).append(
        "Repaired topic card IDs, merged hand-reviewed duplicate cards, and removed exact duplicate key points/examples across cards."
    )

    return {
        "card_count": len(cards),
        "ids_changed": ids_changed,
        "merges_applied": merges_applied,
        "labels_changed": labels_changed,
        "within_card_points_removed": within_points_removed,
        "within_card_examples_removed": within_examples_removed,
        "cross_card_points_removed": cross_points_removed,
        "cross_card_examples_removed": cross_examples_removed,
        "deck_groups": len(payload.get("deck_groups", [])),
    }


def main() -> None:
    payload = json.loads(TOPIC_CARDS_FILE.read_text(encoding="utf-8"))
    summary = repair_payload(payload)
    TOPIC_CARDS_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

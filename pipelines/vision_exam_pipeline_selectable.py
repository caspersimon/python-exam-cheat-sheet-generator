from __future__ import annotations

from typing import Any

from pipelines.vision_exam_pipeline_shared import (
    SELECTABLE_ITEMS_FILE,
    _card_week,
    _safe_str,
    _write_json,
    iter_selectable_items,
    load_topic_cards,
    snippet_identity_for_item,
)


def build_selectable_items_snapshot(
    *,
    output_path=SELECTABLE_ITEMS_FILE,
) -> list[dict[str, Any]]:
    cards = load_topic_cards()
    weeks_by_card = {card["id"]: _card_week(card) for card in cards if isinstance(card, dict) and card.get("id")}
    items = []
    for item in iter_selectable_items(cards):
        if isinstance(item, dict):
            snapshot = dict(item)
            snapshot["week"] = int(weeks_by_card.get(_safe_str(item.get("card_id"))) or 0)
            snippet_id, snippet_label = snippet_identity_for_item(snapshot)
            snapshot["snippet_id"] = snippet_id
            snapshot["snippet_label"] = snippet_label
            items.append(snapshot)
    _write_json(output_path, items)
    return items


def snippet_family_index(selectable_items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    families: dict[str, dict[str, Any]] = {}
    for item in selectable_items:
        if not isinstance(item, dict):
            continue
        item_id = _safe_str(item.get("item_id"))
        snippet_id = _safe_str(item.get("snippet_id"))
        snippet_label = _safe_str(item.get("snippet_label"))
        if not snippet_id:
            snippet_id, snippet_label = snippet_identity_for_item(item)
        if not item_id or not snippet_id:
            continue
        family = families.setdefault(
            snippet_id,
            {
                "snippet_id": snippet_id,
                "snippet_label": snippet_label or _safe_str(item.get("subtopic_title")) or _safe_str(item.get("topic")) or snippet_id,
                "week": int(item.get("week") or 0),
                "topic": _safe_str(item.get("topic")),
                "piece_ids": [],
                "pieces": [],
            },
        )
        family["piece_ids"].append(item_id)
        family["pieces"].append(item)
    return families

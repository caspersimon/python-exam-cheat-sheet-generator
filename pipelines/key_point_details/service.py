from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import unique_detail_id
from .rules_part1 import match_details_part1
from .rules_part2 import match_details_part2
from .rules_part3 import match_details_part3
from .rules_part4 import match_details_part4

ROOT = Path(__file__).resolve().parents[2]
CARDS_FILE = ROOT / "topic_cards.json"

RULE_MATCHERS = [
    match_details_part1,
    match_details_part2,
    match_details_part3,
    match_details_part4,
]


def details_for_point(topic: str, text: str) -> list[dict[str, Any]]:
    lower = text.lower()
    topic_lower = (topic or "").strip().lower()

    for matcher in RULE_MATCHERS:
        matched = matcher(topic_lower=topic_lower, lower=lower, text=text)
        if matched:
            return matched

    return []


def main() -> None:
    data = json.loads(CARDS_FILE.read_text(encoding="utf-8"))
    cards = data.get("cards", [])

    points_with_details = 0
    details_added = 0
    cards_changed = 0

    for card in cards:
        sections = card.get("sections", {})
        key_points = sections.get("key_points_to_remember", [])
        if not isinstance(key_points, list) or not key_points:
            continue

        changed_this_card = False
        taken_ids = {str(kp.get("id", "")).strip() for kp in key_points}
        for kp in key_points:
            for detail in kp.get("details", []) if isinstance(kp.get("details", []), list) else []:
                if detail.get("id"):
                    taken_ids.add(str(detail["id"]).strip())

        for kp in key_points:
            text = str(kp.get("text", "")).strip()
            if not text:
                continue

            existing_details = kp.get("details", [])
            if isinstance(existing_details, list) and existing_details:
                points_with_details += 1
                continue

            generated = details_for_point(str(card.get("topic", "")), text)
            if not generated:
                continue

            base_id = str(kp.get("id", "")).strip() or "kp"
            materialized = []
            for idx, detail in enumerate(generated, start=1):
                detail_obj = {
                    **detail,
                    "id": unique_detail_id(base_id, taken_ids, idx),
                }
                materialized.append(detail_obj)

            kp["details"] = materialized
            details_added += len(materialized)
            points_with_details += 1
            changed_this_card = True

        if changed_this_card:
            cards_changed += 1

    notes = data.setdefault("meta", {}).setdefault("notes", [])
    notes.append("Added optional key point detail blocks (tables/examples/explanations) for reference usage.")

    CARDS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        f"Updated {CARDS_FILE}: details added={details_added}, points_with_details={points_with_details}, cards_changed={cards_changed}."
    )

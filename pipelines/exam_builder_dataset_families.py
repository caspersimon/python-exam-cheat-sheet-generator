from __future__ import annotations

from typing import Any

from pipelines.exam_builder_dataset_specs import (
    canonical_piece_id,
    canonical_snippet_id,
    normalize_options,
    summarize_text,
    topic_assignment,
)
from pipelines.vision_exam_pipeline_shared import snippet_identity_for_item
from scripts.exam_coverage_audit import get_source_split, key_point_groups, load_topic_cards, normalize_common_questions


def build_ai_question_piece(card: dict[str, Any], item: dict[str, Any]) -> dict[str, Any]:
    piece_type = "reference_table" if item.get("table") else "code_example" if item.get("code") else "explanation"
    if piece_type == "reference_table":
        content = {
            "text": "\n".join(filter(None, [item.get("summary"), item.get("detail"), item.get("extra")])),
            "headers": item["table"].get("headers", []),
            "rows": item["table"].get("rows", []),
        }
    elif piece_type == "code_example":
        content = {
            "text": "\n".join(filter(None, [item.get("summary"), item.get("detail"), item.get("extra")])),
            "code": item.get("code", ""),
        }
    else:
        content = {"text": "\n".join(filter(None, [item.get("summary"), item.get("detail"), item.get("extra")]))}
    return {
        "source_piece_id": item["id"],
        "id": canonical_piece_id(card["id"], item["id"]),
        "piece_type": piece_type,
        "title": summarize_text(item.get("summary") or item.get("detail") or "", card["topic"]),
        "content": content,
        "selectable": True,
    }


def build_key_point_piece(card: dict[str, Any], item: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_piece_id": item["id"],
        "id": canonical_piece_id(card["id"], item["id"]),
        "piece_type": "explanation",
        "title": summarize_text(item.get("text", ""), card["topic"]),
        "content": {"text": item.get("text", "")},
        "selectable": True,
    }


def build_detail_piece(card: dict[str, Any], detail: dict[str, Any]) -> dict[str, Any]:
    if detail.get("table"):
        piece_type = "reference_table"
        content = {
            "text": detail.get("text", ""),
            "headers": detail["table"].get("headers", []),
            "rows": detail["table"].get("rows", []),
        }
    elif detail.get("code"):
        piece_type = "code_example"
        content = {"text": detail.get("text", ""), "code": detail.get("code", "")}
    else:
        piece_type = "explanation"
        content = {"text": detail.get("text", "")}
    return {
        "source_piece_id": detail["id"],
        "id": canonical_piece_id(card["id"], detail["id"]),
        "piece_type": piece_type,
        "title": detail.get("title") or card["topic"],
        "content": content,
        "selectable": True,
    }


def build_ai_example_piece(card: dict[str, Any], item: dict[str, Any]) -> dict[str, Any]:
    content: dict[str, Any] = {"code": item.get("code", "")}
    if item.get("why"):
        content["text"] = item.get("why", "")
    if item.get("output"):
        content["output"] = item.get("output", "")
    return {
        "source_piece_id": item["id"],
        "id": canonical_piece_id(card["id"], item["id"]),
        "piece_type": "code_example",
        "title": item.get("title") or card["topic"],
        "content": content,
        "selectable": True,
    }


def build_source_piece(card: dict[str, Any], source_entry: dict[str, Any]) -> dict[str, Any]:
    item = source_entry["item"]
    item_id = source_entry["id"]
    if source_entry["source_type"] == "exam":
        return {
            "source_piece_id": item_id,
            "id": canonical_piece_id(card["id"], item_id),
            "piece_type": "past_exam_piece",
            "title": summarize_text(item.get("question", ""), f"{card['topic']} exam question"),
            "content": {
                "question": item.get("question", ""),
                "code_context": item.get("code_context", ""),
                "options": normalize_options(item.get("options")),
                "correct": item.get("correct", ""),
                "explanation": item.get("explanation", ""),
                "exam_label": item.get("exam_label", ""),
                "number": item.get("number"),
            },
            "selectable": True,
        }
    if source_entry["source_type"] == "lecture":
        examples = item.get("code_examples", [])
        if examples:
            example = examples[0]
            return {
                "source_piece_id": item_id,
                "id": canonical_piece_id(card["id"], item_id),
                "piece_type": "code_example",
                "title": item.get("title") or card["topic"],
                "content": {
                    "text": item.get("explanation", ""),
                    "code": example.get("code", ""),
                    "note": example.get("description", ""),
                },
                "selectable": True,
            }
        return {
            "source_piece_id": item_id,
            "id": canonical_piece_id(card["id"], item_id),
            "piece_type": "explanation",
            "title": item.get("title") or card["topic"],
            "content": {"text": "\n".join(filter(None, [item.get("explanation", ""), item.get("question", "")]))},
            "selectable": True,
        }
    return {
        "source_piece_id": item_id,
        "id": canonical_piece_id(card["id"], item_id),
        "piece_type": "code_example",
        "title": item.get("title") or card["topic"],
        "content": {
            "code": item.get("source", ""),
            "output": "\n".join(item.get("outputs", [])),
        },
        "selectable": True,
    }


def init_family(card: dict[str, Any], snippet_key: str, snippet_label: str, snippet_type: str) -> dict[str, Any]:
    parent_topic, main_topic = topic_assignment(card.get("topic", ""))
    return {
        "id": canonical_snippet_id(snippet_key),
        "source_snippet_id": snippet_key,
        "title": snippet_label or card.get("topic", ""),
        "snippet_type": snippet_type,
        "parent_topic": parent_topic,
        "main_topic": main_topic,
        "main_week": int(card.get("topic_meta", {}).get("week") or (card.get("weeks") or [0])[0] or 0),
        "related_topics": [main_topic],
        "related_weeks": sorted({int(week) for week in card.get("weeks", []) if int(week) > 0}),
        "pieces": [],
        "score_source": "round2_derived",
        "manual_score_reason": "",
    }


def build_existing_families() -> dict[str, dict[str, Any]]:
    cards = load_topic_cards()
    families: dict[str, dict[str, Any]] = {}
    for card in cards:
        for item in normalize_common_questions(card):
            snippet_key, snippet_label = snippet_identity_for_item(
                {
                    "item_id": item["id"],
                    "card_id": card["id"],
                    "subtopic_id": item.get("subtopic_id", ""),
                    "subtopic_title": item.get("subtopic_title", ""),
                    "topic": card.get("topic", ""),
                    "item_type": "ai_common_question",
                }
            )
            family = families.setdefault(snippet_key, init_family(card, snippet_key, snippet_label, "general_snippet"))
            family["pieces"].append(build_ai_question_piece(card, item))

        for group in key_point_groups(card):
            snippet_key, snippet_label = snippet_identity_for_item(
                {
                    "item_id": group["id"],
                    "card_id": card["id"],
                    "subtopic_id": group.get("subtopic_id", ""),
                    "subtopic_title": group.get("subtopic_title", ""),
                    "topic": card.get("topic", ""),
                    "item_type": "key_point",
                }
            )
            family = families.setdefault(snippet_key, init_family(card, snippet_key, snippet_label, "general_snippet"))
            family["pieces"].append(build_key_point_piece(card, group))

            for detail in group.get("details", []):
                detail_key, detail_label = snippet_identity_for_item(
                    {
                        "item_id": detail["id"],
                        "card_id": card["id"],
                        "subtopic_id": detail.get("subtopic_id", ""),
                        "subtopic_title": detail.get("subtopic_title", ""),
                        "topic": card.get("topic", ""),
                        "item_type": "key_point_detail",
                    }
                )
                detail_family = families.setdefault(detail_key, init_family(card, detail_key, detail_label, "general_snippet"))
                detail_family["pieces"].append(build_detail_piece(card, detail))

        for item in card.get("sections", {}).get("ai_examples", []):
            item_id = str(item.get("id") or "").strip()
            if not item_id:
                continue
            snippet_key, snippet_label = snippet_identity_for_item(
                {
                    "item_id": item_id,
                    "card_id": card["id"],
                    "subtopic_id": item.get("subtopic_id", ""),
                    "subtopic_title": item.get("subtopic_title", ""),
                    "topic": card.get("topic", ""),
                    "item_type": "ai_example",
                }
            )
            family = families.setdefault(snippet_key, init_family(card, snippet_key, snippet_label, "general_snippet"))
            family["pieces"].append(build_ai_example_piece(card, item))

        recommended, additional = get_source_split(card)
        for source_entry in [*recommended, *additional]:
            snippet_key, snippet_label = snippet_identity_for_item(
                {
                    "item_id": source_entry["id"],
                    "card_id": card["id"],
                    "subtopic_id": source_entry["item"].get("subtopic_id", ""),
                    "subtopic_title": source_entry["item"].get("subtopic_title", ""),
                    "topic": card.get("topic", ""),
                    "item_type": f"source_{source_entry['source_type']}",
                }
            )
            snippet_type = "past_exam_question" if source_entry["source_type"] == "exam" else "general_snippet"
            family = families.setdefault(snippet_key, init_family(card, snippet_key, snippet_label, snippet_type))
            family["pieces"].append(build_source_piece(card, source_entry))
    return families

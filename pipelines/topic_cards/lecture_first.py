from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

from pipelines.lecture_first_outline import match_outline_target, outline_for_week
from pipelines.shared import compact_text

ROOT = Path(__file__).resolve().parents[2]
OUTPUT_FILE = ROOT / "topic_cards.json"


def _safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _safe_str(value: Any) -> str:
    return str(value or "").strip()


def _norm(text: Any) -> str:
    value = _safe_str(text).lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9*+.# ]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def _match_subtopic(week: int, *texts: Any) -> tuple[str, str]:
    topic, subtopic, _, _ = match_outline_target(week, *texts)
    return topic["id"], subtopic["id"]


def _dedupe(items: list[dict[str, Any]], key_fields: list[str]) -> list[dict[str, Any]]:
    seen: set[tuple[Any, ...]] = set()
    out: list[dict[str, Any]] = []
    for item in items:
        key = tuple(item.get(field) for field in key_fields)
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def _subtopic_lookup(topic: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {subtopic["id"]: subtopic for subtopic in _safe_list(topic.get("subtopics")) if isinstance(subtopic, dict)}


def _topic_summary(topic: dict[str, Any], lecture_snippets: list[dict[str, Any]]) -> str:
    snippets = [snippet.get("explanation", "") for snippet in lecture_snippets if _safe_str(snippet.get("explanation"))]
    if snippets:
        return compact_text(" ".join(snippets[:3]), 420)
    return f"This topic follows the Week {topic.get('week')} lecture outline and groups curated reference snippets under explicit subtopics."


def _common_questions(exam_questions: list[dict[str, Any]], traps: list[dict[str, Any]]) -> list[str]:
    bullets = []
    for question in exam_questions[:4]:
        prompt = compact_text(question.get("question", ""), 160)
        if prompt:
            bullets.append(prompt)
    for trap in traps[:3]:
        text = compact_text(trap.get("trap", ""), 160)
        if text and text not in bullets:
            bullets.append(text)
    return bullets[:6]


def _build_key_points(topic: dict[str, Any], lecture_snippets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    key_points = []
    index = 1
    for snippet in lecture_snippets:
        text = compact_text(snippet.get("explanation", ""), 220)
        if not text:
            continue
        details = []
        for detail_index, example in enumerate(_safe_list(snippet.get("code_examples"))[:2], start=1):
            code = _safe_str(example.get("code"))
            if not code:
                continue
            details.append(
                {
                    "id": f"kp-{index}-d{detail_index}",
                    "kind": "example",
                    "title": _safe_str(example.get("description")) or "Code example",
                    "code": code,
                }
            )
        key_points.append(
            {
                "id": f"kp-{index}",
                "text": text,
                "status": "curated",
                "generator": "lecture-first-build",
                "model": None,
                "subtopic_id": snippet.get("subtopic_id"),
                "subtopic_title": snippet.get("subtopic_title"),
                "details": details,
            }
        )
        index += 1
    return key_points[:10]


def _build_examples(
    lecture_snippets: list[dict[str, Any]],
    notebook_snippets: list[dict[str, Any]],
    exam_questions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    examples = []
    index = 1
    for snippet in lecture_snippets:
        for example in _safe_list(snippet.get("code_examples"))[:2]:
            code = _safe_str(example.get("code"))
            if not code:
                continue
            examples.append(
                {
                    "id": f"ai-example-{index}",
                    "kind": "correct",
                    "title": _safe_str(example.get("description")) or "Lecture example",
                    "code": code,
                    "why": compact_text(snippet.get("explanation", ""), 180),
                    "status": "curated",
                    "subtopic_id": snippet.get("subtopic_id"),
                    "subtopic_title": snippet.get("subtopic_title"),
                }
            )
            index += 1
    for snippet in notebook_snippets[:4]:
        code = _safe_str(snippet.get("source"))
        if not code:
            continue
        examples.append(
            {
                "id": f"ai-example-{index}",
                "kind": "correct",
                "title": _safe_str(snippet.get("title")) or "Notebook example",
                "code": code,
                "why": "Selected from notebook material because it directly reinforces the lecture subtopic.",
                "status": "curated",
                "subtopic_id": snippet.get("subtopic_id"),
                "subtopic_title": snippet.get("subtopic_title"),
            }
        )
        index += 1
    for question in exam_questions[:2]:
        code = _safe_str(question.get("code_context"))
        if not code:
            continue
        examples.append(
            {
                "id": f"ai-example-{index}",
                "kind": "incorrect",
                "title": f"Exam trap • Q{question.get('number') or '?'}",
                "code": code,
                "why": compact_text(question.get("explanation", ""), 180) or "Practice tracing this carefully before checking the answer.",
                "status": "curated",
                "subtopic_id": question.get("subtopic_id"),
                "subtopic_title": question.get("subtopic_title"),
            }
        )
        index += 1
    return examples[:8]


def _recommended_ids(
    lecture_snippets: list[dict[str, Any]],
    exam_questions: list[dict[str, Any]],
    notebook_snippets: list[dict[str, Any]],
) -> list[str]:
    ordered = [item["id"] for item in exam_questions[:4]]
    ordered.extend(item["id"] for item in lecture_snippets[:4])
    ordered.extend(item["id"] for item in notebook_snippets[:4])
    seen = set()
    out = []
    for item_id in ordered:
        if item_id in seen:
            continue
        seen.add(item_id)
        out.append(item_id)
    return out[:8]


def _build_subtopic_meta(topic: dict[str, Any], sections: dict[str, Any]) -> list[dict[str, Any]]:
    lookup = _subtopic_lookup(topic)
    grouped_counts: dict[str, dict[str, list[str]]] = {
        subtopic_id: {
            "lecture_snippet_ids": [],
            "exam_question_ids": [],
            "notebook_snippet_ids": [],
            "example_ids": [],
            "key_point_ids": [],
        }
        for subtopic_id in lookup
    }

    for snippet in sections["lecture_snippets"]:
        grouped_counts[snippet["subtopic_id"]]["lecture_snippet_ids"].append(snippet["id"])
    for snippet in sections["exam_questions"]:
        grouped_counts[snippet["subtopic_id"]]["exam_question_ids"].append(snippet["id"])
    for snippet in sections["notebook_snippets"]:
        grouped_counts[snippet["subtopic_id"]]["notebook_snippet_ids"].append(snippet["id"])
    for item in sections["ai_examples"]:
        grouped_counts[item["subtopic_id"]]["example_ids"].append(item["id"])
    for item in sections["key_points_to_remember"]:
        grouped_counts[item["subtopic_id"]]["key_point_ids"].append(item["id"])

    subtopics = []
    for subtopic in sorted(_safe_list(topic.get("subtopics")), key=lambda item: int(item.get("order") or 999)):
        if not isinstance(subtopic, dict):
            continue
        meta = grouped_counts.get(subtopic["id"], {})
        source_texts = [
            snippet["explanation"]
            for snippet in sections["lecture_snippets"]
            if snippet.get("subtopic_id") == subtopic["id"] and _safe_str(snippet.get("explanation"))
        ]
        summary = compact_text(" ".join(source_texts[:2]), 220) if source_texts else ""
        subtopics.append(
            {
                "id": subtopic["id"],
                "title": subtopic["title"],
                "order": int(subtopic.get("order") or 0),
                "summary": summary,
                "item_ids": meta,
            }
        )
    return subtopics


def _build_traps_for_topic(db: dict[str, Any], week: int, topic_id: str) -> list[dict[str, Any]]:
    traps = []
    for trap in _safe_list(db.get("knowledge", {}).get("key_exam_patterns_and_traps")):
        if not isinstance(trap, dict):
            continue
        match_topic_id, _ = _match_subtopic(week, trap.get("pattern"), trap.get("trap"))
        if match_topic_id != topic_id:
            continue
        traps.append(
            {
                "pattern": _safe_str(trap.get("pattern")),
                "trap": compact_text(_safe_str(trap.get("trap")), 220),
                "weeks": _safe_list(trap.get("weeks")),
                "appears_in_exams": _safe_list(trap.get("appears_in_exams")),
            }
        )
    return traps[:8]


def _build_exam_questions_for_topic(db: dict[str, Any], week: int, topic_id: str) -> list[dict[str, Any]]:
    questions = []
    for exam in _safe_list(db.get("assessments", {}).get("exams")):
        if not isinstance(exam, dict):
            continue
        exam_label = _safe_str(exam.get("exam_label") or exam.get("source")) or "unknown"
        for question in _safe_list(exam.get("questions")):
            if not isinstance(question, dict):
                continue
            if int(question.get("week") or 0) != week:
                continue
            match_topic_id, subtopic_id = _match_subtopic(
                week,
                question.get("topic"),
                question.get("question"),
                question.get("explanation"),
                question.get("code_context"),
            )
            if match_topic_id != topic_id:
                continue
            subtopic = next(
                (item for item in outline_for_week(week)["topics"] if item["id"] == topic_id),
                None,
            )
            subtopic_title = ""
            if subtopic:
                subtopic_title = next(
                    (item["title"] for item in subtopic["subtopics"] if item["id"] == subtopic_id),
                    "",
                )
            questions.append(
                {
                    "id": f"exam-{exam_label}-{question.get('number')}-{topic_id}",
                    "exam_label": exam_label,
                    "exam_source": _safe_str(exam.get("source")),
                    "year": _safe_str(exam.get("year")) or "unknown",
                    "number": question.get("number"),
                    "week": week,
                    "topic": _safe_str(question.get("topic")),
                    "subtopic_id": subtopic_id,
                    "subtopic_title": subtopic_title,
                    "question": compact_text(question.get("question", ""), 1200),
                    "code_context": _safe_str(question.get("code_context")),
                    "options": question.get("options", {}),
                    "correct": _safe_str(question.get("correct_override") or question.get("correct")),
                    "explanation": compact_text(question.get("explanation", ""), 1200),
                }
            )
    return _dedupe(questions, ["id"])


def _build_topic_sections(topic: dict[str, Any], db: dict[str, Any], week: int) -> dict[str, Any]:
    lecture_snippets = []
    notebook_snippets = []
    for subtopic in _safe_list(topic.get("subtopics")):
        if not isinstance(subtopic, dict):
            continue
        for snippet in _safe_list(subtopic.get("knowledge_snippets")):
            if not isinstance(snippet, dict):
                continue
            lecture_snippets.append(
                {
                    "id": snippet["id"],
                    "week": week,
                    "source": _safe_str(_safe_list(snippet.get("source_refs"))[0].get("source") if _safe_list(snippet.get("source_refs")) else ""),
                    "source_type": _safe_str(snippet.get("source_type")),
                    "topic": topic["title"],
                    "subtopic_id": subtopic["id"],
                    "subtopic_title": subtopic["title"],
                    "title": _safe_str(snippet.get("title")),
                    "explanation": compact_text(snippet.get("content", ""), 700),
                    "code_examples": _safe_list(snippet.get("code_examples")),
                }
            )
        for snippet in _safe_list(subtopic.get("code_snippets")):
            if not isinstance(snippet, dict):
                continue
            notebook_snippets.append(
                {
                    "id": snippet["id"],
                    "week": week,
                    "cell_index": None,
                    "cell_type": "code",
                    "source_type": _safe_str(snippet.get("source_type")),
                    "topic": topic["title"],
                    "subtopic_id": subtopic["id"],
                    "subtopic_title": subtopic["title"],
                    "title": _safe_str(snippet.get("title")),
                    "source": _safe_str(snippet.get("content")),
                    "outputs": _safe_list(snippet.get("outputs")),
                }
            )

    lecture_snippets = _dedupe(lecture_snippets, ["id"])
    notebook_snippets = _dedupe(notebook_snippets, ["id"])
    exam_questions = _build_exam_questions_for_topic(db, week, topic["id"])
    traps = _build_traps_for_topic(db, week, topic["id"])

    sections = {
        "lecture_snippets": lecture_snippets,
        "exam_questions": exam_questions,
        "notebook_snippets": notebook_snippets,
    }
    sections["ai_summary"] = {
        "status": "curated",
        "content": _topic_summary({"week": week}, lecture_snippets),
        "generator": "lecture-first-build",
        "model": None,
    }
    sections["ai_common_questions"] = {
        "status": "curated",
        "bullets": _common_questions(exam_questions, traps),
        "generator": "lecture-first-build",
        "model": None,
    }
    sections["key_points_to_remember"] = _build_key_points(topic, lecture_snippets)
    sections["ai_examples"] = _build_examples(lecture_snippets, notebook_snippets, exam_questions)
    sections["recommended_ids"] = _recommended_ids(lecture_snippets, exam_questions, notebook_snippets)
    return sections


def build_cards_from_study_db(db: dict[str, Any]) -> list[dict[str, Any]]:
    cards = []
    for week_record in sorted(_safe_list(db.get("weeks")), key=lambda item: int(item.get("week") or 999)):
        if not isinstance(week_record, dict):
            continue
        week = int(week_record.get("week") or 0)
        for topic in sorted(_safe_list(week_record.get("topics")), key=lambda item: int(item.get("order") or 999)):
            if not isinstance(topic, dict):
                continue
            sections = _build_topic_sections(topic, db, week)
            exam_counts = Counter(item["exam_label"] for item in sections["exam_questions"] if _safe_str(item.get("exam_label")))
            subtopics = _build_subtopic_meta(topic, sections)
            cards.append(
                {
                    "id": topic["id"],
                    "topic": topic["title"],
                    "canonical_topic": topic["id"],
                    "weeks": [week],
                    "week_id": f"week-{week}",
                    "topic_meta": {
                        "week": week,
                        "week_id": f"week-{week}",
                        "week_title": _safe_str(week_record.get("title")) or f"Week {week}",
                        "topic_id": topic["id"],
                        "topic_title": topic["title"],
                        "topic_order": int(topic.get("order") or 0),
                    },
                    "subtopics": subtopics,
                    "exam_stats": {
                        "total_hits": sum(exam_counts.values()),
                        "by_exam": dict(sorted(exam_counts.items(), key=lambda item: (-item[1], item[0]))),
                        "coverage_count": len(exam_counts),
                    },
                    "related_topics": [subtopic["title"] for subtopic in subtopics],
                    "trap_patterns": _build_traps_for_topic(db, week, topic["id"]),
                    "sections": sections,
                }
            )
    return cards


def build_week_groups(cards: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_week: dict[int, list[dict[str, Any]]] = {}
    for card in cards:
        week = int(card.get("topic_meta", {}).get("week") or card.get("weeks", [0])[0] or 0)
        by_week.setdefault(week, []).append(card)

    groups = []
    for week in sorted(by_week):
        cards_for_week = sorted(by_week[week], key=lambda item: int(item.get("topic_meta", {}).get("topic_order") or 999))
        groups.append(
            {
                "id": f"week-{week}",
                "week": week,
                "title": f"Week {week}",
                "topic_groups": [
                    {
                        "id": f"week-{week}-topics",
                        "title": "Topics",
                        "shortTitle": "Topics",
                        "is_default": True,
                        "topic_refs": [
                            {
                                "card_id": card["id"],
                                "topic": card["topic"],
                                "canonical_topic": card["canonical_topic"],
                                "exam_hits": card.get("exam_stats", {}).get("total_hits", 0),
                                "topic_order": card.get("topic_meta", {}).get("topic_order", 0),
                                "subtopic_count": len(card.get("subtopics", [])),
                            }
                            for card in cards_for_week
                        ],
                    }
                ],
            }
        )
    return groups


def build_output(db: dict[str, Any], source_file: Path) -> dict[str, Any]:
    try:
        generated_from = str(source_file.relative_to(OUTPUT_FILE.parent))
    except ValueError:
        generated_from = source_file.name

    cards = build_cards_from_study_db(db)
    return {
        "meta": {
            "generated_from": generated_from,
            "generator": "build_topic_cards.py",
            "course": db.get("meta", {}).get("course"),
            "weeks_covered": db.get("meta", {}).get("weeks_covered", []),
            "total_cards": len(cards),
            "notes": [
                "Cards are materialized directly from the lecture-first canonical study database.",
                "Each card maps to one sidebar topic, with subtopics rendered inside the topic detail page.",
                "AI-style summary, examples, and key points are deterministic curated fallbacks until optional enrichment scripts overwrite them.",
            ],
        },
        "cards": cards,
        "deck_groups": build_week_groups(cards),
    }


def write_output(output: dict[str, Any]) -> None:
    OUTPUT_FILE.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

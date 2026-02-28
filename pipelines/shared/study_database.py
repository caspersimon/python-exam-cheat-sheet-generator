from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
STUDY_DB_FILE = ROOT / "data" / "study_db.json"

_WEEK_SOURCE_RE = re.compile(r"week\s+(\d+)", re.IGNORECASE)


def _as_int(value: Any) -> int | None:
    try:
        week = int(value)
    except (TypeError, ValueError):
        return None
    if week <= 0:
        return None
    return week


def _safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _empty_week_record(week: int) -> dict[str, Any]:
    return {
        "week": week,
        "topics": [],
        "lecture": {
            "concepts": [],
            "lecture_questions": [],
        },
        "notebook_cells": [],
        "sources": [],
    }


def _topic_norm(value: str) -> str:
    text = (value or "").strip().lower()
    text = text.replace("_", " ")
    text = re.sub(r"\s+", " ", text)
    return text


def build_study_db_from_monolith(data: dict[str, Any]) -> dict[str, Any]:
    """One-time converter from the old monolithic source shape into canonical study_db shape."""
    meta = data.get("meta", {}) if isinstance(data.get("meta"), dict) else {}
    week_map: dict[int, dict[str, Any]] = {}

    for lecture in _safe_list(data.get("lectures")):
        if not isinstance(lecture, dict):
            continue
        week = _as_int(lecture.get("week"))
        if week is None:
            continue
        week_rec = week_map.setdefault(week, _empty_week_record(week))
        week_rec["topics"] = _safe_list(lecture.get("topics"))
        lecture_obj = week_rec["lecture"]
        lecture_obj["concepts"] = _safe_list(lecture.get("concepts"))
        lecture_obj["lecture_questions"] = _safe_list(lecture.get("lecture_questions"))

    for cell in _safe_list(data.get("notebooks")):
        if not isinstance(cell, dict):
            continue
        week = _as_int(cell.get("week"))
        if week is None:
            continue
        week_rec = week_map.setdefault(week, _empty_week_record(week))
        week_rec["notebook_cells"].append(cell)

    for source in _safe_list(meta.get("sources")):
        if not isinstance(source, str):
            continue
        match = _WEEK_SOURCE_RE.search(source)
        if not match:
            continue
        week = _as_int(match.group(1))
        if week is None:
            continue
        week_rec = week_map.setdefault(week, _empty_week_record(week))
        if source not in week_rec["sources"]:
            week_rec["sources"].append(source)

    weeks = [week_map[week] for week in sorted(week_map)]
    return {
        "meta": {
            "schema_version": "2.0",
            "course": meta.get("course", ""),
            "description": meta.get("description", ""),
            "weeks_covered": [item["week"] for item in weeks],
            "sources": _safe_list(meta.get("sources")),
        },
        "weeks": weeks,
        "assessments": {
            "exams": _safe_list(data.get("exams")),
        },
        "knowledge": {
            "key_exam_patterns_and_traps": _safe_list(data.get("key_exam_patterns_and_traps")),
            "topic_analysis": data.get("topic_analysis", {}),
        },
    }


def _collect_sources(meta: dict[str, Any], weeks: list[dict[str, Any]], exams: list[dict[str, Any]]) -> list[str]:
    sources = [item for item in _safe_list(meta.get("sources")) if isinstance(item, str)]
    if sources:
        return sources

    derived: list[str] = []
    for week in weeks:
        for source in _safe_list(week.get("sources")):
            if isinstance(source, str) and source not in derived:
                derived.append(source)
    for exam in exams:
        if not isinstance(exam, dict):
            continue
        source = exam.get("source")
        if isinstance(source, str) and source not in derived:
            derived.append(source)
    return derived


def flatten_study_db_for_pipeline(db: dict[str, Any]) -> dict[str, Any]:
    """Build the materialized topic-card input shape from canonical study_db."""
    meta = db.get("meta", {}) if isinstance(db.get("meta"), dict) else {}
    weeks = [item for item in _safe_list(db.get("weeks")) if isinstance(item, dict)]
    weeks = sorted(weeks, key=lambda item: (_as_int(item.get("week")) or 9999))

    lectures: list[dict[str, Any]] = []
    notebooks: list[dict[str, Any]] = []

    for week_rec in weeks:
        week = _as_int(week_rec.get("week"))
        if week is None:
            continue

        lecture = week_rec.get("lecture", {}) if isinstance(week_rec.get("lecture"), dict) else {}
        lectures.append(
            {
                "week": week,
                "topics": _safe_list(week_rec.get("topics")),
                "concepts": _safe_list(lecture.get("concepts")),
                "lecture_questions": _safe_list(lecture.get("lecture_questions")),
            }
        )

        for cell in _safe_list(week_rec.get("notebook_cells")):
            if not isinstance(cell, dict):
                continue
            materialized = dict(cell)
            materialized["week"] = week
            notebooks.append(materialized)

    notebooks.sort(key=lambda item: (_as_int(item.get("week")) or 9999, int(item.get("cell_index") or 0)))

    assessments = db.get("assessments", {}) if isinstance(db.get("assessments"), dict) else {}
    exams = [item for item in _safe_list(assessments.get("exams")) if isinstance(item, dict)]
    knowledge = db.get("knowledge", {}) if isinstance(db.get("knowledge"), dict) else {}

    return {
        "meta": {
            "course": meta.get("course", ""),
            "description": meta.get("description", ""),
            "weeks_covered": [item["week"] for item in lectures],
            "sources": _collect_sources(meta, weeks, exams),
        },
        "lectures": lectures,
        "notebooks": notebooks,
        "exams": exams,
        "key_exam_patterns_and_traps": _safe_list(knowledge.get("key_exam_patterns_and_traps")),
        "topic_analysis": knowledge.get("topic_analysis", {}),
    }


def recompute_topic_analysis(materialized_data: dict[str, Any]) -> dict[str, Any]:
    exam_topic_counts: Counter[str] = Counter()
    exam_question_counts: dict[str, int] = {}

    for exam in _safe_list(materialized_data.get("exams")):
        if not isinstance(exam, dict):
            continue
        label = str(exam.get("exam_label") or exam.get("source") or "unknown")
        questions = [item for item in _safe_list(exam.get("questions")) if isinstance(item, dict)]
        exam_question_counts[label] = len(questions)
        for question in questions:
            topic = str(question.get("topic") or "").strip()
            if topic:
                exam_topic_counts[topic] += 1

    sorted_topics = sorted(exam_topic_counts.items(), key=lambda item: (-item[1], item[0].lower()))
    topic_frequency = [[topic, count] for topic, count in sorted_topics]
    most_tested_topics = [topic for topic, _ in sorted_topics[:5]]

    lecture_topics_seen: list[str] = []
    lecture_topics_norm_seen: set[str] = set()
    for lecture in _safe_list(materialized_data.get("lectures")):
        if not isinstance(lecture, dict):
            continue
        for topic in _safe_list(lecture.get("topics")):
            if not isinstance(topic, str):
                continue
            norm = _topic_norm(topic)
            if norm and norm not in lecture_topics_norm_seen:
                lecture_topics_seen.append(topic)
                lecture_topics_norm_seen.add(norm)
        for concept in _safe_list(lecture.get("concepts")):
            if not isinstance(concept, dict):
                continue
            topic = str(concept.get("topic") or "").strip()
            norm = _topic_norm(topic)
            if norm and norm not in lecture_topics_norm_seen:
                lecture_topics_seen.append(topic)
                lecture_topics_norm_seen.add(norm)

    exam_topics_norm = {_topic_norm(topic) for topic, _ in sorted_topics}
    topics_not_in_exams = [topic for topic in lecture_topics_seen if _topic_norm(topic) not in exam_topics_norm]

    exam_question_counts["total"] = sum(exam_question_counts.values())
    return {
        "topic_frequency_across_all_exams": topic_frequency,
        "most_tested_topics": most_tested_topics,
        "topics_in_lectures_not_yet_in_exams": topics_not_in_exams,
        "exam_question_counts": exam_question_counts,
    }


def load_study_db(path: Path | None = None) -> dict[str, Any]:
    db_path = path or STUDY_DB_FILE
    if not db_path.exists():
        raise FileNotFoundError(f"Canonical study database not found: {db_path}")
    return json.loads(db_path.read_text(encoding="utf-8"))


def write_study_db(db: dict[str, Any], path: Path | None = None) -> Path:
    db_path = path or STUDY_DB_FILE
    _ensure_parent(db_path)
    db_path.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding="utf-8")
    return db_path


def load_topic_pipeline_data() -> tuple[dict[str, Any], Path]:
    db = load_study_db()
    return flatten_study_db_for_pipeline(db), STUDY_DB_FILE

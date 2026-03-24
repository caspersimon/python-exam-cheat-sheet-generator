from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pipelines.shared import load_study_db
from scripts.exam_coverage_audit import (
    DEFAULT_TMP_DIR as AUDIT_TMP_DIR,
    EXAM_SOURCES,
    ROOT,
    iter_selectable_items,
    load_topic_cards,
    portable_path,
    render_exam_pages,
    unique_exam_sources,
)

DATA_ROOT = ROOT / "data" / "vision_exam_pipeline"
TMP_ROOT = ROOT / "tmp" / "vision_exam_pipeline"
LEGACY_ASSESSMENT_DIR = ROOT / "data" / "import_payloads" / "post_midterm_assessments"

PAGE_MANIFEST_FILE = DATA_ROOT / "page_manifest.json"
QUESTION_BANK_FILE = DATA_ROOT / "exam_question_bank.json"
COMPLETENESS_FILE = DATA_ROOT / "exam_question_bank_completeness.json"
SELECTABLE_ITEMS_FILE = DATA_ROOT / "selectable_items_snapshot.json"
REVIEW_DROP_DIR = DATA_ROOT / "review_drops"
EVALUATIONS_DIR = DATA_ROOT / "evaluations"
SYNTHESIS_DIR = DATA_ROOT / "synthesis"
ANALYTICS_DIR = DATA_ROOT / "analytics"
REVIEW_PACKET_DIR = DATA_ROOT / "review_packets"
WORK_PACKET_DIR = DATA_ROOT / "work_packets"

QUESTION_BANK_SCHEMA = "1.0"
PAGE_MANIFEST_SCHEMA = "1.0"
EVALUATION_SCHEMA = "1.1"
SYNTHESIS_SCHEMA = "1.0"
ANALYTICS_SCHEMA = "1.0"
REVIEW_PACKET_SCHEMA = "1.0"

REVIEW_STATUSES = {
    "seeded_legacy_needs_vision_review",
    "pending_vision_review",
    "agent_reviewed_pending_human_confirmation",
    "human_confirmed",
}
EVALUATION_STATUSES = {
    "pending_review",
    "captured_pending_human_confirmation",
    "blocked_missing_question_capture",
    "completed",
}


def timestamp_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _safe_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _safe_str(value: Any) -> str:
    return str(value or "").strip()


def _slugify(value: Any) -> str:
    text = _safe_str(value).lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _write_json(path: Path, payload: dict[str, Any] | list[Any]) -> Path:
    _ensure_parent(path)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _card_week(card: dict[str, Any]) -> int:
    explicit = card.get("topic_meta", {}) if isinstance(card.get("topic_meta"), dict) else {}
    try:
        week = int(explicit.get("week"))
        if week > 0:
            return week
    except (TypeError, ValueError):
        pass
    for value in _safe_list(card.get("weeks")):
        try:
            week = int(value)
        except (TypeError, ValueError):
            continue
        if week > 0:
            return week
    return 0


def snippet_identity_for_item(item: dict[str, Any]) -> tuple[str, str]:
    item_id = _safe_str(item.get("item_id"))
    card_id = _safe_str(item.get("card_id"))
    subtopic_id = _safe_str(item.get("subtopic_id"))
    subtopic_title = _safe_str(item.get("subtopic_title"))
    topic = _safe_str(item.get("topic")) or "Unknown topic"
    item_type = _safe_str(item.get("item_type")) or "unknown"
    if subtopic_id and card_id:
        return (f"subtopic:{card_id}:{subtopic_id}", subtopic_title or topic)
    if card_id and item_type == "source_exam":
        return (f"item:{item_id}", subtopic_title or topic)
    return (f"item:{item_id}", subtopic_title or topic)


def duplicate_exam_aliases() -> list[dict[str, Any]]:
    aliases = []
    for exam in EXAM_SOURCES:
        duplicate_of = _safe_str(exam.get("duplicate_of"))
        if not duplicate_of:
            continue
        aliases.append(
            {
                "exam_id": exam["exam_id"],
                "duplicate_of": duplicate_of,
                "title": exam["title"],
                "pdf_path": portable_path(Path(exam["pdf_path"])),
            }
        )
    return aliases


def _existing_page_paths(exam_id: str) -> list[Path]:
    for directory in [AUDIT_TMP_DIR / "pages" / exam_id, TMP_ROOT / "pages" / exam_id]:
        pages = sorted(directory.glob("page-*.png"))
        if pages:
            return pages
    return []


def _question_id(exam_id: str, number: int) -> str:
    return f"{exam_id}-q{number:02d}"


def _normalize_question_options(options: Any) -> dict[str, str]:
    if not isinstance(options, dict):
        return {}
    return {str(key).strip(): _safe_str(value) for key, value in options.items() if _safe_str(value)}


def _default_blocked_question(exam_id: str, number: int) -> dict[str, Any]:
    return {
        "question_id": _question_id(exam_id, number),
        "number": number,
        "status": "pending_vision_review",
        "reason": "No reviewed question record exists yet. Capture this question from the rendered page PNGs with a vision model.",
    }


def validate_question_bank_payload(payload: dict[str, Any]) -> list[str]:
    errors = []
    seen_exam_ids: set[str] = set()
    for exam in _safe_list(payload.get("exams")):
        if not isinstance(exam, dict):
            errors.append("Exam entry must be an object.")
            continue
        exam_id = _safe_str(exam.get("exam_id"))
        if not exam_id:
            errors.append("Exam entry missing exam_id.")
        elif exam_id in seen_exam_ids:
            errors.append(f"Duplicate exam_id: {exam_id}")
        else:
            seen_exam_ids.add(exam_id)
        expected = int(exam.get("expected_questions") or 0)
        question_numbers = {
            int(question["number"])
            for question in _safe_list(exam.get("questions"))
            if isinstance(question, dict) and str(question.get("number", "")).isdigit()
        }
        blocked_numbers = {
            int(question["number"])
            for question in _safe_list(exam.get("blocked_questions"))
            if isinstance(question, dict) and str(question.get("number", "")).isdigit()
        }
        if question_numbers & blocked_numbers:
            errors.append(f"{exam_id}: same question number present in questions and blocked_questions")
        if expected and len(question_numbers | blocked_numbers) != expected:
            errors.append(f"{exam_id}: expected {expected} accounted question slots, found {len(question_numbers | blocked_numbers)}")
        for blocked in _safe_list(exam.get("blocked_questions")):
            if isinstance(blocked, dict) and not _safe_str(blocked.get("reason")):
                errors.append(f"{exam_id}: blocked question {blocked.get('number')} is missing a reason")
    return errors

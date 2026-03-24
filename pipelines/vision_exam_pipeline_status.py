from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from pipelines.vision_exam_pipeline_shared import (
    ANALYTICS_DIR,
    COMPLETENESS_FILE,
    EVALUATIONS_DIR,
    QUESTION_BANK_FILE,
    REVIEW_PACKET_DIR,
    SYNTHESIS_DIR,
    _read_json,
    _safe_dict,
    _safe_list,
    _safe_str,
    portable_path,
    timestamp_utc,
)


def _existing_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    payload = _read_json(path)
    return payload if isinstance(payload, dict) else {}


def _round_file(directory: Path, round_name: str, suffix: str = ".json") -> Path:
    return directory / f"{round_name}{suffix}"


def build_pipeline_status(*, round_name: str = "round1") -> dict[str, Any]:
    question_bank = _existing_json(QUESTION_BANK_FILE)
    completeness = _existing_json(COMPLETENESS_FILE)
    evaluations = _existing_json(_round_file(EVALUATIONS_DIR, round_name))
    synthesis = _existing_json(_round_file(SYNTHESIS_DIR, round_name))
    analytics = _existing_json(_round_file(ANALYTICS_DIR, round_name))
    review_packet = _existing_json(_round_file(REVIEW_PACKET_DIR, round_name))

    exams = _safe_list(question_bank.get("exams"))
    questions = [
        question
        for exam in exams
        for question in _safe_list(_safe_dict(exam).get("questions"))
        if isinstance(question, dict)
    ]
    blocked = [
        question
        for exam in exams
        for question in _safe_list(_safe_dict(exam).get("blocked_questions"))
        if isinstance(question, dict)
    ]
    review_status_counts = Counter(
        _safe_str(_safe_dict(question.get("provenance")).get("review_status"))
        for question in questions
        if _safe_str(_safe_dict(question.get("provenance")).get("review_status"))
    )

    evaluation_questions = _safe_list(evaluations.get("questions"))
    evaluation_status_counts = Counter(
        _safe_str(_safe_dict(question).get("status"))
        for question in evaluation_questions
        if _safe_str(_safe_dict(question).get("status"))
    )
    answerability_counts = Counter(
        _safe_str(_safe_dict(_safe_dict(question).get("answerability")).get("status"))
        for question in evaluation_questions
        if _safe_str(_safe_dict(question).get("status")) == "completed"
    )

    overall_status = {
        "question_bank_complete": _safe_str(completeness.get("overall_status")) == "complete",
        "evaluation_round_complete": bool(evaluation_questions)
        and evaluation_status_counts.get("completed", 0) == len(evaluation_questions),
        "synthesis_exists": bool(synthesis),
        "analytics_exists": bool(analytics),
        "review_packet_exists": bool(review_packet),
    }
    if overall_status["evaluation_round_complete"] and overall_status["synthesis_exists"]:
        next_gate = "human_review_of_synthesized_changes"
    elif overall_status["question_bank_complete"]:
        next_gate = "finish_or_refresh_question_to_snippet_evaluations"
    else:
        next_gate = "complete_question_bank_capture"

    return {
        "generated_at": timestamp_utc(),
        "round": round_name,
        "paths": {
            "question_bank": portable_path(QUESTION_BANK_FILE),
            "completeness": portable_path(COMPLETENESS_FILE),
            "evaluations": portable_path(_round_file(EVALUATIONS_DIR, round_name)),
            "synthesis": portable_path(_round_file(SYNTHESIS_DIR, round_name)),
            "analytics": portable_path(_round_file(ANALYTICS_DIR, round_name)),
            "review_packet": portable_path(_round_file(REVIEW_PACKET_DIR, round_name)),
            "manual_review_packet": portable_path(REVIEW_PACKET_DIR / f"{round_name}_manual_synthesis.md"),
        },
        "question_bank": {
            "canonical_exam_count": int(question_bank.get("canonical_exam_count") or 0),
            "present_questions": len(questions),
            "blocked_questions": len(blocked),
            "review_status_counts": dict(review_status_counts),
            "completeness_status": _safe_str(completeness.get("overall_status")) or "unknown",
        },
        "evaluation_round": {
            "exists": bool(evaluations),
            "question_count": len(evaluation_questions),
            "status_counts": dict(evaluation_status_counts),
            "completed_evaluations": int(evaluation_status_counts.get("completed", 0)),
            "answerability_counts": dict(answerability_counts),
        },
        "review_outputs": {
            "synthesis_exists": bool(synthesis),
            "suggestion_count": int(_safe_dict(synthesis.get("summary")).get("suggestion_count") or 0),
            "analytics_exists": bool(analytics),
            "review_packet_exists": bool(review_packet),
            "manual_review_packet_exists": (REVIEW_PACKET_DIR / f"{round_name}_manual_synthesis.md").exists(),
        },
        "overall_status": overall_status,
        "next_gate": next_gate,
    }

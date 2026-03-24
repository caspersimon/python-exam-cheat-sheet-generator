from __future__ import annotations

import json
from collections import Counter, defaultdict
from copy import deepcopy
from pathlib import Path
from typing import Any

from pipelines.vision_exam_pipeline_shared import (
    ANALYTICS_DIR,
    ANALYTICS_SCHEMA,
    EVALUATIONS_DIR,
    EVALUATION_SCHEMA,
    EVALUATION_STATUSES,
    QUESTION_BANK_FILE,
    SELECTABLE_ITEMS_FILE,
    SYNTHESIS_DIR,
    SYNTHESIS_SCHEMA,
    WORK_PACKET_DIR,
    _card_week,
    _normalize_question_options,
    _read_json,
    _safe_dict,
    _safe_list,
    _safe_str,
    _write_json,
    iter_selectable_items,
    load_topic_cards,
    portable_path,
    timestamp_utc,
)


def build_selectable_items_snapshot(
    *,
    output_path: Path = SELECTABLE_ITEMS_FILE,
) -> list[dict[str, Any]]:
    cards = load_topic_cards()
    weeks_by_card = {card["id"]: _card_week(card) for card in cards if isinstance(card, dict) and card.get("id")}
    items = []
    for item in iter_selectable_items(cards):
        if isinstance(item, dict):
            snapshot = dict(item)
            snapshot["week"] = int(weeks_by_card.get(_safe_str(item.get("card_id"))) or 0)
            items.append(snapshot)
    _write_json(output_path, items)
    return items


def _findings_index(findings_paths: list[Path]) -> dict[tuple[str, int], list[dict[str, Any]]]:
    index: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
    for path in findings_paths:
        if not path.exists():
            continue
        for exam in _safe_list(_safe_dict(_read_json(path)).get("exams")):
            exam_id = _safe_str(_safe_dict(exam).get("exam_id"))
            for question in _safe_list(_safe_dict(exam).get("questions")):
                if isinstance(question, dict) and str(question.get("question_number", "")).isdigit():
                    index[(exam_id, int(question["question_number"]))].append(deepcopy(question))
    return index

def _evaluation_file(round_name: str) -> Path:
    return EVALUATIONS_DIR / f"{round_name}.json"

def _evaluation_work_packet_dir(round_name: str) -> Path:
    return WORK_PACKET_DIR / "evaluations" / round_name

def _default_answerability() -> dict[str, Any]:
    return {"status": "unknown", "confidence": "unknown", "rationale": "", "usable_without_prior_python_knowledge": False}

def _default_gap_analysis() -> dict[str, Any]:
    return {"summary": "", "missing_concepts": [], "proposed_fix": ""}

def _evaluation_status_for_question(*, question: dict[str, Any], existing: dict[str, Any]) -> str:
    existing_status = _safe_str(existing.get("status"))
    if existing_status == "completed":
        return existing_status
    review_status = _safe_str(_safe_dict(question.get("provenance")).get("review_status"))
    if review_status == "human_confirmed":
        return "pending_review"
    if review_status == "agent_reviewed_pending_human_confirmation":
        return "captured_pending_human_confirmation"
    if review_status == "seeded_legacy_needs_vision_review":
        return "blocked_missing_question_capture"
    return existing_status or "pending_review"

def _gap_analysis_for_question(*, existing: dict[str, Any], status: str) -> dict[str, Any]:
    existing_gap = _safe_dict(existing.get("gap_analysis"))
    if existing_gap:
        return existing_gap
    if status == "captured_pending_human_confirmation":
        return {
            "summary": "Question has been captured with a vision review and is awaiting human confirmation before snippet evaluation.",
            "missing_concepts": [],
            "proposed_fix": "Human-confirm the captured question record, then complete the snippet evaluation.",
        }
    if status == "blocked_missing_question_capture":
        return {
            "summary": "Question still requires vision capture before snippet evaluation can begin.",
            "missing_concepts": [],
            "proposed_fix": "Capture the missing exam question with the vision-review workflow before snippet evaluation.",
        }
    return _default_gap_analysis()

def build_evaluation_scaffold(
    *,
    round_name: str,
    question_bank: dict[str, Any],
    selectable_items: list[dict[str, Any]],
    existing_payload: dict[str, Any] | None = None,
    findings_paths: list[Path] | None = None,
) -> dict[str, Any]:
    selectable_by_id = {item["item_id"]: item for item in selectable_items if isinstance(item, dict) and item.get("item_id")}
    existing_questions = {
        _safe_str(question.get("question_id")): question
        for question in _safe_list(_safe_dict(existing_payload).get("questions"))
        if isinstance(question, dict)
    }
    findings_index = _findings_index(findings_paths or [])
    questions_payload = []

    for exam in _safe_list(question_bank.get("exams")):
        exam_id = _safe_str(_safe_dict(exam).get("exam_id"))
        for question in _safe_list(_safe_dict(exam).get("questions")):
            if not isinstance(question, dict):
                continue
            question_id = _safe_str(question.get("question_id"))
            number = int(question["number"])
            existing = deepcopy(existing_questions.get(question_id, {}))
            status = _evaluation_status_for_question(question=question, existing=existing)
            questions_payload.append(
                {
                    "evaluation_id": _safe_str(existing.get("evaluation_id")) or f"{round_name}:{question_id}",
                    "question_id": question_id,
                    "exam_id": exam_id,
                    "question_number": number,
                    "status": status,
                    "question_snapshot": {
                        "topic": _safe_str(question.get("topic")),
                        "question": _safe_str(question.get("question")),
                        "options": _normalize_question_options(question.get("options")),
                        "correct": _safe_str(question.get("correct")),
                        "explanation": _safe_str(question.get("explanation")),
                        "code_context": _safe_str(question.get("code_context")),
                    },
                    "seed_context": {
                        "exact_match_findings": findings_index.get((exam_id, number), []),
                        "available_seed_snippet_ids": [
                            item_id
                            for finding in findings_index.get((exam_id, number), [])
                            for item_id in _safe_list(_safe_dict(finding).get("evidence_item_ids"))
                            if item_id in selectable_by_id
                        ],
                        "provenance_review_status": _safe_str(_safe_dict(question.get("provenance")).get("review_status")),
                    },
                    "best_single_snippet": existing.get("best_single_snippet"),
                    "top_three_snippets": _safe_list(existing.get("top_three_snippets")),
                    "minimal_sufficient_snippets": _safe_list(existing.get("minimal_sufficient_snippets")),
                    "answerability": _safe_dict(existing.get("answerability")) or _default_answerability(),
                    "gap_analysis": _gap_analysis_for_question(existing=existing, status=status),
                    "suggested_changes": _safe_list(existing.get("suggested_changes")),
                    "review_meta": {"requires_human_review": True, "reviewed_at": _safe_str(_safe_dict(existing.get("review_meta")).get("reviewed_at"))},
                }
            )
        for blocked in _safe_list(_safe_dict(exam).get("blocked_questions")):
            if not isinstance(blocked, dict):
                continue
            question_id = _safe_str(blocked.get("question_id"))
            questions_payload.append(
                {
                    "evaluation_id": f"{round_name}:{question_id}",
                    "question_id": question_id,
                    "exam_id": exam_id,
                    "question_number": int(blocked["number"]),
                    "status": "blocked_missing_question_capture",
                    "question_snapshot": {},
                    "seed_context": {
                        "exact_match_findings": findings_index.get((exam_id, int(blocked["number"])), []),
                        "available_seed_snippet_ids": [],
                        "block_reason": _safe_str(blocked.get("reason")),
                    },
                    "best_single_snippet": None,
                    "top_three_snippets": [],
                    "minimal_sufficient_snippets": [],
                    "answerability": _default_answerability(),
                    "gap_analysis": {
                        "summary": _safe_str(blocked.get("reason")),
                        "missing_concepts": [],
                        "proposed_fix": "Capture the missing exam question with the vision-review workflow before snippet evaluation.",
                    },
                    "suggested_changes": [],
                    "review_meta": {"requires_human_review": True, "reviewed_at": ""},
                }
            )

    return {
        "schema_version": EVALUATION_SCHEMA,
        "generated_at": timestamp_utc(),
        "round": round_name,
        "question_bank_path": portable_path(QUESTION_BANK_FILE),
        "selectable_items_path": portable_path(SELECTABLE_ITEMS_FILE),
        "questions": sorted(questions_payload, key=lambda item: (_safe_str(item.get("exam_id")), int(item.get("question_number") or 0))),
    }

def _write_evaluation_work_packets(*, round_name: str, payload: dict[str, Any]) -> None:
    output_dir = _evaluation_work_packet_dir(round_name)
    questions_by_exam: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for question in _safe_list(payload.get("questions")):
        if isinstance(question, dict):
            questions_by_exam[_safe_str(question.get("exam_id"))].append(question)
    for exam_id, questions in questions_by_exam.items():
        packet = {
            "schema_version": EVALUATION_SCHEMA,
            "generated_at": timestamp_utc(),
            "round": round_name,
            "exam_id": exam_id,
            "question_count": len(questions),
            "pending_question_ids": [question["question_id"] for question in questions if _safe_str(question.get("status")) == "pending_review"],
            "captured_pending_human_confirmation_ids": [
                question["question_id"]
                for question in questions
                if _safe_str(question.get("status")) == "captured_pending_human_confirmation"
            ],
            "blocked_question_ids": [question["question_id"] for question in questions if _safe_str(question.get("status")) == "blocked_missing_question_capture"],
            "questions": questions,
        }
        _write_json(output_dir / f"{exam_id}.json", packet)

def write_evaluation_scaffold(
    *,
    round_name: str,
    question_bank_path: Path = QUESTION_BANK_FILE,
    selectable_items_path: Path = SELECTABLE_ITEMS_FILE,
    findings_paths: list[Path] | None = None,
) -> dict[str, Any]:
    question_bank = _read_json(question_bank_path)
    selectable_items = _read_json(selectable_items_path) if selectable_items_path.exists() else build_selectable_items_snapshot()
    output_path = _evaluation_file(round_name)
    existing = _read_json(output_path) if output_path.exists() else None
    payload = build_evaluation_scaffold(
        round_name=round_name,
        question_bank=question_bank,
        selectable_items=selectable_items,
        existing_payload=existing,
        findings_paths=findings_paths,
    )
    _write_json(output_path, payload)
    _write_evaluation_work_packets(round_name=round_name, payload=payload)
    return payload

def validate_evaluation_payload(payload: dict[str, Any], *, selectable_items: list[dict[str, Any]]) -> list[str]:
    errors = []
    valid_item_ids = {item["item_id"] for item in selectable_items if isinstance(item, dict) and item.get("item_id")}
    seen_question_ids: set[str] = set()
    for item in _safe_list(payload.get("questions")):
        if not isinstance(item, dict):
            errors.append("Evaluation question entry must be an object.")
            continue
        question_id = _safe_str(item.get("question_id"))
        if not question_id:
            errors.append("Evaluation question entry missing question_id.")
        elif question_id in seen_question_ids:
            errors.append(f"Duplicate evaluation question_id: {question_id}")
        else:
            seen_question_ids.add(question_id)
        status = _safe_str(item.get("status"))
        if status not in EVALUATION_STATUSES:
            errors.append(f"{question_id or '<unknown>'}: invalid evaluation status {status!r}")
        for field in ["best_single_snippet"]:
            snippet = item.get(field)
            if isinstance(snippet, dict):
                item_id = _safe_str(snippet.get("item_id"))
                if item_id and item_id not in valid_item_ids:
                    errors.append(f"{question_id}: unknown snippet reference {item_id}")
        for field in ["top_three_snippets", "minimal_sufficient_snippets"]:
            for snippet in _safe_list(item.get(field)):
                if isinstance(snippet, dict):
                    item_id = _safe_str(snippet.get("item_id"))
                    if item_id and item_id not in valid_item_ids:
                        errors.append(f"{question_id}: unknown snippet reference {item_id}")
        for suggestion in _safe_list(item.get("suggested_changes")):
            if isinstance(suggestion, dict):
                target_item_id = _safe_str(suggestion.get("target_item_id"))
                if target_item_id and target_item_id not in valid_item_ids:
                    errors.append(f"{question_id}: unknown target_item_id {target_item_id}")
    return errors


def _synthesis_file(round_name: str) -> Path:
    return SYNTHESIS_DIR / f"{round_name}.json"


def synthesize_suggestions(*, round_name: str, evaluation_path: Path | None = None) -> dict[str, Any]:
    payload = _read_json(evaluation_path or _evaluation_file(round_name))
    grouped: dict[tuple[str, str, str], dict[str, Any]] = {}
    for question in _safe_list(payload.get("questions")):
        if not isinstance(question, dict):
            continue
        question_id = _safe_str(question.get("question_id"))
        exam_id = _safe_str(question.get("exam_id"))
        for suggestion in _safe_list(question.get("suggested_changes")):
            if not isinstance(suggestion, dict):
                continue
            kind = _safe_str(suggestion.get("kind")) or "other"
            target = _safe_str(suggestion.get("target_item_id"))
            proposal = _safe_str(suggestion.get("proposal")) or _safe_str(suggestion.get("proposed_fix"))
            key = (kind, target, proposal)
            entry = grouped.setdefault(
                key,
                {
                    "suggestion_id": f"{round_name}:{len(grouped) + 1}",
                    "kind": kind,
                    "target_item_id": target,
                    "proposal": proposal,
                    "source_question_ids": [],
                    "source_exams": [],
                    "pros": [],
                    "cons": [],
                    "recommended_direction": _safe_str(suggestion.get("recommended_direction")) or "consider_instead",
                    "human_review_status": "pending",
                },
            )
            if question_id and question_id not in entry["source_question_ids"]:
                entry["source_question_ids"].append(question_id)
            if exam_id and exam_id not in entry["source_exams"]:
                entry["source_exams"].append(exam_id)
            for key_name, field_name in [("pros", "why_helpful"), ("cons", "why_maybe_unnecessary")]:
                value = _safe_str(suggestion.get(field_name))
                if value and value not in entry[key_name]:
                    entry[key_name].append(value)

    synthesis = {
        "schema_version": SYNTHESIS_SCHEMA,
        "generated_at": timestamp_utc(),
        "round": round_name,
        "requires_human_review": True,
        "input_evaluations_path": portable_path(evaluation_path or _evaluation_file(round_name)),
        "summary": {
            "evaluation_count": len(_safe_list(payload.get("questions"))),
            "completed_evaluation_count": sum(1 for question in _safe_list(payload.get("questions")) if _safe_str(_safe_dict(question).get("status")) == "completed"),
            "suggestion_count": len(grouped),
        },
        "suggestions": sorted(grouped.values(), key=lambda item: item["suggestion_id"]),
    }
    _write_json(_synthesis_file(round_name), synthesis)
    return synthesis


def _analytics_file(round_name: str) -> Path:
    return ANALYTICS_DIR / f"{round_name}.json"


def _analytics_report_file(round_name: str) -> Path:
    return ANALYTICS_DIR / f"{round_name}.md"


def _comparison_summary(current: dict[str, Any], baseline: dict[str, Any]) -> dict[str, Any]:
    current_counts = Counter(_safe_str(_safe_dict(item.get("answerability")).get("status")) for item in _safe_list(current.get("questions")))
    baseline_counts = Counter(_safe_str(_safe_dict(item.get("answerability")).get("status")) for item in _safe_list(baseline.get("questions")))
    return {
        key: {
            "current": int(current_counts.get(key, 0)),
            "baseline": int(baseline_counts.get(key, 0)),
            "delta": int(current_counts.get(key, 0) - baseline_counts.get(key, 0)),
        }
        for key in sorted(set(current_counts) | set(baseline_counts))
        if key
    }


def build_ranking_analytics(
    *,
    round_name: str,
    evaluation_payload: dict[str, Any],
    selectable_items: list[dict[str, Any]],
    baseline_payload: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], str]:
    selectable_by_id = {item["item_id"]: item for item in selectable_items if isinstance(item, dict) and item.get("item_id")}
    completed = [item for item in _safe_list(evaluation_payload.get("questions")) if _safe_str(_safe_dict(item).get("status")) == "completed"]
    status_counts = Counter(_safe_str(_safe_dict(item).get("status")) for item in _safe_list(evaluation_payload.get("questions")))
    answerability_counts = Counter(_safe_str(_safe_dict(item.get("answerability")).get("status")) for item in completed)
    week_stats: dict[int, dict[str, set[str]]] = defaultdict(lambda: {"top1": set(), "top3": set(), "minimal": set(), "all": set()})

    for item_id, item in selectable_by_id.items():
        week = int(item.get("week") or 0)
        if week > 0:
            week_stats[week]["all"].add(item_id)
    for evaluation in completed:
        best = _safe_dict(evaluation.get("best_single_snippet"))
        item_id = _safe_str(best.get("item_id"))
        if item_id in selectable_by_id:
            week_stats[int(selectable_by_id[item_id].get("week") or 0)]["top1"].add(item_id)
        for bucket_name, key in [("top_three_snippets", "top3"), ("minimal_sufficient_snippets", "minimal")]:
            for snippet in _safe_list(evaluation.get(bucket_name)):
                item_id = _safe_str(_safe_dict(snippet).get("item_id"))
                if item_id in selectable_by_id:
                    week_stats[int(selectable_by_id[item_id].get("week") or 0)][key].add(item_id)

    weeks_payload = []
    for week in sorted(week for week in week_stats if week > 0):
        stats = week_stats[week]
        never_used = sorted(stats["all"] - stats["minimal"])
        weeks_payload.append(
            {
                "week": week,
                "top1_unique_snippets": len(stats["top1"]),
                "top3_unique_snippets": len(stats["top3"]),
                "minimal_set_unique_snippets": len(stats["minimal"]),
                "minimal_set_unused_snippets": len(never_used),
                "unused_snippet_ids": never_used[:50],
            }
        )

    insights = []
    if not completed:
        insights.append("No completed question-to-snippet evaluations yet. Ranking decisions should wait until round reviews are filled in.")
    elif weeks_payload:
        top_week = max(weeks_payload, key=lambda row: row["minimal_set_unique_snippets"])
        insights.append(f"Week {top_week['week']} currently has the broadest minimal-set footprint with {top_week['minimal_set_unique_snippets']} unique snippets.")

    analytics = {
        "schema_version": ANALYTICS_SCHEMA,
        "generated_at": timestamp_utc(),
        "round": round_name,
        "input_evaluations_path": portable_path(_evaluation_file(round_name)),
        "summary": {
            "total_evaluations": len(_safe_list(evaluation_payload.get("questions"))),
            "completed_evaluations": len(completed),
            "status_counts": dict(status_counts),
            "answerability_counts": dict(answerability_counts),
        },
        "weeks": weeks_payload,
        "insights": insights,
        "comparison": _comparison_summary(evaluation_payload, baseline_payload or {}) if baseline_payload else {},
    }

    lines = [
        f"# Ranking Analytics ({round_name})",
        "",
        f"- Total evaluations: `{analytics['summary']['total_evaluations']}`",
        f"- Completed evaluations: `{analytics['summary']['completed_evaluations']}`",
        f"- Status counts: `{json.dumps(analytics['summary']['status_counts'], ensure_ascii=False, sort_keys=True)}`",
    ]
    if analytics["summary"]["answerability_counts"]:
        lines.append(f"- Answerability counts: `{json.dumps(analytics['summary']['answerability_counts'], ensure_ascii=False, sort_keys=True)}`")
    lines.extend(["", "## Week Summary", ""])
    if weeks_payload:
        lines.append("| Week | Top 1 unique | Top 3 unique | Minimal-set unique | Minimal-set unused |")
        lines.append("|---|---:|---:|---:|---:|")
        for row in weeks_payload:
            lines.append(f"| {row['week']} | {row['top1_unique_snippets']} | {row['top3_unique_snippets']} | {row['minimal_set_unique_snippets']} | {row['minimal_set_unused_snippets']} |")
    else:
        lines.append("No completed evaluations yet.")
    if insights:
        lines.extend(["", "## Insights", ""])
        for insight in insights:
            lines.append(f"- {insight}")
    return analytics, "\n".join(lines) + "\n"


def write_ranking_analytics(
    *,
    round_name: str,
    baseline_round: str = "",
    selectable_items_path: Path = SELECTABLE_ITEMS_FILE,
) -> dict[str, Any]:
    evaluations = _read_json(_evaluation_file(round_name))
    selectable_items = _read_json(selectable_items_path) if selectable_items_path.exists() else build_selectable_items_snapshot()
    baseline = _read_json(_evaluation_file(baseline_round)) if baseline_round and _evaluation_file(baseline_round).exists() else None
    analytics, markdown = build_ranking_analytics(
        round_name=round_name,
        evaluation_payload=evaluations,
        selectable_items=selectable_items,
        baseline_payload=baseline,
    )
    _write_json(_analytics_file(round_name), analytics)
    _analytics_report_file(round_name).parent.mkdir(parents=True, exist_ok=True)
    _analytics_report_file(round_name).write_text(markdown, encoding="utf-8")
    return analytics


def validate_all(
    *,
    question_bank_path: Path = QUESTION_BANK_FILE,
    selectable_items_path: Path = SELECTABLE_ITEMS_FILE,
    evaluation_round: str = "",
) -> list[str]:
    from pipelines.vision_exam_pipeline_shared import validate_question_bank_payload

    errors = []
    if question_bank_path.exists():
        errors.extend(validate_question_bank_payload(_read_json(question_bank_path)))
    if evaluation_round:
        evaluation_path = _evaluation_file(evaluation_round)
        if evaluation_path.exists():
            selectable = _read_json(selectable_items_path)
            errors.extend(validate_evaluation_payload(_read_json(evaluation_path), selectable_items=selectable))
    return errors

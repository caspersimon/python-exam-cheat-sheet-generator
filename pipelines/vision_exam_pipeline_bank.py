from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from pipelines.vision_exam_pipeline_shared import (
    COMPLETENESS_FILE,
    LEGACY_ASSESSMENT_DIR,
    PAGE_MANIFEST_FILE,
    PAGE_MANIFEST_SCHEMA,
    QUESTION_BANK_FILE,
    QUESTION_BANK_SCHEMA,
    TMP_ROOT,
    WORK_PACKET_DIR,
    _default_blocked_question,
    _existing_page_paths,
    _normalize_question_options,
    _question_id,
    _read_json,
    _safe_dict,
    _safe_list,
    _safe_str,
    _slugify,
    _write_json,
    duplicate_exam_aliases,
    load_study_db,
    portable_path,
    render_exam_pages,
    timestamp_utc,
    unique_exam_sources,
)


def prepare_page_manifest(
    *,
    tmp_dir: Path = TMP_ROOT,
    manifest_path: Path = PAGE_MANIFEST_FILE,
    dpi: int = 160,
    overwrite: bool = False,
) -> dict[str, Any]:
    page_root = tmp_dir / "pages"
    exams_payload = []
    for exam in unique_exam_sources():
        existing_pages = [] if overwrite else _existing_page_paths(exam["exam_id"])
        if existing_pages:
            pages = existing_pages
            render_status = "reused_existing_pages"
        else:
            pages = render_exam_pages(exam, page_root, dpi=dpi, overwrite=overwrite)
            render_status = "rendered_now"
        exams_payload.append(
            {
                "exam_id": exam["exam_id"],
                "title": exam["title"],
                "group": exam["group"],
                "pdf_path": portable_path(Path(exam["pdf_path"])),
                "expected_questions": int(exam["expected_questions"]),
                "page_count": len(pages),
                "page_image_paths": [portable_path(path) for path in pages],
                "render_status": render_status,
            }
        )
    manifest = {
        "schema_version": PAGE_MANIFEST_SCHEMA,
        "generated_at": timestamp_utc(),
        "policy": {
            "vision_only_question_capture": True,
            "text_layer_extraction_forbidden": True,
            "ocr_forbidden": True,
            "page_rendering_allowed": True,
        },
        "duplicate_aliases": duplicate_exam_aliases(),
        "exams": exams_payload,
    }
    _write_json(manifest_path, manifest)
    return manifest


def _legacy_payload_index(payload_dir: Path = LEGACY_ASSESSMENT_DIR) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for path in sorted(payload_dir.glob("*.json")):
        payload = _read_json(path)
        if not isinstance(payload, dict):
            continue
        payload["_payload_path"] = portable_path(path)
        keys = {
            _slugify(path.stem),
            _slugify(Path(_safe_str(payload.get("source"))).stem),
            _slugify(payload.get("exam_label")),
        }
        for key in keys:
            if key and key not in index:
                index[key] = payload
    return index


def _study_db_assessment_index() -> dict[str, dict[str, Any]]:
    db = load_study_db()
    exams = _safe_list(_safe_dict(db.get("assessments")).get("exams"))
    index: dict[str, dict[str, Any]] = {}
    for exam in exams:
        if not isinstance(exam, dict):
            continue
        keys = {
            _slugify(exam.get("exam_label")),
            _slugify(Path(_safe_str(exam.get("source"))).stem),
        }
        for key in keys:
            if key and key not in index:
                index[key] = exam
    return index


def _seed_question_record(exam_id: str, question: dict[str, Any], *, payload_path: str) -> dict[str, Any]:
    number = int(question["number"])
    return {
        "question_id": _question_id(exam_id, number),
        "number": number,
        "topic": _safe_str(question.get("topic")),
        "question": _safe_str(question.get("question")),
        "options": _normalize_question_options(question.get("options")),
        "correct": _safe_str(question.get("correct")),
        "explanation": _safe_str(question.get("explanation")),
        "code_context": _safe_str(question.get("code_context")),
        "provenance": {
            "origin": "legacy_assessment_payload",
            "origin_path": payload_path,
            "capture_method": "legacy_text_or_ocr_seed",
            "review_status": "seeded_legacy_needs_vision_review",
            "review_pass": 0,
            "human_confirmed": False,
            "page_refs": [],
            "notes": [],
        },
    }


def _merge_questions(
    *,
    exam_id: str,
    expected_questions: int,
    existing_exam: dict[str, Any],
    legacy_payload: dict[str, Any] | None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    existing_questions = {
        int(question["number"]): deepcopy(question)
        for question in _safe_list(existing_exam.get("questions"))
        if isinstance(question, dict) and str(question.get("number", "")).isdigit()
    }
    existing_blocked = {
        int(question["number"]): deepcopy(question)
        for question in _safe_list(existing_exam.get("blocked_questions"))
        if isinstance(question, dict) and str(question.get("number", "")).isdigit()
    }
    legacy_questions: dict[int, dict[str, Any]] = {}
    if legacy_payload:
        payload_path = _safe_str(legacy_payload.get("_payload_path"))
        for question in _safe_list(legacy_payload.get("questions")):
            if isinstance(question, dict) and str(question.get("number", "")).isdigit():
                number = int(question["number"])
                legacy_questions.setdefault(number, _seed_question_record(exam_id, question, payload_path=payload_path))

    merged_questions = []
    blocked_questions = []
    for number in range(1, expected_questions + 1):
        if number in existing_questions:
            merged_questions.append(existing_questions[number])
        elif number in legacy_questions:
            merged_questions.append(legacy_questions[number])
        else:
            blocked_questions.append(existing_blocked.get(number) or _default_blocked_question(exam_id, number))
    return sorted(merged_questions, key=lambda item: int(item["number"])), sorted(blocked_questions, key=lambda item: int(item["number"]))


def _page_manifest_index(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        _safe_str(exam.get("exam_id")): exam
        for exam in _safe_list(manifest.get("exams"))
        if isinstance(exam, dict)
    }


def _review_tracking(questions: list[dict[str, Any]], blocked_questions: list[dict[str, Any]]) -> dict[str, int]:
    confirmed = 0
    seeded = 0
    for question in questions:
        provenance = _safe_dict(question.get("provenance"))
        if bool(provenance.get("human_confirmed")):
            confirmed += 1
        if _safe_str(provenance.get("origin")) == "legacy_assessment_payload":
            seeded += 1
    return {
        "present_questions": len(questions),
        "blocked_questions": len(blocked_questions),
        "human_confirmed_questions": confirmed,
        "legacy_seeded_questions": seeded,
        "pending_vision_questions": len(blocked_questions),
    }


def _exam_status(tracking: dict[str, int]) -> str:
    if tracking["blocked_questions"] == 0 and tracking["present_questions"] == tracking["human_confirmed_questions"]:
        return "complete"
    if tracking["present_questions"] > 0:
        return "partial"
    return "not_started"


def seed_question_bank(
    *,
    question_bank_path: Path = QUESTION_BANK_FILE,
    page_manifest_path: Path = PAGE_MANIFEST_FILE,
) -> dict[str, Any]:
    page_manifest = _read_json(page_manifest_path) if page_manifest_path.exists() else prepare_page_manifest()
    page_index = _page_manifest_index(page_manifest)
    legacy_index = _legacy_payload_index()
    study_db_index = _study_db_assessment_index()
    existing = _read_json(question_bank_path) if question_bank_path.exists() else {}
    existing_exams = {
        _safe_str(exam.get("exam_id")): exam
        for exam in _safe_list(_safe_dict(existing).get("exams"))
        if isinstance(exam, dict)
    }

    exams_payload = []
    for exam in unique_exam_sources():
        exam_id = exam["exam_id"]
        page_entry = page_index.get(exam_id, {})
        lookup_keys = {_slugify(exam_id), _slugify(Path(str(exam["pdf_path"])).stem), _slugify(exam["title"])}
        legacy_payload = next((legacy_index[key] for key in lookup_keys if key in legacy_index), None)
        study_db_exam = next((study_db_index[key] for key in lookup_keys if key in study_db_index), None)
        questions, blocked_questions = _merge_questions(
            exam_id=exam_id,
            expected_questions=int(exam["expected_questions"]),
            existing_exam=deepcopy(existing_exams.get(exam_id, {})),
            legacy_payload=legacy_payload,
        )
        tracking = _review_tracking(questions, blocked_questions)
        exams_payload.append(
            {
                "exam_id": exam_id,
                "title": exam["title"],
                "group": exam["group"],
                "pdf_path": portable_path(Path(exam["pdf_path"])),
                "expected_questions": int(exam["expected_questions"]),
                "page_image_paths": _safe_list(page_entry.get("page_image_paths")),
                "page_count": int(page_entry.get("page_count") or 0),
                "duplicate_aliases": [alias for alias in duplicate_exam_aliases() if _safe_str(alias.get("duplicate_of")) == exam_id],
                "seed_sources": {
                    "legacy_assessment_payload_path": _safe_str(_safe_dict(legacy_payload).get("_payload_path")),
                    "study_db_exam_label": _safe_str(_safe_dict(study_db_exam).get("exam_label")),
                    "study_db_exam_source": _safe_str(_safe_dict(study_db_exam).get("source")),
                    "legacy_provenance_warning": "Existing imported questions may originate from pdftotext/OCR-era extraction and require vision review.",
                },
                "review_tracking": tracking,
                "extraction_status": _exam_status(tracking),
                "questions": questions,
                "blocked_questions": blocked_questions,
            }
        )

    payload = {
        "schema_version": QUESTION_BANK_SCHEMA,
        "generated_at": timestamp_utc(),
        "policy": {
            "vision_only_question_capture": True,
            "text_layer_extraction_forbidden": True,
            "ocr_forbidden": True,
            "human_review_checkpoint_required": True,
        },
        "canonical_exam_count": len(exams_payload),
        "duplicate_aliases": duplicate_exam_aliases(),
        "page_manifest_path": portable_path(page_manifest_path),
        "exams": exams_payload,
    }
    _write_json(question_bank_path, payload)
    return payload


def build_completeness_report(question_bank: dict[str, Any]) -> dict[str, Any]:
    exams_report = []
    incomplete = []
    reviewed_total = 0
    expected_total = 0
    for exam in _safe_list(question_bank.get("exams")):
        if not isinstance(exam, dict):
            continue
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
        missing_without_reason = [number for number in range(1, expected + 1) if number not in question_numbers | blocked_numbers]
        confirmed = sum(
            1
            for question in _safe_list(exam.get("questions"))
            if isinstance(question, dict) and bool(_safe_dict(question.get("provenance")).get("human_confirmed"))
        )
        # Completeness tracks whether every expected question slot is covered.
        # Human confirmation remains a separate provenance signal.
        status = "complete" if not blocked_numbers and not missing_without_reason else "incomplete"
        row = {
            "exam_id": _safe_str(exam.get("exam_id")),
            "title": _safe_str(exam.get("title")),
            "expected_questions": expected,
            "present_questions": len(question_numbers),
            "blocked_questions": len(blocked_numbers),
            "human_confirmed_questions": confirmed,
            "missing_without_reason": missing_without_reason,
            "status": status,
        }
        exams_report.append(row)
        reviewed_total += len(question_numbers)
        expected_total += expected
        if status != "complete":
            incomplete.append(row["exam_id"])
    return {
        "schema_version": QUESTION_BANK_SCHEMA,
        "generated_at": timestamp_utc(),
        "question_bank_schema_version": _safe_str(question_bank.get("schema_version")),
        "overall_status": "complete" if not incomplete else "incomplete",
        "summary": {
            "canonical_exam_count": len(exams_report),
            "complete_exam_count": sum(1 for row in exams_report if row["status"] == "complete"),
            "incomplete_exam_count": len(incomplete),
            "reviewed_question_count": reviewed_total,
            "expected_question_count": expected_total,
        },
        "exams": exams_report,
    }


def write_completeness_report(
    *,
    question_bank_path: Path = QUESTION_BANK_FILE,
    report_path: Path = COMPLETENESS_FILE,
) -> dict[str, Any]:
    report = build_completeness_report(_read_json(question_bank_path))
    _write_json(report_path, report)
    return report


def write_extraction_packets(
    *,
    question_bank_path: Path = QUESTION_BANK_FILE,
    output_dir: Path | None = None,
) -> dict[str, Any]:
    question_bank = _read_json(question_bank_path)
    packet_dir = output_dir or (WORK_PACKET_DIR / "extractions")
    packets = []
    for exam in _safe_list(question_bank.get("exams")):
        if not isinstance(exam, dict):
            continue
        questions = [question for question in _safe_list(exam.get("questions")) if isinstance(question, dict)]
        blocked = [question for question in _safe_list(exam.get("blocked_questions")) if isinstance(question, dict)]
        packet = {
            "schema_version": QUESTION_BANK_SCHEMA,
            "generated_at": timestamp_utc(),
            "exam_id": _safe_str(exam.get("exam_id")),
            "title": _safe_str(exam.get("title")),
            "expected_questions": int(exam.get("expected_questions") or 0),
            "pdf_path": _safe_str(exam.get("pdf_path")),
            "page_image_paths": _safe_list(exam.get("page_image_paths")),
            "captured_question_numbers": [int(question["number"]) for question in questions if str(question.get("number", "")).isdigit()],
            "pending_question_numbers": [int(question["number"]) for question in blocked if str(question.get("number", "")).isdigit()],
            "blocked_questions": blocked,
            "instructions": [
                "Use only the rendered PNG page images for question capture.",
                "Do not use OCR, pdftotext, or any deterministic text extraction.",
                "For each pending question, record the full question text, answer options, correct answer, and explanation with provenance notes.",
            ],
        }
        packets.append(packet)
        _write_json(packet_dir / f"{packet['exam_id']}.json", packet)

    index = {
        "schema_version": QUESTION_BANK_SCHEMA,
        "generated_at": timestamp_utc(),
        "question_bank_path": portable_path(question_bank_path),
        "packet_count": len(packets),
        "packets": [
            {
                "exam_id": packet["exam_id"],
                "expected_questions": packet["expected_questions"],
                "captured_questions": len(packet["captured_question_numbers"]),
                "pending_questions": len(packet["pending_question_numbers"]),
                "packet_path": portable_path(packet_dir / f"{packet['exam_id']}.json"),
            }
            for packet in packets
        ],
    }
    _write_json(packet_dir / "index.json", index)
    return index


def merge_review_drop(
    *,
    review_drop_path: Path,
    question_bank_path: Path = QUESTION_BANK_FILE,
) -> dict[str, Any]:
    review = _read_json(review_drop_path)
    exam_id = _safe_str(review.get("exam_id"))
    if not exam_id:
        raise ValueError(f"Review drop missing exam_id: {review_drop_path}")

    question_bank = _read_json(question_bank_path)
    target_exam = next(
        (exam for exam in _safe_list(question_bank.get("exams")) if isinstance(exam, dict) and _safe_str(exam.get("exam_id")) == exam_id),
        None,
    )
    if target_exam is None:
        raise ValueError(f"Exam not found in question bank: {exam_id}")

    questions_by_number = {
        int(question["number"]): question
        for question in _safe_list(target_exam.get("questions"))
        if isinstance(question, dict) and str(question.get("number", "")).isdigit()
    }
    blocked_by_number = {
        int(question["number"]): question
        for question in _safe_list(target_exam.get("blocked_questions"))
        if isinstance(question, dict) and str(question.get("number", "")).isdigit()
    }

    for update in _safe_list(review.get("question_updates")):
        if not isinstance(update, dict) or not str(update.get("number", "")).isdigit():
            continue
        number = int(update["number"])
        existing = deepcopy(questions_by_number.get(number, {}))
        provenance = {
            "origin": "vision_review_drop",
            "origin_path": portable_path(review_drop_path),
            "capture_method": "vision_model_manual_review",
            "review_status": _safe_str(_safe_dict(update.get("provenance")).get("review_status")) or "agent_reviewed_pending_human_confirmation",
            "review_pass": int(_safe_dict(update.get("provenance")).get("review_pass") or 1),
            "human_confirmed": bool(_safe_dict(update.get("provenance")).get("human_confirmed")),
            "page_refs": _safe_list(_safe_dict(update.get("provenance")).get("page_refs")),
            "notes": _safe_list(_safe_dict(update.get("provenance")).get("notes")),
        }
        questions_by_number[number] = {
            "question_id": _question_id(exam_id, number),
            "number": number,
            "topic": _safe_str(update.get("topic")) or _safe_str(existing.get("topic")),
            "question": _safe_str(update.get("question")) or _safe_str(existing.get("question")),
            "options": _normalize_question_options(update.get("options")) or _normalize_question_options(existing.get("options")),
            "correct": _safe_str(update.get("correct")) or _safe_str(existing.get("correct")),
            "explanation": _safe_str(update.get("explanation")) or _safe_str(existing.get("explanation")),
            "code_context": _safe_str(update.get("code_context")) or _safe_str(existing.get("code_context")),
            "provenance": provenance,
        }
        blocked_by_number.pop(number, None)

    target_exam["questions"] = sorted(questions_by_number.values(), key=lambda item: int(item["number"]))
    target_exam["blocked_questions"] = sorted(blocked_by_number.values(), key=lambda item: int(item["number"]))
    target_exam["review_tracking"] = _review_tracking(target_exam["questions"], target_exam["blocked_questions"])
    target_exam["extraction_status"] = _exam_status(target_exam["review_tracking"])
    question_bank["generated_at"] = timestamp_utc()
    _write_json(question_bank_path, question_bank)
    return target_exam

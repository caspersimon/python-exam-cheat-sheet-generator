from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from pipelines.shared import (
    FAST_GEMINI_AGENT,
    FAST_GEMINI_AGENT_FALLBACK,
    SMART_GEMINI_AGENT,
    SMART_GEMINI_AGENT_FALLBACK,
    extract_json_blob,
)
from pipelines.vision_exam_pipeline_bank import merge_review_drop
from pipelines.vision_exam_pipeline_eval_helpers import (
    candidate_snippet_families_for_question,
    evaluation_prompt,
    normalize_family_selection,
    normalize_near_identical_pieces,
)
from pipelines.vision_exam_pipeline_review import _evaluation_file, _write_evaluation_work_packets
from pipelines.vision_exam_pipeline_shared import (
    QUESTION_BANK_FILE,
    REVIEW_DROP_DIR,
    SELECTABLE_ITEMS_FILE,
    _normalize_question_options,
    _read_json,
    _safe_dict,
    _safe_list,
    _safe_str,
    _write_json,
    portable_path,
    timestamp_utc,
)

ROOT = Path(__file__).resolve().parents[1]


def _model_chain(model: str) -> list[str]:
    if model == SMART_GEMINI_AGENT:
        return [SMART_GEMINI_AGENT, SMART_GEMINI_AGENT_FALLBACK]
    if model == FAST_GEMINI_AGENT:
        return [FAST_GEMINI_AGENT, FAST_GEMINI_AGENT_FALLBACK]
    return [model]


def _run_gemini_json(prompt: str, *, model: str, timeout_seconds: int) -> dict[str, Any]:
    last_error: Exception | None = None
    for candidate in _model_chain(model):
        try:
            result = subprocess.run(
                ["gemini", "-m", candidate, "-p", prompt],
                text=True,
                capture_output=True,
                timeout=timeout_seconds,
            )
            if result.returncode != 0:
                details = (result.stderr or result.stdout or "no stdout/stderr captured").strip()
                raise RuntimeError(f"Gemini failed ({result.returncode}): {details[:1200]}")
            parsed = json.loads(extract_json_blob(result.stdout))
            if not isinstance(parsed, dict):
                raise ValueError("Gemini output must be a JSON object.")
            return parsed
        except Exception as exc:  # noqa: BLE001
            last_error = exc
    raise RuntimeError(f"Gemini prompt failed after retries: {last_error}")


def _page_capture_prompt(
    *,
    exam_id: str,
    title: str,
    page_image_path: Path,
    page_ref: str,
    pending_numbers: list[int],
) -> str:
    return f"""
You are performing a vision-only extraction from a rendered PNG of a Python exam solution page.

Exam ID: {exam_id}
Exam title: {title}
Pending question numbers for this exam: {pending_numbers}
Image: @{page_image_path}

Return ONLY one JSON object with EXACT shape:
{{
  "question_updates": [
    {{
      "number": 0,
      "topic": "",
      "question": "",
      "options": {{"a": "", "b": "", "c": "", "d": ""}},
      "correct": "a",
      "explanation": "",
      "code_context": "",
      "provenance": {{
        "review_status": "agent_reviewed_pending_human_confirmation",
        "review_pass": 1,
        "human_confirmed": false,
        "page_refs": ["{page_ref}"],
        "notes": ["Reviewed from rendered PNG pages only."]
      }}
    }}
  ]
}}

Rules:
- Use ONLY what is visible in the image. Do not use OCR, text layers, or any external context.
- Include only questions whose prompt, answer options, and marked correct answer are visible enough on this image to extract faithfully.
- If no pending question is fully extractable from this image, return {{"question_updates": []}}.
- Use lowercase option keys a/b/c/d.
- `topic` should be the short topic label from the question header, not the full header line.
- `correct` must be the visibly marked answer on the solution page.
- `explanation` should be concise and based only on the visible question and answer.
- `code_context` should contain the visible code block if the question includes one; otherwise "".
- `page_refs` must stay exactly ["{page_ref}"].
- Add a short note in `provenance.notes` if any small detail is hard to read, instead of guessing silently.
""".strip()


def _normalize_capture_update(update: dict[str, Any], *, page_ref: str) -> dict[str, Any] | None:
    if not isinstance(update, dict):
        return None
    number_text = str(update.get("number", "")).strip()
    if not number_text.isdigit():
        return None
    provenance = _safe_dict(update.get("provenance"))
    page_refs = _safe_list(provenance.get("page_refs")) or [page_ref]
    notes = [note for note in _safe_list(provenance.get("notes")) if _safe_str(note)]
    if "Reviewed from rendered PNG pages only." not in notes:
        notes.insert(0, "Reviewed from rendered PNG pages only.")
    return {
        "number": int(number_text),
        "topic": _safe_str(update.get("topic")),
        "question": _safe_str(update.get("question")),
        "options": _normalize_question_options(update.get("options")),
        "correct": _safe_str(update.get("correct")).lower(),
        "explanation": _safe_str(update.get("explanation")),
        "code_context": _safe_str(update.get("code_context")),
        "provenance": {
            "review_status": _safe_str(provenance.get("review_status")) or "agent_reviewed_pending_human_confirmation",
            "review_pass": int(provenance.get("review_pass") or 1),
            "human_confirmed": bool(provenance.get("human_confirmed")),
            "page_refs": page_refs,
            "notes": notes,
        },
    }


def auto_capture_missing_questions(
    *,
    exam_ids: list[str] | None = None,
    question_bank_path: Path = QUESTION_BANK_FILE,
    model: str = SMART_GEMINI_AGENT,
    timeout_seconds: int = 180,
) -> dict[str, Any]:
    question_bank = _read_json(question_bank_path)
    target_exam_ids = {exam_id for exam_id in (exam_ids or []) if exam_id}
    results = []

    for exam in _safe_list(question_bank.get("exams")):
        if not isinstance(exam, dict):
            continue
        exam_id = _safe_str(exam.get("exam_id"))
        if target_exam_ids and exam_id not in target_exam_ids:
            continue
        pending = {
            int(item["number"])
            for item in _safe_list(exam.get("blocked_questions"))
            if isinstance(item, dict) and str(item.get("number", "")).isdigit()
        }
        if not pending:
            continue
        captured: dict[int, dict[str, Any]] = {}
        for page_ref in _safe_list(exam.get("page_image_paths")):
            page_path = Path(page_ref)
            if not page_path.is_absolute():
                page_path = (ROOT / page_ref).resolve()
            if not page_path.exists():
                continue
            prompt = _page_capture_prompt(
                exam_id=exam_id,
                title=_safe_str(exam.get("title")),
                page_image_path=page_path,
                page_ref=_safe_str(page_ref),
                pending_numbers=sorted(pending),
            )
            parsed = _run_gemini_json(prompt, model=model, timeout_seconds=timeout_seconds)
            for raw_update in _safe_list(parsed.get("question_updates")):
                update = _normalize_capture_update(raw_update, page_ref=_safe_str(page_ref))
                if not update:
                    continue
                number = int(update["number"])
                if number in pending and number not in captured:
                    captured[number] = update
            if pending and pending.issubset(set(captured)):
                break
        if not captured:
            results.append({"exam_id": exam_id, "captured_questions": 0, "review_drop_path": "", "present_questions": len(_safe_list(exam.get("questions"))), "blocked_questions": len(_safe_list(exam.get("blocked_questions")))})
            continue
        review_drop_path = REVIEW_DROP_DIR / f"{exam_id}-auto-gemini.json"
        review_drop = {
            "exam_id": exam_id,
            "question_updates": [captured[number] for number in sorted(captured)],
        }
        _write_json(review_drop_path, review_drop)
        merged_exam = merge_review_drop(review_drop_path=review_drop_path, question_bank_path=question_bank_path)
        results.append(
            {
                "exam_id": exam_id,
                "captured_questions": len(captured),
                "review_drop_path": portable_path(review_drop_path),
                "present_questions": int(_safe_dict(merged_exam.get("review_tracking")).get("present_questions") or 0),
                "blocked_questions": int(_safe_dict(merged_exam.get("review_tracking")).get("blocked_questions") or 0),
            }
        )
    return {
        "generated_at": timestamp_utc(),
        "model": model,
        "results": results,
    }


def _normalize_ranked_snippets(values: Any, *, valid_ids: set[str], max_items: int) -> list[dict[str, Any]]:
    items = []
    seen: set[str] = set()
    for value in _safe_list(values):
        entry = _safe_dict(value)
        item_id = _safe_str(entry.get("item_id"))
        if not item_id or item_id in seen or item_id not in valid_ids:
            continue
        seen.add(item_id)
        items.append({"item_id": item_id, "rationale": _safe_str(entry.get("rationale"))})
        if len(items) >= max_items:
            break
    return items


def _normalize_suggested_changes(values: Any, *, valid_ids: set[str]) -> list[dict[str, Any]]:
    items = []
    for value in _safe_list(values):
        entry = _safe_dict(value)
        kind = _safe_str(entry.get("kind"))
        if kind not in {"edit_existing", "add_new"}:
            continue
        target_item_id = _safe_str(entry.get("target_item_id"))
        if target_item_id and target_item_id not in valid_ids:
            target_item_id = ""
        items.append(
            {
                "kind": kind,
                "target_item_id": target_item_id,
                "proposal": _safe_str(entry.get("proposal")),
                "why_helpful": _safe_str(entry.get("why_helpful")),
                "why_maybe_unnecessary": _safe_str(entry.get("why_maybe_unnecessary")),
                "recommended_direction": _safe_str(entry.get("recommended_direction")) or "consider_instead",
            }
        )
    return items


def auto_evaluate_questions(
    *,
    round_name: str,
    model: str = FAST_GEMINI_AGENT,
    timeout_seconds: int = 180,
    limit: int = 0,
    evaluation_path: Path | None = None,
    selectable_items_path: Path = SELECTABLE_ITEMS_FILE,
) -> dict[str, Any]:
    path = evaluation_path or _evaluation_file(round_name)
    payload = _read_json(path)
    selectable_items = _read_json(selectable_items_path)
    valid_ids = {_safe_str(item.get("item_id")) for item in selectable_items if isinstance(item, dict) and _safe_str(item.get("item_id"))}
    valid_snippet_ids = {
        _safe_str(item.get("snippet_id"))
        for item in selectable_items
        if isinstance(item, dict) and _safe_str(item.get("snippet_id"))
    }
    updated = 0
    for question in _safe_list(payload.get("questions")):
        if not isinstance(question, dict):
            continue
        status = _safe_str(question.get("status"))
        if status == "blocked_missing_question_capture":
            continue
        if status == "completed":
            continue
        candidates = candidate_snippet_families_for_question(question=question, selectable_items=selectable_items)
        parsed = _run_gemini_json(
            evaluation_prompt(question=question, candidates=candidates),
            model=model,
            timeout_seconds=timeout_seconds,
        )
        question["near_identical_past_exam_pieces"] = normalize_near_identical_pieces(
            parsed.get("near_identical_past_exam_pieces"),
            valid_piece_ids=valid_ids,
            valid_snippet_ids=valid_snippet_ids,
        )
        best_family = normalize_family_selection(
            parsed.get("best_snippet_family"),
            valid_snippet_ids=valid_snippet_ids,
            valid_piece_ids=valid_ids,
            piece_field="critical_piece_ids",
            max_piece_count=3,
        )
        question["best_snippet_family"] = best_family
        question["supporting_snippet_families"] = [
            family
            for family in [
                normalize_family_selection(
                    value,
                    valid_snippet_ids=valid_snippet_ids,
                    valid_piece_ids=valid_ids,
                    piece_field="critical_piece_ids",
                    max_piece_count=3,
                )
                for value in _safe_list(parsed.get("supporting_snippet_families"))
            ]
            if family
        ][:2]
        question["minimal_snippet_families"] = [
            family
            for family in [
                normalize_family_selection(
                    value,
                    valid_snippet_ids=valid_snippet_ids,
                    valid_piece_ids=valid_ids,
                    piece_field="needed_piece_ids",
                    max_piece_count=6,
                )
                for value in _safe_list(parsed.get("minimal_snippet_families"))
            ]
            if family
        ][:6]
        best = _safe_dict(parsed.get("best_single_snippet"))
        best_id = _safe_str(best.get("item_id"))
        if best_family and _safe_list(best_family.get("critical_piece_ids")):
            question["best_single_snippet"] = {
                "item_id": _safe_list(best_family.get("critical_piece_ids"))[0],
                "rationale": _safe_str(best_family.get("rationale")),
            }
        else:
            question["best_single_snippet"] = {
                "item_id": best_id if best_id in valid_ids else "",
                "rationale": _safe_str(best.get("rationale")),
            } if best_id in valid_ids else None
        top_three = []
        if best_family and _safe_list(best_family.get("critical_piece_ids")):
            top_three.append(
                {
                    "item_id": _safe_list(best_family.get("critical_piece_ids"))[0],
                    "rationale": _safe_str(best_family.get("rationale")),
                }
            )
        for family in _safe_list(question.get("supporting_snippet_families")):
            piece_ids = _safe_list(_safe_dict(family).get("critical_piece_ids"))
            if piece_ids:
                top_three.append({"item_id": piece_ids[0], "rationale": _safe_str(_safe_dict(family).get("rationale"))})
        question["top_three_snippets"] = top_three[:3] or _normalize_ranked_snippets(parsed.get("top_three_snippets"), valid_ids=valid_ids, max_items=3)
        minimal = []
        for family in _safe_list(question.get("minimal_snippet_families")):
            piece_ids = _safe_list(_safe_dict(family).get("needed_piece_ids"))
            if piece_ids:
                minimal.append({"item_id": piece_ids[0], "rationale": _safe_str(_safe_dict(family).get("rationale"))})
        question["minimal_sufficient_snippets"] = minimal[:6] or _normalize_ranked_snippets(parsed.get("minimal_sufficient_snippets"), valid_ids=valid_ids, max_items=6)
        answerability = _safe_dict(parsed.get("answerability"))
        question["answerability"] = {
            "status": _safe_str(answerability.get("status")) or "partial",
            "confidence": _safe_str(answerability.get("confidence")) or "medium",
            "rationale": _safe_str(answerability.get("rationale")),
            "usable_without_prior_python_knowledge": bool(answerability.get("usable_without_prior_python_knowledge")),
        }
        gap = _safe_dict(parsed.get("gap_analysis"))
        question["gap_analysis"] = {
            "summary": _safe_str(gap.get("summary")),
            "missing_concepts": [item for item in _safe_list(gap.get("missing_concepts")) if _safe_str(item)],
            "proposed_fix": _safe_str(gap.get("proposed_fix")),
        }
        question["suggested_changes"] = _normalize_suggested_changes(parsed.get("suggested_changes"), valid_ids=valid_ids)
        question["status"] = "completed"
        review_meta = _safe_dict(question.get("review_meta"))
        review_meta["requires_human_review"] = True
        review_meta["reviewed_at"] = timestamp_utc()
        review_meta["model"] = model
        review_meta["candidate_item_count"] = sum(len(_safe_list(candidate.get("pieces"))) for candidate in candidates)
        review_meta["candidate_snippet_families"] = candidates
        question["review_meta"] = review_meta
        updated += 1
        if limit and updated >= limit:
            break
    payload["generated_at"] = timestamp_utc()
    _write_json(path, payload)
    _write_evaluation_work_packets(round_name=round_name, payload=payload)
    return {
        "generated_at": timestamp_utc(),
        "model": model,
        "updated_questions": updated,
        "evaluation_path": portable_path(path),
    }

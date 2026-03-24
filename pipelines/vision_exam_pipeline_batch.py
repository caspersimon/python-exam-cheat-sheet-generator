from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from pipelines.vision_exam_pipeline_review import _evaluation_file
from pipelines.vision_exam_pipeline_shared import _read_json, _safe_dict, _safe_list, _safe_str


def evaluation_progress_summary(*, round_name: str, evaluation_path: Path | None = None) -> dict[str, Any]:
    path = evaluation_path or _evaluation_file(round_name)
    payload = _read_json(path)
    status_counts = Counter(_safe_str(_safe_dict(question).get("status")) for question in _safe_list(payload.get("questions")))
    total = len(_safe_list(payload.get("questions")))
    blocked = int(status_counts.get("blocked_missing_question_capture", 0))
    completed = int(status_counts.get("completed", 0))
    remaining = total - blocked - completed
    return {
        "total_questions": total,
        "blocked_questions": blocked,
        "completed_questions": completed,
        "remaining_questions": max(remaining, 0),
        "status_counts": dict(status_counts),
        "generated_at": _safe_str(payload.get("generated_at")),
    }

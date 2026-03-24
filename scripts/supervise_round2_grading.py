from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.vision_exam_pipeline import (  # noqa: E402
    SELECTABLE_ITEMS_FILE,
    auto_evaluate_questions,
    build_selectable_items_snapshot,
    validate_all,
    write_ranking_analytics,
)
from pipelines.vision_exam_pipeline_batch import evaluation_progress_summary  # noqa: E402
from pipelines.shared.model_defaults import FAST_GEMINI_AGENT  # noqa: E402


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Robust supervisor for round-2 question evaluation batches.")
    parser.add_argument("--round", default="round2")
    parser.add_argument("--baseline-round", default="round1")
    parser.add_argument("--model", default=FAST_GEMINI_AGENT)
    parser.add_argument("--timeout-seconds", type=int, default=180)
    parser.add_argument("--batch-size", type=int, default=5)
    parser.add_argument("--sleep-seconds", type=float, default=20.0)
    parser.add_argument("--max-stale-batches", type=int, default=8)
    parser.add_argument("--selectable-items-path", type=Path, default=SELECTABLE_ITEMS_FILE)
    parser.add_argument("--log-dir", type=Path, default=ROOT / "tmp/vision_exam_pipeline/round2_grading")
    return parser.parse_args()


def _emit(event: dict[str, object], *, event_log: Path, state_file: Path) -> None:
    line = json.dumps(event, ensure_ascii=False)
    print(line, flush=True)
    with event_log.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")
    state = {
        "updated_at": event.get("generated_at"),
        "event": event.get("phase"),
        "round": event.get("round"),
        "completed_questions": event.get("completed_questions"),
        "remaining_questions": event.get("remaining_questions"),
        "stale_batches": event.get("stale_batches"),
        "last_exit_code": event.get("exit_code", 0),
        "last_error": event.get("error", ""),
    }
    state_file.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _summary(round_name: str) -> dict[str, object]:
    return evaluation_progress_summary(round_name=round_name)


def main() -> int:
    args = _parse_args()
    args.log_dir.mkdir(parents=True, exist_ok=True)
    event_log = args.log_dir / "supervisor.jsonl"
    state_file = args.log_dir / "supervisor_state.json"
    event_log.write_text("", encoding="utf-8")

    if not args.selectable_items_path.exists():
        build_selectable_items_snapshot(output_path=args.selectable_items_path)

    start = _summary(args.round)
    _emit(
        {
            "phase": "start",
            "round": args.round,
            "model": args.model,
            "batch_size": args.batch_size,
            "sleep_seconds": args.sleep_seconds,
            "max_stale_batches": args.max_stale_batches,
            **start,
            "stale_batches": 0,
            "exit_code": 0,
        },
        event_log=event_log,
        state_file=state_file,
    )

    stale_batches = 0
    while True:
        before = _summary(args.round)
        remaining_before = int(before["remaining_questions"])
        completed_before = int(before["completed_questions"])
        if remaining_before <= 0:
            break

        batch_event: dict[str, object] = {
            "phase": "batch",
            "round": args.round,
            "completed_before": completed_before,
            "remaining_before": remaining_before,
        }
        try:
            result = auto_evaluate_questions(
                round_name=args.round,
                model=args.model,
                timeout_seconds=args.timeout_seconds,
                limit=args.batch_size,
                selectable_items_path=args.selectable_items_path,
            )
            batch_event["updated_questions"] = int(result.get("updated_questions") or 0)
            batch_event["exit_code"] = 0
        except Exception as exc:  # pragma: no cover - defensive recovery path
            batch_event["updated_questions"] = 0
            batch_event["exit_code"] = 1
            batch_event["error"] = str(exc)
            batch_event["traceback"] = traceback.format_exc(limit=20)

        after = _summary(args.round)
        completed_after = int(after["completed_questions"])
        progressed = completed_after > completed_before
        stale_batches = 0 if progressed else stale_batches + 1
        batch_event.update(after)
        batch_event["stale_batches"] = stale_batches
        _emit(batch_event, event_log=event_log, state_file=state_file)

        if int(after["remaining_questions"]) <= 0:
            break
        if stale_batches >= args.max_stale_batches:
            break
        time.sleep(args.sleep_seconds)

    analytics = write_ranking_analytics(
        round_name=args.round,
        baseline_round=args.baseline_round,
        selectable_items_path=args.selectable_items_path,
    )
    errors = validate_all(
        selectable_items_path=args.selectable_items_path,
        evaluation_round=args.round,
    )
    final = _summary(args.round)
    complete = int(final["remaining_questions"]) <= 0
    exit_code = 0 if complete and not errors else 2 if not complete else 1
    _emit(
        {
            "phase": "done",
            "round": args.round,
            "analytics_completed_evaluations": int(analytics["summary"]["completed_evaluations"]),
            "validation_status": "pass" if not errors else "fail",
            "validation_error_count": len(errors),
            **final,
            "stale_batches": stale_batches,
            "exit_code": exit_code,
            "error": "" if complete else "stopped_before_completion",
        },
        event_log=event_log,
        state_file=state_file,
    )
    if errors:
        print(json.dumps({"errors": errors}, ensure_ascii=False, indent=2), file=sys.stderr)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())

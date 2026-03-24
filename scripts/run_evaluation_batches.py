from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.vision_exam_pipeline import (
    SELECTABLE_ITEMS_FILE,
    auto_evaluate_questions,
    build_selectable_items_snapshot,
    validate_all,
    write_ranking_analytics,
)
from pipelines.vision_exam_pipeline_batch import evaluation_progress_summary
from pipelines.shared.model_defaults import FAST_GEMINI_AGENT


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run question-to-snippet evaluations in checkpointed batches.")
    parser.add_argument("--round", required=True)
    parser.add_argument("--model", default=FAST_GEMINI_AGENT)
    parser.add_argument("--timeout-seconds", type=int, default=180)
    parser.add_argument("--batch-size", type=int, default=5)
    parser.add_argument("--max-batches", type=int, default=200)
    parser.add_argument("--sleep-seconds", type=float, default=0.0)
    parser.add_argument("--baseline-round", default="")
    parser.add_argument("--selectable-items-path", type=Path, default=SELECTABLE_ITEMS_FILE)
    return parser.parse_args()


def _print_event(payload: dict[str, object]) -> None:
    print(json.dumps(payload, ensure_ascii=False), flush=True)


def main() -> int:
    args = _parse_args()
    if not args.selectable_items_path.exists():
        build_selectable_items_snapshot(output_path=args.selectable_items_path)

    _print_event({"phase": "start", "round": args.round, "batch_size": args.batch_size, "max_batches": args.max_batches})
    previous = evaluation_progress_summary(round_name=args.round)
    _print_event({"phase": "before", **previous})

    ran_batches = 0
    for batch_number in range(1, args.max_batches + 1):
        if previous["remaining_questions"] <= 0:
            break
        result = auto_evaluate_questions(
            round_name=args.round,
            model=args.model,
            timeout_seconds=args.timeout_seconds,
            limit=args.batch_size,
            selectable_items_path=args.selectable_items_path,
        )
        ran_batches += 1
        current = evaluation_progress_summary(round_name=args.round)
        _print_event(
            {
                "phase": "batch",
                "batch_number": batch_number,
                "updated_questions": int(result.get("updated_questions") or 0),
                **current,
            }
        )
        if int(result.get("updated_questions") or 0) <= 0:
            break
        previous = current
        if args.sleep_seconds > 0 and batch_number < args.max_batches:
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
    final_summary = evaluation_progress_summary(round_name=args.round)
    _print_event(
        {
            "phase": "done",
            "round": args.round,
            "batches_ran": ran_batches,
            "analytics_completed_evaluations": int(analytics["summary"]["completed_evaluations"]),
            "validation_status": "pass" if not errors else "fail",
            "validation_error_count": len(errors),
            **final_summary,
        }
    )
    if errors:
        print(json.dumps({"errors": errors}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

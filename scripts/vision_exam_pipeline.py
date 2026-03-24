#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.shared.model_defaults import FAST_GEMINI_AGENT, SMART_GEMINI_AGENT

from pipelines.vision_exam_pipeline import (
    COMPLETENESS_FILE,
    PAGE_MANIFEST_FILE,
    QUESTION_BANK_FILE,
    REVIEW_DROP_DIR,
    SELECTABLE_ITEMS_FILE,
    TMP_ROOT,
    auto_capture_missing_questions,
    auto_evaluate_questions,
    build_selectable_items_snapshot,
    merge_review_drop,
    prepare_page_manifest,
    seed_question_bank,
    synthesize_suggestions,
    validate_all,
    write_completeness_report,
    write_extraction_packets,
    write_evaluation_scaffold,
    write_ranking_analytics,
    write_review_packet,
)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Vision-first exam curation and snippet value pipeline.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare = subparsers.add_parser("prepare-pages", help="Render or reuse exam page PNGs and write a persistent manifest.")
    prepare.add_argument("--tmp-dir", type=Path, default=TMP_ROOT)
    prepare.add_argument("--manifest-path", type=Path, default=PAGE_MANIFEST_FILE)
    prepare.add_argument("--dpi", type=int, default=160)
    prepare.add_argument("--overwrite", action="store_true")

    seed_bank = subparsers.add_parser("seed-question-bank", help="Seed the persistent question bank from legacy assessment payloads.")
    seed_bank.add_argument("--question-bank-path", type=Path, default=QUESTION_BANK_FILE)
    seed_bank.add_argument("--page-manifest-path", type=Path, default=PAGE_MANIFEST_FILE)

    completeness = subparsers.add_parser("audit-completeness", help="Write a completeness manifest for the current question bank.")
    completeness.add_argument("--question-bank-path", type=Path, default=QUESTION_BANK_FILE)
    completeness.add_argument("--report-path", type=Path, default=COMPLETENESS_FILE)
    completeness.add_argument("--strict", action="store_true", help="Exit non-zero if any canonical exam is incomplete.")

    extraction = subparsers.add_parser("dispatch-extraction", help="Build per-exam extraction work packets for vision reviewers.")
    extraction.add_argument("--question-bank-path", type=Path, default=QUESTION_BANK_FILE)

    auto_capture = subparsers.add_parser("auto-capture-missing", help="Use Gemini vision to extract missing questions from rendered PNG pages.")
    auto_capture.add_argument("--exam-id", action="append", default=[], help="Optional exam_id filter. Repeat to process multiple exams.")
    auto_capture.add_argument("--question-bank-path", type=Path, default=QUESTION_BANK_FILE)
    auto_capture.add_argument("--review-drop-dir", type=Path, default=REVIEW_DROP_DIR)
    auto_capture.add_argument("--model", default=SMART_GEMINI_AGENT)
    auto_capture.add_argument("--timeout-seconds", type=int, default=180)

    merge = subparsers.add_parser("merge-review-drop", help="Merge one agent-produced vision review file into the canonical question bank.")
    merge.add_argument("--input", type=Path, required=True, help="Path to one review-drop JSON file.")
    merge.add_argument("--question-bank-path", type=Path, default=QUESTION_BANK_FILE)

    dispatch = subparsers.add_parser("dispatch-evaluations", help="Build or refresh a resumable evaluation scaffold for one round.")
    dispatch.add_argument("--round", required=True, help="Round identifier, for example round1 or round2.")
    dispatch.add_argument("--question-bank-path", type=Path, default=QUESTION_BANK_FILE)
    dispatch.add_argument("--selectable-items-path", type=Path, default=SELECTABLE_ITEMS_FILE)
    dispatch.add_argument(
        "--findings",
        type=Path,
        action="append",
        default=[],
        help="Optional audit findings JSON files used to seed candidate exact-match snippet IDs.",
    )

    auto_evaluate = subparsers.add_parser("auto-evaluate", help="Use Gemini to fill first-pass snippet evaluations for captured questions.")
    auto_evaluate.add_argument("--round", required=True)
    auto_evaluate.add_argument("--model", default=FAST_GEMINI_AGENT)
    auto_evaluate.add_argument("--timeout-seconds", type=int, default=180)
    auto_evaluate.add_argument("--limit", type=int, default=0, help="Optional cap on number of questions to evaluate in this run.")
    auto_evaluate.add_argument("--selectable-items-path", type=Path, default=SELECTABLE_ITEMS_FILE)

    synth = subparsers.add_parser("synthesize-suggestions", help="Group suggested snippet edits/additions from one evaluation round.")
    synth.add_argument("--round", required=True)

    analytics = subparsers.add_parser("generate-ranking-analytics", help="Build analytics and a Markdown report for one evaluation round.")
    analytics.add_argument("--round", required=True)
    analytics.add_argument("--baseline-round", default="", help="Optional earlier round to compare against.")
    analytics.add_argument("--selectable-items-path", type=Path, default=SELECTABLE_ITEMS_FILE)

    review_packet = subparsers.add_parser("generate-review-packet", help="Build a human-friendly review packet for one evaluation round.")
    review_packet.add_argument("--round", required=True)
    review_packet.add_argument("--selectable-items-path", type=Path, default=SELECTABLE_ITEMS_FILE)

    validate = subparsers.add_parser("validate", help="Validate question-bank and evaluation snippet references.")
    validate.add_argument("--evaluation-round", default="", help="Optional evaluation round to validate.")
    validate.add_argument("--question-bank-path", type=Path, default=QUESTION_BANK_FILE)
    validate.add_argument("--selectable-items-path", type=Path, default=SELECTABLE_ITEMS_FILE)

    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    if args.command == "prepare-pages":
        payload = prepare_page_manifest(
            tmp_dir=args.tmp_dir,
            manifest_path=args.manifest_path,
            dpi=args.dpi,
            overwrite=args.overwrite,
        )
        print(json.dumps({"manifest_path": str(args.manifest_path), "exam_count": len(payload["exams"])}))
        return 0

    if args.command == "seed-question-bank":
        payload = seed_question_bank(
            question_bank_path=args.question_bank_path,
            page_manifest_path=args.page_manifest_path,
        )
        print(json.dumps({"question_bank_path": str(args.question_bank_path), "exam_count": len(payload["exams"])}))
        return 0

    if args.command == "audit-completeness":
        report = write_completeness_report(
            question_bank_path=args.question_bank_path,
            report_path=args.report_path,
        )
        print(json.dumps({"report_path": str(args.report_path), "overall_status": report["overall_status"]}))
        return 1 if args.strict and report["overall_status"] != "complete" else 0

    if args.command == "dispatch-extraction":
        payload = write_extraction_packets(question_bank_path=args.question_bank_path)
        print(json.dumps({"packet_count": payload["packet_count"]}))
        return 0

    if args.command == "auto-capture-missing":
        payload = auto_capture_missing_questions(
            exam_ids=args.exam_id,
            question_bank_path=args.question_bank_path,
            model=args.model,
            timeout_seconds=args.timeout_seconds,
        )
        print(json.dumps(payload, ensure_ascii=False))
        return 0

    if args.command == "merge-review-drop":
        payload = merge_review_drop(review_drop_path=args.input, question_bank_path=args.question_bank_path)
        print(json.dumps({"exam_id": payload["exam_id"], "present_questions": payload["review_tracking"]["present_questions"], "blocked_questions": payload["review_tracking"]["blocked_questions"]}))
        return 0

    if args.command == "dispatch-evaluations":
        if not args.selectable_items_path.exists():
            build_selectable_items_snapshot(output_path=args.selectable_items_path)
        payload = write_evaluation_scaffold(
            round_name=args.round,
            question_bank_path=args.question_bank_path,
            selectable_items_path=args.selectable_items_path,
            findings_paths=args.findings,
        )
        print(json.dumps({"evaluation_path": str(ROOT / "data" / "vision_exam_pipeline" / "evaluations" / f"{args.round}.json"), "question_count": len(payload["questions"])}))
        return 0

    if args.command == "auto-evaluate":
        if not args.selectable_items_path.exists():
            build_selectable_items_snapshot(output_path=args.selectable_items_path)
        payload = auto_evaluate_questions(
            round_name=args.round,
            model=args.model,
            timeout_seconds=args.timeout_seconds,
            limit=args.limit,
            selectable_items_path=args.selectable_items_path,
        )
        print(json.dumps(payload, ensure_ascii=False))
        return 0

    if args.command == "synthesize-suggestions":
        payload = synthesize_suggestions(round_name=args.round)
        print(json.dumps({"suggestion_count": payload["summary"]["suggestion_count"]}))
        return 0

    if args.command == "generate-ranking-analytics":
        if not args.selectable_items_path.exists():
            build_selectable_items_snapshot(output_path=args.selectable_items_path)
        payload = write_ranking_analytics(
            round_name=args.round,
            baseline_round=args.baseline_round,
            selectable_items_path=args.selectable_items_path,
        )
        print(json.dumps({"analytics_path": str(ROOT / "data" / "vision_exam_pipeline" / "analytics" / f"{args.round}.json"), "completed_evaluations": payload["summary"]["completed_evaluations"]}))
        return 0

    if args.command == "generate-review-packet":
        if not args.selectable_items_path.exists():
            build_selectable_items_snapshot(output_path=args.selectable_items_path)
        payload = write_review_packet(
            round_name=args.round,
            selectable_items_path=args.selectable_items_path,
        )
        print(json.dumps({"review_packet_path": str(ROOT / "data" / "vision_exam_pipeline" / "review_packets" / f"{args.round}.md"), "theme_count": payload["summary"]["theme_count"]}))
        return 0

    errors = validate_all(
        question_bank_path=args.question_bank_path,
        selectable_items_path=args.selectable_items_path,
        evaluation_round=args.evaluation_round,
    )
    if errors:
        print(json.dumps({"status": "fail", "errors": errors}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps({"status": "pass"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

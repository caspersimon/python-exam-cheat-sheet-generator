#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.shared import SMART_GEMINI_AGENT, SMART_GEMINI_AGENT_FALLBACK
from scripts.lib.gemini_test_protocol_utils import (
    _is_critical_gemini_failure,
    _read_json,
    _run_json_command,
    evaluate_hard_checks,
    report_path,
    run_gemini_checks,
)

DEFAULT_MODEL = SMART_GEMINI_AGENT
DEFAULT_FALLBACK_MODEL = SMART_GEMINI_AGENT_FALLBACK
DEFAULT_SMOKE_CMD = "make smoke-ui"
DEFAULT_STRESS_CMD = "make stress-layout-ui"
DEFAULT_CANVAS_CMD = "make export-canvas-guard-ui"
DEFAULT_FULL_CMD = "make full-ui"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run deterministic UI gates + Gemini micro-audits for screenshot/layout QA.")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--fallback-model", default=DEFAULT_FALLBACK_MODEL)
    parser.add_argument("--smoke-cmd", default=DEFAULT_SMOKE_CMD)
    parser.add_argument("--stress-cmd", default=DEFAULT_STRESS_CMD)
    parser.add_argument("--canvas-cmd", default=DEFAULT_CANVAS_CMD)
    parser.add_argument("--full-cmd", default=DEFAULT_FULL_CMD)
    parser.add_argument("--probe-json", type=Path, default=None)
    parser.add_argument("--stress-json", type=Path, default=None)
    parser.add_argument("--canvas-json", type=Path, default=None)
    parser.add_argument("--full-json", type=Path, default=None)
    parser.add_argument("--skip-gemini", action="store_true")
    parser.add_argument("--strict-gemini", action="store_true")
    parser.add_argument("--report-file", type=Path, default=None)
    parser.add_argument("--timeout-seconds", type=int, default=220)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    smoke = _read_json(args.probe_json) if args.probe_json else _run_json_command(args.smoke_cmd)
    stress = _read_json(args.stress_json) if args.stress_json else _run_json_command(args.stress_cmd)
    canvas = _read_json(args.canvas_json) if args.canvas_json else _run_json_command(args.canvas_cmd)
    full = _read_json(args.full_json) if args.full_json else _run_json_command(args.full_cmd)

    hard_checks = evaluate_hard_checks(smoke, stress, canvas, full)
    gemini_checks: list[dict[str, object]] = []
    if not args.skip_gemini:
        gemini_checks = run_gemini_checks(smoke, stress, canvas, full, args, hard_checks)

    hard_failures = [item for item in hard_checks if item["status"] == "fail"]
    gemini_failures = [item for item in gemini_checks if item["status"] == "fail"]
    gemini_critical_failures = [item for item in gemini_failures if _is_critical_gemini_failure(item)]

    release_gate_failed = bool(hard_failures or gemini_critical_failures)
    if args.strict_gemini and gemini_failures:
        release_gate_failed = True

    overall_status = "fail" if release_gate_failed else "warn" if gemini_failures else "pass"
    release_gate_status = "fail" if release_gate_failed else "pass"
    report = {
        "timestamp_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "models": {
            "primary": args.model,
            "fallback": args.fallback_model,
            "gemini_skipped": bool(args.skip_gemini),
            "strict_gemini": bool(args.strict_gemini),
        },
        "smoke_probe": smoke,
        "stress_probe": stress,
        "export_canvas_probe": canvas,
        "full_ui_probe": full,
        "hard_checks": hard_checks,
        "gemini_checks": gemini_checks,
        "summary": {
            "overall_status": overall_status,
            "release_gate_status": release_gate_status,
            "hard_failures": len(hard_failures),
            "gemini_failures": len(gemini_failures),
            "gemini_critical_failures": len(gemini_critical_failures),
            "smoke_source": str(args.probe_json) if args.probe_json else args.smoke_cmd,
            "stress_source": str(args.stress_json) if args.stress_json else args.stress_cmd,
            "full_source": str(args.full_json) if args.full_json else args.full_cmd,
        },
    }

    out_path = report_path(args.report_file)
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"overall_status": overall_status, "report_file": str(out_path)}, ensure_ascii=False))
    if release_gate_status != "pass":
        raise SystemExit(1)


if __name__ == "__main__":
    main()

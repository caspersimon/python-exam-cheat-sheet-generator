#!/usr/bin/env python3
"""Run lightweight Gemini capability benchmarks and write a dated report."""
from __future__ import annotations
import argparse
import ast
import json
import re
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from pipelines.shared import (  # noqa: E402
    FAST_GEMINI_AGENT,
    SMART_GEMINI_AGENT,
    extract_json_blob,
    run_gemini_cli,
)
DEFAULT_REPORT_FILE = ROOT / "data" / "test_reports" / "gemini_capability_benchmark.json"
DEFAULT_IMAGE = ROOT / "docs" / "assets" / "preview-editing-compact.png"
@dataclass(frozen=True)
class Case:
    case_id: str
    category: str
    prompt: str
    evaluator: Callable[[str], tuple[bool, str, dict[str, Any]]]
def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Gemini capability benchmark.")
    parser.add_argument(
        "--models",
        nargs="+",
        default=[FAST_GEMINI_AGENT, SMART_GEMINI_AGENT],
        help="Model IDs to benchmark.",
    )
    parser.add_argument("--timeout-seconds", type=int, default=120)
    parser.add_argument("--report-file", type=Path, default=DEFAULT_REPORT_FILE)
    parser.add_argument("--image-path", type=Path, default=DEFAULT_IMAGE)
    parser.add_argument("--strict", action="store_true", help="Exit non-zero when any case fails.")
    return parser.parse_args()
def _safe_json_blob(raw: str) -> dict[str, Any]:
    parsed = json.loads(extract_json_blob(raw))
    if not isinstance(parsed, dict):
        raise ValueError("Expected JSON object.")
    return parsed
def _eval_json_contract_1(raw: str) -> tuple[bool, str, dict[str, Any]]:
    data = _safe_json_blob(raw)
    ok = (
        set(data.keys()) == {"answer", "confidence", "tags"}
        and data.get("answer") == "ready"
        and isinstance(data.get("confidence"), (int, float))
        and 0 <= float(data["confidence"]) <= 1
        and data.get("tags") == ["alpha", "beta"]
    )
    return ok, "Strict JSON contract with fixed keys/values.", {"parsed": data}
def _eval_json_contract_2(raw: str) -> tuple[bool, str, dict[str, Any]]:
    data = _safe_json_blob(raw)
    ok = (
        set(data.keys()) == {"product", "classification", "notes"}
        and data.get("product") == 133
        and data.get("classification") in {"prime", "composite"}
        and isinstance(data.get("notes"), list)
        and len(data["notes"]) == 2
    )
    return ok, "Arithmetic+schema adherence under strict format.", {"parsed": data}
def _extract_code(raw: str) -> str:
    text = raw.strip()
    fence = re.search(r"```(?:python)?\s*(.*?)```", text, flags=re.DOTALL | re.IGNORECASE)
    if fence:
        text = fence.group(1).strip()
    return text
def _check_safe_code(code: str) -> None:
    lowered = code.lower()
    banned = ["import ", "open(", "__import__", "eval(", "exec(", "subprocess", "os."]
    for token in banned:
        if token in lowered:
            raise ValueError(f"Generated code contains banned token: {token}")
def _run_function_from_code(code: str, fn_name: str) -> Callable[..., Any]:
    _check_safe_code(code)
    ast.parse(code)
    scope: dict[str, Any] = {}
    exec(code, {}, scope)  # noqa: S102
    fn = scope.get(fn_name)
    if not callable(fn):
        raise ValueError(f"{fn_name} not found or not callable.")
    return fn
def _eval_function_normalize(raw: str) -> tuple[bool, str, dict[str, Any]]:
    code = _extract_code(raw)
    fn = _run_function_from_code(code, "normalize_topic_label")
    tests = [
        ("  dictionaries  ", "dictionary"),
        ("for_loops", "for loop"),
        ("TRY-EXCEPT", "try except"),
        ("class", "class"),
        ("lists", "list"),
        ("boss", "boss"),
    ]
    failures = []
    for source, expected in tests:
        got = fn(source)
        if got != expected:
            failures.append({"input": source, "expected": expected, "got": got})
    return not failures, "Function-writing from clear spec (normalize_topic_label).", {"failures": failures, "code": code}
def _eval_function_parse_int_csv(raw: str) -> tuple[bool, str, dict[str, Any]]:
    code = _extract_code(raw)
    fn = _run_function_from_code(code, "parse_int_csv")
    failures = []
    if fn("1, 2,3") != [1, 2, 3]:
        failures.append("basic_parse")
    if fn("4,, 5 ,") != [4, 5]:
        failures.append("ignore_empty")
    try:
        fn("1, two,3")
        failures.append("expected_value_error")
    except ValueError as exc:
        if "two" not in str(exc).lower():
            failures.append("error_message_missing_token")
    return not failures, "Function-writing from spec + edge cases (parse_int_csv).", {"failures": failures, "code": code}
def _eval_image_structured(raw: str) -> tuple[bool, str, dict[str, Any]]:
    data = _safe_json_blob(raw)
    density = str(data.get("overall_density", "")).lower()
    ok = (
        set(data.keys()) == {"has_header_controls", "has_card_resize_handles", "overall_density", "evidence"}
        and isinstance(data.get("has_header_controls"), bool)
        and isinstance(data.get("has_card_resize_handles"), bool)
        and density in {"low", "medium", "high"}
        and isinstance(data.get("evidence"), str)
        and len(data.get("evidence", "").strip()) >= 8
    )
    return ok, "Image understanding with strict structured output.", {"parsed": data}
def _eval_constraint_summary(raw: str) -> tuple[bool, str, dict[str, Any]]:
    data = _safe_json_blob(raw)
    bullets = data.get("bullets")
    ok = (
        set(data.keys()) == {"bullets"}
        and isinstance(bullets, list)
        and len(bullets) == 3
        and all(isinstance(item, str) and 1 <= len(item.split()) <= 8 for item in bullets)
    )
    return ok, "Constraint-heavy summarization into short bullets.", {"parsed": data}
def _build_cases(image_path: Path) -> list[Case]:
    return [
        Case(
            case_id="json_contract_ready",
            category="instruction_following",
            prompt=(
                "Return ONLY valid JSON, no markdown, no extra text.\n"
                'Exact keys: {"answer": string, "confidence": number, "tags": array}.\n'
                'Set answer="ready", confidence=0.82, tags=["alpha","beta"].'
            ),
            evaluator=_eval_json_contract_1,
        ),
        Case(
            case_id="json_contract_arithmetic",
            category="instruction_following",
            prompt=(
                "Return ONLY valid JSON with exact keys product, classification, notes.\n"
                "Compute 19*7 as product.\n"
                "classification must be prime/composite.\n"
                "notes must be exactly two short strings."
            ),
            evaluator=_eval_json_contract_2,
        ),
        Case(
            case_id="function_normalize_topic",
            category="code_generation",
            prompt=(
                "Write ONLY Python code (no markdown).\n"
                "Define function normalize_topic_label(text: str) -> str with this behavior:\n"
                "- lowercase\n- replace '_' and '-' with spaces\n- collapse spaces\n"
                "- if endswith 'ies' and len>4: replace by 'y'\n"
                "- elif endswith 's' and len>4 and not endswith 'ss': drop trailing 's'\n"
                "- return stripped result."
            ),
            evaluator=_eval_function_normalize,
        ),
        Case(
            case_id="function_parse_int_csv",
            category="code_generation",
            prompt=(
                "Write ONLY Python code (no markdown).\n"
                "Define function parse_int_csv(text: str) -> list[int]. Rules:\n"
                "- split by ','\n- trim each token\n- ignore empty tokens\n"
                "- parse integers\n- on first invalid token raise ValueError containing that token."
            ),
            evaluator=_eval_function_parse_int_csv,
        ),
        Case(
            case_id="vision_structured_layout",
            category="vision",
            prompt=(
                f"Analyze image @{image_path}.\n"
                "Return ONLY JSON with EXACT keys:\n"
                '{"has_header_controls": bool, "has_card_resize_handles": bool, '
                '"overall_density": "low|medium|high", "evidence": "short sentence"}'
            ),
            evaluator=_eval_image_structured,
        ),
        Case(
            case_id="constraint_summary",
            category="reasoning_formatting",
            prompt=(
                "Summarize this text as exactly three bullets, max 8 words each.\n"
                "Text: The app uses swipe selection, preview editing, generated PDF export, "
                "Gemini QA checks, and a maintenance audit to keep quality high.\n"
                "Return ONLY JSON with exact key bullets (array of 3 strings)."
            ),
            evaluator=_eval_constraint_summary,
        ),
    ]
def _run_case(model: str, case: Case, timeout_seconds: int) -> dict[str, Any]:
    started = time.perf_counter()
    status = "fail"
    detail = ""
    metadata: dict[str, Any] = {}
    error = ""
    raw = ""
    try:
        raw = run_gemini_cli(case.prompt, model=model, timeout_seconds=timeout_seconds, stderr_clip=1200)
        ok, detail, metadata = case.evaluator(raw)
        status = "pass" if ok else "fail"
    except Exception as exc:  # noqa: BLE001
        detail = "Execution/parsing error."
        error = str(exc)
    elapsed_ms = int((time.perf_counter() - started) * 1000)
    return {
        "case_id": case.case_id,
        "category": case.category,
        "status": status,
        "detail": detail,
        "latency_ms": elapsed_ms,
        "error": error,
        "metadata": metadata,
        "raw_output_excerpt": raw[:500],
    }
def _summarize(model_results: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(model_results)
    passed = sum(1 for item in model_results if item["status"] == "pass")
    by_category: dict[str, dict[str, int]] = {}
    for item in model_results:
        cat = item["category"]
        entry = by_category.setdefault(cat, {"total": 0, "passed": 0})
        entry["total"] += 1
        if item["status"] == "pass":
            entry["passed"] += 1
    return {"total": total, "passed": passed, "pass_rate": round((passed / total) if total else 0.0, 4), "by_category": by_category}
def main() -> int:
    args = _parse_args()
    if not args.image_path.exists():
        raise SystemExit(f"Image path missing: {args.image_path}")
    cases = _build_cases(args.image_path)
    models_payload: dict[str, Any] = {}
    any_fail = False
    for model in args.models:
        results = [_run_case(model, case, args.timeout_seconds) for case in cases]
        summary = _summarize(results)
        models_payload[model] = {"summary": summary, "results": results}
        if summary["passed"] < summary["total"]:
            any_fail = True
    report = {
        "timestamp_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "models": args.models,
        "cases_total": len(cases),
        "cases": [{"case_id": c.case_id, "category": c.category} for c in cases],
        "results_by_model": models_payload,
    }
    args.report_file.parent.mkdir(parents=True, exist_ok=True)
    args.report_file.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"report_file": str(args.report_file), "models": args.models, "any_fail": any_fail}, ensure_ascii=False))
    return 1 if (args.strict and any_fail) else 0
if __name__ == "__main__":
    raise SystemExit(main())

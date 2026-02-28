#!/usr/bin/env python3
"""Prompt-variant experiments for Gemini code-generation delegation."""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.shared import (  # noqa: E402
    FAST_GEMINI_AGENT,
    FAST_GEMINI_AGENT_FALLBACK,
    run_gemini_cli,
)

DEFAULT_REPORT = ROOT / "data" / "test_reports" / "gemini_prompt_experiments.json"

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run prompt-variant experiments for Gemini code generation.")
    parser.add_argument("--models", nargs="+", default=[FAST_GEMINI_AGENT], help="Requested model IDs.")
    parser.add_argument("--fallback-model", default=FAST_GEMINI_AGENT_FALLBACK)
    parser.add_argument("--trials", type=int, default=5)
    parser.add_argument("--retries", type=int, default=2, help="Retries per model for API/transient failures.")
    parser.add_argument("--timeout-seconds", type=int, default=140)
    parser.add_argument("--report-file", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--strict", action="store_true", help="Exit non-zero when any variant has < 80% pass-rate.")
    return parser.parse_args()

def _extract_code(raw: str) -> str:
    text = raw.strip()
    fence = re.search(r"```(?:python)?\s*(.*?)```", text, flags=re.DOTALL | re.IGNORECASE)
    if fence:
        text = fence.group(1).strip()
    return text

def _check_safe_code(code: str) -> None:
    lowered = code.lower()
    banned = ("import ", "open(", "__import__", "eval(", "exec(", "subprocess", "os.")
    for token in banned:
        if token in lowered:
            raise ValueError(f"banned_token:{token}")

def _run_function_from_code(code: str, fn_name: str) -> Callable[..., Any]:
    _check_safe_code(code)
    ast.parse(code)
    scope: dict[str, Any] = {}
    exec(code, {}, scope)  # noqa: S102
    fn = scope.get(fn_name)
    if not callable(fn):
        raise ValueError("missing_function")
    return fn

def _eval_normalize_topic_label(raw: str) -> tuple[bool, str, dict[str, Any]]:
    code = _extract_code(raw)
    fn = _run_function_from_code(code, "normalize_topic_label")
    tests = [
        ("  dictionaries  ", "dictionary"),
        ("for_loops", "for loop"),
        ("TRY-EXCEPT", "try except"),
        ("lists", "list"),
        ("boss", "boss"),
    ]
    failures = [{"input": src, "expected": exp, "got": fn(src)} for src, exp in tests if fn(src) != exp]
    if failures:
        return False, "behavior_mismatch", {"failure_kind": "behavior_mismatch", "failures": failures, "code": code}
    return True, "pass", {"code": code}

def _eval_parse_int_csv(raw: str) -> tuple[bool, str, dict[str, Any]]:
    code = _extract_code(raw)
    fn = _run_function_from_code(code, "parse_int_csv")
    failures: list[str] = []
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
    if failures:
        return False, "behavior_mismatch", {"failure_kind": "behavior_mismatch", "failures": failures, "code": code}
    return True, "pass", {"code": code}

def _tasks() -> list[dict[str, Any]]:
    return [
        {
            "task_id": "normalize_topic_label",
            "function_name": "normalize_topic_label",
            "spec": (
                "Define normalize_topic_label(text: str) -> str.\n"
                "Rules: lowercase; replace '_' and '-' with spaces; collapse repeated spaces; strip.\n"
                "Plural handling: if endswith 'ies' and len>4 -> replace with 'y'; "
                "elif endswith 's' and len>4 and not endswith 'ss' -> drop trailing 's'."
            ),
            "evaluator": _eval_normalize_topic_label,
        },
        {
            "task_id": "parse_int_csv",
            "function_name": "parse_int_csv",
            "spec": (
                "Define parse_int_csv(text: str) -> list[int].\n"
                "Rules: split by ',', trim tokens, ignore empty tokens, parse integers.\n"
                "On first invalid token raise ValueError and include that token in message."
            ),
            "evaluator": _eval_parse_int_csv,
        },
    ]

def _variants() -> list[dict[str, str]]:
    return [
        {
            "variant_id": "v1_minimal",
            "instruction": "Write Python code for the following task.",
        },
        {
            "variant_id": "v2_strict_output",
            "instruction": (
                "Return ONLY raw Python code, no markdown, no explanation.\n"
                "Do NOT use imports.\n"
                "Define exactly one top-level function with the required name."
            ),
        },
        {
            "variant_id": "v3_strict_with_examples",
            "instruction": (
                "Return ONLY raw Python code, no markdown, no explanation.\n"
                "Do NOT use imports.\n"
                "Define exactly one top-level function with the required name.\n"
                "Before final answer, silently self-check against examples:\n"
                "- normalize_topic_label('for_loops') -> 'for loop'\n"
                "- parse_int_csv('4,, 5 ,') -> [4, 5]"
            ),
        },
    ]

def _build_prompt(task: dict[str, Any], variant: dict[str, str]) -> str:
    return (
        f"{variant['instruction']}\n\n"
        f"Function name must be exactly: {task['function_name']}\n\n"
        f"Task:\n{task['spec']}"
    )

def _classify_error(exc: Exception) -> str:
    text = str(exc).lower()
    if "timed out" in text:
        return "timeout"
    if "quota" in text or "exhausted your capacity" in text:
        return "quota"
    if "banned_token" in text:
        return "banned_token"
    if "missing_function" in text:
        return "missing_function"
    if "syntaxerror" in text:
        return "syntax_error"
    if "gemini failed" in text:
        return "gemini_api_error"
    return "unknown_error"

def _call_with_retries(prompt: str, chain: list[str], timeout_seconds: int, retries: int) -> tuple[str, str]:
    last_exc: Exception | None = None
    for model in chain:
        for _ in range(max(1, retries)):
            try:
                return run_gemini_cli(prompt, model=model, timeout_seconds=timeout_seconds, stderr_clip=900), model
            except Exception as exc:  # noqa: BLE001
                last_exc = exc
    raise RuntimeError(str(last_exc or "unknown error"))

def _summarize(results: list[dict[str, Any]]) -> dict[str, Any]:
    grouped: dict[str, dict[str, list[dict[str, Any]]]] = {}
    for row in results:
        grouped.setdefault(row["model_requested"], {}).setdefault(row["task_id"], []).append(row)
    payload: dict[str, Any] = {}
    for model, by_task in grouped.items():
        model_summary: dict[str, Any] = {"tasks": {}, "recommendations": {}}
        for task_id, rows in by_task.items():
            variants: dict[str, dict[str, Any]] = {}
            for row in rows:
                entry = variants.setdefault(row["variant_id"], {"total": 0, "passed": 0, "latencies": [], "failures": {}})
                entry["total"] += 1
                if row["status"] == "pass":
                    entry["passed"] += 1
                entry["latencies"].append(int(row["latency_ms"]))
                if row["status"] != "pass":
                    key = row.get("failure_kind", "unknown")
                    entry["failures"][key] = entry["failures"].get(key, 0) + 1
            variant_rows: list[dict[str, Any]] = []
            for variant_id, item in variants.items():
                total = item["total"]
                passed = item["passed"]
                avg_latency = round(sum(item["latencies"]) / total, 2) if total else 0.0
                variant_rows.append(
                    {
                        "variant_id": variant_id,
                        "total": total,
                        "passed": passed,
                        "pass_rate": round((passed / total) if total else 0.0, 4),
                        "avg_latency_ms": avg_latency,
                        "failures": item["failures"],
                    }
                )
            best = sorted(
                variant_rows,
                key=lambda row: (
                    float(row.get("pass_rate", 0.0)),
                    int(row.get("passed", 0)),
                    -float(row.get("avg_latency_ms", 10**9)),
                ),
                reverse=True,
            )[0]
            model_summary["tasks"][task_id] = variant_rows
            model_summary["recommendations"][task_id] = best
        payload[model] = model_summary
    return payload

def main() -> int:
    args = _parse_args()
    tasks = _tasks()
    variants = _variants()
    results: list[dict[str, Any]] = []
    for model_requested in args.models:
        chain = [model_requested]
        if args.fallback_model and args.fallback_model not in chain:
            chain.append(args.fallback_model)
        for task in tasks:
            for variant in variants:
                prompt = _build_prompt(task, variant)
                for trial in range(1, max(1, args.trials) + 1):
                    started = time.perf_counter()
                    raw = ""
                    status = "fail"
                    failure_kind = ""
                    detail = ""
                    error = ""
                    model_used = ""
                    metadata: dict[str, Any] = {}
                    try:
                        raw, model_used = _call_with_retries(prompt, chain, args.timeout_seconds, args.retries)
                        evaluator: Callable[[str], tuple[bool, str, dict[str, Any]]] = task["evaluator"]
                        ok, detail, metadata = evaluator(raw)
                        status = "pass" if ok else "fail"
                        failure_kind = "" if ok else str(metadata.get("failure_kind") or detail or "behavior_mismatch")
                    except Exception as exc:  # noqa: BLE001
                        error = str(exc)
                        failure_kind = _classify_error(exc)
                        detail = "execution_or_parsing_error"
                    elapsed_ms = int((time.perf_counter() - started) * 1000)
                    results.append(
                        {
                            "model_requested": model_requested,
                            "model_used": model_used or model_requested,
                            "task_id": str(task["task_id"]),
                            "variant_id": str(variant["variant_id"]),
                            "trial": trial,
                            "status": status,
                            "failure_kind": failure_kind,
                            "detail": detail,
                            "latency_ms": elapsed_ms,
                            "error": error,
                            "metadata": metadata,
                            "raw_output_excerpt": raw[:500],
                        }
                    )
    summary = _summarize(results)
    report = {
        "timestamp_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "models": args.models,
        "fallback_model": args.fallback_model,
        "trials": max(1, args.trials),
        "retries": max(1, args.retries),
        "results": results,
        "summary_by_model": summary,
    }
    args.report_file.parent.mkdir(parents=True, exist_ok=True)
    args.report_file.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    low_confidence = any(
        rec["pass_rate"] < 0.8
        for model_data in summary.values()
        for rec in model_data.get("recommendations", {}).values()
    )
    print(json.dumps({"report_file": str(args.report_file), "models": args.models, "low_confidence": low_confidence}))
    return 1 if args.strict and low_confidence else 0


if __name__ == "__main__":
    raise SystemExit(main())

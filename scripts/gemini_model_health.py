#!/usr/bin/env python3
"""Gemini model health checks for proactive task routing."""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.shared import (  # noqa: E402
    FAST_GEMINI_AGENT,
    FAST_GEMINI_AGENT_FALLBACK,
    SMART_GEMINI_AGENT,
    SMART_GEMINI_AGENT_FALLBACK,
    extract_json_blob,
    run_gemini_cli,
)

DEFAULT_REPORT = ROOT / "data" / "test_reports" / "gemini_model_health.json"
HEALTH_PROMPT = (
    "Return ONLY valid JSON with exact keys: status, pong.\n"
    'Set status="ok" and pong=true.'
)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Probe Gemini model availability and basic contract-following.")
    parser.add_argument(
        "--models",
        nargs="+",
        default=[FAST_GEMINI_AGENT, SMART_GEMINI_AGENT, FAST_GEMINI_AGENT_FALLBACK, SMART_GEMINI_AGENT_FALLBACK],
        help="Model IDs to probe.",
    )
    parser.add_argument("--timeout-seconds", type=int, default=40)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--report-file", type=Path, default=DEFAULT_REPORT)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero when any requested model is unavailable.",
    )
    parser.add_argument(
        "--strict-fast",
        action="store_true",
        help="Exit non-zero when FAST_GEMINI_AGENT is unavailable.",
    )
    return parser.parse_args()


def classify_error(error_text: str) -> str:
    text = (error_text or "").lower()
    if "timed out" in text:
        return "timeout"
    if "quota" in text or "exhausted your capacity" in text:
        return "quota"
    if "unauthorized" in text or "permission denied" in text or "invalid api key" in text:
        return "auth"
    if "network" in text or "connection" in text:
        return "network"
    if "gemini failed" in text:
        return "api_error"
    return "unknown_error"


def parse_probe_json(raw: str) -> tuple[bool, str]:
    try:
        payload = json.loads(extract_json_blob(raw))
    except Exception:  # noqa: BLE001
        return False, "invalid_json"
    if not isinstance(payload, dict):
        return False, "not_object"
    if payload.get("status") != "ok":
        return False, "bad_status_field"
    if payload.get("pong") is not True:
        return False, "bad_pong_field"
    return True, "ok"


def check_model(model: str, timeout_seconds: int, retries: int) -> dict[str, Any]:
    attempts = 0
    last_error = ""
    last_kind = ""
    for _ in range(max(1, retries)):
        attempts += 1
        started = time.perf_counter()
        try:
            raw = run_gemini_cli(
                HEALTH_PROMPT,
                model=model,
                timeout_seconds=timeout_seconds,
                stderr_clip=800,
            )
            ok, reason = parse_probe_json(raw)
            latency = int((time.perf_counter() - started) * 1000)
            if ok:
                return {
                    "model": model,
                    "status": "available",
                    "attempts": attempts,
                    "latency_ms": latency,
                    "error_kind": "",
                    "detail": "ok",
                }
            last_error = reason
            last_kind = "invalid_response"
        except Exception as exc:  # noqa: BLE001
            last_error = str(exc)
            last_kind = classify_error(last_error)
    return {
        "model": model,
        "status": "unavailable",
        "attempts": attempts,
        "latency_ms": 0,
        "error_kind": last_kind,
        "detail": last_error[:500],
    }


def summarize(results: list[dict[str, Any]]) -> dict[str, Any]:
    available = [item for item in results if item["status"] == "available"]
    unavailable = [item for item in results if item["status"] != "available"]
    error_kinds: dict[str, int] = {}
    for item in unavailable:
        key = item.get("error_kind") or "unknown_error"
        error_kinds[key] = error_kinds.get(key, 0) + 1
    recommended_primary = FAST_GEMINI_AGENT if any(item["model"] == FAST_GEMINI_AGENT for item in available) else ""
    if not recommended_primary and available:
        recommended_primary = str(available[0]["model"])
    return {
        "requested": len(results),
        "available": len(available),
        "unavailable": len(unavailable),
        "error_kinds": error_kinds,
        "recommended_primary": recommended_primary,
        "recommended_fallback": FAST_GEMINI_AGENT_FALLBACK if any(item["model"] == FAST_GEMINI_AGENT_FALLBACK for item in available) else "",
    }


def _unique_models(models: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for model in models:
        if model not in seen:
            seen.add(model)
            ordered.append(model)
    return ordered


def main() -> int:
    args = _parse_args()
    models = _unique_models(args.models)
    results = [check_model(model, args.timeout_seconds, args.retries) for model in models]
    summary = summarize(results)
    report = {
        "timestamp_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "aliases": {
            "fast_gemini_agent": FAST_GEMINI_AGENT,
            "smart_gemini_agent": SMART_GEMINI_AGENT,
            "fast_fallback": FAST_GEMINI_AGENT_FALLBACK,
            "smart_fallback": SMART_GEMINI_AGENT_FALLBACK,
        },
        "requested_models": models,
        "results": results,
        "summary": summary,
    }
    args.report_file.parent.mkdir(parents=True, exist_ok=True)
    args.report_file.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    fast_ok = any(item["model"] == FAST_GEMINI_AGENT and item["status"] == "available" for item in results)
    any_fail = any(item["status"] != "available" for item in results)
    print(
        json.dumps(
            {
                "report_file": str(args.report_file),
                "available": summary["available"],
                "requested": summary["requested"],
                "recommended_primary": summary["recommended_primary"],
            },
            ensure_ascii=False,
        )
    )
    if args.strict_fast and not fast_ok:
        return 1
    if args.strict and any_fail:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Aggregate maintenance and Gemini QA reports into one project-health dashboard."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT / "data" / "test_reports" / "quality_dashboard.json"
SOURCE_FILES = {
    "maintenance_audit": ROOT / "data" / "test_reports" / "maintenance_audit.json",
    "gemini_model_health": ROOT / "data" / "test_reports" / "gemini_model_health.json",
    "gemini_capability_benchmark": ROOT / "data" / "test_reports" / "gemini_capability_benchmark.json",
    "gemini_prompt_experiments": ROOT / "data" / "test_reports" / "gemini_prompt_experiments.json",
    "gemini_ui_test_report": ROOT / "data" / "test_reports" / "gemini_ui_test_report.json",
}


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a project quality dashboard from existing reports.")
    parser.add_argument("--report-file", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--max-age-hours", type=float, default=72.0)
    parser.add_argument("--strict", action="store_true", help="Exit non-zero when dashboard status is fail or warn.")
    return parser.parse_args()


def _check_result(
    check_id: str,
    status: str,
    summary: str,
    metric: Any = None,
    findings: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    return {
        "check_id": check_id,
        "status": status,
        "summary": summary,
        "metric": metric,
        "findings": findings or [],
    }


def parse_timestamp_utc(value: str) -> datetime | None:
    text = (value or "").strip()
    if not text:
        return None
    try:
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        return datetime.fromisoformat(text).astimezone(timezone.utc)
    except ValueError:
        return None


def load_json(path: Path) -> tuple[dict[str, Any] | None, str]:
    if not path.exists():
        return None, "missing"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return None, f"parse_error:{exc}"
    if not isinstance(payload, dict):
        return None, "not_object"
    return payload, ""


def freshness_check(name: str, payload: dict[str, Any], max_age_hours: float, now_utc: datetime) -> dict[str, Any]:
    ts = parse_timestamp_utc(str(payload.get("timestamp_utc") or ""))
    if ts is None:
        return _check_result(f"{name}_freshness", "warn", "Missing/invalid timestamp_utc.")
    age_hours = round((now_utc - ts).total_seconds() / 3600.0, 2)
    if age_hours > max_age_hours:
        return _check_result(
            f"{name}_freshness",
            "warn",
            f"Report is stale ({age_hours}h old).",
            {"age_hours": age_hours, "max_age_hours": max_age_hours},
        )
    return _check_result(
        f"{name}_freshness",
        "pass",
        "Report freshness is within threshold.",
        {"age_hours": age_hours, "max_age_hours": max_age_hours},
    )


def check_maintenance(payload: dict[str, Any]) -> dict[str, Any]:
    status = str(payload.get("overall_status") or "warn").lower()
    if status == "fail":
        return _check_result("maintenance_audit_status", "fail", "Maintenance audit failing.")
    if status == "warn":
        checks = payload.get("checks") if isinstance(payload.get("checks"), list) else []
        warn_checks = [item for item in checks if isinstance(item, dict) and str(item.get("status") or "").lower() == "warn"]
        non_soft = [item for item in warn_checks if str(item.get("check_id") or "") != "line_lengths"]
        if non_soft:
            return _check_result("maintenance_audit_status", "warn", "Maintenance audit has non-soft warnings.", findings=non_soft)
        line_lengths = next((item for item in warn_checks if str(item.get("check_id") or "") == "line_lengths"), None)
        soft_count = len((line_lengths or {}).get("findings") or [])
        return _check_result(
            "maintenance_audit_status",
            "pass",
            "Maintenance warnings are soft line-length advisories only.",
            {"soft_line_length_findings": soft_count},
        )
    return _check_result("maintenance_audit_status", "pass", "Maintenance audit is green.")


def check_model_health(payload: dict[str, Any]) -> dict[str, Any]:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    available = int(summary.get("available") or 0)
    requested = int(summary.get("requested") or 0)
    recommended = str(summary.get("recommended_primary") or "")
    if available <= 0:
        return _check_result("gemini_model_health_status", "fail", "No Gemini model is currently available.", summary)
    if not recommended:
        return _check_result("gemini_model_health_status", "warn", "No recommended primary model found.", summary)
    if available < requested:
        return _check_result("gemini_model_health_status", "pass", "Some requested models are unavailable, but a primary model is available.", summary)
    return _check_result("gemini_model_health_status", "pass", "Gemini model health is good.", summary)


def check_benchmark(payload: dict[str, Any]) -> dict[str, Any]:
    results = payload.get("results_by_model") if isinstance(payload.get("results_by_model"), dict) else {}
    if not results:
        return _check_result("gemini_capability_status", "warn", "Capability benchmark missing results_by_model.")
    findings: list[dict[str, Any]] = []
    best_fast_rate = None
    for model, detail in results.items():
        summary = detail.get("summary") if isinstance(detail, dict) else {}
        rate = float(summary.get("pass_rate") or 0.0)
        findings.append({"model": model, "pass_rate": rate})
        if "flash" in model:
            best_fast_rate = rate if best_fast_rate is None else max(best_fast_rate, rate)
    if best_fast_rate is None:
        return _check_result("gemini_capability_status", "warn", "No fast model benchmark result found.", None, findings)
    if best_fast_rate < 0.6:
        return _check_result("gemini_capability_status", "fail", "Fast model benchmark pass rate is too low.", None, findings)
    if best_fast_rate < 0.8:
        return _check_result("gemini_capability_status", "warn", "Fast model benchmark pass rate is moderate.", None, findings)
    return _check_result("gemini_capability_status", "pass", "Fast model benchmark pass rate is strong.", None, findings)


def check_prompt_experiments(payload: dict[str, Any]) -> dict[str, Any]:
    summary_by_model = payload.get("summary_by_model") if isinstance(payload.get("summary_by_model"), dict) else {}
    if not summary_by_model:
        return _check_result("gemini_prompt_experiments_status", "warn", "Prompt experiments missing summary_by_model.")
    weak: list[dict[str, Any]] = []
    for model, model_data in summary_by_model.items():
        recommendations = model_data.get("recommendations") if isinstance(model_data, dict) else {}
        if not isinstance(recommendations, dict):
            continue
        for task_id, rec in recommendations.items():
            rate = float(rec.get("pass_rate") or 0.0)
            if rate < 0.8:
                weak.append({"model": model, "task_id": task_id, "pass_rate": rate, "variant": rec.get("variant_id")})
    if weak:
        return _check_result(
            "gemini_prompt_experiments_status",
            "warn",
            "Some recommended prompt variants are below reliability threshold.",
            None,
            weak,
        )
    return _check_result("gemini_prompt_experiments_status", "pass", "Prompt experiments recommend reliable variants.")


def check_ui_protocol(payload: dict[str, Any]) -> dict[str, Any]:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    status = str(summary.get("overall_status") or "").lower()
    release_gate = str(summary.get("release_gate_status") or "").lower()
    if release_gate == "fail":
        return _check_result("gemini_ui_protocol_status", "fail", "Gemini UI release gate failed.", summary)
    if status in {"pass", "warn", "fail"}:
        if int(summary.get("gemini_failures") or 0) > 0:
            return _check_result("gemini_ui_protocol_status", "pass", "Gemini UI advisory checks reported issues; deterministic gate passed.", summary)
        return _check_result("gemini_ui_protocol_status", "pass", "Gemini UI protocol is green.", summary)
    return _check_result("gemini_ui_protocol_status", "warn", "Gemini UI protocol status unknown.", summary)


def build_dashboard(max_age_hours: float, now_utc: datetime | None = None) -> dict[str, Any]:
    now = now_utc or datetime.now(timezone.utc)
    checks: list[dict[str, Any]] = []
    sources: dict[str, dict[str, Any]] = {}
    for name, path in SOURCE_FILES.items():
        payload, error = load_json(path)
        sources[name] = {"path": str(path), "loaded": bool(payload), "error": error}
        if payload is None:
            checks.append(_check_result(f"{name}_presence", "warn", f"Missing/invalid source: {name}.", {"error": error}))
            continue
        checks.append(freshness_check(name, payload, max_age_hours, now))
        if name == "maintenance_audit":
            checks.append(check_maintenance(payload))
        elif name == "gemini_model_health":
            checks.append(check_model_health(payload))
        elif name == "gemini_capability_benchmark":
            checks.append(check_benchmark(payload))
        elif name == "gemini_prompt_experiments":
            checks.append(check_prompt_experiments(payload))
        elif name == "gemini_ui_test_report":
            checks.append(check_ui_protocol(payload))
    failures = [item for item in checks if item["status"] == "fail"]
    warnings = [item for item in checks if item["status"] == "warn"]
    overall = "fail" if failures else "warn" if warnings else "pass"
    suggested_actions = []
    if any(item["check_id"] == "gemini_model_health_status" and item["status"] != "pass" for item in checks):
        suggested_actions.append("Run make gemini-health and route tasks to the recommended available model.")
    if any(item["check_id"] == "gemini_capability_status" and item["status"] != "pass" for item in checks):
        suggested_actions.append("Run make gemini-benchmark and refresh prompt constraints for weak cases.")
    if any(item["check_id"] == "gemini_prompt_experiments_status" and item["status"] != "pass" for item in checks):
        suggested_actions.append("Run make gemini-prompt-experiments and update delegated prompt templates.")
    if any(item["check_id"] == "gemini_ui_protocol_status" and item["status"] == "fail" for item in checks):
        suggested_actions.append("Run make gemini-ui-protocol and resolve deterministic hard-gate failures first.")
    return {
        "timestamp_utc": now.replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "max_age_hours": max_age_hours,
        "sources": sources,
        "checks": checks,
        "summary": {
            "overall_status": overall,
            "failures": len(failures),
            "warnings": len(warnings),
            "suggested_actions": suggested_actions,
        },
    }


def main() -> int:
    args = _parse_args()
    report = build_dashboard(args.max_age_hours)
    args.report_file.parent.mkdir(parents=True, exist_ok=True)
    args.report_file.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"report_file": str(args.report_file), "overall_status": report["summary"]["overall_status"]}))
    if args.strict and report["summary"]["overall_status"] != "pass":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

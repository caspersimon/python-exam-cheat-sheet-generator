#!/usr/bin/env python3
"""Repository maintenance audit for leave-it-better workflows."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.check_file_lengths import count_lines, iter_code_files

DEFAULT_REPORT = ROOT / "data" / "test_reports" / "maintenance_audit.json"
TODO_PATTERN = re.compile(r"\b(TODO|FIXME|HACK|XXX)\b")
MODEL_LITERAL_PATTERN = re.compile(r"gemini-\d(?:\.\d+)?-[A-Za-z0-9.-]+")


def _norm_text(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip()).lower()


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


def _marker_is_in_comment(line: str, marker_start: int) -> bool:
    return any(token in line[:marker_start] for token in ("#", "//", "/*", "<!--"))


def _marker_looks_inside_string(line: str, marker_start: int) -> bool:
    prefix = line[:marker_start]
    # Coarse heuristic: odd quote count before marker usually means marker is in a string literal.
    return prefix.count('"') % 2 == 1 or prefix.count("'") % 2 == 1


def audit_line_lengths(root: Path, soft_limit: int, hard_limit: int) -> dict[str, Any]:
    soft_hits: list[dict[str, Any]] = []
    hard_hits: list[dict[str, Any]] = []
    largest: list[tuple[Path, int]] = []
    for file_path in iter_code_files(root):
        line_count = count_lines(file_path)
        rel = str(file_path.relative_to(root))
        largest.append((file_path, line_count))
        if line_count > hard_limit:
            hard_hits.append({"path": rel, "line_count": line_count})
        elif line_count > soft_limit:
            soft_hits.append({"path": rel, "line_count": line_count})
    top_largest = [
        {"path": str(path.relative_to(root)), "line_count": count}
        for path, count in sorted(largest, key=lambda item: item[1], reverse=True)[:10]
    ]
    metric = {"soft_limit": soft_limit, "hard_limit": hard_limit, "largest": top_largest}
    if hard_hits:
        return _check_result(
            "line_lengths",
            "fail",
            f"{len(hard_hits)} files exceed hard limit {hard_limit}.",
            metric,
            hard_hits + soft_hits,
        )
    if soft_hits:
        return _check_result(
            "line_lengths",
            "warn",
            f"{len(soft_hits)} files exceed soft limit {soft_limit}.",
            metric,
            soft_hits,
        )
    return _check_result("line_lengths", "pass", "All code files are within soft line-length target.", metric)


def audit_todo_markers(root: Path) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    for file_path in iter_code_files(root):
        rel = str(file_path.relative_to(root))
        with file_path.open("r", encoding="utf-8", errors="ignore") as handle:
            for idx, line in enumerate(handle, start=1):
                match = TODO_PATTERN.search(line)
                if not match or not _marker_is_in_comment(line, match.start()):
                    continue
                if _marker_looks_inside_string(line, match.start()):
                    continue
                findings.append({"path": rel, "line": idx, "marker": match.group(1), "text": line.strip()[:160]})
                if len(findings) >= 40:
                    break
        if len(findings) >= 40:
            break
    if findings:
        return _check_result(
            "todo_markers",
            "warn",
            f"Found {len(findings)} TODO/FIXME/HACK/XXX markers.",
            len(findings),
            findings,
        )
    return _check_result("todo_markers", "pass", "No TODO/FIXME/HACK/XXX markers found.", 0)


def audit_topic_cards_quality(root: Path) -> dict[str, Any]:
    topic_cards_path = root / "topic_cards.json"
    if not topic_cards_path.exists():
        return _check_result("topic_cards_quality", "fail", "topic_cards.json missing.")
    payload = json.loads(topic_cards_path.read_text(encoding="utf-8"))
    cards = payload.get("cards", [])
    key_points_map: dict[str, list[str]] = {}
    examples_map: dict[str, list[str]] = {}
    for card in cards:
        card_id = str(card.get("id") or "")
        sections = card.get("sections", {})
        for item in sections.get("key_points_to_remember", []):
            text = _norm_text(str(item.get("text") or ""))
            if text:
                key_points_map.setdefault(text, []).append(card_id)
        for ex in sections.get("ai_examples", []):
            code = _norm_text(str(ex.get("code") or ""))
            if code:
                examples_map.setdefault(code, []).append(card_id)
    duplicate_kp = [{"value": text[:180], "card_ids": ids} for text, ids in key_points_map.items() if len(set(ids)) > 1]
    duplicate_examples = [
        {"value": code[:180], "card_ids": ids} for code, ids in examples_map.items() if len(set(ids)) > 1
    ]
    findings: list[dict[str, Any]] = []
    if duplicate_kp:
        findings.append({"kind": "duplicate_key_points", "count": len(duplicate_kp), "samples": duplicate_kp[:5]})
    if duplicate_examples:
        findings.append(
            {"kind": "duplicate_ai_examples", "count": len(duplicate_examples), "samples": duplicate_examples[:5]}
        )
    if findings:
        return _check_result("topic_cards_quality", "warn", "Potential duplicate topic-card content found.", None, findings)
    return _check_result("topic_cards_quality", "pass", "No cross-card duplicates detected for key points/examples.")


def audit_study_db(root: Path) -> dict[str, Any]:
    study_db_path = root / "data" / "study_db.json"
    if not study_db_path.exists():
        return _check_result("study_db", "fail", "data/study_db.json missing.")
    payload = json.loads(study_db_path.read_text(encoding="utf-8"))
    weeks = payload.get("weeks", [])
    week_numbers = [week.get("week_number") for week in weeks]
    if any(number is None for number in week_numbers):
        week_numbers = [week.get("week") for week in weeks]
    sorted_unique = sorted(set(week_numbers))
    missing_sources: list[dict[str, Any]] = []
    for week in weeks:
        week_no = week.get("week_number", week.get("week"))
        for source in week.get("sources", []):
            source_path = source if isinstance(source, str) else source.get("path")
            if source_path and not (root / source_path).exists():
                missing_sources.append({"week_number": week_no, "path": source_path})
    findings: list[dict[str, Any]] = []
    status = "pass"
    if week_numbers != sorted_unique:
        status = "fail"
        findings.append({"kind": "week_order_or_duplicates", "week_numbers": week_numbers})
    if missing_sources:
        status = "fail"
        findings.append({"kind": "missing_sources", "count": len(missing_sources), "samples": missing_sources[:10]})
    summary = "Study DB structure health looks good." if status == "pass" else "Study DB has structural issues."
    return _check_result("study_db", status, summary, {"week_count": len(weeks)}, findings)


def audit_docs_system(root: Path) -> dict[str, Any]:
    required = [
        "AGENTS.md",
        "README.md",
        "docs/TESTING.md",
        "docs/ARCHITECTURE.md",
        "docs/MAINTENANCE_PROTOCOL.md",
        "docs/GEMINI_PLAYBOOK.md",
        "docs/ROADMAP.md",
        "docs/specs/SPEC_TEMPLATE.md",
    ]
    missing = [path for path in required if not (root / path).exists()]
    if missing:
        return _check_result(
            "docs_system",
            "fail",
            "Maintenance/system docs missing.",
            len(missing),
            [{"path": path} for path in missing],
        )
    return _check_result("docs_system", "pass", "Maintenance/system docs present.", len(required))


def find_hardcoded_model_literals(root: Path) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    allowed_file = root / "pipelines" / "shared" / "model_defaults.py"
    for search_root in (root / "scripts", root / "pipelines"):
        if not search_root.exists():
            continue
        for file_path in sorted(search_root.rglob("*.py")):
            if file_path == allowed_file:
                continue
            rel = str(file_path.relative_to(root))
            with file_path.open("r", encoding="utf-8", errors="ignore") as handle:
                for idx, line in enumerate(handle, start=1):
                    for match in MODEL_LITERAL_PATTERN.findall(line):
                        findings.append({"path": rel, "line": idx, "literal": match})
    return findings


def audit_model_alias_usage(root: Path) -> dict[str, Any]:
    findings = find_hardcoded_model_literals(root)
    if findings:
        return _check_result(
            "model_alias_usage",
            "fail",
            "Hardcoded Gemini model literals found outside model_defaults.py.",
            len(findings),
            findings[:20],
        )
    return _check_result(
        "model_alias_usage",
        "pass",
        "Gemini model IDs are centralized in pipelines/shared/model_defaults.py.",
        0,
    )


def run_audit(root: Path, soft_line_limit: int, hard_line_limit: int) -> dict[str, Any]:
    checks = [
        audit_line_lengths(root, soft_limit=soft_line_limit, hard_limit=hard_line_limit),
        audit_todo_markers(root),
        audit_topic_cards_quality(root),
        audit_study_db(root),
        audit_model_alias_usage(root),
        audit_docs_system(root),
    ]
    failures = [check for check in checks if check["status"] == "fail"]
    warnings = [check for check in checks if check["status"] == "warn"]
    overall_status = "fail" if failures else "warn" if warnings else "pass"
    advice = {
        "line_lengths": "Split large files into smaller modules/functions; aim for <=300 lines.",
        "todo_markers": "Resolve or roadmap TODO/FIXME/HACK markers.",
        "topic_cards_quality": "Review duplicate key-point/example samples and merge/remove low-value duplicates.",
        "study_db": "Fix study DB week ordering/source references before merging new material.",
        "model_alias_usage": "Use FAST_GEMINI_AGENT/SMART_GEMINI_AGENT aliases instead of hardcoded model literals.",
        "docs_system": "Restore missing maintenance docs and keep AGENTS/README/testing docs aligned.",
    }
    suggested = [advice[check["check_id"]] for check in checks if check["status"] != "pass" and check["check_id"] in advice]
    return {
        "timestamp_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "overall_status": overall_status,
        "summary": {
            "checks_total": len(checks),
            "failures": len(failures),
            "warnings": len(warnings),
            "passes": len(checks) - len(failures) - len(warnings),
        },
        "checks": checks,
        "suggested_next_actions": suggested[:8],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run repo maintenance audit.")
    parser.add_argument("--soft-line-limit", type=int, default=300)
    parser.add_argument("--hard-line-limit", type=int, default=500)
    parser.add_argument("--strict-warnings", action="store_true")
    parser.add_argument("--report-file", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = run_audit(ROOT, soft_line_limit=args.soft_line_limit, hard_line_limit=args.hard_line_limit)
    args.report_file.parent.mkdir(parents=True, exist_ok=True)
    args.report_file.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    should_fail = report["overall_status"] == "fail" or (args.strict_warnings and report["overall_status"] == "warn")
    print(
        json.dumps(
            {
                "overall_status": report["overall_status"],
                "report_file": str(args.report_file),
                "failures": report["summary"]["failures"],
                "warnings": report["summary"]["warnings"],
            },
            ensure_ascii=False,
        )
    )
    return 1 if should_fail else 0


if __name__ == "__main__":
    sys.exit(main())

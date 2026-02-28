from __future__ import annotations

from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import tempfile
import unittest

from scripts import quality_dashboard as dashboard


def _write(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


class QualityDashboardTests(unittest.TestCase):
    def test_parse_timestamp_utc_accepts_zulu(self) -> None:
        dt = dashboard.parse_timestamp_utc("2026-02-28T00:00:00Z")
        self.assertIsNotNone(dt)
        self.assertEqual(timezone.utc, dt.tzinfo)

    def test_build_dashboard_green_when_reports_are_healthy(self) -> None:
        now = datetime(2026, 2, 28, 1, 0, 0, tzinfo=timezone.utc)
        ts = "2026-02-28T00:30:00Z"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            files = {
                "maintenance_audit": root / "maintenance_audit.json",
                "gemini_model_health": root / "gemini_model_health.json",
                "gemini_capability_benchmark": root / "gemini_capability_benchmark.json",
                "gemini_prompt_experiments": root / "gemini_prompt_experiments.json",
                "gemini_ui_test_report": root / "gemini_ui_test_report.json",
            }
            _write(files["maintenance_audit"], {"timestamp_utc": ts, "overall_status": "pass"})
            _write(
                files["gemini_model_health"],
                {"timestamp_utc": ts, "summary": {"available": 2, "requested": 2, "recommended_primary": "gemini-3-flash-preview"}},
            )
            _write(
                files["gemini_capability_benchmark"],
                {"timestamp_utc": ts, "results_by_model": {"gemini-3-flash-preview": {"summary": {"pass_rate": 0.9}}}},
            )
            _write(
                files["gemini_prompt_experiments"],
                {
                    "timestamp_utc": ts,
                    "summary_by_model": {
                        "gemini-3-flash-preview": {
                            "recommendations": {"task_a": {"pass_rate": 1.0, "variant_id": "v2"}},
                        }
                    },
                },
            )
            _write(files["gemini_ui_test_report"], {"timestamp_utc": ts, "summary": {"overall_status": "pass"}})

            original = dashboard.SOURCE_FILES
            try:
                dashboard.SOURCE_FILES = files
                report = dashboard.build_dashboard(max_age_hours=72, now_utc=now)
            finally:
                dashboard.SOURCE_FILES = original

        self.assertEqual("pass", report["summary"]["overall_status"])

    def test_build_dashboard_warns_on_stale_reports(self) -> None:
        now = datetime(2026, 2, 28, 12, 0, 0, tzinfo=timezone.utc)
        stale = (now - timedelta(hours=200)).replace(microsecond=0).isoformat().replace("+00:00", "Z")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            files = {
                "maintenance_audit": root / "maintenance_audit.json",
                "gemini_model_health": root / "gemini_model_health.json",
                "gemini_capability_benchmark": root / "gemini_capability_benchmark.json",
                "gemini_prompt_experiments": root / "gemini_prompt_experiments.json",
                "gemini_ui_test_report": root / "gemini_ui_test_report.json",
            }
            for path in files.values():
                _write(path, {"timestamp_utc": stale, "summary": {"overall_status": "pass"}})
            _write(files["maintenance_audit"], {"timestamp_utc": stale, "overall_status": "pass"})
            _write(
                files["gemini_model_health"],
                {"timestamp_utc": stale, "summary": {"available": 1, "requested": 1, "recommended_primary": "gemini-3-flash-preview"}},
            )
            _write(
                files["gemini_capability_benchmark"],
                {"timestamp_utc": stale, "results_by_model": {"gemini-3-flash-preview": {"summary": {"pass_rate": 0.95}}}},
            )
            _write(
                files["gemini_prompt_experiments"],
                {
                    "timestamp_utc": stale,
                    "summary_by_model": {
                        "gemini-3-flash-preview": {"recommendations": {"task_a": {"pass_rate": 1.0, "variant_id": "v2"}}}
                    },
                },
            )
            _write(files["gemini_ui_test_report"], {"timestamp_utc": stale, "summary": {"overall_status": "pass"}})

            original = dashboard.SOURCE_FILES
            try:
                dashboard.SOURCE_FILES = files
                report = dashboard.build_dashboard(max_age_hours=24, now_utc=now)
            finally:
                dashboard.SOURCE_FILES = original

        self.assertEqual("warn", report["summary"]["overall_status"])
        self.assertGreater(report["summary"]["warnings"], 0)

    def test_check_ui_protocol_treats_advisory_gemini_failures_as_non_blocking(self) -> None:
        payload = {
            "summary": {
                "overall_status": "warn",
                "release_gate_status": "pass",
                "hard_failures": 0,
                "gemini_failures": 2,
            }
        }
        check = dashboard.check_ui_protocol(payload)
        self.assertEqual("pass", check["status"])
        self.assertIn("deterministic gate passed", check["summary"].lower())

    def test_check_maintenance_soft_line_length_warning_is_non_blocking(self) -> None:
        payload = {
            "overall_status": "warn",
            "checks": [
                {
                    "check_id": "line_lengths",
                    "status": "warn",
                    "findings": [{"path": "a.py", "line_count": 320}],
                }
            ],
        }
        check = dashboard.check_maintenance(payload)
        self.assertEqual("pass", check["status"])
        self.assertEqual(1, check["metric"]["soft_line_length_findings"])

    def test_check_model_health_partial_availability_is_non_blocking(self) -> None:
        payload = {"summary": {"available": 2, "requested": 3, "recommended_primary": "gemini-3-flash-preview"}}
        check = dashboard.check_model_health(payload)
        self.assertEqual("pass", check["status"])


if __name__ == "__main__":
    unittest.main()

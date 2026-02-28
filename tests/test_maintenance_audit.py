from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from scripts.maintenance_audit import (
    audit_docs_system,
    find_hardcoded_model_literals,
    run_audit,
)


class MaintenanceAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[1]

    def test_run_audit_has_expected_shape_and_checks(self) -> None:
        report = run_audit(self.root, soft_line_limit=300, hard_line_limit=500)
        self.assertIn("overall_status", report)
        self.assertIn("summary", report)
        self.assertIn("checks", report)
        check_ids = {entry["check_id"] for entry in report["checks"]}
        expected = {
            "line_lengths",
            "todo_markers",
            "topic_cards_quality",
            "study_db",
            "model_alias_usage",
            "docs_system",
        }
        self.assertTrue(expected.issubset(check_ids), f"Missing checks: {expected - check_ids}")

    def test_model_literal_detection_ignores_model_defaults_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "pipelines/shared").mkdir(parents=True, exist_ok=True)
            (root / "scripts").mkdir(parents=True, exist_ok=True)

            (root / "pipelines/shared/model_defaults.py").write_text(
                'SMART_GEMINI_AGENT = "gemini-3-pro-preview"\n',
                encoding="utf-8",
            )
            bad_file = root / "scripts/bad.py"
            bad_file.write_text('MODEL = "gemini-3-pro-preview"\n', encoding="utf-8")

            findings = find_hardcoded_model_literals(root)
            self.assertEqual(1, len(findings))
            self.assertEqual("scripts/bad.py", findings[0]["path"])

    def test_docs_audit_fails_when_required_docs_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs/specs").mkdir(parents=True, exist_ok=True)
            (root / "AGENTS.md").write_text("# agents\n", encoding="utf-8")
            (root / "README.md").write_text("# readme\n", encoding="utf-8")

            check = audit_docs_system(root)
            self.assertEqual("fail", check["status"])
            self.assertGreater(len(check["findings"]), 0)


if __name__ == "__main__":
    unittest.main()

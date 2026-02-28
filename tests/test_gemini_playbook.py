from __future__ import annotations

from pathlib import Path
import re
import unittest


class GeminiPlaybookTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[1]
        cls.playbook = cls.root / "docs" / "GEMINI_PLAYBOOK.md"
        cls.text = cls.playbook.read_text(encoding="utf-8")

    def test_playbook_exists(self) -> None:
        self.assertTrue(self.playbook.exists())

    def test_playbook_has_date_stamp(self) -> None:
        self.assertRegex(self.text, r"Last updated:\s*\d{4}-\d{2}-\d{2}")

    def test_playbook_mentions_model_aliases(self) -> None:
        self.assertIn("fast gemini agent", self.text.lower())
        self.assertIn("smart gemini agent", self.text.lower())
        self.assertIn("gemini-3-flash-preview", self.text)
        self.assertIn("gemini-3-pro-preview", self.text)

    def test_playbook_links_to_report_artifacts(self) -> None:
        expected = [
            "data/test_reports/gemini_capability_benchmark.json",
            "data/test_reports/gemini_prompt_experiments.json",
            "data/test_reports/gemini_ui_test_report.json",
        ]
        for path in expected:
            self.assertIn(path, self.text)


if __name__ == "__main__":
    unittest.main()

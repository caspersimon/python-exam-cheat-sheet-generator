import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class IntegrateHomeworkMaterialScriptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[1]
        cls.script = cls.root / "scripts" / "integrate_homework_material.py"
        cls.study_db = cls.root / "data" / "study_db.json"
        cls.topic_cards = cls.root / "topic_cards.json"

    @staticmethod
    def _digest(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def _run(self, args: list[str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(self.script), *args],
            cwd=self.root,
            capture_output=True,
            text=True,
        )

    def test_dry_run_does_not_modify_data_files(self) -> None:
        before_db = self._digest(self.study_db)
        before_cards = self._digest(self.topic_cards)

        with tempfile.TemporaryDirectory() as tmp:
            report_path = Path(tmp) / "report.json"
            result = self._run(["--dry-run", "--report-file", str(report_path)])

            self.assertEqual(0, result.returncode, msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}")
            self.assertTrue(report_path.exists(), "Expected dry-run report file to be written.")

            after_db = self._digest(self.study_db)
            after_cards = self._digest(self.topic_cards)
            self.assertEqual(before_db, after_db, "Dry-run unexpectedly modified data/study_db.json")
            self.assertEqual(before_cards, after_cards, "Dry-run unexpectedly modified topic_cards.json")

            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertTrue(report.get("dry_run"))
            summary = report.get("study_db_integration", {}).get("summary", {})
            self.assertGreaterEqual(summary.get("total_candidate_homework_cells", 0), 1)


if __name__ == "__main__":
    unittest.main()

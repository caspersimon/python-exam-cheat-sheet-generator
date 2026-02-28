import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class AddWeekMaterialScriptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[1]
        cls.script = cls.root / "scripts" / "add_week_material.py"
        cls.study_db = cls.root / "data" / "study_db.json"

    def _db_digest(self) -> str:
        return hashlib.sha256(self.study_db.read_bytes()).hexdigest()

    def _run(self, args: list[str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(self.script), *args],
            cwd=self.root,
            capture_output=True,
            text=True,
        )

    def _write_payload(self, temp_dir: Path, *, week: int, sources: list[str] | None = None) -> Path:
        payload = {
            "week": week,
            "topics": ["smoke-test-week"],
            "lecture": {
                "concepts": [
                    {
                        "topic": "loops",
                        "explanation": "for loops iterate over iterable values",
                        "code_examples": [],
                    }
                ],
                "lecture_questions": [],
            },
            "notebook_cells": [
                {
                    "cell_index": 1,
                    "cell_type": "code",
                    "topic": "loops",
                    "is_advanced_optional": False,
                    "source": "for i in range(2):\n    print(i)",
                    "outputs": ["0", "1"],
                }
            ],
            "sources": sources or [],
        }
        payload_path = temp_dir / "week.json"
        payload_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return payload_path

    def test_dry_run_writes_report_and_keeps_db_unchanged(self) -> None:
        before_digest = self._db_digest()
        with tempfile.TemporaryDirectory() as tmp:
            temp_dir = Path(tmp)
            payload_path = self._write_payload(temp_dir, week=9501)
            report_path = temp_dir / "report.json"

            result = self._run(
                [
                    "--week-file",
                    str(payload_path),
                    "--skip-ai-curation",
                    "--dry-run",
                    "--no-recompute-topic-analysis",
                    "--report-file",
                    str(report_path),
                ]
            )

            self.assertEqual(0, result.returncode, msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}")
            self.assertTrue(report_path.exists(), "Expected dry-run report file to be written.")
            self.assertEqual(before_digest, self._db_digest(), "Dry-run unexpectedly modified data/study_db.json")

            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertTrue(report.get("dry_run"))
            self.assertEqual("added", report.get("integration_action"))

    def test_missing_sources_fail_without_allow_flag(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            temp_dir = Path(tmp)
            payload_path = self._write_payload(
                temp_dir,
                week=9502,
                sources=["materials/lectures/Lecture Week 999.md"],
            )

            result = self._run(
                [
                    "--week-file",
                    str(payload_path),
                    "--skip-ai-curation",
                    "--dry-run",
                    "--no-recompute-topic-analysis",
                ]
            )

            combined = f"{result.stdout}\n{result.stderr}"
            self.assertNotEqual(0, result.returncode, msg="Expected failure for missing source path.")
            self.assertIn("--allow-missing-sources", combined)

    def test_missing_sources_can_be_allowed_in_dry_run(self) -> None:
        before_digest = self._db_digest()
        with tempfile.TemporaryDirectory() as tmp:
            temp_dir = Path(tmp)
            payload_path = self._write_payload(
                temp_dir,
                week=9503,
                sources=["materials/notebooks/Notebook Week 999.ipynb"],
            )
            report_path = temp_dir / "report.json"

            result = self._run(
                [
                    "--week-file",
                    str(payload_path),
                    "--skip-ai-curation",
                    "--dry-run",
                    "--allow-missing-sources",
                    "--no-recompute-topic-analysis",
                    "--report-file",
                    str(report_path),
                ]
            )

            self.assertEqual(0, result.returncode, msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}")
            self.assertEqual(before_digest, self._db_digest(), "Dry-run unexpectedly modified data/study_db.json")

            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(
                ["materials/notebooks/Notebook Week 999.ipynb"],
                report.get("validation", {}).get("missing_sources"),
            )


if __name__ == "__main__":
    unittest.main()

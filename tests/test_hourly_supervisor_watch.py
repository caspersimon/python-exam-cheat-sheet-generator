from __future__ import annotations

from datetime import datetime
from pathlib import Path
import plistlib
import tempfile
import unittest
from zoneinfo import ZoneInfo

from scripts.hourly_supervisor_watch_manager import LABEL, _build_plist_payload


class HourlySupervisorWatchManagerTests(unittest.TestCase):
    def test_build_plist_payload_has_expected_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            prompt_file = Path(tmp_dir) / "prompt.txt"
            prompt_file.write_text("test", encoding="utf-8")
            watch_dir = Path(tmp_dir) / "watch"
            cutoff = datetime(2026, 3, 24, 8, 15, tzinfo=ZoneInfo("Europe/Amsterdam"))
            payload = _build_plist_payload(
                thread_id="019d1b6e-a202-7f73-9ac1-83f36b6e37d2",
                model="gpt-5.4",
                prompt_file=prompt_file,
                watch_dir=watch_dir,
                cutoff_at=cutoff,
                start_interval_seconds=3600,
                codex_bin="/usr/local/bin/codex",
            )

            self.assertEqual(payload["Label"], LABEL)
            self.assertTrue(payload["RunAtLoad"])
            self.assertEqual(payload["StartInterval"], 3600)
            program_arguments = payload["ProgramArguments"]
            self.assertIn("--thread-id", program_arguments)
            self.assertIn("--cutoff-at", program_arguments)
            self.assertIn(cutoff.isoformat(), program_arguments)
            self.assertIn(str(prompt_file.resolve()), program_arguments)
            self.assertIn("/usr/local/bin/codex", program_arguments)
            self.assertEqual(payload["WorkingDirectory"], str(Path(__file__).resolve().parents[1]))
            self.assertEqual(
                payload["EnvironmentVariables"]["PATH"],
                "/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin",
            )

    def test_plist_payload_serializes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            prompt_file = Path(tmp_dir) / "prompt.txt"
            prompt_file.write_text("test", encoding="utf-8")
            watch_dir = Path(tmp_dir) / "watch"
            cutoff = datetime(2026, 3, 24, 8, 15, tzinfo=ZoneInfo("Europe/Amsterdam"))
            payload = _build_plist_payload(
                thread_id="019d1b6e-a202-7f73-9ac1-83f36b6e37d2",
                model="gpt-5.4",
                prompt_file=prompt_file,
                watch_dir=watch_dir,
                cutoff_at=cutoff,
                start_interval_seconds=3600,
                codex_bin="/usr/local/bin/codex",
            )

            serialized = plistlib.dumps(payload)
            self.assertIn(b"<key>Label</key>", serialized)


if __name__ == "__main__":
    unittest.main()

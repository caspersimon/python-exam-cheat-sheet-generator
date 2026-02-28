from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class GeminiTestProtocolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[1]
        cls.script = cls.root / "scripts" / "gemini_test_protocol.py"

    def _run_protocol(self, probe_payload: dict[str, object]) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as tmp:
            temp_dir = Path(tmp)
            probe_path = temp_dir / "probe.json"
            stress_path = temp_dir / "stress.json"
            report_path = temp_dir / "report.json"
            probe_path.write_text(json.dumps(probe_payload, ensure_ascii=False, indent=2), encoding="utf-8")
            stress_payload = {
                "ok": True,
                "summary": {
                    "scenariosRun": 10,
                    "scenariosFailed": 0,
                    "minOccupiedAreaRatio": 0.58,
                    "maxOverlapAreaRatio": 0.0,
                    "maxOutOfBounds": 0,
                    "worstByUtilization": {"name": "s", "occupiedAreaRatio": 0.58, "screenshotPath": ""},
                },
                "exportSnapshotProbe": {"controlsHidden": True, "headerRatio": 0.05, "screenshotPath": ""},
            }
            stress_path.write_text(json.dumps(stress_payload, ensure_ascii=False, indent=2), encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(self.script),
                    "--probe-json",
                    str(probe_path),
                    "--stress-json",
                    str(stress_path),
                    "--skip-gemini",
                    "--report-file",
                    str(report_path),
                ],
                cwd=self.root,
                capture_output=True,
                text=True,
            )

            self.assertTrue(report_path.exists(), "Protocol should always write a report file.")
            report = json.loads(report_path.read_text(encoding="utf-8"))
            result.report = report  # type: ignore[attr-defined]
            return result

    def test_protocol_passes_with_healthy_probe(self) -> None:
        probe = {
            "ok": True,
            "densityProbe": {"iconButtonsOnly": True, "headerRatio": 0.12},
            "exportProbe": {"supportPrompts": 2, "saveCalls": 1, "printCalls": 1},
            "exportStyleProbe": {"controlsHidden": True, "compactHeader": True, "headerRatio": 0.08},
            "screenshotPath": "docs/smoke-preview.png",
            "exportScreenshotPath": "docs/smoke-export-preview.png",
        }
        result = self._run_protocol(probe)
        self.assertEqual(0, result.returncode, msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}")
        self.assertEqual("pass", result.report["summary"]["overall_status"])  # type: ignore[attr-defined]
        self.assertEqual("pass", result.report["summary"]["release_gate_status"])  # type: ignore[attr-defined]

    def test_protocol_fails_when_export_chrome_leaks(self) -> None:
        probe = {
            "ok": True,
            "densityProbe": {"iconButtonsOnly": True, "headerRatio": 0.11},
            "exportProbe": {"supportPrompts": 2, "saveCalls": 1, "printCalls": 1},
            "exportStyleProbe": {"controlsHidden": False, "compactHeader": False, "headerRatio": 0.2},
            "screenshotPath": "docs/smoke-preview.png",
            "exportScreenshotPath": "docs/smoke-export-preview.png",
        }
        result = self._run_protocol(probe)
        self.assertNotEqual(0, result.returncode, msg="Expected non-zero exit for failing hard checks.")
        self.assertEqual("fail", result.report["summary"]["overall_status"])  # type: ignore[attr-defined]
        self.assertEqual("fail", result.report["summary"]["release_gate_status"])  # type: ignore[attr-defined]


if __name__ == "__main__":
    unittest.main()

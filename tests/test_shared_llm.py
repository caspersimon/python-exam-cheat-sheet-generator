from __future__ import annotations

import subprocess
import unittest
from unittest.mock import patch

from pipelines.shared.llm import run_gemini_cli


class SharedLlmTests(unittest.TestCase):
    def test_run_gemini_cli_uses_json_response_when_supported(self) -> None:
        with patch(
            "pipelines.shared.llm._run_gemini_command",
            return_value=subprocess.CompletedProcess(
                args=["gemini"],
                returncode=0,
                stdout='{"response":"{\\"ok\\": true}"}',
                stderr="",
            ),
        ) as run_command:
            result = run_gemini_cli("hello", model="test-model", timeout_seconds=5, stderr_clip=200)

        self.assertEqual('{"ok": true}', result)
        self.assertEqual(1, run_command.call_count)

    def test_run_gemini_cli_falls_back_when_json_flag_fails(self) -> None:
        with patch(
            "pipelines.shared.llm._run_gemini_command",
            side_effect=[
                subprocess.CompletedProcess(args=["gemini"], returncode=2, stdout="", stderr="unknown flag"),
                subprocess.CompletedProcess(args=["gemini"], returncode=0, stdout='{"ok": true}', stderr=""),
            ],
        ) as run_command:
            result = run_gemini_cli("hello", model="test-model", timeout_seconds=5, stderr_clip=200)

        self.assertEqual('{"ok": true}', result)
        self.assertEqual(2, run_command.call_count)


if __name__ == "__main__":
    unittest.main()

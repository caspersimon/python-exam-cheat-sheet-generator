from __future__ import annotations

import unittest

from scripts import gemini_model_health as health


class GeminiModelHealthTests(unittest.TestCase):
    def test_classify_error_timeout(self) -> None:
        self.assertEqual("timeout", health.classify_error("Command timed out after 40 seconds"))

    def test_classify_error_quota(self) -> None:
        self.assertEqual("quota", health.classify_error("TerminalQuotaError: exhausted your capacity"))

    def test_parse_probe_json_ok(self) -> None:
        ok, reason = health.parse_probe_json('{"status":"ok","pong":true}')
        self.assertTrue(ok)
        self.assertEqual("ok", reason)

    def test_parse_probe_json_invalid_shape(self) -> None:
        ok, reason = health.parse_probe_json('{"status":"ok","pong":"yes"}')
        self.assertFalse(ok)
        self.assertEqual("bad_pong_field", reason)

    def test_summarize_prefers_fast_primary(self) -> None:
        results = [
            {"model": "gemini-3-flash-preview", "status": "available"},
            {"model": "gemini-3-pro-preview", "status": "unavailable", "error_kind": "quota"},
        ]
        summary = health.summarize(results)
        self.assertEqual("gemini-3-flash-preview", summary["recommended_primary"])
        self.assertEqual(1, summary["available"])
        self.assertEqual({"quota": 1}, summary["error_kinds"])


if __name__ == "__main__":
    unittest.main()

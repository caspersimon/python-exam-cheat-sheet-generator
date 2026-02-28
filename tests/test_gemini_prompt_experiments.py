from __future__ import annotations

import unittest

from scripts import gemini_prompt_experiments as experiments


class GeminiPromptExperimentsTests(unittest.TestCase):
    def test_extract_code_from_fence(self) -> None:
        raw = "```python\ndef parse_int_csv(text: str) -> list[int]:\n    return []\n```"
        self.assertIn("def parse_int_csv", experiments._extract_code(raw))

    def test_eval_parse_int_csv_passes_for_valid_function(self) -> None:
        raw = """
def parse_int_csv(text: str) -> list[int]:
    result = []
    for token in text.split(","):
        token = token.strip()
        if not token:
            continue
        try:
            result.append(int(token))
        except ValueError:
            raise ValueError(f"invalid token: {token}") from None
    return result
""".strip()
        ok, _, metadata = experiments._eval_parse_int_csv(raw)
        self.assertTrue(ok, msg=str(metadata))

    def test_eval_parse_int_csv_detects_behavior_mismatch(self) -> None:
        raw = """
def parse_int_csv(text: str) -> list[int]:
    return [1]
""".strip()
        ok, detail, metadata = experiments._eval_parse_int_csv(raw)
        self.assertFalse(ok)
        self.assertEqual("behavior_mismatch", detail)
        self.assertEqual("behavior_mismatch", metadata["failure_kind"])

    def test_classify_error_detects_quota(self) -> None:
        err = RuntimeError("TerminalQuotaError: exhausted your capacity on this model")
        self.assertEqual("quota", experiments._classify_error(err))

    def test_summarize_recommendation_prefers_higher_pass_rate(self) -> None:
        results = [
            {
                "model_requested": "gemini-3-flash-preview",
                "task_id": "parse_int_csv",
                "variant_id": "v1",
                "status": "pass",
                "latency_ms": 100,
                "failure_kind": "",
            },
            {
                "model_requested": "gemini-3-flash-preview",
                "task_id": "parse_int_csv",
                "variant_id": "v1",
                "status": "fail",
                "latency_ms": 100,
                "failure_kind": "behavior_mismatch",
            },
            {
                "model_requested": "gemini-3-flash-preview",
                "task_id": "parse_int_csv",
                "variant_id": "v2",
                "status": "pass",
                "latency_ms": 120,
                "failure_kind": "",
            },
            {
                "model_requested": "gemini-3-flash-preview",
                "task_id": "parse_int_csv",
                "variant_id": "v2",
                "status": "pass",
                "latency_ms": 130,
                "failure_kind": "",
            },
        ]
        summary = experiments._summarize(results)
        rec = summary["gemini-3-flash-preview"]["recommendations"]["parse_int_csv"]
        self.assertEqual("v2", rec["variant_id"])
        self.assertEqual(1.0, rec["pass_rate"])


if __name__ == "__main__":
    unittest.main()

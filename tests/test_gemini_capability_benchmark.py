from __future__ import annotations

from pathlib import Path
import json
import unittest

from scripts import gemini_capability_benchmark as bench


class GeminiCapabilityBenchmarkTests(unittest.TestCase):
    def test_json_contract_1_passes(self) -> None:
        raw = json.dumps({"answer": "ready", "confidence": 0.82, "tags": ["alpha", "beta"]})
        ok, _, meta = bench._eval_json_contract_1(raw)
        self.assertTrue(ok)
        self.assertIn("parsed", meta)

    def test_json_contract_2_fails_when_shape_wrong(self) -> None:
        raw = json.dumps({"product": 133, "classification": "prime", "notes": ["a"], "extra": 1})
        ok, _, _ = bench._eval_json_contract_2(raw)
        self.assertFalse(ok)

    def test_function_normalize_eval(self) -> None:
        code = """
def normalize_topic_label(text: str) -> str:
    value = (text or "").lower().replace("_", " ").replace("-", " ")
    value = " ".join(value.split())
    if value.endswith("ies") and len(value) > 4:
        value = value[:-3] + "y"
    elif value.endswith("s") and len(value) > 4 and not value.endswith("ss"):
        value = value[:-1]
    return value.strip()
""".strip()
        ok, _, meta = bench._eval_function_normalize(code)
        self.assertTrue(ok, msg=str(meta))

    def test_function_parse_int_csv_eval(self) -> None:
        code = """
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
        ok, _, meta = bench._eval_function_parse_int_csv(code)
        self.assertTrue(ok, msg=str(meta))

    def test_image_structured_eval(self) -> None:
        raw = json.dumps(
            {
                "has_header_controls": False,
                "has_card_resize_handles": False,
                "overall_density": "high",
                "evidence": "Cards are compact and controls are not visible.",
            }
        )
        ok, _, _ = bench._eval_image_structured(raw)
        self.assertTrue(ok)

    def test_build_cases_uses_passed_image_path(self) -> None:
        cases = bench._build_cases(Path("docs/assets/preview-editing-compact.png"))
        self.assertEqual(6, len(cases))
        self.assertTrue(any(case.case_id == "vision_structured_layout" for case in cases))


if __name__ == "__main__":
    unittest.main()

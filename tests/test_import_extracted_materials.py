import unittest
from unittest.mock import patch

from scripts.import_extracted_materials import _normalize_import_payload, _normalize_repo_relative_path


class ImportExtractedMaterialsTests(unittest.TestCase):
    def test_normalize_repo_relative_path_prefixes_post_midterm_sources(self) -> None:
        with patch(
            "pathlib.Path.exists",
            autospec=True,
            side_effect=lambda path: str(path).endswith("materials/post_midterm/practice/foo.pdf"),
        ):
            normalized = _normalize_repo_relative_path("practice/foo.pdf")

        self.assertEqual("materials/post_midterm/practice/foo.pdf", normalized)

    def test_normalize_import_payload_repairs_assessment_shape(self) -> None:
        with patch(
            "pathlib.Path.exists",
            autospec=True,
            side_effect=lambda path: str(path).endswith("materials/post_midterm/practice/foo.pdf"),
        ):
            payload = _normalize_import_payload(
                {
                    "exam_label": "sample-final",
                    "source": "practice/foo.pdf",
                    "year": "2025",
                    "questions": [{"number": 1, "options": {"a": "x", "b": "y"}}],
                    "note": "OCR cleanup used",
                }
            )

        self.assertEqual("materials/post_midterm/practice/foo.pdf", payload["source"])
        self.assertEqual(["OCR cleanup used"], payload["notes"])


if __name__ == "__main__":
    unittest.main()

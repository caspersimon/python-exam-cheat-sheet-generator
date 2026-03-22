import json
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import Mock, patch

from pipelines.study_database.raw_sources import (
    OCR_MAX_PAGES,
    PDFTOTEXT_TIMEOUT_SECONDS,
    classify_source,
    extract_ipynb_text,
    extract_pdf_text,
    extract_pptx_text,
    infer_week_number,
    _run_subprocess,
)


class RawSourceExtractionTests(unittest.TestCase):
    def test_classification_and_week_inference(self) -> None:
        self.assertEqual(4, infer_week_number(Path("Exercise_4.1.py")))
        self.assertEqual("week-4", classify_source(Path("Exercise_4.1.py")))
        self.assertEqual("assessment", classify_source(Path("Sample Final plus answers.pdf")))
        self.assertEqual("unassigned", classify_source(Path("OOP.py")))

    def test_extract_ipynb_text_keeps_useful_cell_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            notebook_path = Path(tmp) / "Notebook Week 4.ipynb"
            notebook_path.write_text(
                json.dumps(
                    {
                        "cells": [
                            {"cell_type": "markdown", "source": ["### Heading"]},
                            {
                                "cell_type": "code",
                                "source": ["print('hello')"],
                                "outputs": [{"text": ["hello\n"]}],
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )

            text = extract_ipynb_text(notebook_path)
            self.assertIn("MARKDOWN CELL", text)
            self.assertIn("Heading", text)
            self.assertIn("CODE CELL", text)
            self.assertIn("print('hello')", text)
            self.assertIn("hello", text)

    def test_extract_pptx_text_reads_slide_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pptx_path = Path(tmp) / "Lecture Week 4.pptx"
            with zipfile.ZipFile(pptx_path, "w") as archive:
                archive.writestr(
                    "ppt/slides/slide1.xml",
                    """<?xml version='1.0' encoding='UTF-8'?>
                    <p:sld xmlns:p='http://schemas.openxmlformats.org/presentationml/2006/main'
                           xmlns:a='http://schemas.openxmlformats.org/drawingml/2006/main'>
                      <p:cSld>
                        <p:spTree>
                          <p:sp>
                            <p:txBody>
                              <a:p><a:r><a:t>Week 4</a:t></a:r></a:p>
                              <a:p><a:r><a:t>String methods</a:t></a:r></a:p>
                            </p:txBody>
                          </p:sp>
                        </p:spTree>
                      </p:cSld>
                    </p:sld>""",
                )

            text = extract_pptx_text(pptx_path)
            self.assertIn("Week 4", text)
            self.assertIn("String methods", text)

    def test_extract_pdf_text_uses_pdftotext_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pdf_path = Path(tmp) / "Sample Final plus answers.pdf"

            with patch("pipelines.study_database.raw_sources._run_pdftotext") as run_pdf:
                run_pdf.side_effect = ["", "Question 1"]
                text = extract_pdf_text(pdf_path)

            self.assertEqual("Question 1", text)

    def test_run_subprocess_surfaces_timeout_with_tool_name(self) -> None:
        with patch("pipelines.study_database.raw_sources.subprocess.run", side_effect=subprocess.TimeoutExpired(cmd="pdftotext", timeout=1)):
            with self.assertRaisesRegex(RuntimeError, f"pdftotext timed out after {PDFTOTEXT_TIMEOUT_SECONDS} seconds"):
                _run_subprocess(["pdftotext"], timeout_seconds=PDFTOTEXT_TIMEOUT_SECONDS, failure_label="pdftotext")

    def test_pdf_ocr_limits_rendered_pages(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pdf_path = Path(tmp) / "Sample Final plus answers.pdf"
            with patch("pipelines.study_database.raw_sources._run_pdftotext", side_effect=RuntimeError("pdftotext failed")), patch(
                "pipelines.study_database.raw_sources.shutil.which", return_value="/usr/bin/tool"
            ), patch(
                "pipelines.study_database.raw_sources._run_subprocess"
            ) as run_subprocess, patch("pipelines.study_database.raw_sources.tempfile.TemporaryDirectory") as temp_dir:
                temp_dir.return_value.__enter__.return_value = tmp
                temp_dir.return_value.__exit__.return_value = False
                run_subprocess.side_effect = [
                    Mock(stdout="", returncode=0),
                    Mock(stdout="page 1 text", returncode=0),
                ]
                Path(tmp, "page-1.png").write_text("fake", encoding="utf-8")

                text = extract_pdf_text(pdf_path)

        self.assertEqual("page 1 text", text)
        self.assertEqual("pdftoppm", run_subprocess.call_args_list[0].args[0][0])
        self.assertIn("-l", run_subprocess.call_args_list[0].args[0])
        self.assertIn(str(OCR_MAX_PAGES), run_subprocess.call_args_list[0].args[0])


if __name__ == "__main__":
    unittest.main()

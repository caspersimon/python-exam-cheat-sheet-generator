from __future__ import annotations

import html
import json
import re
import shutil
import subprocess
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from xml.etree import ElementTree

from pipelines.shared import normalize_newlines

WEEK_RE = re.compile(r"(?:week|exercise[_\s-])\s*(\d+)", re.IGNORECASE)
ASSESSMENT_RE = re.compile(r"(final|exam|resit|trial)", re.IGNORECASE)
REPO_ROOT = Path(__file__).resolve().parents[2]
PDFTOTEXT_TIMEOUT_SECONDS = 20
PDFTOPPM_TIMEOUT_SECONDS = 45
TESSERACT_TIMEOUT_SECONDS = 20
OCR_MAX_PAGES = 20


@dataclass(slots=True)
class RawSourceRecord:
    path: Path
    relative_path: str
    kind: str
    role: str
    week: int | None
    text: str


def source_kind(path: Path) -> str:
    return path.suffix.lower().lstrip(".")


def infer_week_number(path: Path) -> int | None:
    match = WEEK_RE.search(path.name)
    if match:
        return int(match.group(1))
    return None


def infer_role(path: Path) -> str:
    name = path.name.lower()
    if path.suffix.lower() == ".pptx":
        return "lecture"
    if path.suffix.lower() == ".ipynb":
        return "notebook"
    if path.suffix.lower() == ".pdf":
        return "assessment"
    if "solution" in name:
        return "solution"
    if name.startswith("exercise") or "exercise" in name:
        return "exercise"
    if path.suffix.lower() in {".py", ".txt", ".md"}:
        return "text"
    return "unknown"


def classify_source(path: Path) -> str:
    if path.suffix.lower() == ".pdf" and ASSESSMENT_RE.search(path.name):
        return "assessment"

    week = infer_week_number(path)
    if week is not None:
        return f"week-{week}"

    if path.suffix.lower() == ".pdf":
        return "assessment"
    return "unassigned"


def extract_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".txt", ".py", ".md"}:
        return normalize_newlines(path.read_text(encoding="utf-8", errors="ignore")).strip()
    if suffix == ".ipynb":
        return extract_ipynb_text(path)
    if suffix == ".pptx":
        return extract_pptx_text(path)
    if suffix == ".pdf":
        return extract_pdf_text(path)
    return normalize_newlines(path.read_text(encoding="utf-8", errors="ignore")).strip()


def extract_ipynb_text(path: Path) -> str:
    notebook = json.loads(path.read_text(encoding="utf-8", errors="ignore"))
    cells = notebook.get("cells", [])
    lines: list[str] = []
    for index, cell in enumerate(cells, start=1):
        cell_type = str(cell.get("cell_type") or "").strip().lower()
        source = "".join(cell.get("source") or [])
        source = normalize_newlines(source).strip()
        if not source:
            continue
        lines.append(f"[{index}] {cell_type.upper()} CELL")
        lines.append(source)
        outputs = []
        for output in cell.get("outputs") or []:
            text = ""
            if isinstance(output, dict):
                if isinstance(output.get("text"), list):
                    text = "".join(output.get("text") or [])
                elif isinstance(output.get("text"), str):
                    text = output["text"]
                elif isinstance(output.get("data"), dict):
                    text = "".join(output["data"].get("text/plain") or [])
            if text.strip():
                outputs.append(normalize_newlines(text).strip())
        if outputs:
            lines.append("OUTPUTS:")
            lines.extend(outputs[:3])
    return "\n".join(lines).strip()


def extract_pptx_text(path: Path) -> str:
    slide_texts: list[str] = []
    with zipfile.ZipFile(path) as archive:
        slide_names = sorted(
            name for name in archive.namelist() if name.startswith("ppt/slides/slide") and name.endswith(".xml")
        )
        for slide_name in slide_names:
            xml = archive.read(slide_name).decode("utf-8", errors="ignore")
            try:
                root = ElementTree.fromstring(xml)
            except ElementTree.ParseError:
                root = None
            texts: list[str] = []
            if root is not None:
                for element in root.iter():
                    if not element.tag.endswith("}t"):
                        continue
                    if element.text and element.text.strip():
                        texts.append(html.unescape(element.text.strip()))
            if not texts:
                texts = [html.unescape(match.strip()) for match in re.findall(r"<a:t>(.*?)</a:t>", xml) if match.strip()]
            if texts:
                slide_texts.append(f"[{slide_name}]")
                slide_texts.extend(texts)
    return "\n".join(slide_texts).strip()


def _run_subprocess(args: list[str], *, timeout_seconds: int, failure_label: str) -> subprocess.CompletedProcess[str]:
    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"{failure_label} timed out after {timeout_seconds} seconds") from exc
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"{failure_label} failed")
    return result


def _run_pdftotext(path: Path, *, layout: bool) -> str:
    args = ["pdftotext"]
    if layout:
        args.append("-layout")
    args.extend([str(path), "-"])
    result = _run_subprocess(args, timeout_seconds=PDFTOTEXT_TIMEOUT_SECONDS, failure_label="pdftotext")
    return normalize_newlines(result.stdout).strip()


def _looks_garbled_pdf_text(text: str) -> bool:
    raw = (text or "").strip()
    if not raw:
        return True

    suspicious = sum(ch in "�ÿ" or ord(ch) < 32 and ch not in "\n\r\t\f" for ch in raw)
    safe_ascii = sum(ch.isascii() and (ch.isalnum() or ch.isspace() or ch in ".,:;!?()[]{}<>-_/\\'\"@#$%^&*+=|`~") for ch in raw)
    ascii_ratio = safe_ascii / max(1, len(raw))
    return suspicious > 12 or ascii_ratio < 0.72


def _run_pdf_ocr(path: Path) -> str:
    if shutil.which("pdftoppm") is None or shutil.which("tesseract") is None:
        raise RuntimeError("OCR dependencies missing: pdftoppm and tesseract are required.")

    with tempfile.TemporaryDirectory(prefix="pdf-ocr-") as tmp:
        temp_dir = Path(tmp)
        prefix = temp_dir / "page"
        _run_subprocess(
            ["pdftoppm", "-png", "-r", "180", "-f", "1", "-l", str(OCR_MAX_PAGES), str(path), str(prefix)],
            timeout_seconds=PDFTOPPM_TIMEOUT_SECONDS,
            failure_label="pdftoppm",
        )

        pages = sorted(temp_dir.glob("page-*.png"))
        page_texts: list[str] = []
        for image_path in pages:
            try:
                ocr = _run_subprocess(
                    ["tesseract", str(image_path), "stdout", "--psm", "6"],
                    timeout_seconds=TESSERACT_TIMEOUT_SECONDS,
                    failure_label=f"tesseract ({image_path.name})",
                )
            except RuntimeError:
                continue
            text = normalize_newlines(ocr.stdout).strip()
            if text:
                page_texts.append(text)
        return "\n\n".join(page_texts).strip()


def extract_pdf_text(path: Path) -> str:
    try:
        text = _run_pdftotext(path, layout=True)
        if text and not _looks_garbled_pdf_text(text):
            return text
    except Exception:
        pass
    try:
        text = _run_pdftotext(path, layout=False)
        if text and not _looks_garbled_pdf_text(text):
            return text
    except Exception:
        pass
    return _run_pdf_ocr(path)


def collect_raw_source_records(source_dir: Path) -> list[RawSourceRecord]:
    records: list[RawSourceRecord] = []
    for path in sorted(source_dir.rglob("*")):
        if not path.is_file() or path.name.startswith("."):
            continue
        try:
            relative_path = path.relative_to(REPO_ROOT).as_posix()
        except ValueError:
            try:
                relative_path = path.relative_to(source_dir).as_posix()
            except ValueError:
                relative_path = path.name
        records.append(
            RawSourceRecord(
                path=path,
                relative_path=relative_path,
                kind=source_kind(path),
                role=infer_role(path),
                week=infer_week_number(path),
                text=extract_text(path),
            )
        )
    return records

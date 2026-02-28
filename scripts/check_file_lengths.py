#!/usr/bin/env python3
"""Enforce repository code-file length policy."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys

MAX_LINES = 500
CODE_EXTENSIONS = {".py", ".js", ".css", ".html", ".mjs", ".cjs"}
EXCLUDED_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv"}


@dataclass(frozen=True)
class Violation:
    path: Path
    line_count: int


def iter_code_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        if path.suffix.lower() not in CODE_EXTENSIONS:
            continue
        files.append(path)
    return sorted(files)


def count_lines(path: Path) -> int:
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        return sum(1 for _ in handle)


def find_violations(root: Path, max_lines: int = MAX_LINES) -> list[Violation]:
    violations: list[Violation] = []
    for path in iter_code_files(root):
        line_count = count_lines(path)
        if line_count > max_lines:
            violations.append(Violation(path=path, line_count=line_count))
    return violations


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    violations = find_violations(root)

    if not violations:
        print(f"OK: all code files are <= {MAX_LINES} lines.")
        return 0

    print(f"Found {len(violations)} code file(s) above {MAX_LINES} lines:")
    for violation in violations:
        rel = violation.path.relative_to(root)
        print(f"- {rel}: {violation.line_count} lines")
    return 1


if __name__ == "__main__":
    sys.exit(main())

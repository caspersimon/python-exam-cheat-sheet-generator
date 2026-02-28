from __future__ import annotations

import subprocess


def run_gemini_cli(
    prompt: str,
    *,
    model: str,
    timeout_seconds: int,
    stderr_clip: int,
) -> str:
    result = subprocess.run(
        ["gemini", "-m", model, "-p", prompt],
        text=True,
        capture_output=True,
        timeout=timeout_seconds,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Gemini failed ({result.returncode}): {result.stderr.strip()[:stderr_clip]}")
    return result.stdout.strip()

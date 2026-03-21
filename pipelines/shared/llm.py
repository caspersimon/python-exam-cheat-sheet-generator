from __future__ import annotations

import json
import subprocess


def _extract_headless_response(stdout: str) -> str:
    raw = (stdout or "").strip()
    if not raw:
        return ""

    start = raw.find("{")
    if start == -1:
        return raw

    try:
        payload = json.loads(raw[start:])
    except json.JSONDecodeError:
        return raw

    response = payload.get("response")
    if isinstance(response, str) and response.strip():
        return response.strip()
    return raw


def run_gemini_cli(
    prompt: str,
    *,
    model: str,
    timeout_seconds: int,
    stderr_clip: int,
) -> str:
    result = subprocess.run(
        ["gemini", "-m", model, "-p", prompt, "--output-format", "json"],
        text=True,
        capture_output=True,
        timeout=timeout_seconds,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Gemini failed ({result.returncode}): {result.stderr.strip()[:stderr_clip]}")
    cleaned = _extract_headless_response(result.stdout)
    if not cleaned:
        raise RuntimeError("Gemini returned empty output.")
    return cleaned

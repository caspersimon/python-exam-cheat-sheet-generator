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


def _clip_process_output(value: str, limit: int) -> str:
    text = (value or "").strip()
    if not text:
        return ""
    return text[:limit]


def _run_gemini_command(args: list[str], *, timeout_seconds: int) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        text=True,
        capture_output=True,
        timeout=timeout_seconds,
    )


def run_gemini_cli(
    prompt: str,
    *,
    model: str,
    timeout_seconds: int,
    stderr_clip: int,
) -> str:
    json_args = ["gemini", "-m", model, "-p", prompt, "--output-format", "json"]
    plain_args = ["gemini", "-m", model, "-p", prompt]

    json_result = _run_gemini_command(json_args, timeout_seconds=timeout_seconds)
    if json_result.returncode == 0:
        cleaned = _extract_headless_response(json_result.stdout)
        if cleaned:
            return cleaned

    plain_result = _run_gemini_command(plain_args, timeout_seconds=timeout_seconds)
    if plain_result.returncode != 0:
        stderr_text = _clip_process_output(plain_result.stderr, stderr_clip)
        stdout_text = _clip_process_output(plain_result.stdout, stderr_clip)
        details = stderr_text or stdout_text or "no stdout/stderr captured"
        raise RuntimeError(f"Gemini failed ({plain_result.returncode}): {details}")
    cleaned = _extract_headless_response(plain_result.stdout)
    if not cleaned:
        raise RuntimeError("Gemini returned empty output.")
    return cleaned

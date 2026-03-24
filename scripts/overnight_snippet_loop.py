from __future__ import annotations

import argparse
from datetime import datetime, time, timedelta
import json
import os
from pathlib import Path
import subprocess
import sys
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROMPT = ROOT / "docs" / "curation" / "OVERNIGHT_SUPERVISOR_PROMPT.txt"
LOOP_DIR = ROOT / "tmp" / "vision_exam_pipeline" / "overnight_loop"
STOP_FILE = LOOP_DIR / "STOP"
PID_FILE = LOOP_DIR / "loop.pid"
STATE_FILE = LOOP_DIR / "state.json"
RUN_LOG = LOOP_DIR / "launcher.log"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a resumable overnight Codex supervisor loop for snippet completeness.")
    parser.add_argument("--prompt-file", type=Path, default=DEFAULT_PROMPT)
    parser.add_argument("--model", default="gpt-5.4")
    parser.add_argument("--timezone", default="Europe/Amsterdam")
    parser.add_argument("--stop-at-hour", type=int, default=8)
    parser.add_argument("--max-iterations", type=int, default=20)
    parser.add_argument("--cooldown-seconds", type=int, default=30)
    parser.add_argument("--codex-bin", default="codex")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def _ensure_dirs() -> None:
    LOOP_DIR.mkdir(parents=True, exist_ok=True)


def _now(tz_name: str) -> datetime:
    return datetime.now(ZoneInfo(tz_name))


def _next_cutoff(tz_name: str, stop_at_hour: int) -> datetime:
    now = _now(tz_name)
    target = datetime.combine(now.date(), time(hour=stop_at_hour), tzinfo=ZoneInfo(tz_name))
    if now >= target:
        target = target + timedelta(days=1)
    return target


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _append_log(message: str) -> None:
    timestamp = datetime.now().isoformat(timespec="seconds")
    with RUN_LOG.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] {message}\n")


def _build_iteration_command(*, codex_bin: str, model: str, prompt_file: Path, output_dir: Path) -> list[str]:
    return [
        codex_bin,
        "exec",
        "--dangerously-bypass-approvals-and-sandbox",
        "--ephemeral",
        "-C",
        str(ROOT),
        "-m",
        model,
        "--json",
        "-o",
        str(output_dir / "last_message.txt"),
        "-",
    ]


def _run_iteration(*, args: argparse.Namespace, iteration: int) -> int:
    iteration_dir = LOOP_DIR / f"iteration-{iteration:03d}"
    iteration_dir.mkdir(parents=True, exist_ok=True)
    stdout_path = iteration_dir / "events.jsonl"
    stderr_path = iteration_dir / "stderr.log"
    command = _build_iteration_command(
        codex_bin=args.codex_bin,
        model=args.model,
        prompt_file=args.prompt_file,
        output_dir=iteration_dir,
    )
    _append_log(f"starting iteration {iteration} with command: {' '.join(command[:-1])} -")
    if args.dry_run:
        return 0
    with args.prompt_file.open("rb") as prompt_handle, stdout_path.open("wb") as stdout_handle, stderr_path.open("wb") as stderr_handle:
        completed = subprocess.run(
            command,
            stdin=prompt_handle,
            stdout=stdout_handle,
            stderr=stderr_handle,
            cwd=ROOT,
            check=False,
        )
    _append_log(f"iteration {iteration} exited with code {completed.returncode}")
    return int(completed.returncode)


def _status_snapshot() -> dict:
    command = [sys.executable, "scripts/vision_exam_pipeline.py", "status", "--round", "round1"]
    completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        return {"error": completed.stderr.strip() or completed.stdout.strip(), "returncode": completed.returncode}
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError:
        return {"error": "status output was not valid JSON", "raw": completed.stdout}


def main() -> int:
    args = _parse_args()
    _ensure_dirs()
    PID_FILE.write_text(str(os.getpid()), encoding="utf-8")
    cutoff = _next_cutoff(args.timezone, args.stop_at_hour)
    state = {
        "started_at": _now(args.timezone).isoformat(),
        "timezone": args.timezone,
        "cutoff_at": cutoff.isoformat(),
        "model": args.model,
        "prompt_file": str(args.prompt_file),
        "iterations_attempted": 0,
        "last_exit_code": None,
    }
    _write_json(STATE_FILE, state)
    _append_log(f"loop started; cutoff={cutoff.isoformat()}")

    try:
        for iteration in range(1, args.max_iterations + 1):
            if STOP_FILE.exists():
                _append_log("stop file present before iteration; exiting")
                break
            if _now(args.timezone) >= cutoff:
                _append_log("cutoff reached; exiting")
                break
            state["iterations_attempted"] = iteration
            state["status_before_iteration"] = _status_snapshot()
            _write_json(STATE_FILE, state)
            exit_code = _run_iteration(args=args, iteration=iteration)
            state["last_exit_code"] = exit_code
            state["last_iteration_finished_at"] = _now(args.timezone).isoformat()
            state["status_after_iteration"] = _status_snapshot()
            _write_json(STATE_FILE, state)
            if STOP_FILE.exists():
                _append_log("stop file present after iteration; exiting")
                break
            if exit_code != 0:
                _append_log(f"iteration {iteration} failed; sleeping {args.cooldown_seconds}s before retry")
            else:
                _append_log(f"iteration {iteration} completed; sleeping {args.cooldown_seconds}s before next loop")
            if iteration < args.max_iterations:
                import time as _time

                _time.sleep(args.cooldown_seconds)
        return 0
    finally:
        if PID_FILE.exists():
            PID_FILE.unlink()


if __name__ == "__main__":
    raise SystemExit(main())

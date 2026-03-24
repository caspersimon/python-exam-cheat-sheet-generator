from __future__ import annotations

import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import subprocess
from zoneinfo import ZoneInfo


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Resume a Codex thread as an hourly supervisor for the overnight orchestrator.")
    parser.add_argument("--thread-id", required=True)
    parser.add_argument("--prompt-file", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--watch-dir", type=Path, required=True)
    parser.add_argument("--model", default="gpt-5.4")
    parser.add_argument("--timezone", default="Europe/Amsterdam")
    parser.add_argument("--cutoff-at")
    parser.add_argument("--codex-bin", default="codex")
    return parser.parse_args()


def _now(timezone_name: str) -> datetime:
    return datetime.now(ZoneInfo(timezone_name))


def _load_cutoff(raw_value: str | None) -> datetime | None:
    if not raw_value:
        return None
    return datetime.fromisoformat(raw_value)


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _append_log(path: Path, message: str) -> None:
    timestamp = datetime.now().isoformat(timespec="seconds")
    with path.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] {message}\n")


def _lock_path(watch_dir: Path) -> Path:
    return watch_dir / "run.lock"


def _acquire_lock(watch_dir: Path, log_path: Path) -> bool:
    lock_path = _lock_path(watch_dir)
    payload = {"pid": os.getpid(), "acquired_at": datetime.now().isoformat(timespec="seconds")}
    try:
        descriptor = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        try:
            existing = json.loads(lock_path.read_text(encoding="utf-8"))
        except Exception:
            existing = {"error": "unreadable lock"}
        pid = existing.get("pid")
        if isinstance(pid, int):
            try:
                os.kill(pid, 0)
            except OSError:
                lock_path.unlink(missing_ok=True)
                _append_log(log_path, f"removed stale lock from pid={pid}")
                return _acquire_lock(watch_dir, log_path)
        _append_log(log_path, f"skipping run because another watcher appears active: {existing}")
        return False
    with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
    return True


def _release_lock(watch_dir: Path) -> None:
    _lock_path(watch_dir).unlink(missing_ok=True)


def _build_resume_command(args: argparse.Namespace, output_dir: Path) -> list[str]:
    return [
        args.codex_bin,
        "exec",
        "resume",
        args.thread_id,
        "--dangerously-bypass-approvals-and-sandbox",
        "-m",
        args.model,
        "--json",
        "-o",
        str(output_dir / "last_message.txt"),
        "-",
    ]


def _run_watch(args: argparse.Namespace, output_dir: Path, log_path: Path) -> int:
    stdout_path = output_dir / "events.jsonl"
    stderr_path = output_dir / "stderr.log"
    command = _build_resume_command(args, output_dir)
    _append_log(log_path, f"starting watch run with command: {' '.join(command[:-1])} -")
    try:
        with args.prompt_file.open("rb") as prompt_handle, stdout_path.open("wb") as stdout_handle, stderr_path.open("wb") as stderr_handle:
            completed = subprocess.run(
                command,
                cwd=args.repo_root,
                stdin=prompt_handle,
                stdout=stdout_handle,
                stderr=stderr_handle,
                check=False,
            )
    except FileNotFoundError as error:
        _append_log(log_path, f"failed to start watch run: {error}")
        return 127
    _append_log(log_path, f"watch run exited with code {completed.returncode}")
    return int(completed.returncode)


def main() -> int:
    args = _parse_args()
    args.repo_root = args.repo_root.resolve()
    args.watch_dir = args.watch_dir.resolve()
    args.prompt_file = args.prompt_file.resolve()
    _ensure_dir(args.watch_dir)
    run_log = args.watch_dir / "launcher.log"
    state_path = args.watch_dir / "state.json"
    cutoff = _load_cutoff(args.cutoff_at)
    started_at = _now(args.timezone)

    if cutoff is not None and started_at >= cutoff:
        state = {
            "skipped": True,
            "reason": "cutoff_reached",
            "started_at": started_at.isoformat(),
            "cutoff_at": cutoff.isoformat(),
            "thread_id": args.thread_id,
        }
        _write_json(state_path, state)
        _append_log(run_log, f"skipping watch run because cutoff was reached at {cutoff.isoformat()}")
        return 0

    if not _acquire_lock(args.watch_dir, run_log):
        return 0

    run_dir = args.watch_dir / started_at.strftime("run-%Y%m%d-%H%M%S")
    _ensure_dir(run_dir)
    state = {
        "skipped": False,
        "started_at": started_at.isoformat(),
        "thread_id": args.thread_id,
        "prompt_file": str(args.prompt_file),
        "repo_root": str(args.repo_root),
        "model": args.model,
        "watch_dir": str(args.watch_dir),
        "cutoff_at": cutoff.isoformat() if cutoff else None,
        "run_dir": str(run_dir),
        "exit_code": None,
    }
    _write_json(state_path, state)

    try:
        exit_code = _run_watch(args, run_dir, run_log)
        finished_at = _now(args.timezone)
        state["exit_code"] = exit_code
        state["finished_at"] = finished_at.isoformat()
        _write_json(state_path, state)
        return exit_code
    finally:
        _release_lock(args.watch_dir)


if __name__ == "__main__":
    raise SystemExit(main())

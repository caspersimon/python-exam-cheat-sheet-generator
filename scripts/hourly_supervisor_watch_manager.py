from __future__ import annotations

import argparse
from datetime import datetime, time, timedelta
import plistlib
from pathlib import Path
import shutil
import subprocess
import sys
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
LABEL = "com.codex.snippet-hourly-supervisor"
DEFAULT_PROMPT = ROOT / "docs" / "curation" / "HOURLY_ORCHESTRATOR_SUPERVISOR_PROMPT.txt"
DEFAULT_WATCH_DIR = ROOT / "tmp" / "vision_exam_pipeline" / "hourly_supervisor_watch"
DEFAULT_THREAD_ID = "019d1b6e-a202-7f73-9ac1-83f36b6e37d2"
PLIST_PATH = Path.home() / "Library" / "LaunchAgents" / f"{LABEL}.plist"
DEFAULT_PATH = "/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install and manage the hourly Codex supervisor watch.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    install = subparsers.add_parser("install")
    install.add_argument("--thread-id", default=DEFAULT_THREAD_ID)
    install.add_argument("--model", default="gpt-5.4")
    install.add_argument("--timezone", default="Europe/Amsterdam")
    install.add_argument("--stop-at-hour", type=int, default=8)
    install.add_argument("--stop-at-minute", type=int, default=15)
    install.add_argument("--start-interval-seconds", type=int, default=3600)
    install.add_argument("--prompt-file", type=Path, default=DEFAULT_PROMPT)
    install.add_argument("--watch-dir", type=Path, default=DEFAULT_WATCH_DIR)
    install.add_argument("--codex-bin", default=shutil.which("codex") or "codex")

    subparsers.add_parser("status")
    subparsers.add_parser("trigger")
    subparsers.add_parser("uninstall")
    return parser.parse_args()


def _run(command: list[str], *, check: bool = True, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=check, text=True, capture_output=capture)


def _next_cutoff(timezone_name: str, stop_at_hour: int, stop_at_minute: int) -> datetime:
    now = datetime.now(ZoneInfo(timezone_name))
    target = datetime.combine(now.date(), time(hour=stop_at_hour, minute=stop_at_minute), tzinfo=ZoneInfo(timezone_name))
    if now >= target:
        target = target + timedelta(days=1)
    return target


def _build_plist_payload(
    *,
    thread_id: str,
    model: str,
    prompt_file: Path,
    watch_dir: Path,
    cutoff_at: datetime,
    start_interval_seconds: int,
    codex_bin: str,
) -> dict:
    return {
        "Label": LABEL,
        "ProgramArguments": [
            sys.executable,
            str(ROOT / "scripts" / "hourly_supervisor_watch.py"),
            "--thread-id",
            thread_id,
            "--prompt-file",
            str(prompt_file.resolve()),
            "--repo-root",
            str(ROOT),
            "--watch-dir",
            str(watch_dir.resolve()),
            "--model",
            model,
            "--codex-bin",
            codex_bin,
            "--timezone",
            str(cutoff_at.tzinfo),
            "--cutoff-at",
            cutoff_at.isoformat(),
        ],
        "WorkingDirectory": str(ROOT),
        "EnvironmentVariables": {
            "PATH": DEFAULT_PATH,
        },
        "RunAtLoad": True,
        "StartInterval": start_interval_seconds,
        "StandardOutPath": str(watch_dir.resolve() / "launchd.stdout.log"),
        "StandardErrorPath": str(watch_dir.resolve() / "launchd.stderr.log"),
    }


def _user_domain() -> str:
    return f"gui/{_run(['id', '-u'], capture=True).stdout.strip()}"


def _bootout_existing() -> None:
    if not PLIST_PATH.exists():
        return
    _run(["launchctl", "bootout", _user_domain(), str(PLIST_PATH)], check=False)


def _install(args: argparse.Namespace) -> int:
    cutoff = _next_cutoff(args.timezone, args.stop_at_hour, args.stop_at_minute)
    args.prompt_file = args.prompt_file.resolve()
    args.watch_dir = args.watch_dir.resolve()
    args.watch_dir.mkdir(parents=True, exist_ok=True)
    PLIST_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = _build_plist_payload(
        thread_id=args.thread_id,
        model=args.model,
        prompt_file=args.prompt_file,
        watch_dir=args.watch_dir,
        cutoff_at=cutoff,
        start_interval_seconds=args.start_interval_seconds,
        codex_bin=args.codex_bin,
    )
    with PLIST_PATH.open("wb") as handle:
        plistlib.dump(payload, handle, sort_keys=False)
    _bootout_existing()
    _run(["launchctl", "bootstrap", _user_domain(), str(PLIST_PATH)])
    _run(["launchctl", "kickstart", "-k", f"{_user_domain()}/{LABEL}"], check=False)
    print(f"installed: {PLIST_PATH}")
    print(f"label: {LABEL}")
    print(f"cutoff_at: {cutoff.isoformat()}")
    print(f"watch_dir: {args.watch_dir}")
    return 0


def _status() -> int:
    print(f"plist: {PLIST_PATH}")
    print(f"exists: {PLIST_PATH.exists()}")
    completed = _run(["launchctl", "print", f"{_user_domain()}/{LABEL}"], check=False, capture=True)
    if completed.returncode == 0:
        print("launchd: loaded")
        print(completed.stdout.strip())
    else:
        print("launchd: not loaded")
        if completed.stderr.strip():
            print(completed.stderr.strip())
    if DEFAULT_WATCH_DIR.exists():
        print(f"watch_dir: {DEFAULT_WATCH_DIR}")
        for name in ["state.json", "launcher.log", "launchd.stdout.log", "launchd.stderr.log"]:
            path = DEFAULT_WATCH_DIR / name
            print(f"{name}: {'present' if path.exists() else 'missing'}")
    return 0


def _trigger() -> int:
    _run(["launchctl", "kickstart", "-k", f"{_user_domain()}/{LABEL}"])
    print(f"triggered: {LABEL}")
    return 0


def _uninstall() -> int:
    _bootout_existing()
    PLIST_PATH.unlink(missing_ok=True)
    print(f"removed: {PLIST_PATH}")
    return 0


def main() -> int:
    args = _parse_args()
    if args.command == "install":
        return _install(args)
    if args.command == "status":
        return _status()
    if args.command == "trigger":
        return _trigger()
    if args.command == "uninstall":
        return _uninstall()
    raise ValueError(f"unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())

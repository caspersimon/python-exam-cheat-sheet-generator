#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.shared import (
    SMART_GEMINI_AGENT,
    SMART_GEMINI_AGENT_FALLBACK,
    extract_json_blob,
    run_gemini_cli,
)

DEFAULT_MODEL = SMART_GEMINI_AGENT
DEFAULT_FALLBACK_MODEL = SMART_GEMINI_AGENT_FALLBACK
DEFAULT_SMOKE_CMD = "make smoke-ui"
DEFAULT_STRESS_CMD = "make stress-layout-ui"
DEFAULT_CANVAS_CMD = "make export-canvas-guard-ui"
DEFAULT_REPORT_DIR = ROOT / "data" / "test_reports"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run deterministic UI gates + Gemini micro-audits for screenshot/layout QA."
    )
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--fallback-model", default=DEFAULT_FALLBACK_MODEL)
    parser.add_argument("--smoke-cmd", default=DEFAULT_SMOKE_CMD)
    parser.add_argument("--stress-cmd", default=DEFAULT_STRESS_CMD)
    parser.add_argument("--canvas-cmd", default=DEFAULT_CANVAS_CMD)
    parser.add_argument("--probe-json", type=Path, default=None, help="Optional smoke probe JSON path.")
    parser.add_argument("--stress-json", type=Path, default=None, help="Optional stress probe JSON path.")
    parser.add_argument("--canvas-json", type=Path, default=None, help="Optional export-canvas probe JSON path.")
    parser.add_argument("--skip-gemini", action="store_true")
    parser.add_argument(
        "--strict-gemini",
        action="store_true",
        help="Fail the release gate when any Gemini advisory check fails.",
    )
    parser.add_argument("--report-file", type=Path, default=None)
    parser.add_argument("--timeout-seconds", type=int, default=220)
    return parser.parse_args()


def _safe_float(value: Any, fallback: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback


def _safe_int(value: Any, fallback: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return fallback


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON object expected: {path}")
    return payload


def _run_json_command(command: str) -> dict[str, Any]:
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    merged = "\n".join([result.stdout or "", result.stderr or ""]).strip()
    if result.returncode != 0:
        raise RuntimeError(f"Command failed ({result.returncode}): {command}\n{merged[-3000:]}")
    blob = extract_json_blob(merged)
    payload = json.loads(blob)
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object from command: {command}")
    return payload


def _artifact_path(*candidates: Any) -> str:
    for value in candidates:
        if isinstance(value, (list, tuple)):
            nested = _artifact_path(*value)
            if nested:
                return nested
            continue
        text = str(value or "").strip()
        if text and Path(text).exists():
            return text
    return ""


def _resolve_existing_path(path_text: str) -> Path | None:
    raw = str(path_text or "").strip()
    if not raw:
        return None
    path = Path(raw)
    if not path.is_absolute():
        path = (ROOT / path).resolve()
    if path.exists() and path.is_file():
        return path
    return None


def _stage_image_for_gemini(source_path: str, staging_dir: Path, check_id: str) -> str:
    source = _resolve_existing_path(source_path)
    if source is None:
        return ""
    suffix = source.suffix or ".png"
    safe_name = "".join(ch if ch.isalnum() or ch in {"-", "_"} else "_" for ch in check_id)
    target = staging_dir / f"{safe_name}{suffix.lower()}"
    shutil.copyfile(source, target)
    return str(target)


def evaluate_hard_checks(smoke: dict[str, Any], stress: dict[str, Any], canvas: dict[str, Any]) -> list[dict[str, Any]]:
    density = smoke.get("densityProbe", {}) if isinstance(smoke.get("densityProbe"), dict) else {}
    export_probe = smoke.get("exportProbe", {}) if isinstance(smoke.get("exportProbe"), dict) else {}
    export_style = smoke.get("exportStyleProbe", {}) if isinstance(smoke.get("exportStyleProbe"), dict) else {}
    support_events = export_probe.get("events") if isinstance(export_probe.get("events"), list) else []
    stress_summary = stress.get("summary", {}) if isinstance(stress.get("summary"), dict) else {}
    stress_export = stress.get("exportSnapshotProbe", {}) if isinstance(stress.get("exportSnapshotProbe"), dict) else {}
    canvas_probe = canvas.get("probe", {}) if isinstance(canvas.get("probe"), dict) else {}
    inline_wrap_probe = canvas.get("inlineWrapProbe", {}) if isinstance(canvas.get("inlineWrapProbe"), dict) else {}

    checks: list[dict[str, Any]] = []

    def add(check_id: str, ok: bool, detail: str, metric: Any = None) -> None:
        checks.append({"check_id": check_id, "status": "pass" if ok else "fail", "detail": detail, "metric": metric})

    add("smoke_ok", bool(smoke.get("ok")), "Smoke Playwright suite completed.", smoke.get("ok"))
    add("stress_ok", bool(stress.get("ok")), "Stress Playwright suite completed.", stress.get("ok"))
    add("export_canvas_guard_ok", bool(canvas.get("ok")), "Export canvas guard suite completed.", canvas.get("ok"))
    add("pdf_export_invoked", _safe_int(export_probe.get("saveCalls")) >= 1, "PDF save path invoked.", export_probe)
    add("print_export_invoked", _safe_int(export_probe.get("printCalls")) >= 1, "Generated-PDF print path invoked.", export_probe)
    add("support_prompt_twice", _safe_int(export_probe.get("supportPrompts")) >= 2, "Support prompt fired after PDF + print.", export_probe)
    if _safe_int(smoke.get("realPdfByteSize")) > 0:
        add("generated_pdf_non_empty", _safe_int(smoke.get("realPdfByteSize")) >= 1500, "Generated PDF blob size indicates non-empty export.", smoke.get("realPdfByteSize"))
    else:
        add("generated_pdf_non_empty", True, "Generated PDF size probe unavailable (skipped).", smoke.get("realPdfByteSize"))
    if support_events:
        first_save = support_events.index("save") if "save" in support_events else -1
        first_support = support_events.index("support") if "support" in support_events else -1
        last_print = len(support_events) - 1 - support_events[::-1].index("print") if "print" in support_events else -1
        support_after_print = any(event == "support" for event in support_events[last_print + 1 :]) if last_print >= 0 else False
        add("support_after_pdf_save", first_save >= 0 and first_support > first_save, "Support prompt appears after PDF save is triggered.", support_events)
        add("support_after_print", last_print >= 0 and support_after_print, "Support prompt appears after print is triggered.", support_events)
    else:
        add("support_after_pdf_save", True, "Support order probe unavailable (skipped).", support_events)
        add("support_after_print", True, "Support order probe unavailable (skipped).", support_events)
    add("export_controls_hidden", bool(export_style.get("controlsHidden")), "Export snapshot hides editing/resize controls.", export_style.get("controlsHidden"))
    add(
        "export_layout_stable",
        export_style.get("layoutStable") is not False,
        "Export snapshot keeps the same card geometry as edit mode.",
        export_style.get("layoutStable"),
    )
    add("export_header_compact", bool(export_style.get("compactHeader")), "Export snapshot header is compact.", export_style.get("compactHeader"))
    add("preview_icon_controls", bool(density.get("iconButtonsOnly")), "Preview edit controls are icon-only.", density.get("iconButtonsOnly"))
    add("preview_header_ratio", _safe_float(density.get("headerRatio"), 1.0) <= 0.2, "Preview header <= 20% of card height.", density.get("headerRatio"))
    add("export_header_ratio", _safe_float(export_style.get("headerRatio"), 1.0) <= 0.12, "Export header <= 12% of card height.", export_style.get("headerRatio"))

    add(
        "stress_scenarios_run",
        _safe_int(stress_summary.get("scenariosRun")) >= 10,
        "Stress suite ran enough scenarios.",
        stress_summary.get("scenariosRun"),
    )
    add(
        "stress_no_failed_scenarios",
        _safe_int(stress_summary.get("scenariosFailed")) == 0,
        "Stress scenarios produced no hard failures.",
        stress_summary.get("scenariosFailed"),
    )
    add(
        "stress_min_utilization",
        _safe_float(stress_summary.get("minOccupiedAreaRatio"), 0.0) >= 0.42,
        "Stress minimum occupied area ratio is acceptable.",
        stress_summary.get("minOccupiedAreaRatio"),
    )
    add(
        "stress_max_overlap",
        _safe_float(stress_summary.get("maxOverlapAreaRatio"), 1.0) <= 0.01,
        "Stress overlap ratio is bounded.",
        stress_summary.get("maxOverlapAreaRatio"),
    )
    add(
        "stress_out_of_bounds",
        _safe_int(stress_summary.get("maxOutOfBounds"), 99) == 0,
        "Stress scenarios keep cards inside page bounds.",
        stress_summary.get("maxOutOfBounds"),
    )
    add(
        "stress_export_controls_hidden",
        bool(stress_export.get("controlsHidden")),
        "Stress export snapshot hides controls.",
        stress_export.get("controlsHidden"),
    )
    add(
        "export_canvas_pages_detected",
        _safe_int(canvas_probe.get("pagesDetected")) >= 1,
        "Export canvas probe detected at least one rendered page.",
        canvas_probe.get("pagesDetected"),
    )
    add(
        "export_canvas_min_bbox_height_ratio",
        _safe_float(canvas_probe.get("minBBoxHeightRatio"), 0.0) >= 0.55,
        "Export canvas content spans enough vertical area to reject top-only clipping.",
        canvas_probe.get("minBBoxHeightRatio"),
    )
    add(
        "export_canvas_min_bottom_ink_ratio",
        _safe_float(canvas_probe.get("minBottomInkRatio"), 0.0) >= 0.02,
        "Export canvas keeps meaningful content in the lower page region.",
        canvas_probe.get("minBottomInkRatio"),
    )
    add(
        "export_inline_wrap_probe_ok",
        bool(inline_wrap_probe.get("ok")),
        "Wrapped inline-code export keeps adjacent plain text visible.",
        inline_wrap_probe,
    )
    add(
        "export_inline_style_parity_ok",
        bool(inline_wrap_probe.get("styleParityOk")),
        "Inline-code chip style remains consistent between preview and export mode.",
        inline_wrap_probe.get("styleMismatches"),
    )
    return checks


def _model_chain(args: argparse.Namespace) -> list[str]:
    chain = [args.model]
    if args.fallback_model and args.fallback_model != args.model:
        chain.append(args.fallback_model)
    return chain


def _run_gemini_json(prompt: str, chain: list[str], timeout_seconds: int) -> tuple[dict[str, Any], str]:
    last_error: Exception | None = None
    for model in chain:
        for _ in range(2):
            try:
                raw = run_gemini_cli(prompt, model=model, timeout_seconds=timeout_seconds, stderr_clip=800)
                parsed = json.loads(extract_json_blob(raw))
                if not isinstance(parsed, dict):
                    raise ValueError("Gemini output is not a JSON object.")
                return parsed, model
            except Exception as exc:  # noqa: BLE001
                last_error = exc
    raise RuntimeError(f"Gemini check failed after retries: {last_error}")


def _prompt_for_structured_check(check_id: str, payload: dict[str, Any]) -> str:
    return f"""
You are a strict QA micro-auditor.
Check ID: {check_id}
Input JSON:
{json.dumps(payload, ensure_ascii=False, indent=2)}

Return ONLY one JSON object with EXACT keys:
{{
  "check_id": "{check_id}",
  "status": "pass|warn|fail",
  "confidence": 0.0,
  "score": 0,
  "summary": "single sentence",
  "must_fix": ["up to 3 items"]
}}

Rules:
- If any `hard_failures` are present, status must be "fail".
- `score` must be 0-100 integer.
- `confidence` must be 0.0-1.0 float.
- No markdown fences, no extra keys.
""".strip()


def _prompt_for_image_check(check_id: str, screenshot_path: str, focus: str, hard_failures: list[dict[str, Any]]) -> str:
    return f"""
You are a strict visual QA micro-auditor.
Check ID: {check_id}
Focus: {focus}
Image: @{screenshot_path}

Return ONLY one JSON object with EXACT keys:
{{
  "check_id": "{check_id}",
  "status": "pass|warn|fail",
  "confidence": 0.0,
  "score": 0,
  "summary": "single sentence",
  "must_fix": ["up to 3 items"]
}}

Hard failures already detected:
{json.dumps(hard_failures, ensure_ascii=False)}

Rules:
- If image cannot be read, set status="fail" and include "CANNOT_READ_IMAGE" in summary.
- If any hard failures exist, status cannot be "pass".
- Judge wasted space, oversized chrome, and readability density for a cheat sheet.
- `score` must be 0-100 integer.
- `confidence` must be 0.0-1.0 float.
- No markdown fences, no extra keys.
""".strip()


def run_gemini_checks(
    smoke: dict[str, Any],
    stress: dict[str, Any],
    canvas: dict[str, Any],
    hard_checks: list[dict[str, Any]],
    args: argparse.Namespace,
) -> list[dict[str, Any]]:
    chain = _model_chain(args)
    hard_failures = [item for item in hard_checks if item["status"] == "fail"]
    results: list[dict[str, Any]] = []

    shared_payload = {
        "hard_failures": hard_failures,
        "smoke_density": smoke.get("densityProbe"),
        "smoke_export": smoke.get("exportStyleProbe"),
        "stress_summary": stress.get("summary"),
        "canvas_summary": canvas.get("probe"),
        "inline_wrap_probe": canvas.get("inlineWrapProbe"),
        "note": "Deterministic probes are primary evidence. Gemini adds secondary judgment.",
    }

    structured_checks = [
        ("density_auditor", {"focus": "space efficiency + information density"}),
        ("export_cleanliness_auditor", {"focus": "chrome removal in exported cheat sheet"}),
        ("protocol_completeness_auditor", {"focus": "whether evidence is sufficient and robust"}),
    ]
    for check_id, meta in structured_checks:
        prompt = _prompt_for_structured_check(check_id, {"check_meta": meta, **shared_payload})
        parsed, model_used = _run_gemini_json(prompt, chain, args.timeout_seconds)
        results.append(_normalize_gemini_result(parsed, check_id, model_used))

    image_checks = [
        (
            "preview_image_density_auditor",
            _artifact_path(smoke.get("previewArtifactPath"), smoke.get("screenshotPath")),
            "Preview mode screenshot: verify compact controls and no large wasted zones inside cards.",
        ),
        (
            "export_image_cleanliness_auditor",
            _artifact_path(smoke.get("exportArtifactPath"), smoke.get("exportScreenshotPath")),
            "Export snapshot screenshot: verify no edit/delete/resize chrome and efficient layout.",
        ),
        (
            "stress_worstcase_image_auditor",
            _artifact_path(
                stress.get("summary", {}).get("worstByUtilization", {}).get("screenshotPath"),
                stress.get("exportSnapshotProbe", {}).get("screenshotPath"),
            ),
            "Stress-case screenshot: check that layout remains dense and readable without dead space.",
        ),
        (
            "export_canvas_clip_auditor",
            _artifact_path(
                canvas.get("primaryArtifactPath"),
                *canvas.get("artifactPaths", []),
            ),
            "Rendered export-canvas image: fail if content is visibly clipped to top or missing lower-page content.",
        ),
        (
            "export_inline_wrap_text_auditor",
            _artifact_path(canvas.get("inlineWrapArtifactPath"), canvas.get("inlineWrapProbe", {}).get("artifactPath")),
            "Wrapped inline-code export image: verify plain text around inline code remains visible and is not replaced by one monolithic code bubble.",
        ),
    ]
    with tempfile.TemporaryDirectory(prefix="gemini_vision_", dir=ROOT) as tmp_dir:
        staging_dir = Path(tmp_dir)
        for check_id, screenshot_path, focus in image_checks:
            staged_path = _stage_image_for_gemini(screenshot_path, staging_dir, check_id)
            if not staged_path:
                results.append(
                    {
                        "check_id": check_id,
                        "status": "fail",
                        "confidence": 1.0,
                        "score": 0,
                        "summary": "CANNOT_READ_IMAGE missing or inaccessible screenshot path.",
                        "must_fix": ["Ensure screenshot artifact path is available in probes."],
                        "model": "none",
                    }
                )
                continue
            prompt = _prompt_for_image_check(check_id, staged_path, focus, hard_failures)
            parsed, model_used = _run_gemini_json(prompt, chain, args.timeout_seconds)
            results.append(_normalize_gemini_result(parsed, check_id, model_used))

    return results


def _normalize_gemini_result(parsed: dict[str, Any], check_id: str, model_used: str) -> dict[str, Any]:
    status = str(parsed.get("status") or "").strip().lower()
    if status not in {"pass", "warn", "fail"}:
        raise ValueError(f"{check_id}: invalid status {status!r}")
    return {
        "check_id": check_id,
        "status": status,
        "confidence": _safe_float(parsed.get("confidence"), 0.0),
        "score": _safe_int(parsed.get("score"), 0),
        "summary": str(parsed.get("summary") or "").strip(),
        "must_fix": [str(item).strip() for item in parsed.get("must_fix", []) if str(item).strip()],
        "model": model_used,
    }


def _is_critical_gemini_failure(check: dict[str, Any]) -> bool:
    if str(check.get("status") or "").lower() != "fail":
        return False
    summary = str(check.get("summary") or "").upper()
    return "CANNOT_READ_IMAGE" in summary


def _report_path(explicit: Path | None) -> Path:
    if explicit is not None:
        explicit.parent.mkdir(parents=True, exist_ok=True)
        return explicit
    DEFAULT_REPORT_DIR.mkdir(parents=True, exist_ok=True)
    return DEFAULT_REPORT_DIR / "gemini_ui_test_report.json"


def main() -> None:
    args = parse_args()
    smoke = _read_json(args.probe_json) if args.probe_json else _run_json_command(args.smoke_cmd)
    stress = _read_json(args.stress_json) if args.stress_json else _run_json_command(args.stress_cmd)
    canvas = _read_json(args.canvas_json) if args.canvas_json else _run_json_command(args.canvas_cmd)

    hard_checks = evaluate_hard_checks(smoke, stress, canvas)
    gemini_checks: list[dict[str, Any]] = []
    if not args.skip_gemini:
        gemini_checks = run_gemini_checks(smoke, stress, canvas, hard_checks, args)

    hard_failures = [item for item in hard_checks if item["status"] == "fail"]
    gemini_failures = [item for item in gemini_checks if item["status"] == "fail"]
    gemini_critical_failures = [item for item in gemini_failures if _is_critical_gemini_failure(item)]

    release_gate_failed = bool(hard_failures or gemini_critical_failures)
    if args.strict_gemini and gemini_failures:
        release_gate_failed = True

    if release_gate_failed:
        overall_status = "fail"
    elif gemini_failures:
        overall_status = "warn"
    else:
        overall_status = "pass"

    release_gate_status = "fail" if release_gate_failed else "pass"

    report = {
        "timestamp_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "models": {
            "primary": args.model,
            "fallback": args.fallback_model,
            "gemini_skipped": bool(args.skip_gemini),
            "strict_gemini": bool(args.strict_gemini),
        },
        "smoke_probe": smoke,
        "stress_probe": stress,
        "export_canvas_probe": canvas,
        "hard_checks": hard_checks,
        "gemini_checks": gemini_checks,
        "summary": {
            "overall_status": overall_status,
            "release_gate_status": release_gate_status,
            "hard_failures": len(hard_failures),
            "gemini_failures": len(gemini_failures),
            "gemini_critical_failures": len(gemini_critical_failures),
            "smoke_source": str(args.probe_json) if args.probe_json else args.smoke_cmd,
            "stress_source": str(args.stress_json) if args.stress_json else args.stress_cmd,
        },
    }

    report_path = _report_path(args.report_file)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"overall_status": overall_status, "report_file": str(report_path)}, ensure_ascii=False))
    if release_gate_status != "pass":
        raise SystemExit(1)


if __name__ == "__main__":
    main()

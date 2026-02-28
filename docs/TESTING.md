# Testing and Validation

## One-command validation

```bash
make validate
```

This runs:

1. JavaScript syntax checks (`node --check` on `app/*.js`)
2. Python compile checks (`python3 -m py_compile` on entrypoints + `pipelines/`)
3. File-length policy check (`python3 scripts/check_file_lengths.py`)
4. Unit/integration tests (`python3 -m unittest discover -s tests -v`)

## Individual commands

```bash
make check-js
make check-py
make check-lines
make test
make maintenance-audit
make leave-better
make leave-better-ui
make smoke-ui
make stress-layout-ui
make gemini-benchmark
make gemini-prompt-experiments
make gemini-health
make quality-dashboard
```

## Maintenance Audit

```bash
make maintenance-audit
```

Runs `scripts/maintenance_audit.py` and writes:

- `data/test_reports/maintenance_audit.json`

Checks covered:

- code line-length hygiene (soft target: 300, hard fail: 500)
- TODO/FIXME/HACK/XXX drift
- topic-card duplicate-risk signals
- study DB week/source integrity
- Gemini model alias centralization
- maintenance docs presence

## Gemini Capability Benchmark

```bash
make gemini-benchmark
```

Runs `scripts/gemini_capability_benchmark.py` and writes:

- `data/test_reports/gemini_capability_benchmark.json`

Coverage:

- strict JSON contract adherence
- function generation under evaluator tests
- image understanding with structured JSON outputs
- constrained formatting/reasoning output

Use this for quick model-level health checks before/after Gemini CLI/model changes.

## Gemini Prompt Experiments

```bash
make gemini-prompt-experiments
```

Runs `scripts/gemini_prompt_experiments.py` and writes:

- `data/test_reports/gemini_prompt_experiments.json`

Coverage:

- prompt-variant A/B tests for code-generation delegation
- trial pass-rate + latency comparisons by variant/task/model
- failure-kind distribution (`timeout`, `quota`, `banned_token`, behavior mismatch)
- recommended prompt variant per task

Use strict mode for gating:

```bash
python3 scripts/gemini_prompt_experiments.py --strict
```

## Gemini Model Health

```bash
make gemini-health
```

Runs `scripts/gemini_model_health.py` and writes:

- `data/test_reports/gemini_model_health.json`

Coverage:

- model availability probe for configured aliases/fallbacks
- strict JSON contract sanity check per model
- error-kind classification (`quota`, `timeout`, `auth`, `network`, `api_error`)
- recommended currently-available primary/fallback model

Use this before expensive Gemini-heavy pipelines.

## Quality Dashboard

```bash
make quality-dashboard
```

Runs `scripts/quality_dashboard.py` and writes:

- `data/test_reports/quality_dashboard.json`

Coverage:

- aggregates maintenance + Gemini reports into one status
- freshness checks for report staleness
- suggested follow-up actions based on failures/warnings

Strict mode:

```bash
python3 scripts/quality_dashboard.py --strict
```

## Gemini QA Protocol (Automated)

```bash
make gemini-ui-protocol
```

This runs `scripts/gemini_test_protocol.py`:

1. Runs `make smoke-ui` to generate deterministic UI/export probes and screenshots.
2. Runs `make stress-layout-ui` to execute exhaustive layout scenarios (auto/manual grid + typography/spacing extremes).
3. Applies hard pass/fail gates (export chrome hidden, compact header, support prompt hook, print/export flow invoked, stress overlap/bounds/utilization checks).
4. Runs multiple small Gemini micro-audits (strict JSON schema per check):
   - `density_auditor`
   - `export_cleanliness_auditor`
   - `protocol_completeness_auditor`
   - `preview_image_density_auditor` (real screenshot input)
   - `export_image_cleanliness_auditor` (real screenshot input)
   - `stress_worstcase_image_auditor` (real screenshot input)
5. Writes reports:
   - `data/test_reports/gemini_ui_test_report.json`

Protocol status semantics:

- `summary.release_gate_status=fail` means deterministic hard gates failed (or critical Gemini infrastructure issues like unreadable images).
- `summary.overall_status=warn` means deterministic gates passed but Gemini advisory checks flagged issues.
- `summary.overall_status=pass` means both deterministic gates and Gemini advisory checks are clean.

Default model chain (quality-first):

- primary (`SMART_GEMINI_AGENT`): `gemini-3-pro-preview`
- fallback (`SMART_GEMINI_AGENT_FALLBACK`): `gemini-3-flash-preview`

Override when needed:

```bash
python3 scripts/gemini_test_protocol.py --model gemini-2.5-pro --fallback-model gemini-2.5-flash
```

## UI Smoke Test (Headless)

```bash
make smoke-ui
```

This runs `scripts/smoke_ui_playwright.js` in an isolated temporary Playwright environment (`/tmp/pwtmp`) and verifies:

- app boot + data load
- splash dismissal
- accept action increments counters
- preview renders cards
- preview card lock blocks accidental drag/resize
- preview item edit (modal path) + in-field keyboard undo (`Ctrl+Z`) before save
- preview item delete + undo restore
- preview delete + undo restore flow
- real generated PDF blob is non-empty (guards blank export regressions)
- PDF export button flow + support prompt callback (must trigger after save path)
- generated-PDF print flow + support prompt callback (must trigger after print path)
- export snapshot hides edit/resize controls
- export snapshot uses compact card headers (space-efficient)

## Playwright Workaround Protocol (No Project Node Setup Required)

If Playwright is not available in your shell/project environment, run the same smoke script via an isolated temp install:

```bash
mkdir -p /tmp/pwtmp
npm install --prefix /tmp/pwtmp playwright --silent
/tmp/pwtmp/node_modules/.bin/playwright install chromium
NODE_PATH=/tmp/pwtmp/node_modules node scripts/smoke_ui_playwright.js
```

Why this exists:

- avoids adding Playwright as a persistent project dependency
- keeps CI/local checks reproducible for agents and contributors
- allows browser regression checks in restricted repos

## Gemini Image Input

Gemini image checks use direct file attachments in prompts (`@/path/to/image.png`).
Because `data/test_reports/**` is gitignored (and Gemini may block ignored files), the protocol stages screenshots into a temporary non-ignored workspace folder before each image audit.

Protocol strategy:

- Playwright still collects deterministic probes (primary truth source).
- Gemini receives both probes and staged attached screenshots for micro-audits.
- Hard deterministic gates stay authoritative so weak model responses cannot silently pass regressions.

Quick CLI sanity check for image understanding:

```bash
cp data/test_reports/artifacts/smoke-export-preview.png tmp_gemini_vision_test.png
gemini -m gemini-3-pro-preview -p "Respond with exactly image_ok if you can read @tmp_gemini_vision_test.png"
python3 - <<'PY'
import os
if os.path.exists("tmp_gemini_vision_test.png"):
    os.remove("tmp_gemini_vision_test.png")
PY
```

## Under-Tested Area Protocols

Use these targeted protocols when touching export or ingestion logic.

### 1) Preview Editing Safety Protocol

1. `make smoke-ui`
2. Confirm script validates:
   - an editable preview item can be edited
   - in-modal text undo (`Ctrl+Z`) remains local to the input and is not intercepted by preview undo
   - preview keyboard undo restores edited content after save
   - preview item delete reduces item count
   - undo restores the deleted item
   - card delete and undo round-trip

### 2) Export + Support Prompt Protocol

1. `make smoke-ui`
2. Confirm script validates:
   - PDF export path is invoked
   - generated-PDF print path is invoked
   - support prompt hook fires after both actions and only after save/print was triggered
   - generated PDF blob is non-empty (rejects near-empty/blank-output regressions)
   - export snapshot does not show edit/remove/resize chrome
   - export snapshot header is compact
3. Perform visual check on `data/test_reports/artifacts/smoke-export-preview.png`:
   - no obvious wasted space in cards (oversized headers, oversized action bars, wide unused gaps)
   - no resize handles or edit/delete controls are visible in exported view

### 3) Exhaustive Layout Stress Protocol

```bash
make stress-layout-ui
```

This validates across multiple scenario variants:

- no out-of-bounds cards
- bounded overlap ratio
- minimum occupied-area ratio (anti-dead-space)
- compact headers under stress configurations
- per-scenario screenshots in `data/test_reports/artifacts/stress/`

### 4) Week Ingestion Safety Protocol

```bash
python3 -m unittest tests/test_add_week_material_script.py -v
```

This validates:

- `--dry-run` does not modify `data/study_db.json`
- missing `sources` fail fast without `--allow-missing-sources`
- missing `sources` are permitted when flag is explicitly set
- curation/validation report is written with expected flags

## Test coverage areas

- `tests/test_file_length_policy.py`: enforces max 500 lines per code file.
- `tests/test_topic_cards_integrity.py`: ID uniqueness + section/recommended-id integrity.
- `tests/test_study_db_integrity.py`: canonical study DB shape + source-path integrity checks.
- `tests/test_week_payload_validators.py`: ingestion payload preflight validation checks.
- `tests/test_add_week_material_script.py`: add-week script integration checks (`dry-run`, missing sources, report output).
- `tests/test_gemini_test_protocol.py`: deterministic gate behavior for `scripts/gemini_test_protocol.py`.
- `tests/test_gemini_prompt_experiments.py`: evaluator/summary logic for Gemini prompt-variant experiments.
- `tests/test_gemini_playbook.py`: playbook metadata/model/report references stay documented.
- `tests/test_gemini_model_health.py`: model-health error parsing, JSON contract, and recommendation logic.
- `tests/test_quality_dashboard.py`: aggregated quality dashboard status/freshness behavior.
- `tests/test_maintenance_audit.py`: maintenance-audit coverage and model-alias/doc-system checks.
- `tests/test_roadmap_specs.py`: roadmap hygiene (IDs/status/spec links).
- `tests/test_detail_rules.py`: key enrichment rule sanity and shape checks.
- `tests/test_js_syntax.py`: JS parsing safety for all app modules.

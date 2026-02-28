# Gemini Playbook (Evidence-Based)

Last updated: 2026-02-28 (UTC)  
Gemini CLI version tested: `0.30.1` (`gemini --version`)  
Model aliases (single source of truth): `pipelines/shared/model_defaults.py`

- `fast gemini agent` = `gemini-3-flash-preview`
- `smart gemini agent` = `gemini-3-pro-preview`

## Evidence Artifacts

- Capability benchmark: `data/test_reports/gemini_capability_benchmark.json` (timestamp `2026-02-28T00:04:11Z`)
- Prompt-variant experiments: `data/test_reports/gemini_prompt_experiments.json` (timestamp `2026-02-28T00:00:12Z`)
- UI protocol (hard gates + Gemini micro-audits): `data/test_reports/gemini_ui_test_report.json`
- Model health gate: `data/test_reports/gemini_model_health.json`
- Aggregated quality view: `data/test_reports/quality_dashboard.json`

## What Gemini Does Well (In This Project)

- Strict JSON output when asked for exact keys and no extra text.
- Fast micro-audits on narrow tasks (density/readability checks, single-check rubrics).
- Small function generation when the prompt includes exact signature, behavior rules, and edge cases.
- Basic image understanding for layout-level cues (header controls present, density low/medium/high).

## Where Gemini Is Weak / Risky

- Prompt looseness: minimal prompts can timeout or drift in format.
- Code-generation policy drift: can add imports (`import re`) unless explicitly forbidden.
- Model availability risk: `gemini-3-pro-preview` may fail due quota/capacity; runs showed repeated `TerminalQuotaError`.
- Vision responses can include extra prose unless strict JSON extraction is enforced.

## Prompting Patterns That Worked Best

Use this pattern for agent tasks:

1. Hard output contract:
   - `Return ONLY valid JSON with EXACT keys ...`
   - or `Return ONLY raw Python code, no markdown, no explanation`
2. Explicit constraints:
   - banned operations (`Do NOT use imports`)
   - exact function name/signature
3. Edge-case examples in prompt:
   - include 1-3 concrete I/O examples
4. Deterministic post-check:
   - parse JSON / run function tests / schema-validate output

Observed result from prompt experiments:

- `v1_minimal` was least reliable (timeouts on both models).
- `v2_strict_output` and `v3_strict_with_examples` reached 100% pass rate in sampled trials.
- `v2` was usually faster; `v3` can improve stability for trickier logic.

## Delegation Policy (CEO Mode)

1. Route by task criticality:
   - Use `fast gemini agent` for repetitive, narrow, structured tasks.
   - Use `smart gemini agent` only for high-judgment tasks (when available).
2. Always keep Codex in the loop for merge gates:
   - schema migrations
   - data integrity / dedup logic
   - security-sensitive code
   - UX/export behavior changes
3. Force machine-verifiable outputs:
   - JSON schema checks
   - unit tests
   - deterministic smoke/stress probes
4. Auto-fallback strategy:
   - on smart-model quota/capacity failure, fall back to fast model for first draft
   - require Codex review before accepting fallback output for critical paths

## Practical Task Routing

- Good Gemini delegation candidates:
  - write pure utility functions from exact spec
  - classify screenshots with strict rubric JSON
  - generate candidate summaries/snippets for later review
- Codex-supervised only:
  - architecture refactors
  - DB schema and migration logic
  - final curation decisions and conflict resolution
  - anything with flaky model evidence

## Known Gaps (Not Fully Automated Yet)

- Long-horizon semantic quality of generated educational explanations still needs human review.
- Cross-week conceptual dedup quality is partially automated, not fully semantic.
- Smart-model quality comparison is currently availability-limited by quota in this environment.

## Recommended Commands

```bash
make gemini-health
make gemini-benchmark
make gemini-prompt-experiments
make gemini-ui-protocol
make quality-dashboard
```

For a strict delegation gate on function-writing reliability:

```bash
python3 scripts/gemini_prompt_experiments.py --strict
```

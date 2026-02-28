# Maintenance Protocol (Leave It Better)

This project follows a camping rule:
after every task, leave the codebase cleaner and more maintainable than before.

## Goals

- Make future tasks easier for humans and agents.
- Keep quality high without relying on memory or heroics.
- Ensure each completed task includes at least one meaningful improvement beyond the asked change.

## Mandatory Agent Workflow

For every feature/fix/content ingestion task:

1. Implement the requested change.
2. Perform one "leave-it-better" improvement from at least one category below.
3. Run validation relevant to the touched area.
4. Update docs/roadmap/specs if behavior or architecture changed.
5. Report what was improved and what remains.

## Leave-It-Better Categories

Pick at least one per task:

- QoL: small UX improvement that reduces friction.
- Testing: add/expand tests or harden the automated protocol.
- Structure: move/split code to improve clarity and ownership boundaries.
- Reliability: fix a nearby bug/risk discovered during implementation.
- Documentation: align README/AGENTS/testing docs with new reality.
- Data quality: detect/remove duplicates or consistency drift.
- Planning: add roadmap/spec entry for uncovered bigger issues.

## Decision Rules

- If you find an issue but cannot solve it in-scope, add it to [ROADMAP](./ROADMAP.md) with a spec link.
- If you change any command/process used by contributors, update [README](../README.md), [AGENTS](../AGENTS.md), and [TESTING](./TESTING.md).
- If you touch UI/export behavior, run smoke + stress tests and keep screenshots current.

## Required Commands

Base:

```bash
make leave-better
```

UI-impacting tasks:

```bash
make leave-better-ui
```

Maintenance audit only:

```bash
make maintenance-audit
```

Strict mode (for cleanup drives):

```bash
python3 scripts/maintenance_audit.py --strict-warnings
```

## Artifacts

- Maintenance report: `data/test_reports/maintenance_audit.json`
- Gemini UI protocol report: `data/test_reports/gemini_ui_test_report.json`
- Visual artifacts: `data/test_reports/artifacts/`

## Human-Friendly Maintenance Prompts

Examples you can give an agent:

- "Here are new week files, integrate them and leave it better."
- "Add feature X, and do one QoL + one testing improvement."
- "Run a cleanup pass: strict maintenance audit, roadmap updates, and any low-risk fixes."

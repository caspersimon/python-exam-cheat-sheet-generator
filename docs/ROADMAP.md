# Roadmap

Backlog of larger improvements that should be tracked even when not solved in the same task.

## Status Legend

- `planned`: approved idea, not started
- `in_progress`: actively being worked
- `blocked`: needs prerequisite/decision
- `done`: shipped

## Active Items

| ID | Priority | Status | Area | Summary | Spec |
|---|---|---|---|---|---|
| RM-001 | High | planned | Preview layout | Auto-fit card heights to content to reduce dead space without manual resize. | [RM-001](./specs/RM-001-card-auto-fit-heights.md) |
| RM-002 | Medium | planned | Layout automation | Add optional "repack cards" action that optimizes density while preserving readability. | [Template](./specs/SPEC_TEMPLATE.md) |
| RM-003 | Medium | planned | QA automation | Add baseline visual diff checks (perceptual threshold) on smoke/stress export snapshots. | [Template](./specs/SPEC_TEMPLATE.md) |
| RM-004 | Medium | planned | Data quality | Add semantic duplicate detection for week ingestion (beyond exact-string duplicates). | [Template](./specs/SPEC_TEMPLATE.md) |
| RM-005 | Medium | planned | Codebase hygiene | Reduce >300-line files to improve readability and maintenance velocity. | [Template](./specs/SPEC_TEMPLATE.md) |

## Triage Rules

- Add an item when an issue is real but too large/off-scope for the current task.
- Every roadmap item must have a spec (or template placeholder).
- When marking `done`, include the commit/PR reference in the spec.

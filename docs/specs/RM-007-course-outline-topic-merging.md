# Spec: RM-007 Course-Outline Topic Merging

## Metadata

- ID: `RM-007`
- Status: `planned`
- Priority: `Medium`
- Owner: `codex/human`
- Last Updated: `2026-03-21`

## Problem

The Topic Explorer now groups granular cards under the course-outline structure, which makes the sidebar much easier to scan. However, the underlying dataset is still intentionally fine-grained, so some course-outline groups still contain many closely related cards (for example function-argument variants or dictionary-comprehension variants).

## Goals

- Identify high-overlap topic clusters that should become single course-facing cards.
- Preserve strong exam evidence, recommended snippet IDs, and key-point detail coverage while merging.
- Reduce sidebar/card sprawl without regressing preview selection quality.

## Non-Goals

- Rebuild the entire generation pipeline.
- Force every course chapter into the same number of cards.

## Proposed Solution

Run a focused manual curation pass on the highest-overlap groups that remain dense even after course-outline grouping. Start with week 2 dictionaries, week 3 function arguments/scope, and week 6 comprehension variants. For each candidate cluster, keep one anchor card ID where possible, merge evidence deliberately, and revalidate recommended snippet IDs plus exam stats after each batch.

## Implementation Plan

1. Export a merge candidate audit grouped by course-outline bucket and exam-hit count.
2. Curate one dense bucket at a time using `docs/curation/TOPIC_MERGING_GUIDELINES.md`.
3. Re-run integrity checks plus UI validation after each merge batch.

## Risks and Mitigations

- Risk: Over-merging could create bloated cards that are harder to use in the preview.
- Mitigation: Cap merges to conceptually tight clusters and keep item-level selection unchanged.
- Risk: Manual merges could break `recommended_ids` or global uniqueness.
- Mitigation: Run integrity validation after each batch and preserve anchor IDs when practical.

## Test Plan

- Unit tests: none expected initially; validate data integrity scripts instead.
- Integration tests: run JSON integrity checks and syntax sanity checks for generated examples/details.
- UI/visual tests: verify grouped sidebar counts, topic detail rendering, and preview selection still work.
- Manual checks: confirm merged cards still read cleanly and do not create empty preview cards.

## Rollout and Validation

- Commands to run:
  - `make leave-better`
  - `make leave-better-ui`
- Success criteria:
  - Fewer dense clusters inside the course-outline groups.
  - No duplicate IDs or broken `recommended_ids`.
  - No regressions in Topic Explorer rendering or preview generation.

## Open Questions

- Which dense groups should be merged first based on actual student value rather than raw overlap count?
- Should some groups stay granular in the data model but render as a single “course topic” card in the UI?

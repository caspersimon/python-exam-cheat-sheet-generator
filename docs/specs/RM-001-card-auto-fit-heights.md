# Spec: RM-001 Card Auto-Fit Heights

## Metadata

- ID: `RM-001`
- Status: `in_progress`
- Priority: `High`
- Owner: `unassigned`
- Last Updated: `2026-03-25`

## Problem

Cards can reserve more vertical space than their content requires. This creates dead space and lowers information density, especially in mixed-content sheets where some cards have fewer selected details.

## Goals

- Automatically shrink card height to fit actual content when feasible.
- Preserve manual resize/drag behavior and user intent.
- Keep export/print geometry identical to preview.

## Non-Goals

- Rewriting the entire preview layout engine.
- Perfect bin-packing optimization in this iteration.

## Proposed Solution

- Introduce an optional auto-fit pass after render that measures each card's content height and applies a tighter minimum height.
- Respect user-resized cards by storing a "manual size lock" flag per card.
- Keep existing minimum size guardrails for usability/accessibility.
- Re-run overlap detection after auto-fit and avoid introducing collisions.
- Extend auto-fit with width-aware placement (multi-column spans) so code/table-heavy snippets can claim more width and reduce vertical clipping.
- Let Smart Fit tune the full layout control surface (font/line-height/padding/gaps/table size/title spacing) via plan scoring instead of static thresholds.

## Implementation Plan

1. Add per-card metadata for `manualSizeLocked`.
2. Add measurement helper in preview render pipeline (`scrollHeight` + header/actions allowance).
3. Apply auto-fit to unlocked cards only.
4. Add stress checks to ensure no out-of-bounds/overlap regressions.
5. Add Gemini visual checks focused on dead-space reduction.

## Risks and Mitigations

- Risk: Frequent re-measurement could cause jank.
- Mitigation: Run auto-fit only on render checkpoints and debounce operations.

- Risk: Auto-fit could conflict with drag/resize persistence.
- Mitigation: Skip auto-fit for cards manually resized by user.

## Test Plan

- Unit tests:
  - Auto-fit height computation for short/long content blocks.
  - Lock behavior for manually resized cards.
- Integration tests:
  - Preview render retains card positions while shrinking unlocked heights.
- UI/visual tests:
  - `make smoke-ui`
  - `make stress-layout-ui`
  - `make gemini-ui-protocol`
- Manual checks:
  - Verify cards with sparse content no longer have excessive whitespace.

## Rollout and Validation

- Commands:
  - `make leave-better-ui`
- Success criteria:
  - No overlap/bounds regressions.
  - Visible reduction in dead space on mixed-content sheets.

## Open Questions

- Should auto-fit be always on or user-toggleable?
- Should we expose a "compact vs readable" Smart Fit intent toggle for users who prefer predictable density targets?

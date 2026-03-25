# HANDOFF

> [!summary] What this package is for
> Production-oriented content dataset for the cheat-sheet builder frontend.

## Key implementation notes

1. **Use SQLite or TSV for metadata**, but render piece bodies from the `content/` directory.
2. A snippet card should load:
   - snippet metadata from `snippets`
   - piece rows from `pieces`
   - markdown bodies via each piece's `body_path`
3. Respect `ui_section_*` for grouping cards inside a subtopic.
4. Respect `default_selected` at piece level and `default_priority` at snippet level when building starter presets.

## Recommended frontend behavior

- show snippet summary on the card
- allow expand/collapse to preview all pieces
- allow per-piece selection toggles
- show trap-heavy snippets with a small badge when `is_trap_heavy = 1`
- optionally show recurrence as a badge: `signature`, `very-common`, `common`, `occasional`, `rare`

## Presets

Current preset IDs:

- `balanced-default`
- `post-midterm-tilted`
- `ultra-dense-core`
- `trap-hunter`
- `max-coverage-v2`

## V2-specific notes

- V2 adds **legacy backup coverage** but keeps the same overall structure.
- The new low-frequency material is intentionally parked in either:
  - dedicated backup snippets, or
  - optional clarifier / trap pieces in existing snippets.
- Do not surface all optional clarifiers by default; the whole point is selective inclusion.

## Search / discoverability suggestions

Use these metadata sources together:

- snippet title
- snippet summary
- `snippet_keywords.tsv`
- trap labels from `trap_catalog.tsv`
- topic / subtopic labels

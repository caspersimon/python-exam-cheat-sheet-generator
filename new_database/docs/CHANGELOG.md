# V2 changelog

> [!summary] Goal
> Integrate the strongest content from the older dataset **without** falling back into a bloated or redundant structure.

## New snippets

| Snippet | Why it was added |
|---|---|
| `syntax-fragments-escapes-raw-strings` | restores exact-syntax reminders for comments, raw strings, escapes, and tiny fragment-reading questions |
| `names-aliasing-and-copies` | restores name-binding / aliasing / copy logic that explains many “why did this change?” mistakes |
| `numeric-corner-cases` | restores negative `//`, `%`, float precision, and order-sensitive equality edge cases |
| `loop-control-and-iterators` | restores `break`, `continue`, `iter()`, and `next()` backup coverage |
| `pandas-missing-values-alignment` | restores `fillna`, `dropna`, and index-alignment gotchas |
| `oop-inheritance-core` | restores inheritance / `super()` / parent-child type relationships |

## Existing snippets extended

- `membership-and-condition-logic` — ternary / branch-order / per-element filtering / mixed-type compare reminder
- `defaults-keyword-arguments` — mutable default trap piece
- `case-and-capitalization` — `strip`, `lstrip`, `rstrip`, `isdigit` reminder
- `fstrings-and-format` — debug `f'{var=}'` piece
- `datetime-strptime-strftime` — object-vs-string mental model
- `datetime-build-from-parts` — direct attributes plus `replace()` returns new datetime
- `oop-state-and-collection-attributes` — class vs instance attribute piece

## Structural upgrades

- the package now ships the actual `content/` markdown files for every piece
- added a `max-coverage-v2` preset
- added a `legacy_integration_map.tsv` export and `LEGACY_INTEGRATION.md`
- expanded exports to include topics, subtopics, keywords, traps, and navigation plan

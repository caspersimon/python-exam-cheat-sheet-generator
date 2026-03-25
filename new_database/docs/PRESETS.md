# Presets

> [!summary] Preset philosophy
> Presets are meant as **good starting packs**, not final answers. Students should still deselect what they already know and add clarifiers where they personally need them.

## Balanced default

> [!summary] Broad starter pack for a student with little pre-existing knowledge.

- preset id: `balanced-default`
- target user: minimal prior knowledge, wants broad coverage
- snippet count: **42**
- piece count: **94**
- estimated chars: **22724**

Includes most high-priority snippets, all default-selected pieces, and a few clarifiers for recurring exact exam patterns.

Top included snippets by piece count:
- `datetime-sequence-generation` — Date sequences (3 pieces)
- `datetime-overlap-logic` — Overlap logic (3 pieces)
- `datetime-strptime-strftime` — strptime() and strftime() (3 pieces)
- `pandas-loc-iloc` — loc vs iloc (3 pieces)
- `pandas-map-vs-apply` — map() vs apply() (3 pieces)
- `split-join-replace` — split(), join(), replace() (3 pieces)
- `zip-enumerate-core` — zip() and enumerate() core patterns (3 pieces)
- `oop-compare-and-report-patterns` — Compare/report method patterns (3 pieces)
- `oop-init-self-defaults` — __init__, self, defaults, attributes (3 pieces)
- `fstrings-and-format` — f-strings and .format() (3 pieces)

## Post-midterm tilted

> [!summary] Weights strings, pandas, datetime, and OOP while still keeping a small pre-midterm rescue layer.

- preset id: `post-midterm-tilted`
- target user: expects the final to skew toward later-course material
- snippet count: **32**
- piece count: **75**
- estimated chars: **18239**

Good default when space is tight but you still want coverage for the most likely post-midterm traps.

Top included snippets by piece count:
- `datetime-strptime-strftime` — strptime() and strftime() (4 pieces)
- `oop-state-and-collection-attributes` — Object state and collection attributes (4 pieces)
- `datetime-overlap-logic` — Overlap logic (3 pieces)
- `datetime-build-from-parts` — Build datetimes from parts (3 pieces)
- `oop-compare-and-report-patterns` — Compare/report method patterns (3 pieces)
- `fstrings-and-format` — f-strings and .format() (3 pieces)
- `oop-init-self-defaults` — __init__, self, defaults, attributes (3 pieces)
- `datetime-sequence-generation` — Date sequences (3 pieces)
- `pandas-loc-iloc` — loc vs iloc (3 pieces)
- `pandas-map-vs-apply` — map() vs apply() (3 pieces)

## Ultra-dense core

> [!summary] Only the highest-yield snippets and their default-selected pieces.

- preset id: `ultra-dense-core`
- target user: very limited space, wants maximum points per line
- snippet count: **21**
- piece count: **43**
- estimated chars: **10354**

Best for students who already remember the basics and want a compact safety net.

Top included snippets by piece count:
- `oop-init-self-defaults` — __init__, self, defaults, attributes (3 pieces)
- `datetime-timedelta-day-counts` — timedelta and day counts (2 pieces)
- `dict-build-count-aggregate` — Build, count, and aggregate dictionaries (2 pieces)
- `dict-comprehension-patterns` — Dictionary comprehension patterns (2 pieces)
- `datetime-strptime-strftime` — strptime() and strftime() (2 pieces)
- `dict-iteration-equality` — Dictionary iteration and equality (2 pieces)
- `list-comprehension-patterns` — List comprehension patterns (2 pieces)
- `mcq-elimination-checklist` — MCQ elimination checklist (2 pieces)
- `local-vs-global-scope` — Local vs global scope (2 pieces)
- `mutation-vs-return` — Mutation vs return value (2 pieces)

## Trap hunter

> [!summary] Focused on the recurrent wrong-answer patterns and elimination traps.

- preset id: `trap-hunter`
- target user: knows the material somewhat, mainly loses points to subtle distractors
- snippet count: **23**
- piece count: **51**
- estimated chars: **12831**

Emphasizes mutation-vs-return, pandas shape traps, scope, parse/format, and method-call gotchas.

Top included snippets by piece count:
- `builtins-return-values` — Built-ins and what they return (3 pieces)
- `datetime-overlap-logic` — Overlap logic (3 pieces)
- `datetime-strptime-strftime` — strptime() and strftime() (3 pieces)
- `oop-init-self-defaults` — __init__, self, defaults, attributes (3 pieces)
- `pandas-loc-iloc` — loc vs iloc (3 pieces)
- `membership-and-condition-logic` — Membership and condition logic (3 pieces)
- `mcq-elimination-checklist` — MCQ elimination checklist (3 pieces)
- `split-join-replace` — split(), join(), replace() (3 pieces)
- `local-vs-global-scope` — Local vs global scope (2 pieces)
- `find-index-count` — find(), index(), count() (2 pieces)

## Max coverage V2

> [!summary] Broadest pack: high-yield core plus the legacy backup material integrated in V2.

- preset id: `max-coverage-v2`
- target user: wants the fullest reference pack, including lower-frequency corner cases
- snippet count: **51**
- piece count: **117**
- estimated chars: **28315**

Includes all default-selected pieces plus selected backup clarifiers from the legacy dataset integration pass.

Top included snippets by piece count:
- `case-and-capitalization` — Case methods and capitalization (3 pieces)
- `datetime-overlap-logic` — Overlap logic (3 pieces)
- `datetime-build-from-parts` — Build datetimes from parts (3 pieces)
- `defaults-keyword-arguments` — Defaults and keyword arguments (3 pieces)
- `fstrings-and-format` — f-strings and .format() (3 pieces)
- `datetime-sequence-generation` — Date sequences (3 pieces)
- `datetime-strptime-strftime` — strptime() and strftime() (3 pieces)
- `oop-state-and-collection-attributes` — Object state and collection attributes (3 pieces)
- `names-aliasing-and-copies` — Names, aliasing, and copies (3 pieces)
- `pandas-missing-values-alignment` — Missing values and index alignment (3 pieces)
# RM-008: External Cheat-Sheet Gap Audit

## Metadata

- ID: `RM-008`
- Status: `done`
- Priority: `High`
- Owner: `Codex`
- Last Updated: `2026-03-22`

## Problem

The repo needed a manual completeness audit against public cheat sheets for the same course before wider student release. The live [topic_cards.json](../../topic_cards.json) is also materially different from the older `174`-card snapshot still described in some repo docs, so the audit had to compare against the current merged `27`-card deck rather than the stale documentation.

## Goals

- Manually review all 9 PDFs in [materials/example_cheat_sheets](../../materials/example_cheat_sheets) using rendered page images, not text-only extraction.
- Normalize overlapping concepts across the public sheets into one actionable inventory.
- Classify each concept as `covered`, `partial`, `missing-course-backed`, or `missing-extra-helpful`.
- Suggest concrete manual additions without mutating [topic_cards.json](../../topic_cards.json) yet.

## Non-Goals

- Automatically importing public-sheet material into [topic_cards.json](../../topic_cards.json).
- Treating generic Python helper content as mandatory course content.
- Changing app behavior or data schema.

## Proposed Solution

Render every public PDF to PNG, review the rendered pages manually with the PDF skill, de-duplicate the extracted concept families, and compare them against the live merged deck by actual snippet/key-point/example presence rather than card titles. Record the results as a split report:

- `Course-backed gaps`: missing or partial concepts that fit the current course-backed card model.
- `Extra-helpful additions`: useful public-sheet content that is broader than the current evidence-backed scope.

## Implementation Plan

1. Render all 9 PDFs to `tmp/pdfs/render/` with `pdftoppm`.
2. Have 3 subagents manually review the rendered pages in parallel using the PDF skill.
3. Manually spot-check representative rendered pages in the main thread to verify the extracted concept families.
4. Normalize duplicates across the 9 PDFs into one concept inventory.
5. Compare each concept family against the live `27` merged cards in [topic_cards.json](../../topic_cards.json).
6. Record the split report and full inventory in this spec.
7. Align stale contributor docs with the live dataset snapshot.

## Manual Review Notes

- Rendered output: `43` PNG pages under `tmp/pdfs/render/`.
- Review method: rendered-page reading with the PDF skill, not `pdftotext` alone.
- Subagent clusters:
  - `athena-python-endterm-study-guide-key-concepts-functions.pdf`
  - `python-resit-cheat-sheet-2022-key-concepts-functions.pdf`
  - `python-exam-content-summary-key-formulas-concepts.pdf`
  - `python-endterm-cheat-sheet-key-concepts-code-snippets.pdf`
  - `python-cheatsheet-for-final-exam-preparation.pdf`
  - `python-codes-for-exam-dictionary-datetime-and-pandas-operations.pdf`
  - `python-101-intro-to-python-basics-and-data-handling-in-week-1-8.pdf`
  - `python-cheat-sheet-methods-on-immutable-lists-dictionaries-final.pdf`
  - `summary-introduction-to-python.pdf`
- Main-thread visual spot checks covered rendered pages including:
  - `athena...:2`
  - `python-101...:2,5,9`
  - `python-codes...:2`
  - `python-cheatsheet-for-final-exam-preparation:2`
  - `python-exam-content-summary...:2`
  - `summary-introduction-to-python:3,6`

## Summary Findings

- The public sheets are mostly redundant with the current deck; they do not reveal large missing topic families across the core course.
- The clearest true content gap is a compact `NumPy` reference block.
- Most other differences are narrower `partial` gaps inside existing merged topics:
  - list aliasing vs copying
  - dict utility idioms
  - typed `except` examples
  - richer string-formatting styles
  - datetime ISO/day-of-year helpers
  - pandas mutation/missing-data/value-op reminders
- The biggest extra-helpful but lower-evidence additions are:
  - practical console workflow (`pwd`, `python3 file.py`, `pip3 install`, `help(...)`)
  - timezone-aware datetime helpers
  - one compact worked aggregation example

Normalized concept-family counts:

- `covered`: 16
- `partial`: 9
- `missing-course-backed`: 1
- `missing-extra-helpful`: 3

## Course-Backed Gaps

| Concept | Source PDF + page | Current mapping | Status | Proposed manual addition |
| --- | --- | --- | --- | --- |
| List copy and alias semantics (`y = x`, `x[:]`, `list(x)`, shallow vs deep copy) | `summary-introduction-to-python.pdf:3`<br>`athena-python-endterm-study-guide-key-concepts-functions.pdf:3`<br>`python-resit-cheat-sheet-2022-key-concepts-functions.pdf:3` | `Objects and Names` / `Lists and Sets` | `partial` | Add a compact example showing aliasing vs real copies, and note that `copy.deepcopy(...)` is needed for nested structures. |
| Dict utility patterns (`update`, `pop`, sorted accumulation, `zip`, `enumerate`) | `python-cheatsheet-for-final-exam-preparation.pdf:2`<br>`python-codes-for-exam-dictionary-datetime-and-pandas-operations.pdf:2` | `Dictionaries and Mappings` | `partial` | Add one mini reference block with `dict.update`, `dict.pop`, `dict(zip(...))`, and a small loop over `.items()`. |
| Typed error handling vs broad `except` | `python-101-intro-to-python-basics-and-data-handling-in-week-1-8.pdf:3`<br>`python-cheat-sheet-methods-on-immutable-lists-dictionaries-final.pdf:2` | `Error Handling` | `partial` | Add a minimal `try/except ValueError` example and a note that bare `except` is broad. |
| String immutability and reassignment after methods | `python-endterm-cheat-sheet-key-concepts-code-snippets.pdf:2`<br>`python-cheat-sheet-methods-on-immutable-lists-dictionaries-final.pdf:2`<br>`python-101-intro-to-python-basics-and-data-handling-in-week-1-8.pdf:3` | `String Operations and Methods` | `partial` | Add one reminder that `replace`, `capitalize`, `split`, and `join` return new strings and do not mutate the original. |
| Formatting styles beyond f-strings (`.format`, conversion flags, compact specifiers) | `python-101-intro-to-python-basics-and-data-handling-in-week-1-8.pdf:3`<br>`python-cheat-sheet-methods-on-immutable-lists-dictionaries-final.pdf:2`<br>`python-exam-content-summary-key-formulas-concepts.pdf:2` | `String Formatting` | `partial` | Extend the formatting card with `.format(...)`, `!r`, `!s`, and a `{:02d}` example. |
| Constructor/default-argument and instance-vs-class-attribute pitfalls | `python-endterm-cheat-sheet-key-concepts-code-snippets.pdf:3`<br>`python-cheatsheet-for-final-exam-preparation.pdf:2`<br>`python-codes-for-exam-dictionary-datetime-and-pandas-operations.pdf:2` | `OOP Fundamentals` | `partial` | Add one compact class example covering `__init__`, default arguments, and the difference between instance and class attributes. |
| Datetime ISO/day-of-year helpers | `python-endterm-cheat-sheet-key-concepts-code-snippets.pdf:2`<br>`python-codes-for-exam-dictionary-datetime-and-pandas-operations.pdf:2` | `Datetime` | `partial` | Add quick refs for `isoweekday()`, `isocalendar()`, and `day_of_year = (dt - datetime(dt.year, 1, 1)).days + 1`. |
| NumPy arrays, vectorized arithmetic, boolean masks, 2D indexing, and `shape` | `summary-introduction-to-python.pdf:6` | `none` | `missing-course-backed` | Add a small `NumPy` topic block or extend an existing week-1/values card with `import numpy as np`, `np.array(...)`, vectorized math, boolean subsetting, 2D indexing, and `.shape`. |
| Pandas value/mutation/missing-data helpers (`T`, `sort_index`, `sort_values`, `drop`, `dropna`, `fillna(method=..., limit=...)`, `set_index`) | `athena-python-endterm-study-guide-key-concepts-functions.pdf:3`<br>`python-resit-cheat-sheet-2022-key-concepts-functions.pdf:3`<br>`python-cheat-sheet-methods-on-immutable-lists-dictionaries-final.pdf:2`<br>`summary-introduction-to-python.pdf:3`<br>`python-codes-for-exam-dictionary-datetime-and-pandas-operations.pdf:3` | `Working With Values` / `Combining Data` | `partial` | Add a compact reminder block covering sort/drop/index/missing-data helpers, and flag `DataFrame.append(...)` as legacy with `pd.concat(...)` preferred. |
| Pandas vectorized string helpers and `apply(..., axis=...)` patterns | `python-endterm-cheat-sheet-key-concepts-code-snippets.pdf:2`<br>`python-cheatsheet-for-final-exam-preparation.pdf:2`<br>`python-codes-for-exam-dictionary-datetime-and-pandas-operations.pdf:2,3` | `Working With Values` | `partial` | Add one short side-by-side example for `.str`, `.map(...)`, and `df.apply(..., axis=0/1)`. |

## Extra-Helpful Additions

| Concept | Source PDF + page | Current mapping | Status | Proposed manual addition |
| --- | --- | --- | --- | --- |
| Timezone-aware datetime variants (`today`, `utcnow`, `datetime.now(tz=...)`, `pytz.timezone(...)`) | `athena-python-endterm-study-guide-key-concepts-functions.pdf:3`<br>`python-resit-cheat-sheet-2022-key-concepts-functions.pdf:3` | `Datetime` | `missing-extra-helpful` | Add a small optional note for UTC vs local time and timezone-aware construction if you want broader real-world usefulness. |
| Practical console workflow (`pwd`, `python3 file.py`, `pip3 install`, `help(...)`) | `summary-introduction-to-python.pdf:2` | `Python Basics` | `missing-extra-helpful` | Add a tiny “run Python locally” helper block near the intro or splash help text. |
| Worked aggregation / weighted-average style practice snippet | `python-exam-content-summary-key-formulas-concepts.pdf:4` | `Loops` / `Working With Values` | `missing-extra-helpful` | Add one loop-based average or weighted-average example if you want one more exam-ready worked pattern. |

## Full Normalized Inventory

| Concept | Source PDF + page | Mapped current topic | Status | Proposed target topic | Proposed section type | Proposed manual addition |
| --- | --- | --- | --- | --- | --- | --- |
| Core primitives, comments, print, input, and basic control-flow framing | `athena-python-endterm-study-guide-key-concepts-functions.pdf:2`<br>`python-resit-cheat-sheet-2022-key-concepts-functions.pdf:2`<br>`python-exam-content-summary-key-formulas-concepts.pdf:2`<br>`python-101-intro-to-python-basics-and-data-handling-in-week-1-8.pdf:2`<br>`summary-introduction-to-python.pdf:2` | `Python Basics` / `Functions and Imports` | `covered` | `Python Basics` | `key_points_to_remember` | No addition needed. |
| Numeric operators and boolean logic | `athena-python-endterm-study-guide-key-concepts-functions.pdf:2`<br>`python-resit-cheat-sheet-2022-key-concepts-functions.pdf:2`<br>`python-exam-content-summary-key-formulas-concepts.pdf:2`<br>`python-101-intro-to-python-basics-and-data-handling-in-week-1-8.pdf:2` | `Operators and Truth` | `covered` | `Operators and Truth` | `key_points_to_remember` | No addition needed. |
| Sequence indexing, slicing, containment, and `range` stop-exclusion | `athena-python-endterm-study-guide-key-concepts-functions.pdf:2`<br>`python-resit-cheat-sheet-2022-key-concepts-functions.pdf:2`<br>`python-exam-content-summary-key-formulas-concepts.pdf:2`<br>`python-101-intro-to-python-basics-and-data-handling-in-week-1-8.pdf:2`<br>`summary-introduction-to-python.pdf:3` | `Sequences and Access` | `covered` | `Sequences and Access` | `key_points_to_remember` | No addition needed. |
| Basic list mutation (`append`, `remove`, slicing, deletion) | `python-101-intro-to-python-basics-and-data-handling-in-week-1-8.pdf:2`<br>`summary-introduction-to-python.pdf:3` | `Lists and Sets` | `covered` | `Lists and Sets` | `key_points_to_remember` | No addition needed. |
| List copy and alias semantics (`y = x`, `x[:]`, `list(x)`, shallow vs deep copy) | `summary-introduction-to-python.pdf:3`<br>`athena-python-endterm-study-guide-key-concepts-functions.pdf:3`<br>`python-resit-cheat-sheet-2022-key-concepts-functions.pdf:3` | `Objects and Names` / `Lists and Sets` | `partial` | `Objects and Names` | `key_points_to_remember` | Add alias-vs-copy example plus a `copy.deepcopy(...)` note for nested structures. |
| Basic dict creation, lookup, membership, iteration, and `dict(zip(...))` | `athena-python-endterm-study-guide-key-concepts-functions.pdf:3`<br>`python-resit-cheat-sheet-2022-key-concepts-functions.pdf:3`<br>`python-101-intro-to-python-basics-and-data-handling-in-week-1-8.pdf:2`<br>`python-cheat-sheet-methods-on-immutable-lists-dictionaries-final.pdf:2`<br>`summary-introduction-to-python.pdf:3` | `Dictionaries and Mappings` | `covered` | `Dictionaries and Mappings` | `lecture_snippets` | No addition needed. |
| Dict utility patterns (`update`, `pop`, sorted accumulation, `zip`, `enumerate`) | `python-cheatsheet-for-final-exam-preparation.pdf:2`<br>`python-codes-for-exam-dictionary-datetime-and-pandas-operations.pdf:2` | `Dictionaries and Mappings` | `partial` | `Dictionaries and Mappings` | `ai_examples` | Add a compact helper block with `update`, `pop`, `.items()`, and `dict(zip(...))`. |
| Loops, `break`, `continue`, `enumerate()`, and dict iteration | `python-101-intro-to-python-basics-and-data-handling-in-week-1-8.pdf:2,3`<br>`summary-introduction-to-python.pdf:3` | `Loops` | `covered` | `Loops` | `ai_examples` | No addition needed. |
| Function and import basics | `athena-python-endterm-study-guide-key-concepts-functions.pdf:2,3`<br>`python-resit-cheat-sheet-2022-key-concepts-functions.pdf:2,3`<br>`python-101-intro-to-python-basics-and-data-handling-in-week-1-8.pdf:3` | `Functions and Imports` | `covered` | `Functions and Imports` | `lecture_snippets` | No addition needed. |
| Default args, `*args`, `**kwargs`, `lambda`, `map`, `filter`, `reduce`, `zip`, and closures | `python-101-intro-to-python-basics-and-data-handling-in-week-1-8.pdf:3`<br>`summary-introduction-to-python.pdf:4`<br>`athena-python-endterm-study-guide-key-concepts-functions.pdf:2,3`<br>`python-resit-cheat-sheet-2022-key-concepts-functions.pdf:2,3`<br>`python-endterm-cheat-sheet-key-concepts-code-snippets.pdf:2`<br>`python-cheatsheet-for-final-exam-preparation.pdf:2` | `Arguments` / `Higher-Order Patterns` | `covered` | `Higher-Order Patterns` | `ai_examples` | No addition needed. |
| Typed error handling vs broad `except` | `python-101-intro-to-python-basics-and-data-handling-in-week-1-8.pdf:3`<br>`python-cheat-sheet-methods-on-immutable-lists-dictionaries-final.pdf:2` | `Error Handling` | `partial` | `Error Handling` | `key_points_to_remember` | Add a small typed-`except` pattern and warn about bare `except`. |
| String quoting, escaping, and method overview | `athena-python-endterm-study-guide-key-concepts-functions.pdf:3`<br>`python-resit-cheat-sheet-2022-key-concepts-functions.pdf:3`<br>`python-101-intro-to-python-basics-and-data-handling-in-week-1-8.pdf:3`<br>`python-cheat-sheet-methods-on-immutable-lists-dictionaries-final.pdf:2`<br>`summary-introduction-to-python.pdf:2,3` | `String Fundamentals` / `String Operations and Methods` | `covered` | `String Operations and Methods` | `lecture_snippets` | No addition needed. |
| String immutability and reassignment after methods | `python-endterm-cheat-sheet-key-concepts-code-snippets.pdf:2`<br>`python-cheat-sheet-methods-on-immutable-lists-dictionaries-final.pdf:2`<br>`python-101-intro-to-python-basics-and-data-handling-in-week-1-8.pdf:3` | `String Operations and Methods` | `partial` | `String Operations and Methods` | `key_points_to_remember` | Add a reminder that methods like `replace` and `capitalize` return new strings. |
| Formatting styles beyond f-strings (`.format`, conversion flags, compact specifiers) | `python-101-intro-to-python-basics-and-data-handling-in-week-1-8.pdf:3`<br>`python-cheat-sheet-methods-on-immutable-lists-dictionaries-final.pdf:2`<br>`python-exam-content-summary-key-formulas-concepts.pdf:2`<br>`python-codes-for-exam-dictionary-datetime-and-pandas-operations.pdf:2` | `String Formatting` | `partial` | `String Formatting` | `lecture_snippets` | Extend with `.format(...)`, `!r`, `!s`, and `{:02d}`; mention `Template.safe_substitute(...)` as optional broader context. |
| OOP basics (`class`, `self`, `__init__`, instantiation, attributes) | `athena-python-endterm-study-guide-key-concepts-functions.pdf:3`<br>`python-resit-cheat-sheet-2022-key-concepts-functions.pdf:3`<br>`python-exam-content-summary-key-formulas-concepts.pdf:2`<br>`python-101-intro-to-python-basics-and-data-handling-in-week-1-8.pdf:3`<br>`python-cheat-sheet-methods-on-immutable-lists-dictionaries-final.pdf:2` | `OOP Fundamentals` | `covered` | `OOP Fundamentals` | `lecture_snippets` | No addition needed. |
| Constructor/default-argument and instance-vs-class-attribute pitfalls | `python-endterm-cheat-sheet-key-concepts-code-snippets.pdf:3`<br>`python-cheatsheet-for-final-exam-preparation.pdf:2`<br>`python-codes-for-exam-dictionary-datetime-and-pandas-operations.pdf:2` | `OOP Fundamentals` | `partial` | `OOP Fundamentals` | `ai_examples` | Add a compact class example with a safe default pattern and class-vs-instance attribute note. |
| Comprehensions | `athena-python-endterm-study-guide-key-concepts-functions.pdf:3`<br>`python-endterm-cheat-sheet-key-concepts-code-snippets.pdf:2` | `Comprehensions` | `covered` | `Comprehensions` | `ai_examples` | No addition needed. |
| Generators and iterators | `athena-python-endterm-study-guide-key-concepts-functions.pdf:3`<br>`python-codes-for-exam-dictionary-datetime-and-pandas-operations.pdf:2` | `Generators and Iterators` | `covered` | `Generators and Iterators` | `ai_examples` | No addition needed. |
| Truthiness, equality, and coercion worked examples | `python-endterm-cheat-sheet-key-concepts-code-snippets.pdf:2`<br>`python-cheatsheet-for-final-exam-preparation.pdf:2` | `Conversion and Truthiness` | `covered` | `Conversion and Truthiness` | `ai_examples` | No addition needed. |
| Local scope vs returned values | `python-endterm-cheat-sheet-key-concepts-code-snippets.pdf:2` | `Scope` / `Return Behavior` | `covered` | `Return Behavior` | `key_points_to_remember` | No addition needed. |
| Datetime basics (`now`, `strftime`, `strptime`, `timedelta`, `replace`) | `athena-python-endterm-study-guide-key-concepts-functions.pdf:3`<br>`python-resit-cheat-sheet-2022-key-concepts-functions.pdf:3`<br>`python-101-intro-to-python-basics-and-data-handling-in-week-1-8.pdf:3`<br>`python-cheat-sheet-methods-on-immutable-lists-dictionaries-final.pdf:2`<br>`python-codes-for-exam-dictionary-datetime-and-pandas-operations.pdf:2` | `Datetime` | `covered` | `Datetime` | `lecture_snippets` | No addition needed. |
| Datetime ISO/day-of-year helpers | `python-endterm-cheat-sheet-key-concepts-code-snippets.pdf:2`<br>`python-codes-for-exam-dictionary-datetime-and-pandas-operations.pdf:2` | `Datetime` | `partial` | `Datetime` | `ai_examples` | Add `isoweekday()`, `isocalendar()`, and reusable day-of-year helper snippets. |
| Timezone-aware datetime variants (`today`, `utcnow`, `datetime.now(tz=...)`, `pytz.timezone(...)`) | `athena-python-endterm-study-guide-key-concepts-functions.pdf:3`<br>`python-resit-cheat-sheet-2022-key-concepts-functions.pdf:3` | `Datetime` | `missing-extra-helpful` | `Datetime` | `key_points_to_remember` | Optional timezone note for broader usefulness. |
| NumPy arrays, vectorized arithmetic, boolean masks, 2D indexing, and `shape` | `summary-introduction-to-python.pdf:6` | `none` | `missing-course-backed` | `NumPy` or existing week-1/values card | `lecture_snippets` | Add a compact NumPy starter reference with arrays, masks, indexing, and `.shape`. |
| Pandas core structures, indexing, and selection basics (`Series`, `DataFrame`, `.loc`, `.iloc`, `.head`, `.tail`, `.describe`) | `athena-python-endterm-study-guide-key-concepts-functions.pdf:3`<br>`python-resit-cheat-sheet-2022-key-concepts-functions.pdf:3`<br>`python-exam-content-summary-key-formulas-concepts.pdf:3`<br>`python-cheat-sheet-methods-on-immutable-lists-dictionaries-final.pdf:2`<br>`summary-introduction-to-python.pdf:3`<br>`python-101-intro-to-python-basics-and-data-handling-in-week-1-8.pdf:9` | `Pandas Core Structures` / `Inspecting and Selecting Data` | `covered` | `Inspecting and Selecting Data` | `lecture_snippets` | No addition needed. |
| Pandas value/mutation/missing-data helpers (`T`, `sort_index`, `sort_values`, `drop`, `dropna`, `fillna(method=..., limit=...)`, `set_index`) | `athena-python-endterm-study-guide-key-concepts-functions.pdf:3`<br>`python-resit-cheat-sheet-2022-key-concepts-functions.pdf:3`<br>`python-cheat-sheet-methods-on-immutable-lists-dictionaries-final.pdf:2`<br>`summary-introduction-to-python.pdf:3`<br>`python-codes-for-exam-dictionary-datetime-and-pandas-operations.pdf:3` | `Working With Values` / `Combining Data` | `partial` | `Working With Values` | `key_points_to_remember` | Add a compact DataFrame manipulation helper block; mention `append` only as a legacy note. |
| Pandas vectorized string helpers and `apply(..., axis=...)` patterns | `python-endterm-cheat-sheet-key-concepts-code-snippets.pdf:2`<br>`python-cheatsheet-for-final-exam-preparation.pdf:2`<br>`python-codes-for-exam-dictionary-datetime-and-pandas-operations.pdf:2,3` | `Working With Values` | `partial` | `Working With Values` | `ai_examples` | Add one short `.str` example plus row-wise vs column-wise `apply`. |
| Practical console workflow (`pwd`, `python3 file.py`, `pip3 install`, `help(...)`) | `summary-introduction-to-python.pdf:2` | `Python Basics` | `missing-extra-helpful` | `Python Basics` | `key_points_to_remember` | Optional quick-start helper block for running code locally. |
| Worked aggregation / weighted-average style practice snippet | `python-exam-content-summary-key-formulas-concepts.pdf:4` | `Loops` / `Working With Values` | `missing-extra-helpful` | `Working With Values` | `ai_examples` | Optional loop-based average or weighted-average worked example. |

## Risks and Mitigations

- Risk: public sheets contain generic Python advice that is useful but not strongly course-backed.
- Mitigation: keep `missing-extra-helpful` separate from course-backed gaps.
- Risk: older repo docs still imply a `174`-card deck and can cause future audits to compare against the wrong baseline.
- Mitigation: align the contributor docs with the live `27`-card snapshot as part of this task.
- Risk: some public snippets use legacy pandas APIs.
- Mitigation: flag legacy patterns explicitly instead of promoting them unqualified.

## Test Plan

- Manual checks:
  - Confirm all 9 PDFs were rendered to `43` PNG pages in `tmp/pdfs/render/`.
  - Confirm all 9 PDFs were reviewed from rendered pages, not text extraction alone.
  - Confirm the inventory compares against the live [topic_cards.json](../../topic_cards.json), not stale docs.
- Validation commands:
  - Run the `topic_cards.json` integrity check from [AGENTS.md](../../AGENTS.md).
  - Run `make leave-better`.

## Rollout and Validation

- Commands run:
  - `pdftoppm -png -rx 180 -ry 180 materials/example_cheat_sheets/*.pdf tmp/pdfs/render/...`
  - `python3 - <<'PY' ... integrity check from AGENTS.md ... PY`
  - `make leave-better`
- Success criteria:
  - Audit artifact exists and lists every normalized concept family from the reviewed PDFs.
  - Gaps are split into course-backed vs extra-helpful.
  - Contributor docs no longer claim the live deck still has `174` cards.

## Open Questions

- If follow-up curation is implemented, should `NumPy` become its own merged topic, or should the starter snippets be folded into an existing week-1 or values-focused card?
- If extra-helpful additions are accepted, should practical workflow notes live in the card dataset or in UI/help copy outside the printable cheat sheet?

# Legacy integration

> [!summary] What this document is
> A transparent record of how the old dataset was folded into the V2 bank.

## Integration table

| Legacy item | Decision | Target snippet | Target piece / note |
|---|---|---|---|
| A child object still counts as the parent type | integrated | `oop-inheritance-core` | parent-child-rules / fast-traps |
| Arithmetic Operator Reference | integrated | `numeric-corner-cases` | operator-mini-table |
| Boolean string predicates | integrated | `case-and-capitalization` | quick-reference / strip-and-predicate-extras |
| Class attribute vs instance attribute | integrated | `oop-state-and-collection-attributes` | class-vs-instance-attribute |
| Comments, Logical Lines, and Raw Strings | integrated | `syntax-fragments-escapes-raw-strings` | syntax-rules-mini-table / tiny-fragments |
| Convert Before Comparing Mixed Types | integrated | `membership-and-condition-logic` | branch-order-and-ternary |
| DatetimeIndex matters only when the index actually stores dates | integrated | `pandas-missing-values-alignment` | alignment-rules |
| Debug output with f'{var=}' | integrated | `fstrings-and-format` | debug-fstring |
| Escape Sequences and Quote Choices | integrated | `syntax-fragments-escapes-raw-strings` | escapes-and-quotes |
| Filter by Applying the Condition to Each Element | integrated | `membership-and-condition-logic` | branch-order-and-ternary |
| Float Precision and Ordered Comparison Traps | integrated | `numeric-corner-cases` | precision-and-order |
| Index alignment can silently create `NaN` values | integrated | `pandas-missing-values-alignment` | alignment-example / alignment-rules |
| Iterator basics | integrated | `loop-control-and-iterators` | iterator-example |
| Missing values: decide whether to keep shape or drop data | integrated | `pandas-missing-values-alignment` | fillna-vs-dropna |
| Mutable, Immutable, and Copying | integrated | `names-aliasing-and-copies` | binding-and-copy-table / aliasing-example |
| Negative Floor-Division and Modulo | integrated | `numeric-corner-cases` | negative-division-and-modulo |
| Object vs string mental model | integrated | `datetime-strptime-strftime` | object-vs-string |
| Read Tiny Syntax Fragments Literally | integrated | `syntax-fragments-escapes-raw-strings` | tiny-fragments |
| Subclass syntax and parent initialization | integrated | `oop-inheritance-core` | inheritance-template |
| Trim whitespace and edges | integrated | `case-and-capitalization` | strip-and-predicate-extras |
| Use `super()` when the parent constructor still matters | integrated | `oop-inheritance-core` | inheritance-template / fast-traps |
| Weekday, month, and year attributes are direct lookups | integrated | `datetime-build-from-parts` | attributes-and-replace |
| `==` compares values; `is` compares identity | integrated | `names-aliasing-and-copies` | equality-vs-identity |
| `replace()` returns a new datetime | integrated | `datetime-build-from-parts` | attributes-and-replace |
| break, continue, and loop control | integrated | `loop-control-and-iterators` | control-table / control-reminders |
| if / elif / else and Ternary Expressions | integrated | `membership-and-condition-logic` | branch-order-and-ternary |
| Legacy format width | intentionally-omitted | `` | Not promoted; modern f-string coverage kept instead. |
| Quick inspection helpers | intentionally-omitted | `` | Useful but not central enough to justify standalone snippet space. |
| String module constants | intentionally-omitted | `` | Too generic / low exam value as a standalone snippet. |
| now(), timestamp(), and ISO helpers | intentionally-omitted | `` | Kept out of front-page coverage because they do not drive the exam bank strongly. |

> [!note] Curation principle
> Legacy content that was clearly useful but missing was imported. Low-value generic references that were redundant with stronger V1 material were intentionally not promoted into standalone V2 snippets.

# Presets

> [!summary] Purpose
> These are ready-made starting selections for the cheat-sheet builder.
> Students should treat them as **starting points**, not fixed final sheets.

## Preset overview

|   # | Preset              | Slug                |   Snippets |   Pieces |   Char count | Best for                                                               | Why choose it                                                                                                              |
|----:|:--------------------|:--------------------|-----------:|---------:|-------------:|:-----------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------|
|   1 | Balanced default    | balanced-default    |         40 |       90 |        21342 | minimal prior knowledge, wants broad coverage                          | Includes most high-priority snippets, all default-selected pieces, and a few clarifiers for recurring exact exam patterns. |
|   2 | Post-midterm tilted | post-midterm-tilted |         31 |       73 |        17737 | expects the final to skew toward later-course material                 | Good default when space is tight but you still want coverage for the most likely post-midterm traps.                       |
|   3 | Ultra-dense core    | ultra-dense-core    |         21 |       43 |        10354 | very limited space, wants maximum points per line                      | Best for students who already remember the basics and want a compact safety net.                                           |
|   4 | Trap hunter         | trap-hunter         |         20 |       46 |        11504 | knows the material somewhat, mainly loses points to subtle distractors | Emphasizes mutation-vs-return, pandas shape traps, scope, parse/format, and method-call gotchas.                           |

## Balanced default

> [!info] Preset metadata
> - Slug: `balanced-default`
> - Snippets: `40`
> - Pieces: `90`
> - Approx char count: `21342`
> - Best for: minimal prior knowledge, wants broad coverage

**Summary.** Broad starter pack for a student with little pre-existing knowledge.

**Why choose it.** Includes most high-priority snippets, all default-selected pieces, and a few clarifiers for recurring exact exam patterns.

|   # | Snippet                                   | Slug                                 | Topic                         |   Pieces selected | Recurrence   |   Priority |
|----:|:------------------------------------------|:-------------------------------------|:------------------------------|------------------:|:-------------|-----------:|
|   1 | Nested indexing and negative indices      | nested-indexing-and-negative-indices | Core Python                   |                 2 | occasional   |          4 |
|   2 | Slicing patterns                          | slicing-patterns                     | Core Python                   |                 2 | very-common  |          5 |
|   3 | Loop templates                            | loop-templates                       | Core Python                   |                 2 | common       |          4 |
|   4 | zip() and enumerate() core patterns       | zip-enumerate-core                   | Core Python                   |                 3 | signature    |          5 |
|   5 | Types, None, bool, equality               | types-none-bool-equality             | Core Python                   |                 2 | signature    |          5 |
|   6 | Membership and condition logic            | membership-and-condition-logic       | Core Python                   |                 2 | common       |          4 |
|   7 | Built-ins and what they return            | builtins-return-values               | Core Python                   |                 2 | very-common  |          4 |
|   8 | timedelta and day counts                  | datetime-timedelta-day-counts        | Datetime                      |                 2 | signature    |          5 |
|   9 | Overlap logic                             | datetime-overlap-logic               | Datetime                      |                 3 | occasional   |          4 |
|  10 | strptime() and strftime()                 | datetime-strptime-strftime           | Datetime                      |                 3 | signature    |          5 |
|  11 | Build datetimes from parts                | datetime-build-from-parts            | Datetime                      |                 2 | very-common  |          4 |
|  12 | Date sequences                            | datetime-sequence-generation         | Datetime                      |                 3 | common       |          4 |
|  13 | List comprehension patterns               | list-comprehension-patterns          | Dictionaries & comprehensions |                 2 | signature    |          5 |
|  14 | Dictionary comprehension patterns         | dict-comprehension-patterns          | Dictionaries & comprehensions |                 2 | signature    |          5 |
|  15 | Build, count, and aggregate dictionaries  | dict-build-count-aggregate           | Dictionaries & comprehensions |                 2 | very-common  |          5 |
|  16 | Dictionary iteration and equality         | dict-iteration-equality              | Dictionaries & comprehensions |                 2 | very-common  |          5 |
|  17 | Running totals and next-link dictionaries | dict-running-totals-and-next-links   | Dictionaries & comprehensions |                 2 | occasional   |          4 |
|  18 | Higher-order functions and lambda         | higher-order-lambda                  | Functions & scope             |                 1 | common       |          4 |
|  19 | Defaults and keyword arguments            | defaults-keyword-arguments           | Functions & scope             |                 2 | very-common  |          4 |
|  20 | *args and **kwargs                        | args-and-kwargs                      | Functions & scope             |                 2 | signature    |          4 |
|  21 | return, None, and function end            | return-none-and-function-end         | Functions & scope             |                 2 | common       |          5 |
|  22 | Local vs global scope                     | local-vs-global-scope                | Functions & scope             |                 2 | signature    |          5 |
|  23 | __init__, self, defaults, attributes      | oop-init-self-defaults               | OOP                           |                 3 | signature    |          5 |
|  24 | Object state and collection attributes    | oop-state-and-collection-attributes  | OOP                           |                 3 | signature    |          4 |
|  25 | Method calls and self                     | oop-method-calls-and-self            | OOP                           |                 2 | common       |          4 |
|  26 | Compare/report method patterns            | oop-compare-and-report-patterns      | OOP                           |                 3 | signature    |          4 |
|  27 | sort_index() vs sort_values()             | pandas-sort-index-vs-values          | Pandas                        |                 2 | common       |          4 |
|  28 | Series vs DataFrame                       | pandas-series-vs-dataframe           | Pandas                        |                 2 | signature    |          5 |
|  29 | loc vs iloc                               | pandas-loc-iloc                      | Pandas                        |                 3 | very-common  |          5 |
|  30 | Boolean masks and indexing                | pandas-boolean-mask-and-indexing     | Pandas                        |                 2 | common       |          5 |
|  31 | Vectorized new columns                    | pandas-vectorized-new-columns        | Pandas                        |                 2 | common       |          5 |
|  32 | map() vs apply()                          | pandas-map-vs-apply                  | Pandas                        |                 3 | very-common  |          5 |
|  33 | String/date columns                       | pandas-string-and-date-columns       | Pandas                        |                 2 | occasional   |          4 |
|  34 | f-strings and .format()                   | fstrings-and-format                  | Strings                       |                 3 | very-common  |          4 |
|  35 | Targeted string edits                     | targeted-string-edit-patterns        | Strings                       |                 2 | very-common  |          4 |
|  36 | split(), join(), replace()                | split-join-replace                   | Strings                       |                 3 | signature    |          5 |
|  37 | find(), index(), count()                  | find-index-count                     | Strings                       |                 2 | common       |          4 |
|  38 | URL, email, and phone parsing             | url-email-phone-parsing              | Strings                       |                 2 | common       |          5 |
|  39 | MCQ elimination checklist                 | mcq-elimination-checklist            | Exam survival                 |                 2 | signature    |          5 |
|  40 | Mutation vs return value                  | mutation-vs-return                   | Exam survival                 |                 2 | signature    |          5 |

## Post-midterm tilted

> [!info] Preset metadata
> - Slug: `post-midterm-tilted`
> - Snippets: `31`
> - Pieces: `73`
> - Approx char count: `17737`
> - Best for: expects the final to skew toward later-course material

**Summary.** Weights strings, pandas, datetime, and OOP while still keeping a small pre-midterm rescue layer.

**Why choose it.** Good default when space is tight but you still want coverage for the most likely post-midterm traps.

|   # | Snippet                                | Slug                                | Topic                         |   Pieces selected | Recurrence   |   Priority |
|----:|:---------------------------------------|:------------------------------------|:------------------------------|------------------:|:-------------|-----------:|
|   1 | Built-ins and what they return         | builtins-return-values              | Core Python                   |                 2 | very-common  |          4 |
|   2 | timedelta and day counts               | datetime-timedelta-day-counts       | Datetime                      |                 2 | signature    |          5 |
|   3 | Overlap logic                          | datetime-overlap-logic              | Datetime                      |                 3 | occasional   |          4 |
|   4 | strptime() and strftime()              | datetime-strptime-strftime          | Datetime                      |                 3 | signature    |          5 |
|   5 | Build datetimes from parts             | datetime-build-from-parts           | Datetime                      |                 3 | very-common  |          4 |
|   6 | Date sequences                         | datetime-sequence-generation        | Datetime                      |                 3 | common       |          4 |
|   7 | Dictionary iteration and equality      | dict-iteration-equality             | Dictionaries & comprehensions |                 2 | very-common  |          5 |
|   8 | Higher-order functions and lambda      | higher-order-lambda                 | Functions & scope             |                 1 | common       |          4 |
|   9 | *args and **kwargs                     | args-and-kwargs                     | Functions & scope             |                 2 | signature    |          4 |
|  10 | return, None, and function end         | return-none-and-function-end        | Functions & scope             |                 2 | common       |          5 |
|  11 | Local vs global scope                  | local-vs-global-scope               | Functions & scope             |                 2 | signature    |          5 |
|  12 | __init__, self, defaults, attributes   | oop-init-self-defaults              | OOP                           |                 3 | signature    |          5 |
|  13 | Object state and collection attributes | oop-state-and-collection-attributes | OOP                           |                 4 | signature    |          4 |
|  14 | Method calls and self                  | oop-method-calls-and-self           | OOP                           |                 2 | common       |          4 |
|  15 | Compare/report method patterns         | oop-compare-and-report-patterns     | OOP                           |                 3 | signature    |          4 |
|  16 | Build DataFrames from arguments        | pandas-build-from-args              | Pandas                        |                 2 | rare         |          3 |
|  17 | sort_index() vs sort_values()          | pandas-sort-index-vs-values         | Pandas                        |                 2 | common       |          4 |
|  18 | Series vs DataFrame                    | pandas-series-vs-dataframe          | Pandas                        |                 2 | signature    |          5 |
|  19 | loc vs iloc                            | pandas-loc-iloc                     | Pandas                        |                 3 | very-common  |          5 |
|  20 | Boolean masks and indexing             | pandas-boolean-mask-and-indexing    | Pandas                        |                 2 | common       |          5 |
|  21 | Vectorized new columns                 | pandas-vectorized-new-columns       | Pandas                        |                 2 | common       |          5 |
|  22 | map() vs apply()                       | pandas-map-vs-apply                 | Pandas                        |                 3 | very-common  |          5 |
|  23 | String/date columns                    | pandas-string-and-date-columns      | Pandas                        |                 2 | occasional   |          4 |
|  24 | f-strings and .format()                | fstrings-and-format                 | Strings                       |                 3 | very-common  |          4 |
|  25 | Targeted string edits                  | targeted-string-edit-patterns       | Strings                       |                 2 | very-common  |          4 |
|  26 | split(), join(), replace()             | split-join-replace                  | Strings                       |                 3 | signature    |          5 |
|  27 | find(), index(), count()               | find-index-count                    | Strings                       |                 2 | common       |          4 |
|  28 | Case methods and capitalization        | case-and-capitalization             | Strings                       |                 2 | common       |          3 |
|  29 | URL, email, and phone parsing          | url-email-phone-parsing             | Strings                       |                 2 | common       |          5 |
|  30 | MCQ elimination checklist              | mcq-elimination-checklist           | Exam survival                 |                 2 | signature    |          5 |
|  31 | Mutation vs return value               | mutation-vs-return                  | Exam survival                 |                 2 | signature    |          5 |

## Ultra-dense core

> [!info] Preset metadata
> - Slug: `ultra-dense-core`
> - Snippets: `21`
> - Pieces: `43`
> - Approx char count: `10354`
> - Best for: very limited space, wants maximum points per line

**Summary.** Only the highest-yield snippets and their default-selected pieces.

**Why choose it.** Best for students who already remember the basics and want a compact safety net.

|   # | Snippet                                  | Slug                             | Topic                         |   Pieces selected | Recurrence   |   Priority |
|----:|:-----------------------------------------|:---------------------------------|:------------------------------|------------------:|:-------------|-----------:|
|   1 | Slicing patterns                         | slicing-patterns                 | Core Python                   |                 2 | very-common  |          5 |
|   2 | zip() and enumerate() core patterns      | zip-enumerate-core               | Core Python                   |                 2 | signature    |          5 |
|   3 | Types, None, bool, equality              | types-none-bool-equality         | Core Python                   |                 2 | signature    |          5 |
|   4 | timedelta and day counts                 | datetime-timedelta-day-counts    | Datetime                      |                 2 | signature    |          5 |
|   5 | strptime() and strftime()                | datetime-strptime-strftime       | Datetime                      |                 2 | signature    |          5 |
|   6 | List comprehension patterns              | list-comprehension-patterns      | Dictionaries & comprehensions |                 2 | signature    |          5 |
|   7 | Dictionary comprehension patterns        | dict-comprehension-patterns      | Dictionaries & comprehensions |                 2 | signature    |          5 |
|   8 | Build, count, and aggregate dictionaries | dict-build-count-aggregate       | Dictionaries & comprehensions |                 2 | very-common  |          5 |
|   9 | Dictionary iteration and equality        | dict-iteration-equality          | Dictionaries & comprehensions |                 2 | very-common  |          5 |
|  10 | return, None, and function end           | return-none-and-function-end     | Functions & scope             |                 2 | common       |          5 |
|  11 | Local vs global scope                    | local-vs-global-scope            | Functions & scope             |                 2 | signature    |          5 |
|  12 | __init__, self, defaults, attributes     | oop-init-self-defaults           | OOP                           |                 3 | signature    |          5 |
|  13 | Series vs DataFrame                      | pandas-series-vs-dataframe       | Pandas                        |                 2 | signature    |          5 |
|  14 | loc vs iloc                              | pandas-loc-iloc                  | Pandas                        |                 2 | very-common  |          5 |
|  15 | Boolean masks and indexing               | pandas-boolean-mask-and-indexing | Pandas                        |                 2 | common       |          5 |
|  16 | Vectorized new columns                   | pandas-vectorized-new-columns    | Pandas                        |                 2 | common       |          5 |
|  17 | map() vs apply()                         | pandas-map-vs-apply              | Pandas                        |                 2 | very-common  |          5 |
|  18 | split(), join(), replace()               | split-join-replace               | Strings                       |                 2 | signature    |          5 |
|  19 | URL, email, and phone parsing            | url-email-phone-parsing          | Strings                       |                 2 | common       |          5 |
|  20 | MCQ elimination checklist                | mcq-elimination-checklist        | Exam survival                 |                 2 | signature    |          5 |
|  21 | Mutation vs return value                 | mutation-vs-return               | Exam survival                 |                 2 | signature    |          5 |

## Trap hunter

> [!info] Preset metadata
> - Slug: `trap-hunter`
> - Snippets: `20`
> - Pieces: `46`
> - Approx char count: `11504`
> - Best for: knows the material somewhat, mainly loses points to subtle distractors

**Summary.** Focused on the recurrent wrong-answer patterns and elimination traps.

**Why choose it.** Emphasizes mutation-vs-return, pandas shape traps, scope, parse/format, and method-call gotchas.

|   # | Snippet                              | Slug                             | Topic                         |   Pieces selected | Recurrence   |   Priority |
|----:|:-------------------------------------|:---------------------------------|:------------------------------|------------------:|:-------------|-----------:|
|   1 | MCQ elimination checklist            | mcq-elimination-checklist        | Exam survival                 |                 3 | signature    |          5 |
|   2 | Mutation vs return value             | mutation-vs-return               | Exam survival                 |                 2 | signature    |          5 |
|   3 | Types, None, bool, equality          | types-none-bool-equality         | Core Python                   |                 2 | signature    |          5 |
|   4 | Membership and condition logic       | membership-and-condition-logic   | Core Python                   |                 2 | common       |          4 |
|   5 | Built-ins and what they return       | builtins-return-values           | Core Python                   |                 3 | very-common  |          4 |
|   6 | Local vs global scope                | local-vs-global-scope            | Functions & scope             |                 2 | signature    |          5 |
|   7 | return, None, and function end       | return-none-and-function-end     | Functions & scope             |                 2 | common       |          5 |
|   8 | split(), join(), replace()           | split-join-replace               | Strings                       |                 3 | signature    |          5 |
|   9 | Targeted string edits                | targeted-string-edit-patterns    | Strings                       |                 2 | very-common  |          4 |
|  10 | find(), index(), count()             | find-index-count                 | Strings                       |                 2 | common       |          4 |
|  11 | Dictionary iteration and equality    | dict-iteration-equality          | Dictionaries & comprehensions |                 2 | very-common  |          5 |
|  12 | __init__, self, defaults, attributes | oop-init-self-defaults           | OOP                           |                 3 | signature    |          5 |
|  13 | Method calls and self                | oop-method-calls-and-self        | OOP                           |                 2 | common       |          4 |
|  14 | strptime() and strftime()            | datetime-strptime-strftime       | Datetime                      |                 2 | signature    |          5 |
|  15 | Overlap logic                        | datetime-overlap-logic           | Datetime                      |                 3 | occasional   |          4 |
|  16 | Series vs DataFrame                  | pandas-series-vs-dataframe       | Pandas                        |                 2 | signature    |          5 |
|  17 | loc vs iloc                          | pandas-loc-iloc                  | Pandas                        |                 3 | very-common  |          5 |
|  18 | Boolean masks and indexing           | pandas-boolean-mask-and-indexing | Pandas                        |                 2 | common       |          5 |
|  19 | map() vs apply()                     | pandas-map-vs-apply              | Pandas                        |                 2 | very-common  |          5 |
|  20 | sort_index() vs sort_values()        | pandas-sort-index-vs-values      | Pandas                        |                 2 | common       |          4 |

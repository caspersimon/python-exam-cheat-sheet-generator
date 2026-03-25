# Navigation plan

> [!summary] Sidebar proposal
> Topics stay at sidebar level. Subtopics hold snippets grouped into `Start here`, `Add next`, and `Edge cases` sections.

## Exam survival

> [!info] Cross-topic elimination tactics and the most repeated trick families.

### Answering strategy

- slug: `answering-strategy`
- snippets: **1**
- note: Fast elimination and wording-decoder pieces.

#### Start here

- `mcq-elimination-checklist` — MCQ elimination checklist (priority 5, signature)

### Cross-topic traps

- slug: `cross-topic-traps`
- snippets: **1**
- note: Trap families that recur across multiple topic areas.

#### Start here

- `mutation-vs-return` — Mutation vs return value (priority 5, signature)

## Core Python

> [!info] Types, truthiness, indexing, slicing, loops, and small built-ins.

### Syntax basics

- slug: `syntax-basics`
- snippets: **1**
- note: Tiny syntax fragments, raw strings, escape sequences, comments, and line continuation.

#### Start here

- `syntax-fragments-escapes-raw-strings` — Syntax fragments, escapes, and raw strings (priority 4, rare)

### Objects & names

- slug: `objects-names`
- snippets: **1**
- note: Name binding, aliasing, copies, equality versus identity.

#### Start here

- `names-aliasing-and-copies` — Names, aliasing, and copies (priority 4, occasional)

### Types & conditions

- slug: `types-conditions`
- snippets: **4**
- note: Truthiness, equality, membership, and built-ins.

#### Start here

- `types-none-bool-equality` — Types, None, bool, equality (priority 5, signature)
- `builtins-return-values` — Built-ins and what they return (priority 4, very-common)

#### Add next

- `membership-and-condition-logic` — Membership and condition logic (priority 4, common)

#### Edge cases

- `numeric-corner-cases` — Numeric corner cases (priority 3, rare)

### Lists, slicing & loops

- slug: `lists-loops`
- snippets: **6**
- note: Indexing, slicing, iteration templates, zip/enumerate.

#### Start here

- `zip-enumerate-core` — zip() and enumerate() core patterns (priority 5, signature)
- `slicing-patterns` — Slicing patterns (priority 5, very-common)
- `list-selection-and-aggregation` — List selection and aggregation (priority 3, very-common)

#### Add next

- `loop-templates` — Loop templates (priority 4, common)
- `nested-indexing-and-negative-indices` — Nested indexing and negative indices (priority 4, occasional)

#### Edge cases

- `loop-control-and-iterators` — Loop control and iterators (priority 3, rare)

## Functions & scope

> [!info] Returns, parameters, scope, imports, and higher-order call patterns.

### Returns & scope

- slug: `returns-scope`
- snippets: **2**
- note: Implicit None, local/global rules, and variable lifetime.

#### Start here

- `local-vs-global-scope` — Local vs global scope (priority 5, signature)
- `return-none-and-function-end` — return, None, and function end (priority 5, common)

### Parameters & flexible args

- slug: `parameters-flexible-args`
- snippets: **2**
- note: Defaults, keyword binding, *args, **kwargs.

#### Start here

- `args-and-kwargs` — *args and **kwargs (priority 4, signature)
- `defaults-keyword-arguments` — Defaults and keyword arguments (priority 4, very-common)

### Imports & lambda

- slug: `imports-lambda`
- snippets: **2**
- note: Import names, aliases, lambda, and call shapes.

#### Add next

- `higher-order-lambda` — Higher-order functions and lambda (priority 4, common)

#### Edge cases / niche

- `imports-and-aliases` — Imports and aliases (priority 3, rare)

## Strings

> [!info] String methods, formatting, and parsing mini-problems.

### Methods

- slug: `methods`
- snippets: **3**
- note: split/join/replace/find/count/case methods.

#### Start here

- `split-join-replace` — split(), join(), replace() (priority 5, signature)

#### Add next

- `find-index-count` — find(), index(), count() (priority 4, common)
- `case-and-capitalization` — Case methods and capitalization (priority 3, common)

### Formatting

- slug: `formatting`
- snippets: **2**
- note: f-strings, .format(), and targeted edits.

#### Start here

- `fstrings-and-format` — f-strings and .format() (priority 4, very-common)
- `targeted-string-edit-patterns` — Targeted string edits (priority 4, very-common)

### Parsing

- slug: `parsing`
- snippets: **1**
- note: URL, email, and phone parsing patterns.

#### Start here

- `url-email-phone-parsing` — URL, email, and phone parsing (priority 5, common)

## Dictionaries & comprehensions

> [!info] Building mappings, comprehension syntax, sets, and dict iteration.

### Dictionary patterns

- slug: `dicts`
- snippets: **3**
- note: Counting, aggregation, iteration, equality, running links.

#### Start here

- `dict-build-count-aggregate` — Build, count, and aggregate dictionaries (priority 5, very-common)
- `dict-iteration-equality` — Dictionary iteration and equality (priority 5, very-common)

#### Add next

- `dict-running-totals-and-next-links` — Running totals and next-link dictionaries (priority 4, occasional)

### Comprehensions

- slug: `comprehensions`
- snippets: **3**
- note: List/dict/set comprehension construction and syntax placement.

#### Start here

- `dict-comprehension-patterns` — Dictionary comprehension patterns (priority 5, signature)
- `list-comprehension-patterns` — List comprehension patterns (priority 5, signature)

#### Edge cases / niche

- `set-vs-list-vs-dict` — Set vs list vs dict (priority 3, rare)

## OOP

> [!info] Constructors, state, methods, and object comparison/reporting patterns.

### Constructors & state

- slug: `constructors-and-state`
- snippets: **2**
- note: What goes in __init__, where state lives, collection attributes.

#### Start here

- `oop-init-self-defaults` — __init__, self, defaults, attributes (priority 5, signature)
- `oop-state-and-collection-attributes` — Object state and collection attributes (priority 4, signature)

### Methods & comparison

- slug: `methods-and-comparison`
- snippets: **2**
- note: self, method calls, comparison/reporting patterns.

#### Start here

- `oop-compare-and-report-patterns` — Compare/report method patterns (priority 4, signature)

#### Add next

- `oop-method-calls-and-self` — Method calls and self (priority 4, common)

### Inheritance

- slug: `inheritance`
- snippets: **1**
- note: Subclass syntax, super(), inherited methods, and parent/child relationships.

#### Start here

- `oop-inheritance-core` — Inheritance core patterns (priority 3, rare)

## Datetime

> [!info] Parsing, formatting, date arithmetic, overlap logic, and date sequences.

### Parsing & formatting

- slug: `parsing-formatting`
- snippets: **2**
- note: strptime/strftime and building datetime objects.

#### Start here

- `datetime-strptime-strftime` — strptime() and strftime() (priority 5, signature)
- `datetime-build-from-parts` — Build datetimes from parts (priority 4, very-common)

### Arithmetic & overlap

- slug: `arithmetic-and-overlap`
- snippets: **2**
- note: timedelta, day counts, date windows, overlap logic.

#### Start here

- `datetime-timedelta-day-counts` — timedelta and day counts (priority 5, signature)

#### Add next

- `datetime-overlap-logic` — Overlap logic (priority 4, occasional)

### Sequence generation

- slug: `sequence-generation`
- snippets: **1**
- note: Build repeated date sequences from ranges or dicts.

#### Add next

- `datetime-sequence-generation` — Date sequences (priority 4, common)

## Pandas

> [!info] Selection, transforms, boolean masks, construction, and sorting.

### Selection

- slug: `selection`
- snippets: **3**
- note: Series/DataFrame, loc/iloc, masks, index alignment.

#### Start here

- `pandas-series-vs-dataframe` — Series vs DataFrame (priority 5, signature)
- `pandas-loc-iloc` — loc vs iloc (priority 5, very-common)
- `pandas-boolean-mask-and-indexing` — Boolean masks and indexing (priority 5, common)

### Transforms

- slug: `transforms`
- snippets: **4**
- note: Vectorized columns, map/apply, string/date transforms.

#### Start here

- `pandas-map-vs-apply` — map() vs apply() (priority 5, very-common)
- `pandas-vectorized-new-columns` — Vectorized new columns (priority 5, common)

#### Add next

- `pandas-string-and-date-columns` — String/date columns (priority 4, occasional)

#### Edge cases

- `pandas-missing-values-alignment` — Missing values and index alignment (priority 3, rare)

### Construction & sorting

- slug: `construction-and-sorting`
- snippets: **2**
- note: Creating DataFrames and sorting them correctly.

#### Add next

- `pandas-sort-index-vs-values` — sort_index() vs sort_values() (priority 4, common)

#### Edge cases / niche

- `pandas-build-from-args` — Build DataFrames from arguments (priority 3, rare)

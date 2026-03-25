# Navigation plan

> [!summary] Purpose
> This is the final step-9 navigation recommendation for the frontend.
> It keeps the existing website idea intact:
> topic -> subtopic -> snippet grid
>
> The extra curation layer is the snippet-group header inside each subtopic:
>
> - `Start here`
> - `Add next`
> - `Edge cases / niche`

> [!tip] Why these section headers exist
> They make it easier to find the highest-yield snippets first without hiding the long-tail material.

## Sidebar structure

| Topic                    |   # | Subtopic                   | Slug                     |   Snippets |
|:-------------------------|----:|:---------------------------|:-------------------------|-----------:|
| core-python              |   1 | Types & conditions         | types-conditions         |          3 |
| core-python              |   2 | Lists, slicing & loops     | lists-loops              |          5 |
| datetime                 |   1 | Parsing & formatting       | parsing-formatting       |          2 |
| datetime                 |   2 | Arithmetic & overlap       | arithmetic-and-overlap   |          2 |
| datetime                 |   3 | Sequence generation        | sequence-generation      |          1 |
| dicts-and-comprehensions |   1 | Dictionary patterns        | dicts                    |          3 |
| dicts-and-comprehensions |   2 | Comprehensions             | comprehensions           |          3 |
| functions-and-scope      |   1 | Returns & scope            | returns-scope            |          2 |
| functions-and-scope      |   2 | Parameters & flexible args | parameters-flexible-args |          2 |
| functions-and-scope      |   3 | Imports & lambda           | imports-lambda           |          2 |
| oop                      |   1 | Constructors & state       | constructors-and-state   |          2 |
| oop                      |   2 | Methods & comparison       | methods-and-comparison   |          2 |
| pandas                   |   1 | Selection                  | selection                |          3 |
| pandas                   |   2 | Transforms                 | transforms               |          3 |
| pandas                   |   3 | Construction & sorting     | construction-and-sorting |          2 |
| strings                  |   1 | Methods                    | methods                  |          3 |
| strings                  |   2 | Formatting                 | formatting               |          2 |
| strings                  |   3 | Parsing                    | parsing                  |          1 |
| survival                 |   1 | Answering strategy         | answering-strategy       |          1 |
| survival                 |   2 | Cross-topic traps          | cross-topic-traps        |          1 |

## Grid grouping recommendation

- group cards by `ui_section_title`
- within a section, sort by `ui_card_order`
- show recurrence / phase / trap-heavy badges on each card
- let users sort secondarily by priority or recurrence if needed


# Exam survival

> [!info] Topic summary
> Cross-topic elimination tactics and the most repeated trick families.
> Total snippets: **2**

## Answering strategy

> [!tip] Subtopic summary
> Fast elimination and wording-decoder pieces.
> Total snippets: **1**

### Start here

|   # | Snippet                   | Slug                      |   Priority | Recurrence   |   Default pieces |   Total pieces |   Q refs |   Trap slugs |
|----:|:--------------------------|:--------------------------|-----------:|:-------------|-----------------:|---------------:|---------:|-------------:|
|   1 | MCQ elimination checklist | mcq-elimination-checklist |          5 | signature    |                2 |              4 |        8 |            4 |

## Cross-topic traps

> [!tip] Subtopic summary
> Trap families that recur across multiple topic areas.
> Total snippets: **1**

### Start here

|   # | Snippet                  | Slug               |   Priority | Recurrence   |   Default pieces |   Total pieces |   Q refs |   Trap slugs |
|----:|:-------------------------|:-------------------|-----------:|:-------------|-----------------:|---------------:|---------:|-------------:|
|   1 | Mutation vs return value | mutation-vs-return |          5 | signature    |                2 |              3 |        6 |            3 |

# Core Python

> [!info] Topic summary
> Types, truthiness, indexing, slicing, loops, and small built-ins.
> Total snippets: **8**

## Types & conditions

> [!tip] Subtopic summary
> Truthiness, equality, membership, and built-ins.
> Total snippets: **3**

### Start here

|   # | Snippet                        | Slug                     |   Priority | Recurrence   |   Default pieces |   Total pieces |   Q refs |   Trap slugs |
|----:|:-------------------------------|:-------------------------|-----------:|:-------------|-----------------:|---------------:|---------:|-------------:|
|   1 | Types, None, bool, equality    | types-none-bool-equality |          5 | signature    |                2 |              3 |       15 |            4 |
|   2 | Built-ins and what they return | builtins-return-values   |          4 | very-common  |                2 |              4 |       11 |            2 |

### Add next

|   # | Snippet                        | Slug                           |   Priority | Recurrence   |   Default pieces |   Total pieces |   Q refs |   Trap slugs |
|----:|:-------------------------------|:-------------------------------|-----------:|:-------------|-----------------:|---------------:|---------:|-------------:|
|   1 | Membership and condition logic | membership-and-condition-logic |          4 | common       |                2 |              4 |        5 |            2 |

## Lists, slicing & loops

> [!tip] Subtopic summary
> Indexing, slicing, iteration templates, zip/enumerate.
> Total snippets: **5**

### Start here

|   # | Snippet                             | Slug                           |   Priority | Recurrence   |   Default pieces |   Total pieces |   Q refs |   Trap slugs |
|----:|:------------------------------------|:-------------------------------|-----------:|:-------------|-----------------:|---------------:|---------:|-------------:|
|   1 | zip() and enumerate() core patterns | zip-enumerate-core             |          5 | signature    |                2 |              3 |       14 |            2 |
|   2 | Slicing patterns                    | slicing-patterns               |          5 | very-common  |                2 |              3 |        9 |            2 |
|   3 | List selection and aggregation      | list-selection-and-aggregation |          3 | very-common  |                2 |              3 |        6 |            2 |

### Add next

|   # | Snippet                              | Slug                                 |   Priority | Recurrence   |   Default pieces |   Total pieces |   Q refs |   Trap slugs |
|----:|:-------------------------------------|:-------------------------------------|-----------:|:-------------|-----------------:|---------------:|---------:|-------------:|
|   1 | Loop templates                       | loop-templates                       |          4 | common       |                2 |              3 |        5 |            2 |
|   2 | Nested indexing and negative indices | nested-indexing-and-negative-indices |          4 | occasional   |                2 |              3 |        3 |            2 |

# Functions & scope

> [!info] Topic summary
> Returns, parameters, scope, imports, and higher-order call patterns.
> Total snippets: **6**

## Returns & scope

> [!tip] Subtopic summary
> Implicit None, local/global rules, and variable lifetime.
> Total snippets: **2**

### Start here

|   # | Snippet                        | Slug                         |   Priority | Recurrence   |   Default pieces |   Total pieces |   Q refs |   Trap slugs |
|----:|:-------------------------------|:-----------------------------|-----------:|:-------------|-----------------:|---------------:|---------:|-------------:|
|   1 | Local vs global scope          | local-vs-global-scope        |          5 | signature    |                2 |              3 |        7 |            2 |
|   2 | return, None, and function end | return-none-and-function-end |          5 | common       |                2 |              3 |        6 |            2 |

## Parameters & flexible args

> [!tip] Subtopic summary
> Defaults, keyword binding, *args, **kwargs.
> Total snippets: **2**

### Start here

|   # | Snippet                        | Slug                       |   Priority | Recurrence   |   Default pieces |   Total pieces |   Q refs |   Trap slugs |
|----:|:-------------------------------|:---------------------------|-----------:|:-------------|-----------------:|---------------:|---------:|-------------:|
|   1 | *args and **kwargs             | args-and-kwargs            |          4 | signature    |                2 |              3 |        7 |            2 |
|   2 | Defaults and keyword arguments | defaults-keyword-arguments |          4 | very-common  |                2 |              3 |        7 |            2 |

## Imports & lambda

> [!tip] Subtopic summary
> Import names, aliases, lambda, and call shapes.
> Total snippets: **2**

### Add next

|   # | Snippet                           | Slug                |   Priority | Recurrence   |   Default pieces |   Total pieces |   Q refs |   Trap slugs |
|----:|:----------------------------------|:--------------------|-----------:|:-------------|-----------------:|---------------:|---------:|-------------:|
|   1 | Higher-order functions and lambda | higher-order-lambda |          4 | common       |                1 |              3 |        5 |            1 |

### Edge cases / niche

|   # | Snippet             | Slug                |   Priority | Recurrence   |   Default pieces |   Total pieces |   Q refs |   Trap slugs |
|----:|:--------------------|:--------------------|-----------:|:-------------|-----------------:|---------------:|---------:|-------------:|
|   1 | Imports and aliases | imports-and-aliases |          3 | rare         |                2 |              2 |        2 |            1 |

# Strings

> [!info] Topic summary
> String methods, formatting, and parsing mini-problems.
> Total snippets: **6**

## Methods

> [!tip] Subtopic summary
> split/join/replace/find/count/case methods.
> Total snippets: **3**

### Start here

|   # | Snippet                    | Slug               |   Priority | Recurrence   |   Default pieces |   Total pieces |   Q refs |   Trap slugs |
|----:|:---------------------------|:-------------------|-----------:|:-------------|-----------------:|---------------:|---------:|-------------:|
|   1 | split(), join(), replace() | split-join-replace |          5 | signature    |                2 |              3 |       12 |            2 |

### Add next

|   # | Snippet                         | Slug                    |   Priority | Recurrence   |   Default pieces |   Total pieces |   Q refs |   Trap slugs |
|----:|:--------------------------------|:------------------------|-----------:|:-------------|-----------------:|---------------:|---------:|-------------:|
|   1 | find(), index(), count()        | find-index-count        |          4 | common       |                2 |              3 |        5 |            2 |
|   2 | Case methods and capitalization | case-and-capitalization |          3 | common       |                2 |              2 |        5 |            1 |

## Formatting

> [!tip] Subtopic summary
> f-strings, .format(), and targeted edits.
> Total snippets: **2**

### Start here

|   # | Snippet                 | Slug                          |   Priority | Recurrence   |   Default pieces |   Total pieces |   Q refs |   Trap slugs |
|----:|:------------------------|:------------------------------|-----------:|:-------------|-----------------:|---------------:|---------:|-------------:|
|   1 | f-strings and .format() | fstrings-and-format           |          4 | very-common  |                2 |              4 |        7 |            2 |
|   2 | Targeted string edits   | targeted-string-edit-patterns |          4 | very-common  |                2 |              3 |        6 |            2 |

## Parsing

> [!tip] Subtopic summary
> URL, email, and phone parsing patterns.
> Total snippets: **1**

### Start here

|   # | Snippet                       | Slug                    |   Priority | Recurrence   |   Default pieces |   Total pieces |   Q refs |   Trap slugs |
|----:|:------------------------------|:------------------------|-----------:|:-------------|-----------------:|---------------:|---------:|-------------:|
|   1 | URL, email, and phone parsing | url-email-phone-parsing |          5 | common       |                2 |              3 |        5 |            2 |

# Dictionaries & comprehensions

> [!info] Topic summary
> Building mappings, comprehension syntax, sets, and dict iteration.
> Total snippets: **6**

## Dictionary patterns

> [!tip] Subtopic summary
> Counting, aggregation, iteration, equality, running links.
> Total snippets: **3**

### Start here

|   # | Snippet                                  | Slug                       |   Priority | Recurrence   |   Default pieces |   Total pieces |   Q refs |   Trap slugs |
|----:|:-----------------------------------------|:---------------------------|-----------:|:-------------|-----------------:|---------------:|---------:|-------------:|
|   1 | Build, count, and aggregate dictionaries | dict-build-count-aggregate |          5 | very-common  |                2 |              3 |       11 |            2 |
|   2 | Dictionary iteration and equality        | dict-iteration-equality    |          5 | very-common  |                2 |              3 |        9 |            2 |

### Add next

|   # | Snippet                                   | Slug                               |   Priority | Recurrence   |   Default pieces |   Total pieces |   Q refs |   Trap slugs |
|----:|:------------------------------------------|:-----------------------------------|-----------:|:-------------|-----------------:|---------------:|---------:|-------------:|
|   1 | Running totals and next-link dictionaries | dict-running-totals-and-next-links |          4 | occasional   |                2 |              3 |        3 |            2 |

## Comprehensions

> [!tip] Subtopic summary
> List/dict/set comprehension construction and syntax placement.
> Total snippets: **3**

### Start here

|   # | Snippet                           | Slug                        |   Priority | Recurrence   |   Default pieces |   Total pieces |   Q refs |   Trap slugs |
|----:|:----------------------------------|:----------------------------|-----------:|:-------------|-----------------:|---------------:|---------:|-------------:|
|   1 | Dictionary comprehension patterns | dict-comprehension-patterns |          5 | signature    |                2 |              3 |       10 |            2 |
|   2 | List comprehension patterns       | list-comprehension-patterns |          5 | signature    |                2 |              3 |        7 |            1 |

### Edge cases / niche

|   # | Snippet             | Slug                |   Priority | Recurrence   |   Default pieces |   Total pieces |   Q refs |   Trap slugs |
|----:|:--------------------|:--------------------|-----------:|:-------------|-----------------:|---------------:|---------:|-------------:|
|   1 | Set vs list vs dict | set-vs-list-vs-dict |          3 | rare         |                1 |              2 |        2 |            2 |

# OOP

> [!info] Topic summary
> Constructors, state, methods, and object comparison/reporting patterns.
> Total snippets: **4**

## Constructors & state

> [!tip] Subtopic summary
> What goes in __init__, where state lives, collection attributes.
> Total snippets: **2**

### Start here

|   # | Snippet                                | Slug                                |   Priority | Recurrence   |   Default pieces |   Total pieces |   Q refs |   Trap slugs |
|----:|:---------------------------------------|:------------------------------------|-----------:|:-------------|-----------------:|---------------:|---------:|-------------:|
|   1 | __init__, self, defaults, attributes   | oop-init-self-defaults              |          5 | signature    |                3 |              3 |       10 |            4 |
|   2 | Object state and collection attributes | oop-state-and-collection-attributes |          4 | signature    |                2 |              5 |        7 |            2 |

## Methods & comparison

> [!tip] Subtopic summary
> self, method calls, comparison/reporting patterns.
> Total snippets: **2**

### Start here

|   # | Snippet                        | Slug                            |   Priority | Recurrence   |   Default pieces |   Total pieces |   Q refs |   Trap slugs |
|----:|:-------------------------------|:--------------------------------|-----------:|:-------------|-----------------:|---------------:|---------:|-------------:|
|   1 | Compare/report method patterns | oop-compare-and-report-patterns |          4 | signature    |                3 |              3 |        7 |            2 |

### Add next

|   # | Snippet               | Slug                      |   Priority | Recurrence   |   Default pieces |   Total pieces |   Q refs |   Trap slugs |
|----:|:----------------------|:--------------------------|-----------:|:-------------|-----------------:|---------------:|---------:|-------------:|
|   1 | Method calls and self | oop-method-calls-and-self |          4 | common       |                2 |              3 |        4 |            2 |

# Datetime

> [!info] Topic summary
> Parsing, formatting, date arithmetic, overlap logic, and date sequences.
> Total snippets: **5**

## Parsing & formatting

> [!tip] Subtopic summary
> strptime/strftime and building datetime objects.
> Total snippets: **2**

### Start here

|   # | Snippet                    | Slug                       |   Priority | Recurrence   |   Default pieces |   Total pieces |   Q refs |   Trap slugs |
|----:|:---------------------------|:---------------------------|-----------:|:-------------|-----------------:|---------------:|---------:|-------------:|
|   1 | strptime() and strftime()  | datetime-strptime-strftime |          5 | signature    |                2 |              3 |       12 |            2 |
|   2 | Build datetimes from parts | datetime-build-from-parts  |          4 | very-common  |                2 |              3 |        6 |            2 |

## Arithmetic & overlap

> [!tip] Subtopic summary
> timedelta, day counts, date windows, overlap logic.
> Total snippets: **2**

### Start here

|   # | Snippet                  | Slug                          |   Priority | Recurrence   |   Default pieces |   Total pieces |   Q refs |   Trap slugs |
|----:|:-------------------------|:------------------------------|-----------:|:-------------|-----------------:|---------------:|---------:|-------------:|
|   1 | timedelta and day counts | datetime-timedelta-day-counts |          5 | signature    |                2 |              3 |        7 |            2 |

### Add next

|   # | Snippet       | Slug                   |   Priority | Recurrence   |   Default pieces |   Total pieces |   Q refs |   Trap slugs |
|----:|:--------------|:-----------------------|-----------:|:-------------|-----------------:|---------------:|---------:|-------------:|
|   1 | Overlap logic | datetime-overlap-logic |          4 | occasional   |                3 |              3 |        2 |            2 |

## Sequence generation

> [!tip] Subtopic summary
> Build repeated date sequences from ranges or dicts.
> Total snippets: **1**

### Add next

|   # | Snippet        | Slug                         |   Priority | Recurrence   |   Default pieces |   Total pieces |   Q refs |   Trap slugs |
|----:|:---------------|:-----------------------------|-----------:|:-------------|-----------------:|---------------:|---------:|-------------:|
|   1 | Date sequences | datetime-sequence-generation |          4 | common       |                3 |              3 |        4 |            2 |

# Pandas

> [!info] Topic summary
> Selection, transforms, boolean masks, construction, and sorting.
> Total snippets: **8**

## Selection

> [!tip] Subtopic summary
> Series/DataFrame, loc/iloc, masks, index alignment.
> Total snippets: **3**

### Start here

|   # | Snippet                    | Slug                             |   Priority | Recurrence   |   Default pieces |   Total pieces |   Q refs |   Trap slugs |
|----:|:---------------------------|:---------------------------------|-----------:|:-------------|-----------------:|---------------:|---------:|-------------:|
|   1 | Series vs DataFrame        | pandas-series-vs-dataframe       |          5 | signature    |                2 |              3 |        7 |            1 |
|   2 | loc vs iloc                | pandas-loc-iloc                  |          5 | very-common  |                2 |              3 |        8 |            2 |
|   3 | Boolean masks and indexing | pandas-boolean-mask-and-indexing |          5 | common       |                2 |              3 |        5 |            2 |

## Transforms

> [!tip] Subtopic summary
> Vectorized columns, map/apply, string/date transforms.
> Total snippets: **3**

### Start here

|   # | Snippet                | Slug                          |   Priority | Recurrence   |   Default pieces |   Total pieces |   Q refs |   Trap slugs |
|----:|:-----------------------|:------------------------------|-----------:|:-------------|-----------------:|---------------:|---------:|-------------:|
|   1 | map() vs apply()       | pandas-map-vs-apply           |          5 | very-common  |                2 |              3 |        7 |            2 |
|   2 | Vectorized new columns | pandas-vectorized-new-columns |          5 | common       |                2 |              3 |        7 |            2 |

### Add next

|   # | Snippet             | Slug                           |   Priority | Recurrence   |   Default pieces |   Total pieces |   Q refs |   Trap slugs |
|----:|:--------------------|:-------------------------------|-----------:|:-------------|-----------------:|---------------:|---------:|-------------:|
|   1 | String/date columns | pandas-string-and-date-columns |          4 | occasional   |                2 |              3 |        3 |            2 |

## Construction & sorting

> [!tip] Subtopic summary
> Creating DataFrames and sorting them correctly.
> Total snippets: **2**

### Add next

|   # | Snippet                       | Slug                        |   Priority | Recurrence   |   Default pieces |   Total pieces |   Q refs |   Trap slugs |
|----:|:------------------------------|:----------------------------|-----------:|:-------------|-----------------:|---------------:|---------:|-------------:|
|   1 | sort_index() vs sort_values() | pandas-sort-index-vs-values |          4 | common       |                2 |              3 |        4 |            1 |

### Edge cases / niche

|   # | Snippet                         | Slug                   |   Priority | Recurrence   |   Default pieces |   Total pieces |   Q refs |   Trap slugs |
|----:|:--------------------------------|:-----------------------|-----------:|:-------------|-----------------:|---------------:|---------:|-------------:|
|   1 | Build DataFrames from arguments | pandas-build-from-args |          3 | rare         |                2 |              2 |        2 |            1 |

# Round 1 Manual Review Packet

This packet is a hand-synthesized review document based on:

- `data/vision_exam_pipeline/synthesis/round1.json`
- `data/vision_exam_pipeline/evaluations/round1.json`
- `data/vision_exam_pipeline/analytics/round1.json`

The goal is not to preserve all 151 raw suggestions. It is to collapse semantically duplicate edit/addition requests into decision-ready clusters for human review.

## Current State

- Completed question evaluations: `168 / 168`
- Answerable with certainty: `88`
- Partially answerable: `40`
- Insufficient with current snippets: `40`
- We are at the human review gate before any snippet/content implementation round.

## Recommended Review Order

1. Strings, slicing, formatting, and basic operators
2. Iteration helpers and comprehension syntax
3. Dictionary construction and iteration patterns
4. Pandas selection/indexing/filtering
5. Datetime parsing, formatting, and arithmetic
6. OOP fundamentals and comparison logic
7. Flexible function signatures, return semantics, and scope cleanup
8. Exact-match retrieval fixes for existing snippets

## Deduplicated Recommendation Clusters

### 1. Essential String Methods and Indexing Reference

- Absorbs duplicate requests about `.split()`, `.join()`, `.replace()`, `.find()`, negative indexing, slicing, nested indexing, `.index()`, and reverse-step slicing.
- Representative raw asks include:
  - `round1:12`
  - `round1:84`
  - `round1:96`
  - `round1:103`
  - `round1:104`
  - `round1:132`
- Why it helps:
  - This is the single biggest beginner-mechanics gap in the round-1 evaluations.
  - It would directly reduce the large cluster of string-method and indexing questions that are currently partial or insufficient.
  - It should replace many tiny string-specific additions with one reusable exam-oriented reference.
- Why it may not be necessary:
  - Some exact-match exam snippets already solve the concrete questions if the user happens to find the right one.
  - A very large card could become bloated if it tries to cover every string method.
- Suggested direction: `add`
- Preferred form:
  - One compact card titled something like `Essential String Methods and Indexing`
  - Include only exam-relevant primitives and 4-6 tiny examples

### 2. Output Formatting and String Construction

- Absorbs duplicate requests about f-strings, `.format()`, decimal formatting, list-to-sentence output, and cases where `join()` is not enough because the required output contains custom wording like `", and "`.
- Representative raw asks include:
  - `round1:58`
  - `round1:85`
  - `round1:105`
  - `round1:122`
  - `round1:136`
- Why it helps:
  - Several questions are not conceptually hard; they fail because the user cannot reconstruct the exact output format.
  - One card would cover both beginner formatting syntax and common exam traps.
- Why it may not be necessary:
  - There is overlap with the broader string-method cluster above.
  - If space is tight, this could be merged into the same string card instead of becoming its own standalone item.
- Suggested direction: `add`, but merge into cluster 1 if density becomes a concern.

### 3. Boolean String Predicates

- Absorbs duplicate requests about `.islower()`, `.isupper()`, `.isdigit()`, and how punctuation/spaces affect those methods.
- Representative raw asks include:
  - `round1:80`
  - `round1:101`
  - `round1:127`
- Why it helps:
  - This exact gap appeared in repeated evaluations of the same style of question.
  - It is especially useful for zero-knowledge users who cannot infer the non-letter behavior of these methods.
- Why it may not be necessary:
  - This is too narrow to justify a standalone large card.
  - It fits naturally as a sub-block inside the string reference.
- Suggested direction: `add`, but as a subsection of cluster 1, not as a separate standalone snippet.

### 4. Iteration Helpers and Basic Operator Traps

- Absorbs duplicate requests about `zip()`, `enumerate()`, membership with `in`, tuple unpacking in loops, `//`, `%`, and boolean-to-int counting with `sum(...)`.
- Representative raw asks include:
  - `round1:10`
  - `round1:22`
  - `round1:26`
  - `round1:50`
  - `round1:54`
  - `round1:70`
  - `round1:81`
  - `round1:102`
  - `round1:131`
  - `round1:149`
- Why it helps:
  - This is one of the clearest duplicate families in the synthesis.
  - The same mechanics recur across multiple exams and multiple weeks.
  - A compact reference would make several currently-insufficient questions fully answerable.
- Why it may not be necessary:
  - The operator half is slightly broader than the iteration half.
  - If the card gets too wide, the operator notes could instead be added to an existing fundamentals key point.
- Suggested direction: `add`
- Preferred form:
  - One card for `zip`, `enumerate`, tuple unpacking, and membership
  - One small sidebar/subsection for `/` vs `//`, `%`, and boolean counting with `sum(...)`

### 5. Comprehension Syntax Reference

- Absorbs duplicate requests about list, dict, and set comprehensions; placement of `key: value`; filter-vs-transform syntax; and conditional expressions inside comprehensions.
- Representative raw asks include:
  - `round1:23`
  - `round1:28`
  - `round1:49`
  - `round1:126`
  - `round1:129`
  - `round1:143`
  - `round1:147`
- Why it helps:
  - Many questions are failing because the syntax is not recognized quickly enough.
  - This is a high-yield addition because it unifies several repeated requests into one pattern card.
- Why it may not be necessary:
  - Some comprehension questions already have direct-match exam snippets.
  - A card that is too abstract could be less useful than a syntax table with tiny examples.
- Suggested direction: `add`

### 6. Dictionary Construction and Iteration Patterns

- Absorbs duplicate requests about dictionary comprehensions, `dict(zip(...))`, `.keys()`, `.values()`, `.items()`, sorted dictionary iteration, dictionary equality, and counting patterns.
- Representative raw asks include:
  - `round1:16`
  - `round1:19`
  - `round1:76`
  - `round1:79`
  - `round1:97`
  - `round1:99`
  - `round1:130`
  - `round1:148`
  - `round1:150`
- Why it helps:
  - The synthesis shows two superficially separate clusters here, but they are really one decision: users need a compact dictionary reference that covers both construction and iteration.
  - This cluster spans exact-match retrieval fixes and genuine concept gaps.
- Why it may not be necessary:
  - Some of these requests are already covered by strong existing exam snippets.
  - If we overbuild this, it may become a generic Python dictionary page rather than an exam tool.
- Suggested direction: `add`
- Preferred form:
  - Focus on exam mechanics only: comprehension template, `dict(zip(...))`, `.keys/.values/.items`, `sum(d.values())`, equality ignoring insertion order, and sorted traversal

### 7. Pandas Selection and Indexing Rules

- Absorbs duplicate requests about `df['col']`, `df[['col1', 'col2']]`, `.loc`, `.iloc`, boolean masks, row/column selection, and invalid indexing forms like `df[row, col]`.
- Representative raw asks include:
  - `round1:6`
  - `round1:35`
  - `round1:59`
  - `round1:89`
  - `round1:111`
  - `round1:139`
- Why it helps:
  - This is the clearest Pandas gap in the evaluation set.
  - Several currently-insufficient questions would become much easier with one rule-based card.
- Why it may not be necessary:
  - Week 5 already has some very strong exact-match snippets.
  - A weak generic Pandas card could duplicate those without improving retrieval.
- Suggested direction: `add`
- Preferred form:
  - A strict, example-heavy “valid vs invalid” indexing reference

### 8. Pandas Filtering, Aggregation, and Column Arithmetic

- Absorbs duplicate requests about boolean filtering, `mean()`, `sum()`, `count()`, `sort_values`, and row-wise column arithmetic like `df['C'] = df['A'] + df['B']` or subtraction.
- Representative raw asks include:
  - `round1:5`
  - `round1:7`
  - `round1:65`
  - `round1:93`
  - `round1:95`
  - `round1:137`
- Why it helps:
  - This is another recurring Pandas failure mode, especially for students with no prior intuition for vectorized column operations.
  - It complements cluster 7 cleanly.
- Why it may not be necessary:
  - Some of the strongest existing snippets in the whole dataset are already Week 5 Pandas source exams.
  - This may be better as an edit/expansion of existing high-performing Pandas snippets instead of a wholly new card.
- Suggested direction: `consider add`, leaning `edit existing` if you want to stay lean.

### 9. Lambda, `map`, and `apply`

- Absorbs duplicate requests about what `lambda x` means, how `.map()` differs from passing a precomputed Series, and when `apply(..., axis=1)` is needed.
- Representative raw asks include:
  - `round1:4`
  - `round1:21`
  - `round1:41`
  - `round1:66`
  - `round1:94`
  - `round1:119`
- Why it helps:
  - This is a genuine conceptual gap and repeatedly appears in both Pandas and non-Pandas forms.
  - One compact card would be much better than multiple micro-snippets.
- Why it may not be necessary:
  - If added, it should be tightly scoped. A generic lambda tutorial would be too broad for the cheat sheet.
  - Some of this could be absorbed into existing Week 5 Pandas examples.
- Suggested direction: `add`

### 10. Datetime Parse/Format Cheat Sheet

- Absorbs duplicate requests about `datetime(...)`, `strptime`, `strftime`, and format-code references such as `%Y`, `%m`, `%d`, `%H`, and `%M`.
- Representative raw asks include:
  - `round1:11`
  - `round1:36`
  - `round1:60`
  - `round1:88`
  - `round1:92`
  - `round1:110`
  - `round1:116`
  - `round1:124`
  - `round1:125`
  - `round1:141`
- Why it helps:
  - Datetime requests are heavily duplicated and mostly point to one missing artifact: a compact parse/format reference.
  - This is one of the cleanest “many duplicate requests, one right addition” clusters in the whole review.
- Why it may not be necessary:
  - None of the individual asks need to be implemented separately if this one cheat sheet exists.
  - It only becomes unnecessary if the existing Week 6 content is already sufficient for the intended exam style, which the evaluations suggest it is not.
- Suggested direction: `add`

### 11. Datetime Object-vs-String Arithmetic

- Absorbs duplicate requests about `timedelta`, adding minutes/days, extracting day/month/year, and the crucial distinction that `strptime` returns a datetime object while `strftime` returns a string.
- Representative raw asks include:
  - `round1:42`
  - `round1:43`
  - `round1:67`
  - `round1:69`
  - `round1:91`
  - `round1:115`
  - `round1:142`
- Why it helps:
  - Several round-1 failures are not about formatting codes; they are about reasoning with datetime objects after parsing.
  - This is a separate conceptual cluster from parse/format syntax.
- Why it may not be necessary:
  - If the parse/format cheat sheet is carefully designed, much of this can be embedded there instead of creating a second large datetime card.
- Suggested direction: `add`, but preferably as part 2 of the same datetime reference family rather than a disconnected standalone card.

### 12. OOP Fundamentals: `self`, `__init__`, Attributes, and Defaults

- Absorbs duplicate requests about assigning to `self`, default constructor arguments, calculated attributes, and instance attribute access.
- Representative raw asks include:
  - `round1:37`
  - `round1:61`
  - `round1:87`
  - `round1:109`
  - `round1:113`
  - `round1:120`
  - `round1:134`
- Why it helps:
  - The evaluations repeatedly show that users can often piece together OOP answers only by combining several snippets.
  - One canonical OOP fundamentals card would reduce that fragmentation.
- Why it may not be necessary:
  - There are already multiple strong OOP snippets in Week 4.
  - A new card should replace duplication, not add yet another OOP variant.
- Suggested direction: `add`

### 13. OOP Comparison Logic

- Absorbs duplicate requests about comparison methods, asymmetric criteria, and returning `None` when neither object clearly wins.
- Representative raw asks include:
  - `round1:1`
  - `round1:90`
  - `round1:112`
  - `round1:114`
- Why it helps:
  - This is a real gap, especially in the 2022 final Book comparison question family.
- Why it may not be necessary:
  - There is already a strong existing comparison-oriented snippet (`manual-oop-state-compare`) and a strong exam snippet around comparing books.
  - This feels more like an expansion of current content than a net-new concept family.
- Suggested direction: `edit existing`
- Preferred approach:
  - Expand the strongest existing OOP comparison item with explicit asymmetric logic and the `None` case

### 14. Flexible Arguments, Returns, and `kwargs`

- Absorbs duplicate requests about `*args`, `**kwargs`, `.keys()/.values()`, tuple returns, and flexible-argument helper functions.
- Representative raw asks include:
  - `round1:19`
  - `round1:33`
  - `round1:57`
  - `round1:76`
  - `round1:77`
  - `round1:151`
- Why it helps:
  - This cluster appears across return-behavior and function-signature questions, not just one exam.
- Why it may not be necessary:
  - Some of these are quite specific to individual questions and could bloat the function material.
  - The highest-value version is probably a compact “function signatures and returns” block rather than multiple separate additions.
- Suggested direction: `add`, but keep it compact.

### 15. Return-Value and Scope Cleanup

- Absorbs duplicate requests about implicit `None`, in-place methods returning `None`, and nested/local/global scope clarification.
- Representative raw asks include:
  - `round1:3`
  - `round1:14`
  - `round1:31`
  - `round1:47`
  - `round1:74`
- Why it helps:
  - These are real beginner traps that appear across multiple topics.
- Why it may not be necessary:
  - The scope part is already almost covered.
  - The return-value part may be better handled by strengthening existing fundamentals content rather than adding new standalone snippets.
- Suggested direction: `edit existing`

### 16. Exact-Match Retrieval Fixes

- Absorbs duplicate requests that are not new concept gaps, but fixes to existing snippets whose `search_text`, explanation, or option traces are incomplete or misleading.
- Representative raw asks include:
  - `round1:27`
  - `round1:48`
  - `round1:77`
  - `round1:96`
  - `round1:97`
  - `round1:98`
  - `round1:100`
  - `round1:103`
  - `round1:109`
  - `round1:145`
- Why it helps:
  - This directly improves retrieval quality of already-valuable snippets.
  - It is especially important because the strongest existing snippets are mostly `source_exam` items.
- Why it may not be necessary:
  - These edits do not increase conceptual coverage by themselves.
  - They should come after the higher-value conceptual additions are reviewed.
- Suggested direction: `edit existing`

## Suggested First-Pass Decisions

If we want a practical round-2 implementation list, the highest-value shortlist is:

1. Add `Essential String Methods and Indexing`
2. Add `Iteration Helpers and Basic Operator Traps`
3. Add `Comprehension Syntax Reference`
4. Add `Dictionary Construction and Iteration Patterns`
5. Add `Pandas Selection and Indexing Rules`
6. Add `Datetime Parse/Format Cheat Sheet`
7. Add `OOP Fundamentals`
8. Edit the strongest existing OOP comparison snippet instead of adding a new comparison card
9. Edit existing fundamentals content for return-value traps and scope notes
10. Fix truncated or misleading exact-match `search_text` / explanation fields

## Likely Skip or Absorb

- Skip separate standalone file-handling work in this round.
  - No meaningful file-handling cluster emerged from round 1.
- Skip separate tiny OOP worked examples.
  - Best absorbed into the main OOP fundamentals card.
- Skip a standalone boolean-string-methods card.
  - Best absorbed into the main strings reference.

## Existing High-Value Snippets Worth Preserving

These are the strongest existing anchors in the current data and should be treated as “do not accidentally dilute” items during the next round:

1. `exam-intro_python_sample_final_24_25-8-w4-string-fundamentals`
   - Week 5, topic `Working With Values`
   - Best single: `10`, Top 3: `20`, Minimal set: `18`
   - Strongest overall snippet in the dataset right now

2. `exam-midterm_2023-14-w2-loops`
   - Week 2, topic `Loops`
   - Best single: `5`, Top 3: `21`, Minimal set: `12`

3. `exam-intro_python_sample_final_24_25-6-w4-string-operations-and-methods`
   - Week 5, topic `Inspecting and Selecting Data`
   - Best single: `6`, Top 3: `13`, Minimal set: `11`

4. `exam-Resit 22/23-7-w2-dictionaries-and-mappings`
   - Week 2, topic `Dictionaries and Mappings`
   - Best single: `4`, Top 3: `21`, Minimal set: `10`

5. `exam-intro_python_sample_final_24_25-5-w4-string-fundamentals`
   - Week 5, topic `Pandas Core Structures`
   - Best single: `4`, Top 3: `15`, Minimal set: `12`

6. `exam-Test Exam 07-06-22-2-w4-oop-fundamentals`
   - Week 4, topic `OOP Fundamentals`
   - Best single: `7`, Top 3: `11`, Minimal set: `9`

7. `exam-Trial final exam Introduction to Python-1-w4-oop-fundamentals`
   - Week 4, topic `OOP Fundamentals`
   - Best single: `3`, Top 3: `15`, Minimal set: `11`

8. `exam-intro_python_sample_final_24_25-10-w6-datetime`
   - Week 6, topic `Datetime`
   - Best single: `5`, Top 3: `8`, Minimal set: `8`

## Week-Level Signals for Later Ranking Work

- Week 5 is the most concentrated high-value week.
  - Only a small number of Pandas snippets are doing most of the real exam work.
- Weeks 4 and 6 are also fairly concentrated.
  - Good candidates for meaningful leaderboard pages later.
- Weeks 1 and 2 have a large unused tail.
  - Good candidates for future pruning or stricter recommended/additional separation.
- The strongest items are overwhelmingly `source_exam` snippets.
  - That suggests future “highest value” logic should not assume key points or manual snippets naturally outrank exam-like examples.

## Human Review Questions

Before implementation, decide:

1. Do we want a lean round-2 focused on the top 6-8 clusters only, or a broader round that also includes function-signature cleanup?
2. For Pandas, do we prefer:
   - one new indexing card plus edits to existing high-performing snippets
   - or two new cards: indexing and filtering/aggregation
3. For datetime, do we prefer:
   - one dense combined datetime reference
   - or two smaller cards: parse/format and arithmetic/object-vs-string
4. For OOP comparison logic, do we agree that `edit existing` is better than adding another comparison snippet?

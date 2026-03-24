# Feedback on suggested edits
### 1. Essential String Methods and Indexing Reference

Yes, add this.

### 2. Output Formatting and String Construction

Yes, add this.

### 3. Boolean String Predicates

Yes, add this, but only very briefly. Perhaps it's good to have a table with incorrect/correct use (if that's something the questions asked often).

### 4. Iteration Helpers and Basic Operator Traps

Add this.

### 5. Comprehension Syntax Reference

Yes, add this, but see if it's possible to get the best of both worlds.

Perhaps even consider doing both:

- a table with syntax
- a table with tiny examples that explain what that syntax does

In the next pass we'll see if agents actually use it (and which one they use more) so we can determine what the better approach is.


### 6. Dictionary Construction and Iteration Patterns

Yes, add this.

### 7. Pandas Selection and Indexing Rules

Add this.

Considering that "Week 5 already has some very strong exact-match snippets." --> consider whether it's possible to absorb some (parts of) these snippets into those of week 5

### 8. Pandas Filtering, Aggregation, and Column Arithmetic

Please edit/expand existing

### 9. Lambda, `map`, and `apply`

Add!

### 10. Datetime Parse/Format Cheat Sheet

Add please

### 11. Datetime Object-vs-String Arithmetic

but preferably as part 2 of the same datetime reference family rather than a disconnected standalone card. (like, make it separately selectable, so that users can choose which parts they want)

### 12. OOP Fundamentals: `self`, `__init__`, Attributes, and Defaults

Add (see if you can absorb (parts of) some of the existing snippets into this one)

### 13. OOP Comparison Logic

add or merge into existing

### 14. Flexible Arguments, Returns, and `kwargs`

Please add

### 15. Return-Value and Scope Cleanup

Please edit existing

### 16. Exact-Match Retrieval Fixes

Sure! But don't spend too much time on this. Remember, people will not be able to search during an exam. They will mostly just create a cheat sheet beforehand and then print it out. Improving the search_text will improve how quickly agents can find relevant snippets and will be useful for generating insights about which snippets are relevant, but the end user will barely use this, if at all.

We should also be careful not to bias the agents to certain snippets simply because they arbitrarily have better search terms. 

So please make sure that the search_text treats all the different snippets fairly.


## Next Steps

### (1) Architecture changes to keep in mind
Many topics span multiple different weeks, so it's good to rework the data architecture and come loose from the strict week > topic > snippets structure

Instead, the new snippets should have metadata `main_theme` (just one) `related_themes` (can be multiple), `main_week` (just one) and `related_weeks` (can be multiple).

Old snippets will also be ported that arcitecture eventually. 

However, for this current phase, these architecture changes should be treated as metadata-only changes to keep in mind while creating/improving snippets. They should not turn into a larger UI refactor or a full data-model overhaul yet. The current priority is completeness of the snippet corpus. The bigger architecture/UI changes can happen later, once the new snippets are in place and the next grading pass gives better evidence about how the topics should actually be grouped.

### (2) Creating new snippets

The next step is to actually create the new snippets that were missing, based on the earlier findings (that I agree with). The goal here is to make all the snippets that would answer all the questions. 

Snippet considerations that apply to all:

* they should be consise and clear, not verbose
* they should convey information in the most efficient way possible (sometimes that's a table, other times it's a text-explanation, or a code example, or a combination of different elements)
* snippets should have separate selectable elements for different bits of information. This allows users to choose exactly what they want to include or exclude, and use the available space on their cheat sheet for only the bits that they need. For example, a text-explanation, a table, a code example, and another table should have different selectable items for all the unique elements. 
* snippets should assume two audiences and create different selectable elements for the two. (1) people with some prior knowledge about python that mostly need references about syntax and (2) people with very little prior knowledge that need more complete explanations. A snippet can convey the same information twice (once in compact form and once in more complete explanation), and these should be separately selectable. 

But there are some important guardrails here:

* do not split pieces too aggressively just because it is technically possible. Split a snippet into separate selectable pieces only when a user might reasonably want one part without the other.
* avoid exploding the total number of tiny pieces. If two parts are only useful together, keep them bundled.
* for the "two audiences" idea, the preferred pattern is usually:
  * one compact reference piece
  * one optional explanation piece
* only include both when they genuinely add different value. If the explanation is barely adding anything, do not duplicate the same information just for the sake of it.

#### Snippet element: code examples

It's good to keep in mind that the current snippets are based on the same exams that they are being evaluated against. But the goal is to design snippets that would also work really well for the next exam (that is not yet known). 

Therefore, I think the snippets can use some different kinds of examples but should avoid other kinds.

**Use these example types**

* short pieces of correct syntax that efficiently demonstrate how the syntax works
* short pieces of incorrect syntax that efficiently demostrate how students can recognise when errors would occur
* somewhat longer examples that provide insights about many different topics / types of syntax, or clearly demonstrate common (in)correct patterns so students can easily recognise them

--> if examples are the best way to show a specific concept/type of syntax, use already-exisitng examples from the source material or (more likely): generate one or a few example lines of code to demonstrate it quickly. 
--> only if the same, or very similar questions appear accross multiple exams, it might be good to make a "common exam question"-style snippet with an example. Generate an example that synthesises multiple exam questions into one.


**Formatting**

Code examples can be:

* inline for very simple explanations (use `code-snippet` backticks)
* as a small code block

```python
slightly longer code-piece # this is an example
wow there are two lines!
```

* In a markdown-style table, for example with headers like "code" and "output", or "correct" "incorrect" "explanation", or any other table format that makes sense

#### Snippet element: reference table

I really want to make this more common. Reference tables are a really good way to summarize information very efficiently.

As mentioned above, reference tables can include examples of (in)correct syntax and their output/what it does, but also other things that can be handy to know on an exam. This is very often the best way to present information so that it's easy to understand at a glance while still being detailed

#### Snippet element: textual explanation

Adding textual explanation of what syntax does, what things are (in)correct and why, or other clarification can be a good way to make things clearer. However, it can also add bloat. So, if there is a texual element to a snippet, make sure it's selectable separately from the rest so that people don't *have* to include it if they don't need the extra explanation.

Textual explanations should still always be brief and straight to the point. 

#### Snippet element: something else

It is very possible that there is a different way to more efficiently display information. Please feel free to come up with other snippet element types! Make sure they:

* work well on a printed cheat sheet
* align with other considerations explained in the previous sections


### (3) Curation pass and building up the new, complete database: unifying with near-duplicates and removing low-quality snippets from the available corpus

After the new snippets are created, there should be a pass to reduce the available corpus to only high quality snippets. Agents should manually curate them.

For the remainder of this section, I will use certain terms. And this is what I mean by them:

* a "piece" is one element that a user can select. A "piece" is the smallest unit in the database. It is a single element that a user can select for their cheat sheet. This is for example, one reference table, one textual explanation, one code example, etc.
* a "snippet" is a bundle of different "pieces" that logically belong together. So, it can be a bundle that include a longer textual explanation, a shorter textual explanation, a table, and one or a few code examples that all relate to the same thing.
* a "topic" is a collection of "snippets" that relate to that topic. A topic can be, for example, "working with values" or "loops"


The goal of this pass is to combine the best snippets from the old dataset with the new dataset into an untimate final dataset with only the highest value and highest quality snippets.

Agents should manually curate this to:

* create snippets that bundle all the loose pieces from the old and new datasets
* merge near-duplicates into one cannonical snippet
* minimize duplication of information, but retain all the information that is in the old + new snippets

for the new dataset, we simplify the metadata that we show on the frontend. We no longer show where snippets came from (except when they're from a specific past exam). And we change the canonical type of snippet to only be "past exam question" or "general_snippet". This allows us to be more loose with merging multiple pieces into into one snippet, or dropping low-value pieces.

For example, notebook cells are very often low value and are often better merged into a reference table, or dropped alltogether if they don't add anything new. 

We'll also drop the "key points" section and instead allow these key points to be merged into a bigger canonical snippet or including it into a reference table.

We'll also drop the specific "code examples" section, and instead prefer including it into a larger canonical snippet or transforming it into a reference table to more efficiently give the same information.

It is, however, important that we don't degrade the depth or breadth of information. We simply transform the existing information into a more compact form optimised for a cheat sheet. In some cases, retaining code snippets how they are is the best call, but it should always be considered wehether there is a better way. When in doubt, keep the old one around, but also make a more compact version and let the user pick which they like best.

Also, this curation pass should be conservative before the next grading pass:

* merge obvious near-duplicates early
* improve weak snippets early
* but do not aggressively hard-prune snippets from the available corpus yet

The reason is that after the new snippets are added, the next grading pass will provide much better evidence about what is actually low-value, redundant, or unnecessary. So, before that grading pass, the bias should be toward retaining information unless there is a very clear reason to remove it.

### (4) Snippet grading pass

This will be slightly different than the original plan. Mostly because I realise that the snippets often contain real past exam examples (and the past exams are exactly what the agents are grading the snippets against).

What should happen is: each exam question is considered individually. The agent should imagine they have almost no prior knowledge about how python works.

For each question, the agent should first determine:

* is there a past exam question example in the snippets/pieces that is (near-)identical to this question (yes/no; if yes, which one(s))

Then, excluding the near-identical past exam question piece:

* which 1 snippet provides the highest value for being able to answer this question?
	* from that one snippet, select between 1 and 3 (inclusive) pieces that are most critical
* which other 1-2 snippet(s), beside the number 1, provide the highest value for being able to answer this question?
* what is the minimal set of snippets that I would need to be able to confidently answer this question? 
	* from that minimal set of snippets, which pieces would I need?

	
--> for all these questions, the agent should provide a short reason. We can use this for a sanity check and to see whether the agent understood the instructions.

After this pass is done, we have great insight into

* which questions repeat often (if different questions have the same near-identical past exam questions, we know that it's likely they'll ask that question again)
* which snippets provide the highest value
* which pieces are most important

### (5) Topic-categorisation pass

It's nice that we have all that data about the snippets, but we also need to use it for our beautiful cheat sheet builder.

we need to do a couple of things:

**Identify topics**

Here, we identify which snippets belong together under one topic. We know this based on (1) common sense, but we can also be informed by (2) which snippets were often used together to answer one question. For example, if snippets A, B and C were often used together in the minimal set of snippets, and snippets x, y and Z were also often used together, then we can group A, B and C under one canonical main_topic and snippets x, y and z into another main_topic. 

We'll probably end up with somewhere between 20-40 main_topics

**create parent_topic**

To make the UI easier to navigate, i think we should put the topics into parent_topic entries. This will replace the "week" (1-6) that we currently have. So I think we should have at least 6 and at most 10 parent topics to keep a usable structure. 

one parent topic can have between 2 and 7 main topics (aim for exactly 5). 

And the main topic then houses the snippets

**Assign a main_topic to each snippet**

This is relatively easy for the snippets that were cited often by the agents during the snippet grading pass, but for the snippets where there isn't overwhelming evidence, pick the one that makes most sense.

**Assign a week to each of the snippets**

This is very easy for the already-existing databse: they already have a week assigned to them. For the other ones, just pick one that makes most sense. This is not very important because the week explorer is not a priority

### (6) Snippet-ranking pass

We do this based on the findings of the snippet grading pass. 

I think we should rethink the way that snippets are presented. Now, it's just too much. We have:

- common exam questions
- key points
- code examples
- recommended snippets
- additional snippets

I want to change it to:

- **Expect these questions**: shows snippets that were marked as near-identical to an exam question at least twice. The snippets that were marked most often appear at the top, and a maximum of 5 snippets is shown initially. At the bottom of this section, there is a button with "show more" upon which the page extends and shows the complete list of all the snippets that were marked at least twice. Naturally, there also is a "hide" or "show less" button as well. 
- **Highest value snippets**: shows snippets based on how often they were included as top 1, or top 2/3
	- The snippets are ranked based on a score that is computed in the backend. Each time a snippet is marked as top 1 it gets 1.5 point. Each time a snippet is marked as top 2/3 it gets 1 point.
	- This section initially shows a variable amount of snippets depending on how the points were distributed in that main_topic. The cumulative amount of the shown snippets should be at least 50% of the total points in that main_topic, but only the minimum amount of snippets to satisfy that requirement 
	- An exception is when there are less than 3 snippets that cumulatively have more than 50% of the points. In that case, there are 3 snippets shown.
	- There is a "show more" button as well to expand to all the snippets that have at least 1 point. Of course, also a "show less" button.
- **Don't forget about**: this section shows the snippets that were never marked as top 1/2/3, but that WERE included in the minimal set of snippets needed to answer a question. It should show the top 5 snippets based on how often they were marked as minimal required. Again, with a "show more" and "show less" button.
- **Maybe you'll need these, you never know**: shows the list of snippets that were never included in top 1/2/3, and never marked as minimal required. Rank them on how many different unique selectable items they have and what kind (you can think of the exact algorithm yourself).
	- 	snippets with past exam questions or reference tables should be promoted a bit more to the top
	-  snippets with only text should be ranked lower
-  show the top 5, and have a show less/more button as well.

For this last ranking bucket, be careful not to reward bloat. Ranking should not simply promote snippets because they have more selectable pieces. Use some kind of diminishing-return logic so that very large snippets are not automatically treated as higher value just because they contain more elements. Reference tables and past exam questions can be promoted somewhat, but long bloated snippets should not be unfairly rewarded.

	
	

from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable


def apply_overrides_weeks_1_3(
    card: dict[str, Any],
    *,
    safe_str: Callable[[object], str],
    rewrite_text: Callable[[object], str],
    match_topic: Callable[..., bool],
    looks_invalid_python: Callable[[str], bool],
) -> bool:
    topic_id = safe_str(card.get("id"))
    sections = card.get("sections", {})

    if topic_id == "w1-python-basics":
        sections["ai_common_questions"]["items"] = [
            {
                "id": "manual-comments",
                "summary": "How do comments start, and what does Python ignore after `#`?",
                "detail": "Everything after `#` on that logical line is ignored by Python.",
                "extra": "",
                "code": "x = 3  # this comment does not execute\nprint(x)",
                "table": None,
            },
            {
                "id": "manual-logical-lines",
                "summary": "How can one logical line span multiple physical lines?",
                "detail": "Use open brackets or an explicit backslash to continue a statement across lines.",
                "extra": "",
                "code": "numbers = [\n    1,\n    2,\n    3,\n]",
                "table": None,
            },
        ]
        return True

    if topic_id == "w1-functions-and-imports":
        sections["ai_common_questions"]["items"] = [
            {
                "id": "manual-import-names",
                "summary": "How do different import forms change the names you can use locally?",
                "detail": "`import math` gives `math.sqrt`, `import math as m` gives `m.sqrt`, and `from math import sqrt` gives `sqrt(...)` directly.",
                "extra": "",
                "code": "import math\nimport math as m\nfrom math import sqrt",
                "table": None,
            },
            {
                "id": "manual-print-vs-return",
                "summary": "What is the difference between printing a value and returning a value from a function?",
                "detail": "`print(x)` shows a value on screen. `return x` sends a value back to the caller so it can be stored, reused, or printed later.",
                "extra": "",
                "code": "def f(x):\n    return x + 1\n\nprint(f(3))",
                "table": None,
            },
            {
                "id": "manual-implicit-none",
                "summary": "What does a function return if it reaches the end without `return`?",
                "detail": "Python returns `None` if no `return` statement is executed.",
                "extra": "",
                "code": "def f():\n    print('hi')\n\nprint(f())",
                "table": None,
            },
        ]
        for item in sections.get("key_points_to_remember", []):
            if "Print is a function and tells Python to output" in safe_str(item.get("text")):
                item["text"] = "A function groups reusable code; `print(x)` displays a value, and a function returns `None` unless it explicitly uses `return`."
        import_titles = [
            "Import module under its original name",
            "Direct import plus alias binds both names",
            "from-import binds only the imported name",
            "Aliased from-import uses the alias locally",
            "import module does not create bare globals",
        ]
        for idx, item in enumerate(sections.get("ai_examples", [])):
            if safe_str(item.get("title")).lower() in {"import forms and aliases", "import styles"}:
                item["title"] = import_titles[idx % len(import_titles)]
        for item in sections.get("ai_examples", []):
            if "Exam trap" in safe_str(item.get("title")) and "lambda" in safe_str(item.get("why")).lower():
                item["title"] = "Income tax branches and return shape"
                item["why"] = "Check branch boundaries, rounding, and whether the function returns `{'total_tax': ..., 'net_income': ...}`."
        return True

    if topic_id == "w2-dictionaries-and-mappings":
        question_items = []
        replacements = [
            "Which update makes `library['books'] = 6` and adds `library['years']`?",
            "What does `list(x.values()) + list(x.keys())` print?",
        ]
        replace_index = 0
        for item in sections.get("ai_common_questions", {}).get("items", []):
            next_item = deepcopy(item)
            if safe_str(next_item.get("summary")) == "Suppose you have the following dictionary:" and replace_index < len(replacements):
                next_item["summary"] = replacements[replace_index]
                replace_index += 1
            question_items.append(next_item)
        sections["ai_common_questions"]["items"] = question_items[:8]
        return True

    if topic_id == "w2-lists-and-sets":
        titles = [
            "Create a list literal",
            "Delete by index with `del`",
            "Two ways to create an empty list",
            "Lists are mutable: replace by index",
        ]
        title_index = 0
        for item in sections.get("ai_examples", []):
            raw_title = safe_str(item.get("title")).lower()
            if raw_title in {"lists", "list"} and title_index < len(titles):
                item["title"] = titles[title_index]
                title_index += 1
        return True

    if topic_id == "w2-conditions":
        sections["ai_common_questions"]["items"] = [
            {
                "id": "manual-bool-precedence",
                "summary": "How do `not`, `and`, and `or` combine when there are no extra parentheses?",
                "detail": "`not` is evaluated first, then `and`, then `or`, so parenthesize whenever the intended logic is not obvious.",
                "extra": "",
                "code": "print(not False and True or False)",
                "table": None,
            },
            {
                "id": "manual-filter-condition",
                "summary": "Trace `main(lst, condition)` and identify which values satisfy `lambda x: x % 2 != 0`.",
                "detail": "Apply the condition to one element first, then keep only the values for which it returns `True`.",
                "extra": "",
                "code": "def main(lst, condition):\n    return [x for x in lst if condition(x)]",
                "table": None,
            },
            {
                "id": "manual-conditional-expression",
                "summary": "When should you use `x if cond else y` instead of a multi-line `if/else` block?",
                "detail": "Use the conditional expression for a single value choice; use a full block when each branch needs multiple statements.",
                "extra": "",
                "code": "label = 'pass' if score >= 10 else 'fail'",
                "table": None,
            },
        ]
        sections["key_points_to_remember"] = [
            {
                "id": "kp-manual-precedence",
                "text": "`not` binds tighter than `and`, and `and` binds tighter than `or`; add parentheses when the intended grouping is not obvious.",
            },
            {
                "id": "kp-manual-ternary",
                "text": "Use `x if cond else y` when both branches are single expressions; use a full `if/elif/else` block when the branches need multiple statements.",
            },
        ]
        curated_examples = []
        for item in sections.get("ai_examples", []):
            title = safe_str(item.get("title"))
            if "Augmented assignment" in title:
                continue
            if title == "Precedence trap":
                item["output"] = "True\nFalse"
            elif title == "Inclusion check — 'in' operator":
                item["output"] = "True\nTrue\nTrue\nTrue\nFalse\nTrue"
            if title == "Condition result":
                code = safe_str(item.get("code"))
                if "not True" in code:
                    item["title"] = "`not` flips booleans"
                    item["why"] = "`not True` becomes `False` and `not False` becomes `True`."
                    item["output"] = "False\nTrue"
                elif "3 > 2" in code:
                    item["title"] = "Comparison operators return booleans"
                    item["why"] = "A comparison like `3 > 2` evaluates to either `True` or `False`."
                    item["output"] = "True"
            curated_examples.append(item)
        sections["ai_examples"] = curated_examples[:6]
        return True

    if topic_id == "w2-loops":
        sections["ai_summary"]["content"] = "Use `for` to iterate over items and `while` to repeat while a condition stays `True`. Know what `break`, `continue`, `enumerate`, and `zip` do inside the loop body."
        for subtopic in card.get("subtopics", []):
            subtopic["summary"] = sections["ai_summary"]["content"]
        sections["key_points_to_remember"] = [
            {
                "id": "kp-manual-loop-core",
                "text": "Use `for` when you already have an iterable; use `while` when repetition should continue only while a condition stays `True`.",
            },
            {
                "id": "kp-manual-break-continue",
                "text": "`break` exits the loop immediately; `continue` skips the rest of the current iteration and moves to the next one.",
            },
            {
                "id": "kp-manual-enumerate",
                "text": "`enumerate(seq, start)` gives `(index, value)` pairs; `zip(a, b)` gives tuples of items from multiple iterables in parallel.",
            },
            {
                "id": "kp-manual-while-truthy",
                "text": "A `while` condition is checked before every iteration, so a list loop like `while items:` keeps going only while the list is non-empty.",
            },
        ]
        sections["ai_examples"] = [
            item
            for item in sections.get("ai_examples", [])
            if "augmented" not in safe_str(item.get("title")).lower()
            and "alphabet" not in safe_str(item.get("code")).lower()
            and "input(" not in safe_str(item.get("code"))
            and "walrus" not in safe_str(item.get("title")).lower()
        ][:8]
        for item in sections.get("ai_examples", []):
            title = safe_str(item.get("title"))
            if title == "For-loop with continue":
                item["title"] = "Skip certain values with `continue`"
                item["why"] = "Use `continue` to ignore the current item and jump straight to the next iteration."
                item["output"] = "18"
            elif title == "Loop variable not used — use _":
                item["why"] = "Use `_` when the loop should repeat a fixed number of times but the loop variable itself is not needed."
                item["output"] = "Hello\nHello\nHello\nHello\nHello"
            elif title == "enumerate with start=1":
                item["title"] = "`enumerate(seq, start=1)`"
                item["why"] = "Use `enumerate` when you need both index and value, and set `start=1` if the numbering should begin at 1."
                item["output"] = "Andorra has index: 1\nBelgium has index: 2"
            elif title == "zip two lists":
                item["title"] = "`zip(a, b)` pairs items in parallel"
                item["why"] = "Use `zip` when two sequences should be processed position by position together."
                item["output"] = "Andorra has capital: Andorra la Vella\nBelgium has capital: Brussels"
            elif title == "Truthy/Falsy in while condition":
                item["title"] = "`while items:` repeats until the list is empty"
                item["why"] = "Non-empty lists are truthy and empty lists are falsy, so `while items:` is a common consume-until-empty loop."
                item["output"] = "21"
        sections["ai_common_questions"]["items"] = [
            {
                "id": "manual-loop-translate",
                "summary": "Translate `alphabet[1::2]` into a loop that collects every second character starting at index 1.",
                "detail": "Initialize an empty result, loop over the needed indices, and append the selected characters in order.",
                "extra": "",
                "code": "result = ''\nfor i in range(1, len(alphabet), 2):\n    result += alphabet[i]",
                "table": None,
            },
            {
                "id": "manual-break-continue",
                "summary": "What is the difference between `break` and `continue` inside a loop?",
                "detail": "`break` exits the loop immediately; `continue` skips the rest of the current iteration and moves to the next one.",
                "extra": "",
                "code": "for x in data:\n    if x < 0:\n        continue\n    if x == 0:\n        break",
                "table": None,
            },
            {
                "id": "manual-enumerate-zip",
                "summary": "When do you reach for `enumerate` versus `zip`?",
                "detail": "Use `enumerate(seq)` when you need index and value together; use `zip(a, b)` when you need items from multiple iterables in parallel.",
                "extra": "",
                "code": "for i, value in enumerate(seq):\n    ...\nfor left, right in zip(a, b):\n    ...",
                "table": None,
            },
        ]
        return True

    if topic_id == "w2-conversion-and-truthiness":
        title_map = [
            "str(1) versus int('1')",
            "Why `'1' + 2` raises `TypeError`",
            "Why `dict([1, 2])` raises `ValueError`",
            "Why `int('1a')` raises `ValueError`",
            "Truthy list in a `while` condition",
        ]
        title_index = 0
        for item in sections.get("ai_examples", []):
            if safe_str(item.get("title")).lower() in {"type_conversion", "augmented assignment (`+=`)", "augmented assignment (`+=`) behavior"} and title_index < len(title_map):
                item["title"] = title_map[title_index]
                title_index += 1
        return True

    if topic_id == "w3-defining-and-calling-functions":
        sections["ai_common_questions"]["items"] = [
            {
                "id": "manual-call-vs-index",
                "summary": "What error do you get from `print[1]` and from `[1, 2, 3](0)`?",
                "detail": "`print[1]` tries to subscript a function, while `[1, 2, 3](0)` tries to call a list. Both raise `TypeError`, but for opposite reasons.",
                "extra": "",
                "code": "print[1]\n[1, 2, 3](0)",
                "table": None,
            },
            {
                "id": "manual-string-return-shape",
                "summary": "How do you recognize that a function should `return` a string instead of `print` it?",
                "detail": "If the result must be reused later, the function should `return` the string so the caller can store, combine, or print it afterwards.",
                "extra": "",
                "code": "def get_tld(url):\n    parts = url.split('.')\n    return parts[-1].split('/')[0]",
                "table": None,
            },
            {
                "id": "manual-list-of-dicts-loop",
                "summary": "How do you access values when looping over a list of dictionaries?",
                "detail": "Each loop iteration gives one dictionary, so read fields with keys like `student['Name']` and `student['Grade']`.",
                "extra": "",
                "code": "for student in students:\n    print(student['Name'], student['Grade'])",
                "table": None,
            },
        ]
        for item in sections.get("key_points_to_remember", []):
            if rewrite_text(item.get("text")).startswith("Pattern to remember: def get_tld(url):"):
                item["text"] = "Function skeleton: `def f(x): return result`. Define with `def ...`, call with `()`, and use `[]` only for indexing."
        curated_examples = []
        for item in sections.get("ai_examples", []):
            if not match_topic(topic_id, item.get("title"), item.get("why"), item.get("code")) or looks_invalid_python(item.get("code", "")):
                continue
            if safe_str(item.get("title")) == "Condition flow and branch result":
                continue
            if safe_str(item.get("title")) == "Basic function":
                item["title"] = "Define, call, and return a value"
                item["output"] = "3"
            elif safe_str(item.get("title")) == "Wrong bracket errors":
                item["output"] = "TypeError\nTypeError"
            elif safe_str(item.get("title")) == "Method on immutable — must capture return value":
                item["output"] = "UVA AMSTERDAM"
            elif safe_str(item.get("title")) == "Method on mutable — changes in place vs returns value":
                item["output"] = "[1, 2, 3]\n1"
            curated_examples.append(item)
        sections["ai_examples"] = curated_examples[:4]
        return True

    if topic_id == "w3-scope":
        sections["ai_common_questions"]["items"] = [
            {
                "id": "manual-local-name",
                "summary": "Why does `print(n1)` fail outside `def adder(n1, n2): ...`?",
                "detail": "Parameter names are local to the function body, so they do not exist in the global scope after the call finishes.",
                "extra": "",
                "code": "def adder(n1, n2):\n    return n1 + n2\n\nadder(1, 2)\nprint(n1)",
                "table": None,
            },
            {
                "id": "manual-unboundlocal",
                "summary": "Why can assigning to a name inside a function cause `UnboundLocalError`?",
                "detail": "If a function assigns to a name anywhere in its body, Python treats that name as local throughout the function unless you declare it `global` or `nonlocal`.",
                "extra": "",
                "code": "b = 1\n\ndef main(a):\n    b = b\n    return a",
                "table": None,
            },
            {
                "id": "manual-global",
                "summary": "When do you need `global`?",
                "detail": "Use `global name` only when the function should rebind a global variable; simple reads of a global name do not need it.",
                "extra": "",
                "code": "n1 = 1\n\ndef changer():\n    global n1\n    n1 = n1 + 1",
                "table": None,
            },
        ]
        sections["key_points_to_remember"] = [
            {
                "id": "kp-manual-scope-local",
                "text": "Names assigned inside a function are local by default, including parameter names.",
            },
            {
                "id": "kp-manual-scope-unbound",
                "text": "If a function assigns to a name anywhere, Python treats that name as local throughout that function unless `global` or `nonlocal` says otherwise.",
            },
            {
                "id": "kp-manual-scope-global",
                "text": "Use `global x` only when the function should rebind the global name `x`; mutating an object passed in as an argument does not require `global`.",
            },
        ]
        sections["ai_examples"] = [
            {
                "id": "manual-scope-local-name",
                "kind": "correct",
                "title": "Parameter names stay local to the function",
                "code": "def adder(n1, n2):\n    return n1 + n2\n\nprint(adder(1, 2))\nprint(n1)",
                "output": "3\nNameError",
                "why": "After the function call, `n1` and `n2` do not exist outside the function body.",
                "status": "curated",
                "subtopic_id": card.get("subtopics", [{}])[0].get("id", ""),
                "subtopic_title": card.get("subtopics", [{}])[0].get("title", ""),
            },
            {
                "id": "manual-scope-unbound",
                "kind": "correct",
                "title": "Assignment makes the name local",
                "code": "b = 1\n\ndef main(a):\n    b = b\n    return a\n\nprint(main(1))",
                "output": "UnboundLocalError",
                "why": "Because `b` is assigned inside `main`, Python treats it as local before the `b = b` line runs.",
                "status": "curated",
                "subtopic_id": card.get("subtopics", [{}])[0].get("id", ""),
                "subtopic_title": card.get("subtopics", [{}])[0].get("title", ""),
            },
            {
                "id": "manual-scope-global-change",
                "kind": "correct",
                "title": "Use `global` to rebind a global name",
                "code": "n1 = 1\n\ndef changer():\n    global n1\n    n1 = n1 + 1\n\nchanger()\nprint(n1)",
                "output": "2",
                "why": "With `global n1`, the assignment updates the global name instead of creating a local one.",
                "status": "curated",
                "subtopic_id": card.get("subtopics", [{}])[0].get("id", ""),
                "subtopic_title": card.get("subtopics", [{}])[0].get("title", ""),
            },
            {
                "id": "manual-scope-rebind-parameter",
                "kind": "correct",
                "title": "Rebinding a parameter does not change the caller's name",
                "code": "def changer(n1):\n    n1 = n1 + 1\n    return n1\n\na = 1\na = changer(a)\nprint(a)",
                "output": "2",
                "why": "The function works with its local parameter; the caller changes only because the returned value is assigned back to `a`.",
                "status": "curated",
                "subtopic_id": card.get("subtopics", [{}])[0].get("id", ""),
                "subtopic_title": card.get("subtopics", [{}])[0].get("title", ""),
            },
        ]
        return True

    if topic_id == "w3-arguments":
        for item in sections.get("ai_common_questions", {}).get("items", []):
            if item.get("summary") == "Mutable arguments":
                item["detail"] = "Mutating a passed list changes the caller's object; rebinding the parameter does not."
            if "summarize" in safe_str(item.get("summary")).lower():
                item["detail"] = "Return `{'amount': len(nums), 'smallest': min(nums), 'largest': max(nums), 'total': sum(nums)}`."
        return True

    return False

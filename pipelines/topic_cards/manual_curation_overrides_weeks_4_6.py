from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable


def apply_overrides_weeks_4_6(
    card: dict[str, Any],
    *,
    safe_str: Callable[[object], str],
    rewrite_text: Callable[[object], str],
    match_topic: Callable[..., bool],
    looks_invalid_python: Callable[[str], bool],
) -> bool:
    topic_id = safe_str(card.get("id"))
    sections = card.get("sections", {})

    if topic_id == "w4-string-fundamentals":
        items = sections.get("ai_common_questions", {}).get("items", [])
        items = [item for item in items if match_topic(topic_id, item.get("summary"), item.get("detail"), item.get("code"))]
        items = [
            item
            for item in items
            if "default" not in safe_str(item.get("summary")).lower()
            and "mutable parameter" not in safe_str(item.get("summary")).lower()
        ]
        manual = [
            {
                "id": "manual-string-immutability",
                "summary": "Why does `s[0] = 'A'` fail?",
                "detail": "Strings are immutable, so you must build a new string such as `s = 'A' + s[1:]` instead of assigning by index.",
                "extra": "",
                "code": "s = 'abcd'\ns = 'A' + s[1:]",
                "table": None,
            },
            {
                "id": "manual-string-escapes",
                "summary": "How do you include quotes or a newline inside a string literal?",
                "detail": "Pick the other quote style or escape the inner quote; use `\\n` for a newline.",
                "extra": "",
                "code": "print(\"it's\")\nprint('He said \"hi\"')\nprint(\"Line 1\\nLine 2\")",
                "table": None,
            },
        ]
        sections["ai_common_questions"]["items"] = items[:1] + manual

        key_points = []
        for item in sections.get("key_points_to_remember", []):
            next_item = deepcopy(item)
            text = rewrite_text(next_item.get("text"))
            if text == 'Pattern to remember: df.loc[:,"C"] = df.loc[:,"A"] + df.loc[:,"B"]':
                text = "Strings are immutable: `s[0] = 'A'` fails, so rebuild or rebind, for example `s = 'A' + s[1:]`."
            next_item["text"] = text
            key_points.append(next_item)
        sections["key_points_to_remember"] = key_points

        curated_examples = []
        for item in sections.get("ai_examples", []):
            if looks_invalid_python(item.get("code", "")):
                continue
            if not match_topic(topic_id, item.get("title"), item.get("why"), item.get("code")):
                continue
            if safe_str(item.get("title")).startswith("def main("):
                continue
            if safe_str(item.get("title")).startswith("def my_isupper("):
                item["title"] = "Filter uppercase letters with a helper function"
                item["why"] = "Trace the loop character by character and keep only the uppercase letters that satisfy the test."
            if safe_str(item.get("title")) == "Attempting to change a string":
                item["title"] = "Methods return new strings"
                item["output"] = "abcd"
            if safe_str(item.get("title")) == "a = 'adbc'":
                item["title"] = "`len(s)` counts characters"
                item["why"] = "Count every character in the string, including letters, spaces, and punctuation if they are present."
                item["output"] = "4"
            curated_examples.append(item)
        curated_examples.append(
            {
                "id": "manual-string-literals-example",
                "kind": "correct",
                "title": "Quotes and newline escapes",
                "code": "print(\"it's\")\nprint('He said \"hi\"')\nprint(\"Line 1\\nLine 2\")",
                "output": "it's\nHe said \"hi\"\nLine 1\nLine 2",
                "why": "Use matching quotes or escape the inner quote; `\\n` inserts a newline.",
                "status": "curated",
                "subtopic_id": card.get("subtopics", [{}])[0].get("id", ""),
                "subtopic_title": card.get("subtopics", [{}])[0].get("title", ""),
            }
        )
        sections["ai_examples"] = curated_examples[:8]
        return True

    if topic_id == "w4-string-operations-and-methods":
        items = []
        for item in sections.get("ai_common_questions", {}).get("items", []):
            if match_topic(topic_id, item.get("summary"), item.get("detail"), item.get("code")):
                items.append(item)
        items.append(
            {
                "id": "manual-find-vs-index",
                "summary": "What is the difference between `s.find(x)` and `s.index(x)` when `x` is missing?",
                "detail": "`find` returns `-1`; `index` raises `ValueError`.",
                "extra": "",
                "code": "s = 'banana'\nprint(s.find('x'))\nprint(s.index('x'))  # ValueError",
                "table": None,
            }
        )
        sections["ai_common_questions"]["items"] = items[:8]
        for item in sections.get("key_points_to_remember", []):
            text = rewrite_text(item.get("text"))
            if text == 'Pattern to remember: df.loc[df.index % 2 == 0, ["B"]]':
                item["text"] = "Pattern to remember: `find` returns `-1`; `index` raises `ValueError` if the substring is missing."
        return True

    if topic_id == "w4-oop-fundamentals":
        sections["ai_common_questions"]["items"] = [
            {
                "id": "manual-self",
                "summary": "Why is `self` the first parameter of an instance method?",
                "detail": "`self` is the current object, so the method can read and update that object's attributes.",
                "extra": "",
                "code": "class Flight:\n    def set_date(self, date):\n        self.date = date",
                "table": None,
            },
            {
                "id": "manual-method-call",
                "summary": "Why does `obj.set_date(obj, x)` pass too many arguments?",
                "detail": "When you call a method on an object, Python passes the object as `self` automatically. Writing it again adds one argument too many.",
                "extra": "",
                "code": "obj.set_date(x)      # correct\nobj.set_date(obj, x) # too many args",
                "table": None,
            },
            {
                "id": "manual-init-default",
                "summary": "How do default values in `__init__` make constructor arguments optional?",
                "detail": "A default like `vehicle_mode='land'` can be omitted when the object is created, but the instance still receives that attribute value.",
                "extra": "",
                "code": "class Vehicle:\n    def __init__(self, name, vehicle_mode='land'):\n        self.name = name\n        self.vehicle_mode = vehicle_mode",
                "table": None,
            },
        ]
        for item in sections.get("key_points_to_remember", []):
            text = rewrite_text(item.get("text"))
            if text.startswith("Pattern to remember: The first argument"):
                item["text"] = "Method calls pass `self` automatically: `obj.set_date(x)` is correct; `obj.set_date(obj, x)` passes one argument too many."
        sections["ai_examples"] = [
            item
            for item in sections.get("ai_examples", [])
            if match_topic(topic_id, item.get("title"), item.get("why"), item.get("code"))
            and not looks_invalid_python(item.get("code", ""))
            and safe_str(item.get("title")) != "class Rectangle:"
        ][:6]
        for item in sections["ai_examples"]:
            if safe_str(item.get("title")).startswith("class New_str"):
                item["title"] = "Subclassing `str`"
                item["why"] = "You can subclass a built-in type to add custom methods while keeping the original string behavior."
        sections["ai_examples"].append(
            {
                "id": "manual-oop-attrs",
                "kind": "correct",
                "title": "Class attribute vs instance attribute",
                "code": "class Rectangle:\n    units = 'cm'\n\n    def __init__(self, width):\n        self.width = width\n\nr1 = Rectangle(3)\nr2 = Rectangle(5)\nr2.units = 'm'\nprint(r1.units, r2.units)",
                "output": "cm m",
                "why": "`self.width` is per object; `Class.units` is shared until an instance shadows it with its own attribute.",
                "status": "curated",
                "subtopic_id": card.get("subtopics", [{}])[0].get("id", ""),
                "subtopic_title": card.get("subtopics", [{}])[0].get("title", ""),
            }
        )
        return True

    if topic_id == "w5-pandas-core-structures":
        sections["ai_common_questions"]["items"] = [
            {
                "id": "manual-series-vs-dataframe",
                "summary": "What does `df['A']` return versus `df[['A']]`?",
                "detail": "`df['A']` returns a `Series`; `df[['A']]` returns a one-column `DataFrame`.",
                "extra": "",
                "code": "df['A']\ndf[['A']]",
                "table": None,
            },
            {
                "id": "manual-series-index",
                "summary": "What index does a `Series` get if you do not provide one explicitly?",
                "detail": "Pandas uses the default integer index `0, 1, 2, ...`.",
                "extra": "",
                "code": "s = pd.Series([10, 20, 30])",
                "table": None,
            },
            {
                "id": "manual-df-constructor",
                "summary": "How do you build a `DataFrame` from a dict of column names to lists?",
                "detail": "Each key becomes a column, and each list supplies that column's values row by row.",
                "extra": "",
                "code": "df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})",
                "table": None,
            },
        ]
        sections["key_points_to_remember"] = [
            {
                "id": "kp-manual-series-default-index",
                "text": "A `Series` is 1D labeled data; if you do not supply an index, pandas uses `0, 1, 2, ...`.",
            },
            {
                "id": "kp-manual-df-constructor",
                "text": "A `DataFrame` is a 2D table; a dict of column names to equal-length lists is the standard constructor pattern.",
            },
            {
                "id": "kp-manual-series-vs-df",
                "text": "`df['A']` gives a `Series`, while `df[['A']]` gives a one-column `DataFrame`.",
            },
        ]
        sections["ai_examples"] = [
            {
                "id": "manual-pandas-import",
                "kind": "correct",
                "title": "Import pandas with the conventional alias",
                "code": "import pandas as pd",
                "why": "Use the `pd` alias so constructors and methods stay short and readable during the exam.",
                "status": "curated",
                "subtopic_id": card.get("subtopics", [{}])[0].get("id", ""),
                "subtopic_title": card.get("subtopics", [{}])[0].get("title", ""),
            },
            {
                "id": "manual-pandas-series",
                "kind": "correct",
                "title": "Create a `Series` from a list",
                "code": "s = pd.Series([153, 160, 150], name='Length')\nprint(s)",
                "output": "0    153\n1    160\n2    150\nName: Length, dtype: int64",
                "why": "Without an explicit index, pandas labels the rows `0, 1, 2, ...`.",
                "status": "curated",
                "subtopic_id": card.get("subtopics", [{}])[0].get("id", ""),
                "subtopic_title": card.get("subtopics", [{}])[0].get("title", ""),
            },
            {
                "id": "manual-pandas-df",
                "kind": "correct",
                "title": "Build a `DataFrame` from a dict of columns",
                "code": "df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})\nprint(df)",
                "output": "   A  B\n0  1  3\n1  2  4",
                "why": "Each dict key becomes a column and the lists provide the row values for that column.",
                "status": "curated",
                "subtopic_id": card.get("subtopics", [{}])[0].get("id", ""),
                "subtopic_title": card.get("subtopics", [{}])[0].get("title", ""),
            },
            {
                "id": "manual-pandas-select-shape",
                "kind": "correct",
                "title": "`df['A']` versus `df[['A']]`",
                "code": "df['A']      # Series\ndf[['A']]    # one-column DataFrame",
                "why": "Check the brackets carefully: one pair returns a `Series`, two pairs return a `DataFrame`.",
                "status": "curated",
                "subtopic_id": card.get("subtopics", [{}])[0].get("id", ""),
                "subtopic_title": card.get("subtopics", [{}])[0].get("title", ""),
            },
        ]
        return True

    if topic_id == "w6-datetime":
        sections["ai_common_questions"]["items"] = [
            {
                "id": "manual-strftime-vs-strptime",
                "summary": "When do you use `strftime` versus `strptime`?",
                "detail": "`strftime` formats a datetime into text; `strptime` parses text into a datetime object.",
                "extra": "",
                "code": "dt.strftime('%Y-%m-%d')\ndatetime.strptime('2024-05-20', '%Y-%m-%d')",
                "table": None,
            },
            {
                "id": "manual-timedelta-attrs",
                "summary": "Which attributes exist directly on a `timedelta` object?",
                "detail": "A `timedelta` stores `days`, `seconds`, and `microseconds`; hours or weeks must be derived or supplied when constructing it.",
                "extra": "",
                "code": "delta = end - start\nprint(delta.days, delta.seconds)",
                "table": None,
            },
            {
                "id": "manual-day-of-year",
                "summary": "How can you compute the day number within the year from a datetime?",
                "detail": "Subtract January 1st of the same year, take `.days`, and add 1 so January 1st becomes day 1.",
                "extra": "",
                "code": "def day_of_year(dt):\n    return (dt - datetime(dt.year, 1, 1)).days + 1",
                "table": None,
            },
        ]
        sections["key_points_to_remember"] = [
            {
                "id": "kp-manual-datetime-now",
                "text": "`datetime.now()` gives the current local datetime; use `.timestamp()` only when you specifically need seconds since the Unix epoch.",
            },
            {
                "id": "kp-manual-datetime-format",
                "text": "`strftime` formats a datetime into text; `strptime` parses text into a datetime object.",
            },
            {
                "id": "kp-manual-datetime-delta",
                "text": "Subtracting two datetimes gives a `timedelta`; its most-used direct attributes are `.days`, `.seconds`, and `.microseconds`.",
            },
            {
                "id": "kp-manual-datetime-replace",
                "text": "Datetime objects are immutable, so `.replace(...)` returns a new datetime instead of modifying the original one.",
            },
        ]
        sections["ai_examples"] = [
            {
                "id": "manual-datetime-format",
                "kind": "correct",
                "title": "Format a datetime with `strftime`",
                "code": "from datetime import datetime\n\ndt = datetime(2024, 5, 20, 14, 30)\nprint(dt.strftime('%Y-%m-%d %H:%M'))",
                "output": "2024-05-20 14:30",
                "why": "Use `strftime` when the exam asks for a formatted string such as year-month-day or hour-minute.",
                "status": "curated",
                "subtopic_id": card.get("subtopics", [{}])[0].get("id", ""),
                "subtopic_title": card.get("subtopics", [{}])[0].get("title", ""),
            },
            {
                "id": "manual-datetime-parse",
                "kind": "correct",
                "title": "Parse text with `strptime`",
                "code": "from datetime import datetime\n\ndt = datetime.strptime('2024-05-20', '%Y-%m-%d')\nprint(dt)",
                "output": "2024-05-20 00:00:00",
                "why": "The format string must match the input text exactly, including separators.",
                "status": "curated",
                "subtopic_id": card.get("subtopics", [{}])[0].get("id", ""),
                "subtopic_title": card.get("subtopics", [{}])[0].get("title", ""),
            },
            {
                "id": "manual-datetime-delta",
                "kind": "correct",
                "title": "Subtract datetimes to get a `timedelta`",
                "code": "from datetime import datetime\n\nstart = datetime(2024, 1, 1)\nend = datetime(2024, 1, 4)\nprint((end - start).days)",
                "output": "3",
                "why": "Datetime subtraction gives a `timedelta`, whose `.days` attribute is often what exam questions want.",
                "status": "curated",
                "subtopic_id": card.get("subtopics", [{}])[0].get("id", ""),
                "subtopic_title": card.get("subtopics", [{}])[0].get("title", ""),
            },
            {
                "id": "manual-datetime-replace",
                "kind": "correct",
                "title": "`.replace(...)` returns a new datetime",
                "code": "from datetime import datetime\n\nd = datetime(2024, 5, 20)\nprint(d.replace(year=2026))\nprint(d)",
                "output": "2026-05-20 00:00:00\n2024-05-20 00:00:00",
                "why": "Datetime objects are immutable, so `.replace(...)` does not modify the original object in place.",
                "status": "curated",
                "subtopic_id": card.get("subtopics", [{}])[0].get("id", ""),
                "subtopic_title": card.get("subtopics", [{}])[0].get("title", ""),
            },
        ]
        return True

    return False

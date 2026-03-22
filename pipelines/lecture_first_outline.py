from __future__ import annotations

import copy
import re
from typing import Any


def _safe_str(value: Any) -> str:
    return str(value or "").strip()


def _norm(text: Any) -> str:
    value = _safe_str(text).lower()
    value = value.replace("&", " and ")
    value = re.sub(r"[^a-z0-9*+.# ]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def tag_in_haystack(haystack: str, tag: str) -> bool:
    cleaned = _norm(tag)
    variants = {cleaned}
    if cleaned.endswith("y") and len(cleaned) > 2:
        variants.add(f"{cleaned[:-1]}ies")
    if cleaned.endswith("ies") and len(cleaned) > 3:
        variants.add(f"{cleaned[:-3]}y")
    if cleaned.endswith("s") and len(cleaned) > 3:
        variants.add(cleaned[:-1])
    elif len(cleaned) > 2:
        variants.add(f"{cleaned}s")
    return any(variant and variant in haystack for variant in variants)

OUTLINE_SPEC: list[dict[str, Any]] = [
    {
        "week": 1,
        "title": "Week 1",
        "topics": [
            {
                "id": "w1-python-basics",
                "title": "Python Basics",
                "topic_tags": ["python basics", "execution model", "comments"],
                "subtopics": [
                    {
                        "id": "w1-python-basics-execution-model",
                        "title": "Execution Model, Logical Lines, and Comments",
                        "tags": [
                            "execution model",
                            "byte code",
                            "machine code",
                            "logical line",
                            "physical line",
                            "comment",
                            "intro",
                        ],
                    }
                ],
            },
            {
                "id": "w1-objects-and-names",
                "title": "Objects and Names",
                "topic_tags": ["object", "type", "mutable", "assignment", "name"],
                "subtopics": [
                    {
                        "id": "w1-objects-and-names-core",
                        "title": "Objects, Types, Mutability, Assignment, and Names",
                        "tags": [
                            "object",
                            "identity",
                            "id",
                            "type",
                            "mutable",
                            "immutable",
                            "assignment",
                            "name",
                            "variable naming",
                            "types",
                        ],
                    }
                ],
            },
            {
                "id": "w1-operators-and-truth",
                "title": "Operators and Truth",
                "topic_tags": ["arithmetic", "comparison", "boolean"],
                "subtopics": [
                    {
                        "id": "w1-operators-and-truth-core",
                        "title": "Arithmetic, Comparison, and Boolean Operators",
                        "tags": ["arithmetic", "comparison", "boolean operator", "operator"],
                    }
                ],
            },
            {
                "id": "w1-sequences-and-access",
                "title": "Sequences and Access",
                "topic_tags": ["indexing", "slicing", "range", "sequence"],
                "subtopics": [
                    {
                        "id": "w1-sequences-and-access-core",
                        "title": "Indexing, Slicing, and range()",
                        "tags": ["indexing", "slicing", "slice", "range", "sequence", "strings"],
                    }
                ],
            },
            {
                "id": "w1-functions-and-imports",
                "title": "Functions and Imports",
                "topic_tags": ["function", "import", "package"],
                "subtopics": [
                    {
                        "id": "w1-functions-and-imports-core",
                        "title": "Built-ins Intro, Functions, and Modules",
                        "tags": ["function", "built in", "import", "package", "module"],
                    }
                ],
            },
        ],
    },
    {
        "week": 2,
        "title": "Week 2",
        "topics": [
            {
                "id": "w2-dictionaries-and-mappings",
                "title": "Dictionaries and Mappings",
                "topic_tags": ["dictionary", "mapping"],
                "subtopics": [
                    {
                        "id": "w2-dictionaries-and-mappings-core",
                        "title": "Creation, Lookup, Updates, and Key Constraints",
                        "tags": ["dictionary", "dict", "mapping", "key value", "hashable"],
                    }
                ],
            },
            {
                "id": "w2-lists-and-sets",
                "title": "Lists and Sets",
                "topic_tags": ["list", "set", "ordered", "unordered"],
                "subtopics": [
                    {
                        "id": "w2-lists-and-sets-core",
                        "title": "Sequences, Uniqueness, and Common Operations",
                        "tags": ["list", "set", "ordered", "unordered", "sequence"],
                    }
                ],
            },
            {
                "id": "w2-conditions",
                "title": "Conditions",
                "topic_tags": ["condition", "boolean", "precedence", "conditional"],
                "subtopics": [
                    {
                        "id": "w2-conditions-core",
                        "title": "Comparisons, `in`, Precedence, and Conditional Expressions",
                        "tags": ["condition", "boolean", "precedence", "conditional", "comparison", " in "],
                    }
                ],
            },
            {
                "id": "w2-loops",
                "title": "Loops",
                "topic_tags": ["loop", "for", "while", "enumerate", "zip", "walrus"],
                "subtopics": [
                    {
                        "id": "w2-loops-core",
                        "title": "for, while, Dictionary Iteration, enumerate(), zip(), and Walrus",
                        "tags": ["for loop", "while loop", "looping", "enumerate", "zip", "walrus", "loop"],
                    }
                ],
            },
            {
                "id": "w2-conversion-and-truthiness",
                "title": "Conversion and Truthiness",
                "topic_tags": ["type conversion", "truthy", "falsy"],
                "subtopics": [
                    {
                        "id": "w2-conversion-and-truthiness-core",
                        "title": "Explicit Conversion and Truthy/Falsy Rules",
                        "tags": ["type conversion", "truthy", "falsy", "conversion"],
                    }
                ],
            },
        ],
    },
    {
        "week": 3,
        "title": "Week 3",
        "topics": [
            {
                "id": "w3-defining-and-calling-functions",
                "title": "Defining and Calling Functions",
                "topic_tags": ["function definition", "calling", "methods"],
                "subtopics": [
                    {
                        "id": "w3-defining-and-calling-functions-core",
                        "title": "def, Calls, and Methods vs Functions",
                        "tags": ["function definition", "function call", "calling", "method", "function"],
                    }
                ],
            },
            {
                "id": "w3-return-behavior",
                "title": "Return Behavior",
                "topic_tags": ["return", "none", "pass", "tuple"],
                "subtopics": [
                    {
                        "id": "w3-return-behavior-core",
                        "title": "return, Implicit None, Multiple Returns, pass, and Single-Element Tuples",
                        "tags": ["return", "none", "pass", "tuple", "single element tuple"],
                    }
                ],
            },
            {
                "id": "w3-scope",
                "title": "Scope",
                "topic_tags": ["scope", "global", "local", "unboundlocal"],
                "subtopics": [
                    {
                        "id": "w3-scope-core",
                        "title": "Global vs Local Names and Scope Errors",
                        "tags": ["scope", "global", "local", "unboundlocal", "name resolution"],
                    }
                ],
            },
            {
                "id": "w3-arguments",
                "title": "Arguments",
                "topic_tags": ["argument", "args", "kwargs", "default"],
                "subtopics": [
                    {
                        "id": "w3-arguments-core",
                        "title": "Positional, Keyword, Default, *args, **kwargs, and Mutable Argument Traps",
                        "tags": ["argument", "*args", "**kwargs", "kwargs", "default", "mutable argument"],
                    }
                ],
            },
            {
                "id": "w3-higher-order-patterns",
                "title": "Higher-Order Patterns",
                "topic_tags": ["nested", "factory", "lambda", "map", "filter", "reduce", "sorted"],
                "subtopics": [
                    {
                        "id": "w3-higher-order-patterns-core",
                        "title": "Nested Functions, Factories, lambda, map, filter, reduce, and sorted(key=...)",
                        "tags": ["nested", "factory", "lambda", "map", "filter", "reduce", "sorted key"],
                    }
                ],
            },
        ],
    },
    {
        "week": 4,
        "title": "Week 4",
        "topics": [
            {
                "id": "w4-string-fundamentals",
                "title": "String Fundamentals",
                "topic_tags": ["quote", "escape", "immutability"],
                "subtopics": [
                    {
                        "id": "w4-string-fundamentals-core",
                        "title": "Quotes, Escape Characters, and Immutability",
                        "tags": ["quote", "escape", "immutability", "string immutability", "defining strings"],
                    }
                ],
            },
            {
                "id": "w4-string-operations-and-methods",
                "title": "String Operations and Methods",
                "topic_tags": ["join", "replace", "find", "index", "strip", "string module", "slice"],
                "subtopics": [
                    {
                        "id": "w4-string-operations-and-methods-core",
                        "title": "Slicing with Step, Search, replace, join, strip, and the string Module",
                        "tags": ["join", "replace", "find", "index", "strip", "string module", "slicing", "step"],
                    }
                ],
            },
            {
                "id": "w4-string-formatting",
                "title": "String Formatting",
                "topic_tags": ["f string", "formatting"],
                "subtopics": [
                    {
                        "id": "w4-string-formatting-core",
                        "title": "f-strings Basics, Formatting, and Debug Form",
                        "tags": ["f string", "formatted string", "formatting", "debugging"],
                    }
                ],
            },
            {
                "id": "w4-oop-fundamentals",
                "title": "OOP Fundamentals",
                "topic_tags": ["class", "__init__", "self", "attribute", "oop"],
                "subtopics": [
                    {
                        "id": "w4-oop-fundamentals-core",
                        "title": "Class Definition, __init__, self, and Attribute Basics",
                        "tags": ["class", "__init__", "self", "attribute", "oop", "instance"],
                    }
                ],
            },
            {
                "id": "w4-error-handling",
                "title": "Error Handling",
                "topic_tags": ["try", "except", "raise"],
                "subtopics": [
                    {
                        "id": "w4-error-handling-core",
                        "title": "try/except and raise",
                        "tags": ["try", "except", "raise", "error handling"],
                    }
                ],
            },
        ],
    },
    {
        "week": 5,
        "title": "Week 5",
        "topics": [
            {
                "id": "w5-pandas-core-structures",
                "title": "Pandas Core Structures",
                "topic_tags": ["series", "dataframe", "create"],
                "subtopics": [
                    {
                        "id": "w5-pandas-core-structures-core",
                        "title": "Series, DataFrame, and Creation Patterns",
                        "tags": ["series", "dataframe", "pd.series", "pd.dataframe", "create"],
                    }
                ],
            },
            {
                "id": "w5-inspecting-and-selecting-data",
                "title": "Inspecting and Selecting Data",
                "topic_tags": ["head", "tail", "describe", "loc", "iloc", "selection", "boolean indexing"],
                "subtopics": [
                    {
                        "id": "w5-inspecting-and-selecting-data-core",
                        "title": "head, tail, describe, loc, iloc, Result Types, and Boolean Indexing",
                        "tags": ["head", "tail", "describe", "loc", "iloc", "selection", "boolean indexing"],
                    }
                ],
            },
            {
                "id": "w5-working-with-values",
                "title": "Working With Values",
                "topic_tags": ["sorting", "missing", "broadcasting", "vectorized", "isin", "map", "apply"],
                "subtopics": [
                    {
                        "id": "w5-working-with-values-core",
                        "title": "Sorting, Missing Data, Broadcasting, Vectorized Strings, isin, map, and apply",
                        "tags": ["sorting", "missing", "broadcasting", "vectorized", "isin", "map", "apply"],
                    }
                ],
            },
            {
                "id": "w5-combining-data",
                "title": "Combining Data",
                "topic_tags": ["concatenate", "merge", "groupby", "grouping", "join"],
                "subtopics": [
                    {
                        "id": "w5-combining-data-core",
                        "title": "Concatenation, Merging, and Grouping",
                        "tags": ["concatenate", "concat", "merge", "groupby", "grouping", "join"],
                    }
                ],
            },
        ],
    },
    {
        "week": 6,
        "title": "Week 6",
        "topics": [
            {
                "id": "w6-comprehensions",
                "title": "Comprehensions",
                "topic_tags": ["comprehension", "walrus", "enumerate"],
                "subtopics": [
                    {
                        "id": "w6-comprehensions-core",
                        "title": "List/Dict/Set Comprehensions, Nested Variants, Logic Filters, Walrus, and enumerate Patterns",
                        "tags": ["comprehension", "walrus", "enumerate", "join", "nested dictionary"],
                    }
                ],
            },
            {
                "id": "w6-generators-and-iterators",
                "title": "Generators and Iterators",
                "topic_tags": ["generator", "iterator", "yield"],
                "subtopics": [
                    {
                        "id": "w6-generators-and-iterators-core",
                        "title": "Iterator Protocol, Generator Functions, and Generator Comprehensions",
                        "tags": ["generator", "iterator", "yield", "iterable"],
                    }
                ],
            },
            {
                "id": "w6-datetime",
                "title": "Datetime",
                "topic_tags": ["datetime", "timestamp", "strftime", "strptime", "timedelta"],
                "subtopics": [
                    {
                        "id": "w6-datetime-core",
                        "title": "now, Timestamps, strftime, strptime, timedelta, and Date Arithmetic",
                        "tags": ["datetime", "timestamp", "strftime", "strptime", "timedelta", "date arithmetic"],
                    }
                ],
            },
        ],
    },
]


def outline_for_week(week: int) -> dict[str, Any]:
    for item in OUTLINE_SPEC:
        if item["week"] == week:
            return copy.deepcopy(item)
    return {
        "week": week,
        "title": f"Week {week}",
        "topics": [
            {
                "id": f"w{week}-topic-1",
                "title": f"Week {week} Topic",
                "topic_tags": [],
                "subtopics": [
                    {
                        "id": f"w{week}-topic-1-core",
                        "title": "Core Material",
                        "tags": [],
                    }
                ],
            }
        ],
    }


def match_outline_target(week: int, *texts: Any) -> tuple[dict[str, Any], dict[str, Any], int, list[str]]:
    haystack = " ".join(_norm(text) for text in texts if _safe_str(text))
    primary = _norm(texts[0]) if texts else ""
    outline = outline_for_week(week)
    ranked: list[tuple[int, int, dict[str, Any], dict[str, Any], list[str]]] = []
    for topic in outline["topics"]:
        for subtopic in topic["subtopics"]:
            hits = [tag for tag in subtopic.get("tags", []) if tag_in_haystack(haystack, tag)]
            score = len(hits) * 3
            score += sum(1 for tag in topic.get("topic_tags", []) if tag_in_haystack(haystack, tag))
            score += sum(3 for tag in topic.get("topic_tags", []) if tag_in_haystack(primary, tag))
            score += sum(2 for tag in subtopic.get("tags", []) if tag_in_haystack(primary, tag))
            if subtopic["title"].lower() in haystack:
                score += 2
            ranked.append((score, -subtopic.get("order", 0), topic, subtopic, hits))
    ranked.sort(key=lambda item: (-item[0], item[1], item[2]["title"]))
    if ranked and ranked[0][0] > 0:
        _, _, topic, subtopic, hits = ranked[0]
        return topic, subtopic, ranked[0][0], hits
    topic = outline["topics"][0]
    subtopic = topic["subtopics"][0]
    return topic, subtopic, 0, []

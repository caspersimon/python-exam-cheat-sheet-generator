from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any


PARENT_TOPIC_SPECS = [
    ("python-foundations", "Python Foundations", ["Python Basics", "Objects and Names", "Operators and Truth", "Conditions"]),
    ("collections-and-iteration", "Collections and Iteration", ["Lists and Sets", "Dictionaries and Mappings", "Loops", "Comprehensions"]),
    ("functions-and-program-flow", "Functions and Program Flow", ["Functions and Imports", "Flexible Arguments and kwargs", "Scope and Return Behavior", "Lambda and Higher-Order Patterns"]),
    ("strings-and-output", "Strings and Output", ["String Fundamentals", "String Operations and Methods", "Output Formatting"]),
    ("pandas-data-work", "Pandas Data Work", ["Pandas Core Structures", "Inspecting and Selecting Data", "Working With Values"]),
    ("datetime-and-time-logic", "Datetime and Time Logic", ["Datetime Parsing and Formatting", "Datetime Arithmetic and Comparisons"]),
    ("object-oriented-python", "Object-Oriented Python", ["OOP Fundamentals", "OOP Comparison Logic", "Inheritance and Class Relationships"]),
]

MAIN_TOPIC_SUMMARIES = {
    "Python Basics": "Execution model, syntax basics, and quick mental models for reading simple Python safely under exam pressure.",
    "Objects and Names": "Identity, mutability, assignment, copying, and what names really point to.",
    "Operators and Truth": "Arithmetic, comparison, precedence, and boolean reasoning traps.",
    "Conditions": "Truthiness, comparisons, branching, and condition-building patterns.",
    "Lists and Sets": "Sequence access, ordering, slicing, and list/set behavior differences.",
    "Dictionaries and Mappings": "Construction, lookup, iteration, equality, and counting patterns.",
    "Loops": "Iteration patterns, zip/enumerate, membership, and counting logic.",
    "Comprehensions": "Syntax templates and fast recognition for list, set, and dict comprehensions.",
    "Functions and Imports": "Defining functions, calling conventions, built-ins, and import styles.",
    "Flexible Arguments and kwargs": "Variable argument patterns, kwargs, and signature reading.",
    "Scope and Return Behavior": "Local vs global names, implicit None, tuple returns, and caller-visible effects.",
    "Lambda and Higher-Order Patterns": "Short anonymous functions, map/apply-style patterns, and callback reading.",
    "String Fundamentals": "Immutability, basic access, and string-as-sequence reasoning.",
    "String Operations and Methods": "Methods, indexing, slicing, split/join, replace, search, and predicates.",
    "Output Formatting": "F-strings, .format, separators, and output-shape control.",
    "Pandas Core Structures": "Series/DataFrame basics, creation patterns, and shape intuition.",
    "Inspecting and Selecting Data": "head/tail/describe plus valid row/column selection rules.",
    "Working With Values": "Filtering, sorting, vectorized string ops, isin, map, apply, and column arithmetic.",
    "Datetime Parsing and Formatting": "Parsing strings into datetimes and formatting datetimes back into strings.",
    "Datetime Arithmetic and Comparisons": "Timedeltas, comparisons, replacement, and object-vs-string reasoning.",
    "OOP Fundamentals": "Classes, __init__, self, attributes, defaults, and method calls.",
    "OOP Comparison Logic": "Custom compare-style methods, asymmetric rules, and None fallback.",
    "Inheritance and Class Relationships": "Subclassing, super(), and parent/child relationships.",
}

TOPIC_MAPPING = {
    "Python Basics": ("Python Foundations", "Python Basics"),
    "Objects and Names": ("Python Foundations", "Objects and Names"),
    "Operators and Truth": ("Python Foundations", "Operators and Truth"),
    "Sequences and Access": ("Collections and Iteration", "Lists and Sets"),
    "Functions and Imports": ("Functions and Program Flow", "Functions and Imports"),
    "Dictionaries and Mappings": ("Collections and Iteration", "Dictionaries and Mappings"),
    "Lists and Sets": ("Collections and Iteration", "Lists and Sets"),
    "Conditions": ("Python Foundations", "Conditions"),
    "Loops": ("Collections and Iteration", "Loops"),
    "Conversion and Truthiness": ("Python Foundations", "Conditions"),
    "Defining and Calling Functions": ("Functions and Program Flow", "Functions and Imports"),
    "Return Behavior": ("Functions and Program Flow", "Scope and Return Behavior"),
    "Scope": ("Functions and Program Flow", "Scope and Return Behavior"),
    "Arguments": ("Functions and Program Flow", "Flexible Arguments and kwargs"),
    "Higher-Order Patterns": ("Functions and Program Flow", "Lambda and Higher-Order Patterns"),
    "String Fundamentals": ("Strings and Output", "String Fundamentals"),
    "String Operations and Methods": ("Strings and Output", "String Operations and Methods"),
    "String Formatting": ("Strings and Output", "Output Formatting"),
    "OOP Fundamentals": ("Object-Oriented Python", "OOP Fundamentals"),
    "Error Handling": ("Functions and Program Flow", "Scope and Return Behavior"),
    "Pandas Core Structures": ("Pandas Data Work", "Pandas Core Structures"),
    "Inspecting and Selecting Data": ("Pandas Data Work", "Inspecting and Selecting Data"),
    "Working With Values": ("Pandas Data Work", "Working With Values"),
    "Combining Data": ("Pandas Data Work", "Working With Values"),
    "Comprehensions": ("Collections and Iteration", "Comprehensions"),
    "Generators and Iterators": ("Collections and Iteration", "Loops"),
    "Datetime": ("Datetime and Time Logic", "Datetime Parsing and Formatting"),
}


def timestamp_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def slugify(value: str) -> str:
    text = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return re.sub(r"-+", "-", text)


def canonical_snippet_id(source_snippet_id: str) -> str:
    return f"snippet-{slugify(source_snippet_id)}"


def canonical_piece_id(card_id: str, item_id: str) -> str:
    return f"piece-{slugify(card_id)}-{slugify(item_id)}"


def summarize_text(value: str, fallback: str, limit: int = 72) -> str:
    text = " ".join(str(value or "").replace("\r", "\n").replace("\n", " ").split()).strip()
    if not text:
        return fallback
    if len(text) <= limit:
        return text
    return f"{text[: limit - 1].rstrip()}…"


def topic_assignment(topic: str) -> tuple[str, str]:
    return TOPIC_MAPPING.get(topic, ("Python Foundations", "Python Basics"))


def normalize_options(options: Any) -> dict[str, str]:
    if isinstance(options, dict):
        return {str(key): str(value) for key, value in options.items()}
    return {}

import re
import hashlib
from pathlib import Path

from pipelines.shared import compact_text as shared_compact_text

ROOT = Path(__file__).resolve().parents[2]
OUTPUT_FILE = ROOT / "topic_cards.json"

STOP_WORDS = {
    "vs",
    "versus",
    "and",
    "or",
    "the",
    "a",
    "an",
    "to",
    "of",
    "in",
    "on",
    "with",
    "for",
    "intro",
    "introduction",
    "basic",
    "basics",
    "types",
    "type",
    "question",
    "questions",
    "operators",
    "operator",
    "methods",
    "method",
    "statement",
    "statements",
    "model",
    "core",
    "properties",
    "examples",
    "example",
}

TOKEN_ALIASES = {
    "dict": "dictionary",
}

LOW_VALUE_PHRASES = {
    "below you will find",
    "the following",
    "function definitions start",
    "you call functions",
    "if you need more advanced structures",
    "dictionaries are",
    "global and local names",
    "indexing",
    "slicing",
    "for-loops",
    "while loop",
}

GENERIC_FALLBACKS = {
    "oop",
    "strings",
    "dictionaries",
    "fun example",
    "lists",
    "scope",
    "slicing",
    "pandas",
    "indexing",
    "conditions",
    "map",
    "return none",
    "data types",
    "sets",
    "enumerate",
    "zip",
    "comprehensions",
    "star args",
    "lambda",
    "objects",
}

TOPIC_LABEL_OVERRIDES = {
    "loop": "Loops",
    "loop while": "While Loops",
    "loop range": "Loops with range()",
    "loop nested": "Nested Loops",
    "loop nested pair": "Nested Loop Pairs",
    "control loop while": "While Loop Control",
    "complexity loop nested": "Nested Loop Complexity",
    "dictionary looping over": "Looping Over Dictionaries",
    "enumerate loop": "enumerate() in Loops",
    "formatting loop string while": "String Formatting in While Loops",
    "loop walru while": "Walrus in While Loops",
    "string": "Strings",
    "module string": "String Utilities",
    "f formatting string": "String Formatting",
    "f string": "f-Strings",
    "find index searching string": "String Searching",
    "immutability string": "String Immutability",
    "string stripping": "String Stripping",
    "string vectorized": "Vectorized String Operations",
    "date strftime string": "strftime() Date Formatting",
    "date string strptime": "strptime() Date Parsing",
    "dictionary": "Dictionaries",
    "dictionary slicing": "Dictionary Slicing",
    "dictionary iteration": "Dictionary Iteration",
    "1 2 dictionary manipulation": "Dictionary Manipulation",
    "1 2 dictionary slicing": "Dictionary Membership and Slicing",
    "dictionary indexing": "Dictionary Indexing",
    "average dictionary": "Dictionary Averages",
    "comprehension dictionary": "Dictionary Comprehensions",
    "2 comprehension dictionary": "Dictionary Comprehensions II",
    "1 2 comprehension dictionary": "Dictionary Comprehensions I",
    "3 comprehension dictionary": "Dictionary Comprehension Variants",
    "comprehension dictionary logic": "Dictionary Comprehension Logic",
    "comprehension dictionary nested": "Nested Dictionary Comprehensions",
    "list": "Lists",
    "list slicing": "List Slicing",
    "list tuple": "Lists and Tuples",
    "append extend list": "append() vs extend()",
    "comprehension list": "List Comprehensions",
    "1 2 comprehension list": "List Comprehensions I",
    "comprehension list string transformation via": "String List Transformations",
    "global local scope": "Global vs Local Scope",
    "scope unboundlocalerror": "UnboundLocalError and Scope",
    "function scope": "Function Scope",
    "function nested scope": "Nested Function Scope",
    "scope": "Scope",
    "1 scope": "Scope Lifetimes",
    "1 2 scope": "Scope Basics",
    "1 3 scope": "Scope Access Rules",
    "panda": "Pandas Basics",
    "panda sery string": "Pandas String Series",
    "indexing panda": "Pandas Indexing",
    "panda sort subset": "Pandas Sorting and Subsetting",
    "pd.dataframe": "Pandas DataFrames",
    "data": "Data Basics",
    "data missing": "Missing Data",
    "data viewing": "Viewing Data",
    "function": "Functions and Methods",
    "calling definition function": "Function Definition and Calls",
    "argument flexible function": "Flexible Function Arguments",
    "3 argument function": "Function Arguments",
    "3 argument flexible function": "Flexible Function Arguments",
    "factory function nested": "Function Factories",
    "closure factory function": "Closures and Factories",
    "filter function": "filter() Functions",
    "function reduce": "reduce() Functions",
    "2 3 built function": "Built-in Functions",
    "args star": "*args",
    "args function star": "Argument Unpacking",
    "args double kwarg star": "*args and **kwargs Basics",
    "argument double keyword kwarg star": "Argument Unpacking with *args and **kwargs",
    "return": "Return Values",
    "none return": "None Returns",
    "implicit none return": "Implicit None Returns",
    "global none return": "Globals and None Returns",
    "condition falsy truthy": "Truthy and Falsy",
    "condition conditional expression": "Conditional Expressions",
    "conditional expression": "Ternary Expressions",
    "boolean condition precedence": "Boolean Precedence",
    "boolean": "Booleans",
    "indexing": "Indexing",
    "conversion indexing": "Conversion and Indexing",
    "boolean indexing": "Boolean Indexing",
    "slicing": "Slicing",
    "indexing slicing": "Indexing and Slicing",
    "negative slicing step": "Negative-Step Slicing",
    "map": "map()",
    "function map": "map() Functions",
    "filter map": "filter() and map()",
    "comprehension filter map vs.": "Comprehensions vs map()",
    "lambda": "lambda",
    "function lambda": "Lambda Functions",
    "lambda sorted": "lambda with sorted()",
    "object": "Objects",
    "identity object": "Object Identity",
    "8 know object": "Object Basics",
    "sets": "Sets",
    "duplicate list sets": "Sets for Deduplication",
    "dictionary list ordered sets unordered": "Ordered Lists vs Unordered Sets",
    "zip": "zip()",
    "looping zip": "Looping with zip()",
    "counting dictionary zip": "Counting with zip() and Dictionaries",
    "enumerate": "enumerate()",
    "condition dictionary enumerate": "enumerate() with Dictionaries",
    "comprehension enumerate": "enumerate() in Comprehensions",
    "comprehension": "Comprehensions",
    "comprehension set": "Set Comprehensions",
    "comprehension walru": "Comprehensions with Walrus",
    "loc selection": "Selection with .loc",
    "iloc selection": "Selection with .iloc",
    "1 2 logic": "Logic Basics",
    "1 2 variable": "Variable Basics",
    "1 3 logic": "Logic Rules",
    "1 3 variable": "Variable Scope Rules",
}

TOKEN_DISPLAY = {
    "oop": "OOP",
    "args": "*args",
    "kwargs": "**kwargs",
    "kwarg": "kwargs",
    "f": "f",
    "panda": "Pandas",
    "sery": "Series",
    "strftime": "strftime()",
    "strptime": "strptime()",
    "none": "None",
    "unboundlocalerror": "UnboundLocalError",
    "pd.dataframe": "Pandas DataFrame",
    "walru": "Walrus",
    "zip": "zip()",
    "enumerate": "enumerate()",
    "map": "map()",
    "filter": "filter()",
    "reduce": "reduce()",
    "lambda": "lambda",
}


def normalize_text(value: str) -> str:
    text = (value or "").lower()
    text = text.replace("**", " double_star ")
    text = text.replace("*", " star ")
    text = re.sub(r"[_/|\\,:;()\[\]{}-]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def token_set(value: str) -> set[str]:
    text = normalize_text(value)
    tokens = [t for t in text.split(" ") if t and t not in STOP_WORDS]
    cleaned = []
    for token in tokens:
        if token.endswith("ies") and len(token) > 4:
            token = token[:-3] + "y"
        elif token.endswith("es") and len(token) > 4 and (
            token.endswith(("ses", "xes", "zes", "ches", "shes"))
        ):
            token = token[:-2]
        elif token.endswith("s") and len(token) > 4 and not token.endswith("ss"):
            token = token[:-1]
        token = TOKEN_ALIASES.get(token, token)
        cleaned.append(token)
    return set(cleaned)


def topic_key(value: str) -> str:
    tokens = sorted(token_set(value))
    if not tokens:
        return "misc"

    alias_join = " ".join(tokens)
    aliases = {
        "arg kwargs star": "args kwargs",
        "global scope": "scope global",
        "lambda map": "lambda map",
        "lambda reduce": "lambda reduce",
        "lambda sorted": "lambda sorted",
        "mutable default": "mutable default",
        "mutable immutable": "mutable immutable",
        "return none": "return none",
        "scope unboundlocalerror": "scope unboundlocalerror",
        "truthy falsy": "truthy falsy",
        "zip enumerate": "zip enumerate",
    }
    return aliases.get(alias_join, " ".join(tokens))


def make_id(prefix: str, content: str) -> str:
    digest = hashlib.md5(content.encode("utf-8")).hexdigest()[:10]
    return f"{prefix}-{digest}"


def similarity(key_a: str, key_b: str) -> float:
    a = set(key_a.split())
    b = set(key_b.split())
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    if union == 0:
        return 0.0
    return inter / union


def is_relevant(card_key: str, source_key: str, threshold: float = 0.5) -> bool:
    if card_key == source_key:
        return True
    if card_key in source_key or source_key in card_key:
        return True
    return similarity(card_key, source_key) >= threshold


def pretty_topic(key: str, fallback: str) -> str:
    raw_key = normalize_text(key)
    stripped_key = re.sub(r"\b\d+\b", " ", raw_key)
    stripped_key = re.sub(r"\s+", " ", stripped_key).strip()
    if not stripped_key and not raw_key:
        return (fallback or "").strip() or "Misc"

    if raw_key in TOPIC_LABEL_OVERRIDES:
        key_label = TOPIC_LABEL_OVERRIDES[raw_key]
    elif stripped_key in TOPIC_LABEL_OVERRIDES:
        key_label = TOPIC_LABEL_OVERRIDES[stripped_key]
    else:
        words = []
        for raw_word in stripped_key.split():
            if raw_word.isdigit():
                continue
            words.append(TOKEN_DISPLAY.get(raw_word, raw_word.capitalize()))
        key_label = " ".join(words).strip() or "Misc"

    fallback_text = (fallback or "").strip()
    if not fallback_text:
        return key_label

    if raw_key in TOPIC_LABEL_OVERRIDES and normalize_text(fallback_text) != normalize_text(key_label):
        return key_label

    fallback_norm = normalize_text(fallback_text)
    fallback_tokens = token_set(fallback_text)
    key_tokens = token_set(raw_key or stripped_key)
    if fallback_norm in GENERIC_FALLBACKS:
        return key_label
    if re.search(r"[_\d]", fallback_text):
        return key_label
    if len(fallback_tokens) <= 1 and len(key_tokens) > 1:
        return key_label
    if fallback_tokens and key_tokens and fallback_tokens.issubset(key_tokens) and len(key_tokens) > len(fallback_tokens):
        return key_label
    return fallback_text


def compact_text(value: str, max_len: int = 500) -> str:
    return shared_compact_text(value, max_len)


def looks_like_python_code(value: str) -> bool:
    text = (value or "").strip()
    if not text:
        return False
    if "\n" in text:
        return True

    code_signals = (
        "=",
        "(",
        ")",
        "[",
        "]",
        "{",
        "}",
        ".",
        ":",
        "+",
        "-",
        "*",
        "/",
        "%",
    )
    code_keywords = (
        "print",
        "for ",
        "while ",
        "if ",
        "elif ",
        "else",
        "def ",
        "return",
        "import ",
        "from ",
        "lambda",
        "range",
        "len",
        "sorted",
        "map",
        "filter",
        "reduce",
    )

    lower = text.lower()
    if any(signal in text for signal in code_signals) and any(ch.isalpha() for ch in text):
        return True
    return any(lower.startswith(keyword) or f" {keyword}" in lower for keyword in code_keywords)


def is_low_value_single_line(value: str) -> bool:
    text = (value or "").strip()
    if not text:
        return True

    if "\n" in text:
        return False

    lower = text.lower().strip()

    if lower.startswith("#"):
        return True
    if lower.startswith("##") or lower.startswith("###"):
        return True

    if any(phrase in lower for phrase in LOW_VALUE_PHRASES) and not looks_like_python_code(text):
        return True

    if not looks_like_python_code(text):
        words = re.findall(r"[a-zA-Z]+", text)
        if len(words) <= 8:
            return True

    return False


def clean_code_example(code: str) -> str:
    text = (code or "").strip()
    if not text:
        return ""
    if is_low_value_single_line(text):
        return ""
    return compact_text(text, 1400)


def clean_notebook_source(source: str, cell_type: str) -> str:
    text = (source or "").strip()
    if not text:
        return ""

    if "\n" not in text:
        if cell_type == "markdown" and is_low_value_single_line(text):
            return ""
        if cell_type == "code" and text.startswith("#"):
            return ""
        if cell_type == "code" and is_low_value_single_line(text) and not looks_like_python_code(text):
            return ""

    if len(text) <= 4:
        return ""

    return compact_text(text, 1200)


def dedupe_list(items: list[dict], key_fields: list[str]) -> list[dict]:
    seen = set()
    out = []
    for item in items:
        key = tuple(item.get(k) for k in key_fields)
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out

import json
import re
import hashlib
from collections import defaultdict
from pathlib import Path

from pipelines.shared import compact_text as shared_compact_text

ROOT = Path(__file__).resolve().parents[2]
SOURCE_FILE = ROOT / "study_data.json"
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
    if fallback and fallback.strip():
        return fallback.strip()
    words = key.split()
    return " ".join(word.capitalize() for word in words)


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


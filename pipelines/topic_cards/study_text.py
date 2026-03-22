from __future__ import annotations

import re

from pipelines.shared import compact_text


def _safe_str(value: object) -> str:
    return str(value or "").strip()


def _normalized(text: object) -> str:
    return re.sub(r"\s+", " ", _safe_str(text)).strip()


def _boundary_compact(text: str, limit: int) -> str:
    value = _normalized(text)
    if len(value) <= limit:
        return value
    for marker in (". ", "; ", " / ", ": "):
        cut = value.rfind(marker, 0, limit)
        if cut >= int(limit * 0.55):
            return value[: cut + 1].strip()
    return value


def _generic_prompt(line: str) -> bool:
    value = line.lower().strip(" :?")
    return value in {
        "what will be printed",
        "what is the output of the following code",
        "what is the output of this code",
        "what is the result of",
        "what does the following program do",
        "consider the following code snippet",
    }


def _first_meaningful_code_line(text: object) -> str:
    for line in _safe_str(text).splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith(("A ", "B ", "C ", "D ")):
            continue
        if stripped.lower().startswith(("what will be printed", "what is the output", "consider the following")):
            continue
        return stripped
    return ""


def infer_pattern_label(*parts: object) -> str:
    source = " \n".join(_safe_str(part) for part in parts if _safe_str(part))
    normalized = source.lower()
    if "l3 = l1[:]" in source or ("[:]" in source and any(token in source for token in ("append(", "] =", ".remove(", ".sort("))):
        return "Aliasing vs slice-copy after mutation"
    if any(token in source for token in ("[::-1]", "[::-2]", "[::2]")):
        return "Negative-step slicing and slice order"
    if "range(" in source:
        return "range() values and stop exclusion"
    if any(token in source for token in (".upper(", ".lower(", ".replace(", ".strip(", ".split(", ".join(")):
        return "String method return values"
    if any(token in source for token in (".append(", ".remove(", ".sort(", ".extend(")):
        return "List method effects and resulting list"
    if ".loc[" in source and "=" in source:
        return "Vectorized `.loc` column assignment"
    if ".loc[" in source or ".iloc[" in source:
        return ".loc / .iloc selection rules"
    if ".map(" in source or "lambda" in source:
        return "Elementwise transformation with `map`/`lambda`"
    if "strftime" in normalized or "strptime" in normalized:
        return "Datetime formatting and parsing"
    if "+=" in source:
        return "Augmented assignment (`+=`) behavior"
    if "==" in source and " is " in normalized:
        return "`==` versus `is`"
    if "def " in source and "return" in normalized:
        return "Function return value and trace"
    if "if " in source or "elif " in source:
        return "Condition flow and branch result"
    gist = _first_meaningful_code_line(source)
    return compact_text(gist or _normalized(parts[0] if parts else ""), 90)


def normalize_rule_text(text: object) -> str:
    value = _normalized(text)
    if not value:
        return ""
    value = re.sub(r"</?br\s*/?>", " ", value, flags=re.IGNORECASE)
    value = re.sub(r"</?(ul|ol|p)>", " ", value, flags=re.IGNORECASE)
    value = re.sub(r"<li>", " ", value, flags=re.IGNORECASE)
    value = re.sub(r"</li>", "; ", value, flags=re.IGNORECASE)
    value = re.sub(r"#+\s*", "", value)
    value = value.replace("Stop is NOT inclusive.", "Stop is excluded.")
    value = value.replace("start default=0, step default=1.", "`start` defaults to 0 and `step` defaults to 1.")
    value = value.replace("Works like slicing but defaults differ slightly.", "Same stop-excluded rule as slicing.")
    value = value.replace("Representative exam answer shape:", "Pattern to remember:")
    return _boundary_compact(value, 320)


def pattern_hint(*parts: object) -> str:
    source = " \n".join(_safe_str(part) for part in parts if _safe_str(part))
    normalized = source.lower()
    if "l3 = l1[:]" in source or ("[:]" in source and any(token in source for token in ("append(", "] =", ".remove(", ".sort("))):
        return "Track which names point to the same object and which slice creates a copy before the mutation happens."
    if any(token in source for token in ("[::-1]", "[::-2]", "[::2]")):
        return "Read the slice as `start:stop:step`; with a negative step Python walks right-to-left and still excludes the stop position."
    if "range(" in source:
        return "Expand `range(start, stop, step)` manually; `stop` is excluded and the next value is found by adding `step` each time."
    if any(token in source for token in (".upper(", ".lower(", ".replace(", ".strip(", ".split(", ".join(")):
        return "String methods return a new string; the original value changes only if you assign the result back."
    if any(token in source for token in (".append(", ".remove(", ".sort(", ".extend(")):
        return "Check whether the method mutates the list in place and what the list looks like after each call."
    if ".loc[" in source and "=" in source:
        return "Use `.loc[:, column] = ...` when the assignment should fill or update an entire column by label."
    if ".loc[" in source or ".iloc[" in source:
        return "Decide first whether the code is using labels (`.loc`) or integer positions (`.iloc`)."
    if ".map(" in source or "lambda" in source:
        return "Apply the lambda/function to one element first, then extend that same transformation to the rest of the Series or iterable."
    if "strftime" in normalized or "strptime" in normalized:
        return "Remember the direction: `strftime` formats a datetime into text, `strptime` parses text into a datetime."
    if "+=" in source:
        return "For numeric variables, `a += 1` updates the stored value the same way as `a = a + 1`."
    if "==" in source and " is " in normalized:
        return "`==` compares value equality; `is` compares whether two names refer to the same object."
    if "return" in normalized:
        return "Trace the returned value, not just what gets printed while the function runs."
    return "Work through the code in execution order and keep track of the exact value after each step."


def question_summary_text(question: object, *, code_context: object = "", title: object = "", explanation: object = "") -> str:
    lines = [line.strip() for line in _safe_str(question).splitlines() if line.strip()]
    first = lines[0] if lines else ""
    normalized_first = first.lower()
    if "anagram" in normalized_first:
        return "Choose the correct anagram implementation"
    if "students" in normalized_first and "grade" in normalized_first:
        return "Format student names and grades from a list of dicts"
    if "define a class called vehicle" in normalized_first:
        return "Define `__init__` with required and default attributes"
    if "compare the book" in normalized_first and "review" in normalized_first:
        return "Book comparison method: score plus review count"
    if "dataframe called df" in normalized_first and "column called \"c\"" in normalized_first:
        return "Create a full DataFrame column by vectorized addition"
    if "series s with municipality and province names" in normalized_first:
        return "Split each string and keep the municipality name"
    if "which of the following code segments will return the number of the day" in normalized_first:
        return "Compute day-of-year from a datetime"
    if first and not _generic_prompt(first):
        if len(first) > 260:
            inferred = infer_pattern_label(question, code_context, title, explanation)
            if inferred:
                return inferred
        return first
    if _safe_str(title):
        label = infer_pattern_label(title, code_context, explanation)
        if label:
            return label
    return infer_pattern_label(question, code_context, explanation)

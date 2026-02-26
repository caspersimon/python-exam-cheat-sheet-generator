from __future__ import annotations

import re


def extract_json_blob(text: str) -> str:
    raw = (text or "").strip()
    if not raw:
        raise ValueError("Empty model output")

    if raw.startswith("```"):
        raw = re.sub(r"^```[a-zA-Z0-9_-]*\\n", "", raw)
        raw = re.sub(r"\\n```$", "", raw).strip()

    starts = [idx for idx in [raw.find("["), raw.find("{")] if idx != -1]
    if not starts:
        raise ValueError("No JSON start token found")

    start = min(starts)
    stack = []
    in_string = False
    escape = False

    for i in range(start, len(raw)):
        ch = raw[i]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue

        if ch == '"':
            in_string = True
            continue

        if ch in "[{":
            stack.append(ch)
        elif ch in "]}":
            if not stack:
                continue
            open_ch = stack.pop()
            if (open_ch == "[" and ch != "]") or (open_ch == "{" and ch != "}"):
                raise ValueError("Mismatched JSON brackets")
            if not stack:
                return raw[start : i + 1]

    raise ValueError("JSON closing token not found")

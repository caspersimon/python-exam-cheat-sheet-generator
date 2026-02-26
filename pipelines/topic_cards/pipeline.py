from __future__ import annotations

import json

from .assembly import (
    attach_exam_content,
    attach_lecture_content,
    attach_notebook_content,
    attach_patterns,
    collect_card_topics,
    sort_cards,
)
from .core import OUTPUT_FILE, SOURCE_FILE


def main() -> None:
    data = json.loads(SOURCE_FILE.read_text(encoding="utf-8"))

    cards = collect_card_topics(data)
    attach_lecture_content(cards, data)
    attach_exam_content(cards, data)
    attach_notebook_content(cards, data)
    attach_patterns(cards, data)

    output = {
        "meta": {
            "generated_from": SOURCE_FILE.name,
            "generator": "build_topic_cards.py",
            "course": data.get("meta", {}).get("course"),
            "weeks_covered": data.get("meta", {}).get("weeks_covered", []),
            "total_cards": 0,
            "notes": [
                "Sections (1) lecture snippets, (2) exam Q&A, and (4) notebook snippets are sourced from study_data.json.",
                "Low-value one-line notebook/heading snippets are filtered out automatically.",
                "AI sections are generated separately (summary, common questions, examples).",
            ],
        },
        "cards": [],
    }

    output["cards"] = sort_cards(cards)
    output["meta"]["total_cards"] = len(output["cards"])

    OUTPUT_FILE.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUTPUT_FILE} with {output['meta']['total_cards']} cards")

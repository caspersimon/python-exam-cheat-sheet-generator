from __future__ import annotations

from typing import Any, Callable

from pipelines.topic_cards.manual_curation_overrides_weeks_1_3 import apply_overrides_weeks_1_3
from pipelines.topic_cards.manual_curation_overrides_weeks_4_6 import apply_overrides_weeks_4_6


def apply_card_specific_adjustments(
    card: dict[str, Any],
    *,
    safe_str: Callable[[object], str],
    rewrite_text: Callable[[object], str],
    match_topic: Callable[..., bool],
    looks_invalid_python: Callable[[str], bool],
) -> None:
    for handler in (apply_overrides_weeks_1_3, apply_overrides_weeks_4_6):
        if handler(
            card,
            safe_str=safe_str,
            rewrite_text=rewrite_text,
            match_topic=match_topic,
            looks_invalid_python=looks_invalid_python,
        ):
            return

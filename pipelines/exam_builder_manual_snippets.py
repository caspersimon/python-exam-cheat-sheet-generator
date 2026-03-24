from __future__ import annotations

from typing import Any

from pipelines.exam_builder_manual_snippets_part1 import MANUAL_SNIPPETS_PART1
from pipelines.exam_builder_manual_snippets_part2 import MANUAL_SNIPPETS_PART2


MANUAL_SNIPPETS: list[dict[str, Any]] = [*MANUAL_SNIPPETS_PART1, *MANUAL_SNIPPETS_PART2]

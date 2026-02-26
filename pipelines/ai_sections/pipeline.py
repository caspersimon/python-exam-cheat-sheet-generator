from __future__ import annotations

import json
import time
from typing import Any

from .common import (
    CARDS_FILE,
    CHUNK_SIZE,
    apply_generated,
    chunked,
    fallback_ai_bundle,
    generate_for_chunk,
    normalize_generated_entry,
    sanitize_topic_context,
    validate_ai_fields,
)


def main() -> None:
    data = json.loads(CARDS_FILE.read_text(encoding="utf-8"))
    cards = data.get("cards", [])
    if not cards:
        raise RuntimeError("No cards found in topic_cards.json")

    contexts = [sanitize_topic_context(card) for card in cards]
    chunks = chunked(contexts, CHUNK_SIZE)

    generated_by_id: dict[str, dict[str, Any]] = {}

    for index, chunk in enumerate(chunks, start=1):
        print(f"Generating chunk {index}/{len(chunks)} ({len(chunk)} topics)...", flush=True)
        try:
            raw_entries = generate_for_chunk(chunk)
            if len(raw_entries) != len(chunk):
                raise RuntimeError(f"Chunk {index} length mismatch: expected {len(chunk)}, got {len(raw_entries)}")

            for card_ctx, raw_entry in zip(chunk, raw_entries):
                card_stub = {"topic": card_ctx.get("topic"), "trap_patterns": card_ctx.get("trap_patterns", [])}
                generated_by_id[card_ctx["id"]] = normalize_generated_entry(raw_entry if isinstance(raw_entry, dict) else {}, card_stub)
        except Exception as exc:  # noqa: BLE001
            print(f"Chunk {index} failed ({exc}). Using local fallback for this chunk.", flush=True)
            for card_ctx in chunk:
                generated_by_id[card_ctx["id"]] = fallback_ai_bundle(
                    {"topic": card_ctx.get("topic"), "trap_patterns": card_ctx.get("trap_patterns", [])}
                )

        time.sleep(0.7)

    apply_generated(data, generated_by_id)

    notes = data.setdefault("meta", {}).setdefault("notes", [])
    notes.append("AI summary/common-questions/examples generated with gemini-cli and validated.")

    validate_ai_fields(data)

    CARDS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Updated {CARDS_FILE} with generated AI sections for {len(cards)} topics.")

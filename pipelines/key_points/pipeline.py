from __future__ import annotations

import json
import time
from typing import Any

from .common import (
    CARDS_FILE,
    CHUNK_SIZE,
    FILTER_AUDIT_FILE,
    MODEL,
    chunked,
    context_for_card,
    fallback_result,
    generate_chunk,
    init_filter_audit,
    normalize_key_points_no_filter,
    record_filter_decisions,
    sanitize_key_points,
    sanitize_key_points_with_audit,
    sanitize_recommended_ids,
    snippet_candidates,
)


def main() -> None:
    data = json.loads(CARDS_FILE.read_text(encoding="utf-8"))
    cards = data.get("cards", [])
    card_by_id = {str(card.get("id")): card for card in cards if card.get("id")}

    contexts = [context_for_card(card) for card in cards]
    chunks = chunked(contexts, CHUNK_SIZE)

    generated: dict[str, dict[str, Any]] = {}
    filter_audit = init_filter_audit()
    cards_with_rejections: set[str] = set()
    cards_using_fallback: set[str] = set()

    for idx, chunk in enumerate(chunks, start=1):
        print(f"Generating recommendations chunk {idx}/{len(chunks)} ({len(chunk)} topics)...", flush=True)
        try:
            out = generate_chunk(chunk)
            if len(out) != len(chunk):
                raise RuntimeError(f"Length mismatch expected {len(chunk)} got {len(out)}")

            for ctx, raw in zip(chunk, out):
                card_id = str(ctx.get("id") or "")
                card = card_by_id.get(card_id)
                if not card or not isinstance(raw, dict):
                    continue

                valid_ids = {c.get("id") for c in ctx["source_candidates"] if c.get("id")}
                fallback = fallback_result(card)

                key_points, rejected = sanitize_key_points_with_audit(raw.get("key_points_to_remember", []))
                record_filter_decisions(
                    filter_audit,
                    card_id=card_id,
                    topic=str(card.get("topic", "")),
                    source="model",
                    kept=key_points,
                    rejected=rejected,
                )
                if rejected:
                    cards_with_rejections.add(card_id)

                if len(key_points) < 3:
                    fb_points, fb_rejected = sanitize_key_points_with_audit(fallback["key_points_to_remember"])
                    record_filter_decisions(
                        filter_audit,
                        card_id=card_id,
                        topic=str(card.get("topic", "")),
                        source="fallback",
                        kept=fb_points,
                        rejected=fb_rejected,
                    )
                    if fb_rejected:
                        cards_with_rejections.add(card_id)
                    if len(fb_points) < 3:
                        fb_points = normalize_key_points_no_filter(fallback["key_points_to_remember"])
                    key_points = fb_points
                    cards_using_fallback.add(card_id)

                rec_ids = sanitize_recommended_ids(raw.get("recommended_ids", []), valid_ids)
                if len(rec_ids) < 2:
                    rec_ids = sanitize_recommended_ids(fallback["recommended_ids"], valid_ids)

                generated[card_id] = {
                    "key_points_to_remember": key_points,
                    "recommended_ids": rec_ids,
                }

        except Exception as exc:  # noqa: BLE001
            print(f"Chunk {idx} failed ({exc}). Using fallback for this chunk.", flush=True)
            for ctx in chunk:
                card_id = str(ctx.get("id") or "")
                card = card_by_id.get(card_id)
                if not card:
                    continue
                fb = fallback_result(card)
                valid_ids = {c.get("id") for c in ctx["source_candidates"] if c.get("id")}
                fb_points, fb_rejected = sanitize_key_points_with_audit(fb["key_points_to_remember"])
                record_filter_decisions(
                    filter_audit,
                    card_id=card_id,
                    topic=str(card.get("topic", "")),
                    source="fallback_chunk_failure",
                    kept=fb_points,
                    rejected=fb_rejected,
                )
                if fb_rejected:
                    cards_with_rejections.add(card_id)
                if len(fb_points) < 3:
                    fb_points = normalize_key_points_no_filter(fb["key_points_to_remember"])
                cards_using_fallback.add(card_id)
                generated[card_id] = {
                    "key_points_to_remember": fb_points,
                    "recommended_ids": sanitize_recommended_ids(fb["recommended_ids"], valid_ids),
                }

        time.sleep(0.5)

    for card in cards:
        cid = card.get("id")
        sections = card.setdefault("sections", {})
        bundle = generated.get(cid) or fallback_result(card)

        points = sanitize_key_points(bundle.get("key_points_to_remember", []))
        sections["key_points_to_remember"] = [
            {
                "id": f"kp-{i+1}",
                "text": p,
                "status": "generated",
                "model": MODEL,
                "generator": "gemini-cli",
            }
            for i, p in enumerate(points)
        ]

        valid_ids = {c.get("id") for c in snippet_candidates(card) if c.get("id")}
        rec_ids = sanitize_recommended_ids(bundle.get("recommended_ids", []), valid_ids)
        sections["recommended_ids"] = rec_ids

    notes = data.setdefault("meta", {}).setdefault("notes", [])
    notes.append("Generated key_points_to_remember and recommended_ids via gemini-cli.")

    filter_audit["summary"]["cards_with_rejections"] = len(cards_with_rejections)
    filter_audit["summary"]["cards_using_fallback_points"] = len(cards_using_fallback)

    CARDS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    FILTER_AUDIT_FILE.write_text(json.dumps(filter_audit, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Updated {CARDS_FILE} with key points and recommendation splits for {len(cards)} cards.")
    print(
        "Filter audit:",
        f"{filter_audit['summary']['kept']} kept / {filter_audit['summary']['rejected']} rejected",
        f"across {filter_audit['summary']['total_candidates']} candidates.",
    )
    print(f"Wrote filter audit to {FILTER_AUDIT_FILE}.")

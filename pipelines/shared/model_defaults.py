from __future__ import annotations

# Centralized default model IDs used across scripts/pipelines.
# Keep these values aligned with what is available in the local Gemini CLI.

# Aliases requested by project maintainers:
# - FAST_GEMINI_AGENT: cheaper/faster model for lighter tasks.
# - SMART_GEMINI_AGENT: stronger model for high-judgment tasks.

FAST_GEMINI_AGENT = "gemini-3-flash-preview"
SMART_GEMINI_AGENT = "gemini-3-pro-preview"

# Optional conservative fallbacks.
FAST_GEMINI_AGENT_FALLBACK = "gemini-2.5-flash"
SMART_GEMINI_AGENT_FALLBACK = FAST_GEMINI_AGENT

# Human-readable aliases requested by maintainers.
GEMINI_AGENT_MODELS = {
    "fast gemini agent": FAST_GEMINI_AGENT,
    "smart gemini agent": SMART_GEMINI_AGENT,
}

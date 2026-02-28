from .iterables import chunked
from .json_tools import extract_json_blob
from .llm import run_gemini_cli
from .model_defaults import (
    FAST_GEMINI_AGENT,
    FAST_GEMINI_AGENT_FALLBACK,
    GEMINI_AGENT_MODELS,
    SMART_GEMINI_AGENT,
    SMART_GEMINI_AGENT_FALLBACK,
)
from .study_database import (
    STUDY_DB_FILE,
    build_study_db_from_monolith,
    flatten_study_db_for_pipeline,
    load_study_db,
    load_topic_pipeline_data,
    recompute_topic_analysis,
    write_study_db,
)
from .text import compact_text, normalize_newlines, normalize_space, trim_lines

__all__ = [
    "STUDY_DB_FILE",
    "build_study_db_from_monolith",
    "chunked",
    "compact_text",
    "extract_json_blob",
    "FAST_GEMINI_AGENT",
    "FAST_GEMINI_AGENT_FALLBACK",
    "GEMINI_AGENT_MODELS",
    "SMART_GEMINI_AGENT",
    "SMART_GEMINI_AGENT_FALLBACK",
    "flatten_study_db_for_pipeline",
    "load_study_db",
    "load_topic_pipeline_data",
    "normalize_newlines",
    "normalize_space",
    "recompute_topic_analysis",
    "run_gemini_cli",
    "trim_lines",
    "write_study_db",
]

__all__ = [
    "WeekCurationError",
    "analyze_assessment_payload",
    "analyze_week_payload",
    "coerce_week_payload_to_v3",
    "curate_week_payload",
    "migrate_study_db_to_v3",
    "missing_source_paths",
    "normalize_assessment_payload",
    "normalize_v3_week_payload",
    "normalize_week_payload",
]


def __getattr__(name):
    if name in {"WeekCurationError", "curate_week_payload", "normalize_week_payload"}:
        from .curation import WeekCurationError, curate_week_payload, normalize_week_payload

        mapping = {
            "WeekCurationError": WeekCurationError,
            "curate_week_payload": curate_week_payload,
            "normalize_week_payload": normalize_week_payload,
        }
        return mapping[name]

    if name in {"coerce_week_payload_to_v3", "migrate_study_db_to_v3", "normalize_v3_week_payload"}:
        from .lecture_first import coerce_week_payload_to_v3, migrate_study_db_to_v3, normalize_v3_week_payload

        mapping = {
            "coerce_week_payload_to_v3": coerce_week_payload_to_v3,
            "migrate_study_db_to_v3": migrate_study_db_to_v3,
            "normalize_v3_week_payload": normalize_v3_week_payload,
        }
        return mapping[name]

    if name in {"analyze_assessment_payload", "analyze_week_payload", "missing_source_paths", "normalize_assessment_payload"}:
        from .validators import (
            analyze_assessment_payload,
            analyze_week_payload,
            missing_source_paths,
            normalize_assessment_payload,
        )

        mapping = {
            "analyze_assessment_payload": analyze_assessment_payload,
            "analyze_week_payload": analyze_week_payload,
            "missing_source_paths": missing_source_paths,
            "normalize_assessment_payload": normalize_assessment_payload,
        }
        return mapping[name]

    raise AttributeError(name)

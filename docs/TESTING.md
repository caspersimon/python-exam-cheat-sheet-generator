# Testing and Validation

## One-command validation

```bash
make validate
```

This runs:

1. JavaScript syntax checks (`node --check` on `app/*.js`)
2. Python compile checks (`python3 -m py_compile` on entrypoints + `pipelines/`)
3. File-length policy check (`python3 scripts/check_file_lengths.py`)
4. Unit/integration tests (`python3 -m unittest discover -s tests -v`)

## Individual commands

```bash
make check-js
make check-py
make check-lines
make test
```

## UI Smoke Test (Headless)

```bash
make smoke-ui
```

This runs `scripts/smoke_ui_playwright.js` in an isolated temporary Playwright environment (`/tmp/pwtmp`) and verifies:

- app boot + data load
- splash dismissal
- accept action increments counters
- preview renders cards

## Test coverage areas

- `tests/test_file_length_policy.py`: enforces max 500 lines per code file.
- `tests/test_topic_cards_integrity.py`: ID uniqueness + section/recommended-id integrity.
- `tests/test_detail_rules.py`: key enrichment rule sanity and shape checks.
- `tests/test_js_syntax.py`: JS parsing safety for all app modules.

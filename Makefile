.PHONY: check-js check-py check-lines test smoke-ui stress-layout-ui export-canvas-guard-ui gemini-ui-protocol gemini-benchmark gemini-prompt-experiments gemini-health quality-dashboard maintenance-audit leave-better leave-better-ui validate

check-js:
	node --check app/state-and-init.js
	node --check app/splash-storage.js
	node --check app/preview-pointer.js
	node --check app/view-and-data.js
	node --check app/render-card-sections.js
	node --check app/text-render-utils.js
	node --check app/card-interactions.js
	node --check app/preview-render.js
	node --check app/preview-card-render.js
	node --check app/preview-history.js
	node --check app/preview-edit-modal.js
	node --check app/preview-editing.js
	node --check app/layout-export-utils.js
	node --check app/pdf-export-utils.js
	node --check app/main.js
	node --check scripts/export_canvas_guard_playwright.js
	node --check scripts/smoke_ui_playwright.js
	node --check scripts/stress_layout_playwright.js

check-py:
	python3 -m py_compile build_topic_cards.py generate_ai_sections.py generate_key_points_and_recommendations.py enrich_key_point_details.py
	python3 -m py_compile scripts/add_week_material.py scripts/migrate_study_database.py scripts/gemini_test_protocol.py scripts/maintenance_audit.py scripts/gemini_capability_benchmark.py scripts/gemini_prompt_experiments.py scripts/gemini_model_health.py scripts/quality_dashboard.py
	python3 -m py_compile $$(find pipelines -name '*.py' -type f)

check-lines:
	python3 scripts/check_file_lengths.py

test:
	python3 -m unittest discover -s tests -v

smoke-ui:
	mkdir -p /tmp/pwtmp
	npm install --prefix /tmp/pwtmp playwright --silent
	/tmp/pwtmp/node_modules/.bin/playwright install chromium
	NODE_PATH=/tmp/pwtmp/node_modules node scripts/smoke_ui_playwright.js

stress-layout-ui:
	mkdir -p /tmp/pwtmp
	npm install --prefix /tmp/pwtmp playwright --silent
	/tmp/pwtmp/node_modules/.bin/playwright install chromium
	NODE_PATH=/tmp/pwtmp/node_modules node scripts/stress_layout_playwright.js

export-canvas-guard-ui:
	mkdir -p /tmp/pwtmp
	npm install --prefix /tmp/pwtmp playwright --silent
	/tmp/pwtmp/node_modules/.bin/playwright install chromium
	NODE_PATH=/tmp/pwtmp/node_modules node scripts/export_canvas_guard_playwright.js

gemini-ui-protocol:
	python3 scripts/gemini_test_protocol.py --canvas-cmd "make export-canvas-guard-ui"

gemini-benchmark:
	python3 scripts/gemini_capability_benchmark.py

gemini-prompt-experiments:
	python3 scripts/gemini_prompt_experiments.py

gemini-health:
	python3 scripts/gemini_model_health.py

quality-dashboard:
	python3 scripts/quality_dashboard.py

maintenance-audit:
	python3 scripts/maintenance_audit.py

leave-better: validate

leave-better-ui: validate smoke-ui stress-layout-ui maintenance-audit

validate: check-js check-py check-lines test maintenance-audit

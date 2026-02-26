.PHONY: check-js check-py check-lines test smoke-ui validate

check-js:
	node --check app/state-and-init.js
	node --check app/splash-storage.js
	node --check app/preview-pointer.js
	node --check app/view-and-data.js
	node --check app/render-card-sections.js
	node --check app/text-render-utils.js
	node --check app/card-interactions.js
	node --check app/preview-render.js
	node --check app/layout-export-utils.js
	node --check app/main.js

check-py:
	python3 -m py_compile build_topic_cards.py generate_ai_sections.py generate_key_points_and_recommendations.py enrich_key_point_details.py
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

validate: check-js check-py check-lines test

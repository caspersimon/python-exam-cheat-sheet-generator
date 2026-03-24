#!/usr/bin/env bash
set -euo pipefail

cd "/Users/juliuseikmans/Desktop/Studies/2025-2026/intro to python/python-exam-cheat-sheet-generator"
python3 scripts/supervise_round2_grading.py --round round2 --baseline-round round1 --batch-size 5 --sleep-seconds 20 --max-stale-batches 8 2>&1 | tee "/Users/juliuseikmans/Desktop/Studies/2025-2026/intro to python/python-exam-cheat-sheet-generator/tmp/vision_exam_pipeline/round2_grading/supervisor.log"
echo "${PIPESTATUS[0]}" > "/Users/juliuseikmans/Desktop/Studies/2025-2026/intro to python/python-exam-cheat-sheet-generator/tmp/vision_exam_pipeline/round2_grading/supervisor.exit"

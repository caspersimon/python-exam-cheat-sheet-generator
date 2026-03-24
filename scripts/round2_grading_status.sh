#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SESSION_NAME="${1:-round2-grading}"
LOG_DIR="${ROOT}/tmp/vision_exam_pipeline/round2_grading"

echo "== tmux =="
if tmux has-session -t "${SESSION_NAME}" 2>/dev/null; then
  echo "session: running (${SESSION_NAME})"
else
  echo "session: not running (${SESSION_NAME})"
fi

echo
echo "== log files =="
for file in supervisor.log supervisor.exit supervisor.jsonl supervisor_state.json; do
  path="${LOG_DIR}/${file}"
  if [[ -f "${path}" ]]; then
    echo "present: ${path}"
  else
    echo "missing: ${path}"
  fi
done

echo
echo "== round2 status =="
python3 "${ROOT}/scripts/vision_exam_pipeline.py" status --round round2

for file in supervisor_state.json supervisor.log; do
  path="${LOG_DIR}/${file}"
  if [[ -f "${path}" ]]; then
    echo
    echo "== tail: ${file} =="
    tail -n 20 "${path}"
  fi
done

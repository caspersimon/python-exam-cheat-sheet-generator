#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SESSION_NAME="${1:-snippet-overnight}"
LOOP_DIR="${ROOT}/tmp/vision_exam_pipeline/overnight_loop"

echo "== tmux =="
if tmux has-session -t "${SESSION_NAME}" 2>/dev/null; then
  echo "session: running (${SESSION_NAME})"
else
  echo "session: not running (${SESSION_NAME})"
fi

echo
echo "== files =="
for file in "${LOOP_DIR}/state.json" "${LOOP_DIR}/launcher.log" "${LOOP_DIR}/STOP"; do
  if [[ -f "${file}" ]]; then
    echo "present: ${file}"
  else
    echo "missing: ${file}"
  fi
done

if [[ -f "${LOOP_DIR}/state.json" ]]; then
  echo
  echo "== state =="
  cat "${LOOP_DIR}/state.json"
fi

if [[ -f "${LOOP_DIR}/launcher.log" ]]; then
  echo
  echo "== recent launcher log =="
  tail -n 20 "${LOOP_DIR}/launcher.log"
fi

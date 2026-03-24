#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SESSION_NAME="${1:-snippet-overnight}"
MODEL="${OVERNIGHT_MODEL:-gpt-5.4}"
STOP_AT_HOUR="${OVERNIGHT_STOP_AT_HOUR:-8}"
TIMEZONE="${OVERNIGHT_TIMEZONE:-Europe/Amsterdam}"
MAX_ITERATIONS="${OVERNIGHT_MAX_ITERATIONS:-20}"
COOLDOWN_SECONDS="${OVERNIGHT_COOLDOWN_SECONDS:-30}"

if tmux has-session -t "${SESSION_NAME}" 2>/dev/null; then
  echo "tmux session already exists: ${SESSION_NAME}" >&2
  exit 1
fi

mkdir -p "${ROOT}/tmp/vision_exam_pipeline/overnight_loop"
rm -f "${ROOT}/tmp/vision_exam_pipeline/overnight_loop/STOP"

CMD="cd \"${ROOT}\" && python3 scripts/overnight_snippet_loop.py --model \"${MODEL}\" --timezone \"${TIMEZONE}\" --stop-at-hour \"${STOP_AT_HOUR}\" --max-iterations \"${MAX_ITERATIONS}\" --cooldown-seconds \"${COOLDOWN_SECONDS}\""

tmux new-session -d -s "${SESSION_NAME}" "${CMD}"
echo "started tmux session: ${SESSION_NAME}"
echo "attach with: tmux attach -t ${SESSION_NAME}"

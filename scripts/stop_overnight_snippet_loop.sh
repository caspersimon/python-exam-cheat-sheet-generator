#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SESSION_NAME="${1:-snippet-overnight}"
LOOP_DIR="${ROOT}/tmp/vision_exam_pipeline/overnight_loop"

mkdir -p "${LOOP_DIR}"
printf "manual stop requested at %s\n" "$(date -Iseconds)" > "${LOOP_DIR}/STOP"

if tmux has-session -t "${SESSION_NAME}" 2>/dev/null; then
  echo "stop file written for session: ${SESSION_NAME}"
  echo "the loop will stop after the current iteration or before the next one"
else
  echo "stop file written, but tmux session was not found: ${SESSION_NAME}"
fi

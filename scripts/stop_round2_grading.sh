#!/usr/bin/env bash
set -euo pipefail

SESSION_NAME="${1:-round2-grading}"
if tmux has-session -t "${SESSION_NAME}" 2>/dev/null; then
  tmux kill-session -t "${SESSION_NAME}"
  echo "stopped tmux session: ${SESSION_NAME}"
else
  echo "tmux session not running: ${SESSION_NAME}"
fi

#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SESSION_NAME="${1:-round2-grading}"
LOG_DIR="${ROOT}/tmp/vision_exam_pipeline/round2_grading"
mkdir -p "${LOG_DIR}"
rm -f "${LOG_DIR}/supervisor.log" "${LOG_DIR}/supervisor.exit" "${LOG_DIR}/supervisor.jsonl" "${LOG_DIR}/supervisor_state.json"
RUNNER="${LOG_DIR}/runner.sh"

if tmux has-session -t "${SESSION_NAME}" 2>/dev/null; then
  echo "tmux session already exists: ${SESSION_NAME}" >&2
  exit 1
fi

cat > "${RUNNER}" <<EOF
#!/usr/bin/env bash
set -euo pipefail

cd "${ROOT}"
python3 scripts/supervise_round2_grading.py --round round2 --baseline-round round1 --batch-size 5 --sleep-seconds 20 --max-stale-batches 8 2>&1 | tee "${LOG_DIR}/supervisor.log"
echo "\${PIPESTATUS[0]}" > "${LOG_DIR}/supervisor.exit"
EOF
chmod +x "${RUNNER}"

tmux new-session -d -s "${SESSION_NAME}" "${RUNNER}"
echo "started tmux session: ${SESSION_NAME}"
echo "logs: ${LOG_DIR}"

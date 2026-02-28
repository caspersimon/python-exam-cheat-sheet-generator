const MAX_PREVIEW_HISTORY_ENTRIES = 60;

function capturePreviewSnapshot() {
  return {
    decisions: deepClone(state.decisions),
    acceptedOrder: [...state.acceptedOrder],
    previewCards: deepClone(state.previewCards),
    previewZCounter: Number(state.previewZCounter) || 1,
  };
}

function pushPreviewHistorySnapshot(reason = "") {
  if (!state.cards.length) {
    return;
  }
  if (!Array.isArray(state.previewHistory)) {
    state.previewHistory = [];
  }

  state.previewHistory.push({
    ...capturePreviewSnapshot(),
    reason: String(reason || "").trim(),
    timestamp: Date.now(),
  });

  if (state.previewHistory.length > MAX_PREVIEW_HISTORY_ENTRIES) {
    state.previewHistory.splice(0, state.previewHistory.length - MAX_PREVIEW_HISTORY_ENTRIES);
  }
  syncPreviewUndoAvailability();
}

function restorePreviewSnapshot(snapshot) {
  if (!snapshot || typeof snapshot !== "object") {
    return false;
  }

  state.decisions = deepClone(snapshot.decisions || {});
  state.acceptedOrder = Array.isArray(snapshot.acceptedOrder) ? [...snapshot.acceptedOrder] : [];
  state.previewCards = deepClone(snapshot.previewCards || {});
  state.previewZCounter = clamp(Number(snapshot.previewZCounter) || 1, 1, 99999);
  return true;
}

function undoLastPreviewChange() {
  if (!Array.isArray(state.previewHistory) || state.previewHistory.length === 0) {
    syncPreviewUndoAvailability();
    return false;
  }

  const snapshot = state.previewHistory.pop();
  if (!restorePreviewSnapshot(snapshot)) {
    syncPreviewUndoAvailability();
    return false;
  }

  renderAll();
  syncPreviewUndoAvailability();
  return true;
}

function clearPreviewHistory() {
  state.previewHistory = [];
  syncPreviewUndoAvailability();
}

function syncPreviewUndoAvailability() {
  if (!refs.previewUndoBtn) {
    return;
  }
  const history = Array.isArray(state.previewHistory) ? state.previewHistory : [];
  const nextEntry = history[history.length - 1];
  refs.previewUndoBtn.disabled = history.length === 0;
  refs.previewUndoBtn.title = nextEntry?.reason
    ? `Undo: ${nextEntry.reason}`
    : "Undo preview edit/delete (Ctrl/Cmd+Z)";
}

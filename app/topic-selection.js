function ensureDraft(snippet) {
  if (state.drafts[snippet.id]) {
    return state.drafts[snippet.id];
  }

  state.drafts[snippet.id] = {
    selected: {
      pieces: [],
    },
    overrides: {
      pieces: {},
    },
  };
  return state.drafts[snippet.id];
}

function cloneDraft(draft) {
  return {
    selected: {
      pieces: [...(draft.selected?.pieces || [])],
    },
    overrides: {
      pieces: deepClone(draft.overrides?.pieces || {}),
    },
  };
}

function ensureSelectionOverrides(selection) {
  if (!selection || typeof selection !== "object") {
    return { pieces: {} };
  }
  if (!selection.overrides || typeof selection.overrides !== "object") {
    selection.overrides = {};
  }
  if (!selection.overrides.pieces || typeof selection.overrides.pieces !== "object") {
    selection.overrides.pieces = {};
  }
  return selection.overrides;
}

function getRenderableSelection(snippet, draft) {
  if (!draft) {
    return null;
  }

  const normalized = cloneDraft(draft);
  const validIds = new Set(getSnippetSelectablePieceIds(snippet));
  normalized.selected.pieces = normalized.selected.pieces.filter((pieceId) => validIds.has(pieceId));
  const cleanOverrides = {};
  Object.entries(normalized.overrides.pieces || {}).forEach(([pieceId, value]) => {
    if (validIds.has(pieceId) && value && typeof value === "object") {
      cleanOverrides[pieceId] = deepClone(value);
    }
  });
  normalized.overrides.pieces = cleanOverrides;
  return normalized;
}

function getSelectionCounts(snippet, draft = ensureDraft(snippet)) {
  const selection = getRenderableSelection(snippet, draft);
  const selectedSet = new Set(selection?.selected?.pieces || []);
  return {
    total: selectedSet.size,
  };
}

function getSelectedPieceContexts(snippet, draft = ensureDraft(snippet)) {
  const selection = getRenderableSelection(snippet, draft);
  const selectedSet = new Set(selection?.selected?.pieces || []);
  return (snippet.pieces || []).filter((piece) => selectedSet.has(piece.id)).map((piece) => ({ snippet, piece }));
}

function getSelectedPreviewEntries() {
  return [...state.snippets]
    .sort((a, b) => {
      if (a.topicTitle !== b.topicTitle) {
        return a.topicTitle.localeCompare(b.topicTitle);
      }
      if (a.subtopicTitle !== b.subtopicTitle) {
        return a.subtopicTitle.localeCompare(b.subtopicTitle);
      }
      return a.sortOrder - b.sortOrder || a.title.localeCompare(b.title);
    })
    .map((snippet) => {
      const selection = getRenderableSelection(snippet, ensureDraft(snippet));
      if (!selection?.selected?.pieces?.length) {
        return null;
      }
      return { snippet, selection };
    })
    .filter(Boolean);
}

function getSelectedItemTotals() {
  const entries = getSelectedPreviewEntries();
  return {
    snippets: entries.length,
    items: entries.reduce((sum, entry) => sum + (entry.selection.selected.pieces || []).length, 0),
  };
}

function getPieceOverride(selection, piece) {
  const overrides = ensureSelectionOverrides(selection);
  const value = overrides.pieces[piece.id];
  if (!value || typeof value !== "object") {
    return piece;
  }

  return {
    ...piece,
    title: typeof value.title === "string" && value.title.trim() ? value.title.trim() : piece.title,
    bodyMarkdown:
      typeof value.bodyMarkdown === "string"
        ? value.bodyMarkdown
        : typeof value.body_markdown === "string"
        ? value.body_markdown
        : piece.bodyMarkdown,
    bodyBlocks: Array.isArray(value.bodyBlocks)
      ? value.bodyBlocks
      : Array.isArray(value.body_blocks)
      ? value.body_blocks
      : piece.bodyBlocks,
  };
}

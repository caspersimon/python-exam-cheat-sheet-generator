function ensureDraft(card) {
  if (state.drafts[card.id]) {
    return state.drafts[card.id];
  }

  state.drafts[card.id] = {
    ui: {
      expandedSections: {},
    },
    selected: {
      pieces: [],
    },
    overrides: {
      pieces: {},
    },
  };
  return state.drafts[card.id];
}

function cloneDraft(draft) {
  return {
    ui: {
      expandedSections: deepClone(draft.ui?.expandedSections || {}),
    },
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

function getRenderableSelection(card, draft) {
  if (!draft) {
    return null;
  }

  const normalized = cloneDraft(draft);
  const validIds = new Set(getAllSelectablePieceIds(card));
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

function getSelectionCounts(card, draft = ensureDraft(card)) {
  const selection = getRenderableSelection(card, draft);
  const selectedSet = new Set(selection?.selected?.pieces || []);
  const selectedSnippetIds = new Set();
  const selectedSectionKeys = new Set();

  getExamCardSections(card).forEach((section) => {
    section.snippets.forEach((snippet) => {
      if (snippet.pieces.some((piece) => selectedSet.has(piece.id))) {
        selectedSnippetIds.add(snippet.id);
        selectedSectionKeys.add(section.key);
      }
    });
  });

  return {
    total: selectedSet.size,
    snippets: selectedSnippetIds.size,
    sections: selectedSectionKeys.size,
  };
}

function getSelectedPieceContexts(card, draft = ensureDraft(card)) {
  const selection = getRenderableSelection(card, draft);
  const selectedSet = new Set(selection?.selected?.pieces || []);
  const contexts = [];

  getExamCardSections(card).forEach((section) => {
    section.snippets.forEach((snippet) => {
      snippet.pieces.forEach((piece) => {
        if (selectedSet.has(piece.id)) {
          contexts.push({ section, snippet, piece });
        }
      });
    });
  });

  return contexts;
}

function getSelectedPreviewEntries() {
  return sortTopicCards(state.cards)
    .map((card) => {
      const selection = getRenderableSelection(card, ensureDraft(card));
      if (!selection?.selected?.pieces?.length) {
        return null;
      }
      return { card, selection };
    })
    .filter(Boolean);
}

function getSelectedItemTotals() {
  const entries = getSelectedPreviewEntries();
  return {
    topics: entries.length,
    items: entries.reduce((sum, entry) => sum + (entry.selection.selected.pieces || []).length, 0),
  };
}

function getSectionSelectedCount(card, draft, sectionKey) {
  const selection = getRenderableSelection(card, draft);
  const selectedSet = new Set(selection?.selected?.pieces || []);
  return getSectionSelectablePieceIds(card, sectionKey).filter((pieceId) => selectedSet.has(pieceId)).length;
}

function getSnippetSelectedCount(card, draft, snippetId) {
  const selection = getRenderableSelection(card, draft);
  const selectedSet = new Set(selection?.selected?.pieces || []);
  return getSnippetSelectablePieceIds(card, snippetId).filter((pieceId) => selectedSet.has(pieceId)).length;
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
    content: {
      ...(piece.content || {}),
      ...(value.content && typeof value.content === "object" ? value.content : {}),
    },
  };
}

function isPastExamSnippet(snippet) {
  return snippet?.snippetType === "past_exam_question";
}

function sectionNeedsShowMore(section, draft) {
  return section.snippets.length > section.initialVisibleCount && !draft.ui.expandedSections?.[section.key];
}

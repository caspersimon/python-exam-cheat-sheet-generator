function bindPreviewEditingEvents() {
  if (!refs.previewView) {
    return;
  }
  refs.previewView.addEventListener("click", handlePreviewEditingClick);
}

function handlePreviewEditingClick(event) {
  const editCardTitleBtn = event.target.closest("[data-role='preview-edit-card-title']");
  if (editCardTitleBtn) {
    event.preventDefault();
    void editPreviewCardTitle(editCardTitleBtn.dataset.cardId || "");
    return;
  }

  const toggleLockBtn = event.target.closest("[data-role='preview-toggle-lock']");
  if (toggleLockBtn) {
    event.preventDefault();
    togglePreviewCardLock(toggleLockBtn.dataset.cardId || "");
    return;
  }

  const deleteCardBtn = event.target.closest("[data-role='preview-delete-card']");
  if (deleteCardBtn) {
    event.preventDefault();
    deletePreviewCard(deleteCardBtn.dataset.cardId || "");
    return;
  }

  const deleteItemBtn = event.target.closest("[data-role='preview-delete-item']");
  if (deleteItemBtn) {
    event.preventDefault();
    deletePreviewItem(deleteItemBtn.dataset.sourceCardId || "", deleteItemBtn.dataset.pieceId || "");
    return;
  }

  const editItemBtn = event.target.closest("[data-role='preview-edit-item']");
  if (editItemBtn) {
    event.preventDefault();
    void editPreviewItem(editItemBtn.dataset.sourceCardId || "", editItemBtn.dataset.pieceId || "");
  }
}

function getPreviewEntry(previewId) {
  return state.previewEntries?.[previewId] || null;
}

function getDraftSnippetContext(snippetId) {
  const snippet = findSnippetById(snippetId);
  if (!snippet) {
    return null;
  }
  const draft = ensureDraft(snippet);
  return { snippet, draft };
}

function deletePreviewCard(previewId) {
  if (!previewId) {
    return;
  }
  const entry = getPreviewEntry(previewId);
  if (!entry) {
    return;
  }

  const confirmed = window.confirm(`Remove "${entry.snippet.title}" from the cheat sheet preview?`);
  if (!confirmed) {
    return;
  }

  pushPreviewHistorySnapshot(`Remove card "${entry.snippet.title}"`);
  const draft = ensureDraft(entry.snippet);
  draft.selected.pieces = [];
  draft.overrides = { pieces: {} };

  delete state.previewCards[previewId];
  renderAll();
}

function togglePreviewCardLock(previewId) {
  if (!previewId) {
    return;
  }
  const entry = getPreviewEntry(previewId);
  const layout = state.previewCards[previewId];
  if (!entry || !layout) {
    return;
  }

  const nextLocked = !Boolean(layout.locked);
  pushPreviewHistorySnapshot(`${nextLocked ? "Lock" : "Unlock"} card "${entry.snippet.title}"`);
  layout.locked = nextLocked;
  renderPreview();
}

async function editPreviewCardTitle(previewId) {
  if (!previewId) {
    return;
  }
  const entry = getPreviewEntry(previewId);
  const layout = state.previewCards[previewId];
  if (!entry || !layout) {
    return;
  }

  const currentTitle = getPreviewCardTitle(entry, layout);
  const values = await requestPreviewEditValues({
    title: "Edit Card Title",
    subtitle: `${entry.snippet.topicTitle} · ${entry.snippet.subtopicTitle}`,
    fields: [
      {
        id: "title",
        label: "Card title",
        prompt: "Edit card title:",
        value: currentTitle,
      },
    ],
  });
  if (!values) {
    return;
  }

  const nextTitle = String(values.title || "").trim();
  pushPreviewHistorySnapshot(`Edit card title for "${entry.snippet.title}"`);
  const defaultTitle = derivePreviewCardTitle(entry);
  layout.title = nextTitle && nextTitle !== defaultTitle ? nextTitle : "";
  renderPreview();
}

function deletePreviewItem(snippetId, pieceId) {
  if (!snippetId || !pieceId) {
    return;
  }

  const context = getDraftSnippetContext(snippetId);
  if (!context) {
    return;
  }

  const { snippet, draft } = context;
  const overrides = ensureSelectionOverrides(draft);
  pushPreviewHistorySnapshot(`Delete piece in "${snippet.title}"`);
  draft.selected.pieces = (draft.selected.pieces || []).filter((id) => id !== pieceId);
  delete overrides.pieces[pieceId];
  renderPreview();
}

async function editPreviewItem(snippetId, pieceId) {
  if (!snippetId || !pieceId) {
    return;
  }
  const context = getDraftSnippetContext(snippetId);
  if (!context) {
    return;
  }

  const { snippet, draft } = context;
  const match = findPieceContext(snippet, pieceId);
  if (!match) {
    return;
  }

  const current = getPieceOverride(draft, match.piece);
  const values = await requestPreviewEditValues(buildPieceEditRequest(snippet, current));
  if (!values) {
    return;
  }

  const nextOverride = buildPieceOverrideFromValues(current, values);
  if (!nextOverride) {
    deletePreviewItem(snippetId, pieceId);
    return;
  }

  pushPreviewHistorySnapshot(`Edit piece in "${snippet.title}"`);
  ensureSelectionOverrides(draft).pieces[pieceId] = nextOverride;
  renderPreview();
}

function buildPieceEditRequest(snippet, piece) {
  return {
    title: "Edit Piece",
    subtitle: `${snippet.topicTitle} · ${snippet.subtopicTitle}`,
    fields: [
      {
        id: "title",
        label: "Piece title",
        prompt: "Edit piece title:",
        value: piece.title || "",
      },
      {
        id: "body_markdown",
        label: "Piece body (Markdown)",
        prompt: "Edit markdown body:",
        value: String(piece.bodyMarkdown || ""),
        multiline: true,
        rows: 12,
        kind: "markdown",
      },
    ],
  };
}

function buildPieceOverrideFromValues(piece, values) {
  const nextTitle = String(values.title || "").trim();
  const nextBodyMarkdown = normalizeNewlines(String(values.body_markdown || "")).trim();
  if (!nextTitle && !nextBodyMarkdown) {
    return null;
  }

  return {
    title: nextTitle || piece.title,
    bodyMarkdown: nextBodyMarkdown,
    bodyBlocks: compileMarkdownBodyBlocks(nextBodyMarkdown),
  };
}

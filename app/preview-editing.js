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

  const sendBackBtn = event.target.closest("[data-role='preview-send-back']");
  if (sendBackBtn) {
    event.preventDefault();
    sendPreviewCardBackward(sendBackBtn.dataset.cardId || "");
    return;
  }

  const bringFrontBtn = event.target.closest("[data-role='preview-bring-front']");
  if (bringFrontBtn) {
    event.preventDefault();
    bringPreviewCardForward(bringFrontBtn.dataset.cardId || "");
    return;
  }

  const attachParentBtn = event.target.closest("[data-role='preview-attach-parent']");
  if (attachParentBtn) {
    event.preventDefault();
    attachDetachedPieceToParent(attachParentBtn.dataset.cardId || "");
    return;
  }

  const deleteCardBtn = event.target.closest("[data-role='preview-delete-card']");
  if (deleteCardBtn) {
    event.preventDefault();
    deletePreviewCard(deleteCardBtn.dataset.cardId || "");
    return;
  }

  const deleteSummaryBtn = event.target.closest("[data-role='preview-delete-summary']");
  if (deleteSummaryBtn) {
    event.preventDefault();
    deletePreviewSummary(deleteSummaryBtn.dataset.cardId || "");
    return;
  }

  const editSummaryBtn = event.target.closest("[data-role='preview-edit-summary']");
  if (editSummaryBtn) {
    event.preventDefault();
    void editPreviewSummary(editSummaryBtn.dataset.cardId || "");
    return;
  }

  const deleteItemBtn = event.target.closest("[data-role='preview-delete-item']");
  if (deleteItemBtn) {
    event.preventDefault();
    deletePreviewItem(deleteItemBtn.dataset.sourceCardId || "", deleteItemBtn.dataset.pieceId || "");
    return;
  }

  const detachItemBtn = event.target.closest("[data-role='preview-detach-item']");
  if (detachItemBtn) {
    event.preventDefault();
    detachPreviewItem(detachItemBtn.dataset.sourceCardId || "", detachItemBtn.dataset.pieceId || "");
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

  const isDetachedPieceCard = entry.entryType === "detached-piece";
  const confirmed = window.confirm(
    isDetachedPieceCard
      ? `Delete detached piece "${entry.snippet.title}" from the cheat sheet?`
      : `Move "${entry.snippet.title}" back to staged snippets?`
  );
  if (!confirmed) {
    return;
  }

  if (isDetachedPieceCard) {
    pushPreviewHistorySnapshot(`Delete detached piece "${entry.snippet.title}"`);
    removeDetachedPiece(previewId);
  } else {
    pushPreviewHistorySnapshot(`Stage snippet "${entry.snippet.title}"`);
    stageSnippetFromPreview(previewId);
  }
  renderAll();
}

function updatePreviewCardLockUI(cardId, nextLocked) {
  const cardElement = document.querySelector(`.preview-card[data-card-id="${CSS.escape(cardId)}"]`);
  if (!cardElement) {
    return false;
  }

  const nextLockedBool = Boolean(nextLocked);
  cardElement.classList.toggle("is-locked", nextLockedBool);
  cardElement.dataset.locked = String(nextLockedBool);

  const lockButton = cardElement.querySelector("[data-role='preview-toggle-lock']");
  if (lockButton) {
    const lockTitle = nextLockedBool ? "Unlock card position and size" : "Lock card position and size";
    const lockAria = nextLockedBool ? "Unlock card position and size" : "Lock card position and size";
    const lockIcon = nextLockedBool ? "&#128275;" : "&#128274;";
    lockButton.dataset.locked = String(nextLockedBool);
    lockButton.title = lockTitle;
    lockButton.setAttribute("aria-label", lockAria);
    const iconSpan = lockButton.querySelector("span");
    if (iconSpan) {
      iconSpan.innerHTML = lockIcon;
    }
  }

  const cardHead = cardElement.querySelector(".preview-card-head");
  if (cardHead) {
    cardHead.title = nextLockedBool ? "Card locked: unlock to move or resize" : "Drag to move this card";
  }

  const dragHint = cardElement.querySelector(".preview-drag-hint");
  if (dragHint) {
    dragHint.title = nextLockedBool ? "Card locked" : "Drag card";
    dragHint.innerHTML = nextLockedBool ? "&#128274;" : "&#8942;";
  }

  return true;
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
  if (!updatePreviewCardLockUI(previewId, nextLocked)) {
    renderPreview();
    return;
  }

  schedulePersistState();
}

function bringPreviewCardForward(previewId) {
  if (!previewId || !state.previewCards?.[previewId]) {
    return;
  }
  const entry = getPreviewEntry(previewId);
  pushPreviewHistorySnapshot(`Bring "${entry?.snippet?.title || previewId}" to front`);
  bringPreviewCardToFront(previewId);
  renderPreview();
}

function sendPreviewCardBackward(previewId) {
  if (!previewId || !state.previewCards?.[previewId]) {
    return;
  }
  const entry = getPreviewEntry(previewId);
  pushPreviewHistorySnapshot(`Send "${entry?.snippet?.title || previewId}" to back`);
  sendPreviewCardToBack(previewId);
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

  const detachedPiece = getDetachedPieceById(snippetId);
  if (detachedPiece) {
    pushPreviewHistorySnapshot(`Delete detached piece "${detachedPiece.title}"`);
    removeDetachedPiece(snippetId);
    renderAll();
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
  if (!draft.selected.pieces.length) {
    draft.selected.inPreview = false;
    delete state.previewCards[snippet.id];
  }
  renderAll();
}

async function editPreviewItem(snippetId, pieceId) {
  if (!snippetId || !pieceId) {
    return;
  }

  const detachedPiece = getDetachedPieceById(snippetId);
  if (detachedPiece) {
    const currentDetached = {
      title: detachedPiece.title,
      bodyMarkdown: detachedPiece.bodyMarkdown,
      bodyBlocks: detachedPiece.bodyBlocks,
      kind: detachedPiece.pieceKind || "paragraph",
    };
    const values = await requestPreviewEditValues(
      buildPieceEditRequest(
        {
          topicTitle: detachedPiece.topicTitle || "Detached",
          subtopicTitle: detachedPiece.subtopicTitle || "Detached piece",
        },
        currentDetached
      )
    );
    if (!values) {
      return;
    }

    const nextDetached = buildPieceOverrideFromValues(currentDetached, values);
    pushPreviewHistorySnapshot(`Edit detached piece "${detachedPiece.title}"`);
    if (!nextDetached) {
      removeDetachedPiece(snippetId);
    } else {
      updateDetachedPiece(snippetId, nextDetached);
    }
    renderAll();
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

function detachPreviewItem(snippetId, pieceId) {
  if (!snippetId || !pieceId) {
    return;
  }
  const snippet = findSnippetById(snippetId);
  if (!snippet) {
    return;
  }

  pushPreviewHistorySnapshot(`Detach piece from "${snippet.title}"`);
  const detachedId = detachPieceFromSnippet(snippetId, pieceId);
  if (!detachedId) {
    return;
  }
  renderAll();
}

function attachDetachedPieceToParent(detachedId) {
  if (!detachedId) {
    return;
  }
  const detached = getDetachedPieceById(detachedId);
  if (!detached) {
    return;
  }

  const parentSnippet = findSnippetById(detached.sourceSnippetId);
  const parentTitle = parentSnippet?.title || detached.sourceSnippetId;
  const confirmed = window.confirm(`Attach this detached piece back to "${parentTitle}"?`);
  if (!confirmed) {
    return;
  }

  pushPreviewHistorySnapshot(`Attach detached piece back to "${parentTitle}"`);
  const attached = addDetachedPieceBackToParent(detachedId);
  if (!attached) {
    return;
  }
  renderAll();
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

function deletePreviewSummary(cardId) {
  if (!cardId) {
    return;
  }
  const layout = state.previewCards[cardId];
  if (!layout) {
    return;
  }
  pushPreviewHistorySnapshot("Hide summary text");
  layout.summaryOverride = "";
  renderPreview();
}

async function editPreviewSummary(cardId) {
  if (!cardId) {
    return;
  }
  const layout = state.previewCards[cardId];
  if (!layout) {
    return;
  }
  const entry = getPreviewEntry(cardId);
  const currentText = layout.summaryOverride !== undefined ? layout.summaryOverride : (entry?.snippet?.summary || "");
  const values = await requestPreviewEditValues({
    title: "Edit Summary Text",
    subtitle: entry ? `${entry.snippet.topicTitle} · ${entry.snippet.subtopicTitle}` : cardId,
    fields: [
      {
        id: "summary",
        label: "Summary text",
        prompt: "Edit summary text:",
        value: currentText,
      },
    ],
  });
  if (!values) {
    return;
  }
  pushPreviewHistorySnapshot("Edit summary text");
  layout.summaryOverride = String(values.summary || "").trim();
  renderPreview();
}

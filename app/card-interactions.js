function isInteractiveNode(node) {
  return Boolean(node.closest("input,button,label,select,textarea,a,pre,code"));
}

function getCardById(cardId) {
  return state.cards.find((entry) => entry.id === cardId) || null;
}

function handleCardInputChange(event) {
  const input = event.target;
  const role = input.dataset.role;
  if (role !== "item-toggle") {
    return;
  }

  const card = getCardById(input.dataset.cardId || "");
  if (!card) {
    return;
  }

  const draft = ensureDraft(card);
  const pieceId = input.dataset.pieceId || "";
  if (!pieceId) {
    return;
  }

  const next = new Set(draft.selected.pieces || []);
  if (input.checked) {
    next.add(pieceId);
  } else {
    next.delete(pieceId);
  }
  draft.selected.pieces = [...next];
  renderAll();
}

function handleCardClick(event) {
  const openTopicTrigger = event.target.closest("[data-role='open-topic']");
  if (openTopicTrigger) {
    event.preventDefault();
    setActiveTopic(openTopicTrigger.dataset.cardId || "", openTopicTrigger.dataset.parentId || "");
    closeTopicSidebar();
    renderAll();
    return;
  }

  const toggleParentTrigger = event.target.closest("[data-role='toggle-parent']");
  if (toggleParentTrigger) {
    event.preventDefault();
    toggleParentExpanded(toggleParentTrigger.dataset.parentId || "");
    return;
  }

  const closeSidebarTrigger = event.target.closest("[data-role='close-topic-sidebar']");
  if (closeSidebarTrigger) {
    event.preventDefault();
    closeTopicSidebar();
    renderSwipe();
    schedulePersistState();
    return;
  }

  const selectAllSectionTrigger = event.target.closest("[data-role='select-all-section']");
  if (selectAllSectionTrigger) {
    event.preventDefault();
    selectAllSectionPieces(selectAllSectionTrigger.dataset.cardId || "", selectAllSectionTrigger.dataset.sectionKey || "");
    return;
  }

  const clearSectionTrigger = event.target.closest("[data-role='clear-section']");
  if (clearSectionTrigger) {
    event.preventDefault();
    clearSectionPieces(clearSectionTrigger.dataset.cardId || "", clearSectionTrigger.dataset.sectionKey || "");
    return;
  }

  const selectAllSnippetTrigger = event.target.closest("[data-role='select-all-snippet']");
  if (selectAllSnippetTrigger) {
    event.preventDefault();
    selectAllSnippetPieces(selectAllSnippetTrigger.dataset.cardId || "", selectAllSnippetTrigger.dataset.snippetId || "");
    return;
  }

  const clearSnippetTrigger = event.target.closest("[data-role='clear-snippet']");
  if (clearSnippetTrigger) {
    event.preventDefault();
    clearSnippetPieces(clearSnippetTrigger.dataset.cardId || "", clearSnippetTrigger.dataset.snippetId || "");
    return;
  }

  const toggleSectionExpandedTrigger = event.target.closest("[data-role='toggle-section-expanded']");
  if (toggleSectionExpandedTrigger) {
    event.preventDefault();
    toggleSectionExpanded(toggleSectionExpandedTrigger.dataset.cardId || "", toggleSectionExpandedTrigger.dataset.sectionKey || "");
    return;
  }

  const resetIntroTrigger = event.target.closest("[data-role='reset-splash']");
  if (resetIntroTrigger) {
    event.preventDefault();
    resetSplashIntro();
    return;
  }

  const resetProgressTrigger = event.target.closest("[data-role='reset-progress']");
  if (resetProgressTrigger) {
    event.preventDefault();
    resetAppProgress();
  }
}

function handleCardMouseOver(_event) {}

function selectAllSectionPieces(cardId, sectionKey) {
  const card = getCardById(cardId);
  if (!card) {
    return;
  }
  const draft = ensureDraft(card);
  draft.selected.pieces = [...new Set([...(draft.selected.pieces || []), ...getSectionSelectablePieceIds(card, sectionKey)])];
  renderAll();
}

function clearSectionPieces(cardId, sectionKey) {
  const card = getCardById(cardId);
  if (!card) {
    return;
  }
  const draft = ensureDraft(card);
  const removeIds = new Set(getSectionSelectablePieceIds(card, sectionKey));
  draft.selected.pieces = (draft.selected.pieces || []).filter((pieceId) => !removeIds.has(pieceId));
  const overrides = ensureSelectionOverrides(draft);
  Object.keys(overrides.pieces).forEach((pieceId) => {
    if (removeIds.has(pieceId)) {
      delete overrides.pieces[pieceId];
    }
  });
  renderAll();
}

function selectAllSnippetPieces(cardId, snippetId) {
  const card = getCardById(cardId);
  if (!card) {
    return;
  }
  const draft = ensureDraft(card);
  draft.selected.pieces = [...new Set([...(draft.selected.pieces || []), ...getSnippetSelectablePieceIds(card, snippetId)])];
  renderAll();
}

function clearSnippetPieces(cardId, snippetId) {
  const card = getCardById(cardId);
  if (!card) {
    return;
  }
  const draft = ensureDraft(card);
  const removeIds = new Set(getSnippetSelectablePieceIds(card, snippetId));
  draft.selected.pieces = (draft.selected.pieces || []).filter((pieceId) => !removeIds.has(pieceId));
  const overrides = ensureSelectionOverrides(draft);
  Object.keys(overrides.pieces).forEach((pieceId) => {
    if (removeIds.has(pieceId)) {
      delete overrides.pieces[pieceId];
    }
  });
  renderAll();
}

function toggleSectionExpanded(cardId, sectionKey) {
  const card = getCardById(cardId);
  if (!card) {
    return;
  }
  const draft = ensureDraft(card);
  draft.ui.expandedSections[sectionKey] = !Boolean(draft.ui.expandedSections[sectionKey]);
  renderAll();
  schedulePersistState();
}

function closeOpenInfoPopovers() {}

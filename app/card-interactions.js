function isInteractiveNode(node) {
  return Boolean(node.closest("input,button,label,select,textarea,a,pre,code"));
}

function getSnippetById(snippetId) {
  return findSnippetById(snippetId);
}

function getSubtopicById(subtopicId) {
  for (const topic of state.topics) {
    const subtopic = topic.subtopics.find((entry) => entry.id === subtopicId);
    if (subtopic) {
      return subtopic;
    }
  }
  return null;
}

function handleCardInputChange(event) {
  const input = event.target;
  if (input.dataset.role !== "item-toggle") {
    return;
  }

  const snippet = getSnippetById(input.dataset.snippetId || "");
  if (!snippet) {
    return;
  }

  const draft = ensureDraft(snippet);
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
    setActiveTopic(openTopicTrigger.dataset.topicId || "");
    closeTopicSidebar();
    renderAll();
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

  const selectAllSubtopicTrigger = event.target.closest("[data-role='select-all-subtopic']");
  if (selectAllSubtopicTrigger) {
    event.preventDefault();
    selectAllSubtopicPieces(selectAllSubtopicTrigger.dataset.subtopicId || "");
    return;
  }

  const clearSubtopicTrigger = event.target.closest("[data-role='clear-subtopic']");
  if (clearSubtopicTrigger) {
    event.preventDefault();
    clearSubtopicPieces(clearSubtopicTrigger.dataset.subtopicId || "");
    return;
  }

  const selectAllSnippetTrigger = event.target.closest("[data-role='select-all-snippet']");
  if (selectAllSnippetTrigger) {
    event.preventDefault();
    selectAllSnippetPieces(selectAllSnippetTrigger.dataset.snippetId || "");
    return;
  }

  const clearSnippetTrigger = event.target.closest("[data-role='clear-snippet']");
  if (clearSnippetTrigger) {
    event.preventDefault();
    clearSnippetPieces(clearSnippetTrigger.dataset.snippetId || "");
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

function selectAllSubtopicPieces(subtopicId) {
  const subtopic = getSubtopicById(subtopicId);
  if (!subtopic) {
    return;
  }
  subtopic.snippets.forEach((snippet) => {
    const draft = ensureDraft(snippet);
    draft.selected.pieces = [...new Set([...(draft.selected.pieces || []), ...getSnippetSelectablePieceIds(snippet)])];
  });
  renderAll();
}

function clearSubtopicPieces(subtopicId) {
  const subtopic = getSubtopicById(subtopicId);
  if (!subtopic) {
    return;
  }
  subtopic.snippets.forEach((snippet) => {
    const draft = ensureDraft(snippet);
    const removeIds = new Set(getSnippetSelectablePieceIds(snippet));
    draft.selected.pieces = (draft.selected.pieces || []).filter((pieceId) => !removeIds.has(pieceId));
    const overrides = ensureSelectionOverrides(draft);
    Object.keys(overrides.pieces).forEach((pieceId) => {
      if (removeIds.has(pieceId)) {
        delete overrides.pieces[pieceId];
      }
    });
  });
  renderAll();
}

function selectAllSnippetPieces(snippetId) {
  const snippet = getSnippetById(snippetId);
  if (!snippet) {
    return;
  }
  const draft = ensureDraft(snippet);
  draft.selected.pieces = [...new Set([...(draft.selected.pieces || []), ...getSnippetSelectablePieceIds(snippet)])];
  renderAll();
}

function clearSnippetPieces(snippetId) {
  const snippet = getSnippetById(snippetId);
  if (!snippet) {
    return;
  }
  const draft = ensureDraft(snippet);
  const removeIds = new Set(getSnippetSelectablePieceIds(snippet));
  draft.selected.pieces = (draft.selected.pieces || []).filter((pieceId) => !removeIds.has(pieceId));
  const overrides = ensureSelectionOverrides(draft);
  Object.keys(overrides.pieces).forEach((pieceId) => {
    if (removeIds.has(pieceId)) {
      delete overrides.pieces[pieceId];
    }
  });
  renderAll();
}

function closeOpenInfoPopovers() {}

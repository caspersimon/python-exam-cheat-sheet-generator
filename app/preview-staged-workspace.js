const STAGED_SNIPPET_DRAG_MIME = "application/x-cheatsheet-staged-snippet";

const previewWorkspaceDragState = {
  stagedSnippetId: "",
};

function clearPreviewDropTargets() {
  refs.page1Content?.classList.remove("is-drop-target");
  refs.page2Content?.classList.remove("is-drop-target");
}

function createDetachedPieceId(snippetId, pieceId) {
  const nonce = Math.random().toString(36).slice(2, 8);
  return `detached__${snippetId}__${pieceId}__${Date.now().toString(36)}__${nonce}`;
}

function getDetachedPieceEntries() {
  return Object.values(state.detachedPieces || {});
}

function getDetachedPieceById(detachedId) {
  return state.detachedPieces?.[detachedId] || null;
}

function detachPieceFromSnippet(snippetId, pieceId) {
  const snippet = findSnippetById(snippetId);
  if (!snippet || !pieceId) {
    return "";
  }

  const draft = ensureDraft(snippet);
  const selected = new Set(draft.selected?.pieces || []);
  if (!selected.has(pieceId)) {
    return "";
  }

  const piece = (snippet.pieces || []).find((entry) => entry.id === pieceId);
  if (!piece) {
    return "";
  }

  const effectivePiece = getPieceOverride(draft, piece);
  const detachedId = createDetachedPieceId(snippetId, pieceId);

  state.detachedPieces[detachedId] = {
    id: detachedId,
    sourceSnippetId: snippetId,
    sourcePieceId: pieceId,
    parentThemeId: getParentTopicThemeId(snippet),
    topicTitle: snippet.topicTitle,
    subtopicTitle: snippet.subtopicTitle,
    pieceKind: effectivePiece.kind || piece.kind || "paragraph",
    piecePresentation:
      effectivePiece.presentation && typeof effectivePiece.presentation === "object"
        ? deepClone(effectivePiece.presentation)
        : piece.presentation && typeof piece.presentation === "object"
        ? deepClone(piece.presentation)
        : null,
    title: effectivePiece.title || piece.title || "Detached piece",
    bodyMarkdown: String(effectivePiece.bodyMarkdown || ""),
    bodyBlocks: Array.isArray(effectivePiece.bodyBlocks)
      ? deepClone(effectivePiece.bodyBlocks)
      : compileMarkdownBodyBlocks(String(effectivePiece.bodyMarkdown || "")),
  };

  selected.delete(pieceId);
  draft.selected.pieces = [...selected];
  delete ensureSelectionOverrides(draft).pieces[pieceId];
  const sourceLayout = state.previewCards?.[snippetId] ? deepClone(state.previewCards[snippetId]) : null;

  if (!draft.selected.pieces.length) {
    draft.selected.inPreview = false;
    delete state.previewCards[snippetId];
  }

  const grid = getEffectiveGridSettings(Math.max(1, buildMergedPreviewEntries().length + 1));
  const fallback = getDefaultPreviewLayout(buildMergedPreviewEntries().length, grid);
  const detachedMinHeight = getMinimumPreviewCardHeight(detachedId, MIN_PREVIEW_CARD_HEIGHT);
  const detachedLayout = sourceLayout
    ? {
        page: sourceLayout.page,
        x: sourceLayout.x + 14,
        y: sourceLayout.y + 14,
        width: Math.max(MIN_PREVIEW_CARD_WIDTH, Math.round(sourceLayout.width * 0.76)),
        height: Math.max(detachedMinHeight, Math.round(sourceLayout.height * 0.72)),
        z: state.previewZCounter,
      }
    : {
        ...fallback,
        z: state.previewZCounter,
      };

  state.previewCards[detachedId] = sanitizePreviewCardLayout(detachedLayout, fallback, {
    cardId: detachedId,
    minWidth: MIN_PREVIEW_CARD_WIDTH,
    minHeight: detachedMinHeight,
  });
  state.previewZCounter = Math.max(state.previewZCounter, (state.previewCards[detachedId]?.z || 1) + 1);

  return detachedId;
}

function removeDetachedPiece(detachedId) {
  if (!detachedId || !state.detachedPieces?.[detachedId]) {
    return false;
  }
  delete state.detachedPieces[detachedId];
  delete state.previewCards[detachedId];
  delete state.previewEntries[detachedId];
  return true;
}

function updateDetachedPiece(detachedId, nextPiece) {
  const current = getDetachedPieceById(detachedId);
  if (!current || !nextPiece || typeof nextPiece !== "object") {
    return false;
  }

  current.title = String(nextPiece.title || current.title || "Detached piece").trim() || "Detached piece";
  current.bodyMarkdown = String(nextPiece.bodyMarkdown || "");
  current.bodyBlocks = Array.isArray(nextPiece.bodyBlocks)
    ? deepClone(nextPiece.bodyBlocks)
    : compileMarkdownBodyBlocks(current.bodyMarkdown);
  return true;
}

function buildDetachedPreviewEntry(detached) {
  const piece = {
    id: detached.id,
    title: detached.title,
    kind: detached.pieceKind,
    presentation:
      detached.piecePresentation && typeof detached.piecePresentation === "object" ? deepClone(detached.piecePresentation) : undefined,
    bodyMarkdown: detached.bodyMarkdown,
    bodyBlocks: Array.isArray(detached.bodyBlocks) ? deepClone(detached.bodyBlocks) : compileMarkdownBodyBlocks(detached.bodyMarkdown),
    selectable: true,
  };

  const snippet = {
    id: detached.id,
    slug: detached.id,
    title: detached.title,
    summary: "",
    topicTitle: detached.topicTitle || "Detached",
    subtopicTitle: detached.subtopicTitle ? `${detached.subtopicTitle} (detached)` : "Detached piece",
    sortOrder: 0,
    pieces: [piece],
    topicSlug: detached.parentThemeId || "",
  };

  return {
    previewId: detached.id,
    snippet,
    card: snippet,
    entryType: "detached-piece",
    detachedId: detached.id,
    selectionsByCard: {
      [snippet.id]: {
        selected: {
          pieces: [piece.id],
          inPreview: true,
        },
        overrides: { pieces: {} },
      },
    },
  };
}

function buildMergedPreviewEntries() {
  const snippetEntries = getIncludedPreviewEntries().map(({ snippet, selection }) => ({
    previewId: snippet.id,
    card: snippet,
    snippet,
    entryType: "snippet",
    selectionsByCard: {
      [snippet.id]: selection,
    },
  }));

  const detachedEntries = getDetachedPieceEntries().map((entry) => buildDetachedPreviewEntry(entry));

  return [...snippetEntries, ...detachedEntries].sort((a, b) => {
    if (a.snippet.topicTitle !== b.snippet.topicTitle) {
      return a.snippet.topicTitle.localeCompare(b.snippet.topicTitle);
    }
    if (a.snippet.subtopicTitle !== b.snippet.subtopicTitle) {
      return a.snippet.subtopicTitle.localeCompare(b.snippet.subtopicTitle);
    }
    return a.snippet.sortOrder - b.snippet.sortOrder || a.snippet.title.localeCompare(b.snippet.title);
  });
}

function renderStagedPiecePreview(entry) {
  const selectedSet = new Set(entry.selection?.selected?.pieces || []);
  if (!selectedSet.size) {
    return "";
  }

  const selectedPieces = (entry.snippet.pieces || [])
    .filter((piece) => selectedSet.has(piece.id))
    .map((piece) => {
      const effective = getPieceOverride(entry.selection, piece);
      const presentation = getPiecePresentation(effective);
      const emphasis = presentation?.emphasis || "";
      return `
        <li class="staged-piece-item${emphasis ? ` is-${escapeHtml(emphasis)}` : ""}"${
          emphasis ? ` data-piece-emphasis="${escapeHtml(emphasis)}"` : ""
        }>
          ${renderPiecePresentationBadge(presentation)}
          <span>${renderInlineCode(effective.title || piece.title)}</span>
        </li>
      `;
    });

  if (!selectedPieces.length) {
    return "";
  }

  return `<ul class="staged-piece-list">${selectedPieces.join("")}</ul>`;
}

function renderStagedSidebar(stagedEntries) {
  if (!refs.stagedSnippetList || !refs.stagedSnippetCount) {
    return;
  }

  refs.stagedSnippetCount.textContent = String(stagedEntries.length);
  if (refs.addAllStagedBtn) {
    refs.addAllStagedBtn.disabled = stagedEntries.length === 0;
  }

  if (!stagedEntries.length) {
    refs.stagedSnippetList.innerHTML = `<div class="staged-empty">No staged snippets. Select pieces in Topic Explorer, then drag snippets here to place them on pages.</div>`;
    return;
  }

  refs.stagedSnippetList.innerHTML = stagedEntries
    .map((entry) => {
      const pieceCount = entry.selection?.selected?.pieces?.length || 0;
      const piecePreviewHtml = renderStagedPiecePreview(entry);
      return `
        <article class="staged-snippet-item" draggable="true" data-role="staged-snippet" data-snippet-id="${escapeHtml(entry.snippet.id)}">
          <div class="staged-snippet-copy">
            <h4>${renderInlineCode(entry.snippet.title)}</h4>
            <p>${renderInlineCode(entry.snippet.subtopicTitle || entry.snippet.topicTitle || "")}</p>
            <span class="snippet-tag">${escapeHtml(`${pieceCount} piece${pieceCount === 1 ? "" : "s"}`)}</span>
            ${piecePreviewHtml}
          </div>
          <button type="button" class="ghost-btn compact-btn" data-role="staged-add-snippet" data-snippet-id="${escapeHtml(entry.snippet.id)}" title="Add to canvas">Add</button>
        </article>
      `;
    })
    .join("");
}

function addSnippetToPreview(snippetId, options = {}) {
  const snippet = findSnippetById(snippetId);
  if (!snippet) {
    return false;
  }

  const draft = ensureDraft(snippet);
  const selection = getRenderableSelection(snippet, draft);
  if (!selection?.selected?.pieces?.length) {
    return false;
  }

  draft.selected.inPreview = true;

  const existing = state.previewCards?.[snippetId];
  if (!existing) {
    const currentCount = buildMergedPreviewEntries().length;
    const grid = getEffectiveGridSettings(Math.max(1, currentCount));
    const fallback = getDefaultPreviewLayout(Math.max(0, currentCount - 1), grid);
    const page = Number(options.page) === 2 ? 2 : 1;
    const pageContent = getPreviewPageContent(page);
    const pageRect = pageContent.getBoundingClientRect();
    const hasDropPoint = Number.isFinite(Number(options.clientX)) && Number.isFinite(Number(options.clientY));

    const droppedX = hasDropPoint
      ? Number(options.clientX) - pageRect.left - fallback.width / 2
      : fallback.x;
    const droppedY = hasDropPoint
      ? Number(options.clientY) - pageRect.top - 18
      : fallback.y;

    const layout = sanitizePreviewCardLayout(
      {
        page,
        x: droppedX,
        y: droppedY,
        width: fallback.width,
        height: fallback.height,
        z: state.previewZCounter,
      },
      fallback,
      { cardId: snippetId, minHeight: MIN_PREVIEW_CARD_HEIGHT, minWidth: MIN_PREVIEW_CARD_WIDTH }
    );
    state.previewCards[snippetId] = layout;
    state.previewZCounter = Math.max(state.previewZCounter, layout.z + 1);
  }

  return true;
}

function addAllStagedSnippets() {
  const staged = getStagedPreviewEntries();
  if (!staged.length) {
    return 0;
  }

  staged.forEach((entry) => {
    const draft = ensureDraft(entry.snippet);
    draft.selected.inPreview = true;
  });

  return staged.length;
}

function stageSnippetFromPreview(snippetId) {
  const snippet = findSnippetById(snippetId);
  if (!snippet) {
    return false;
  }
  const draft = ensureDraft(snippet);
  draft.selected.inPreview = false;
  delete state.previewCards[snippet.id];
  return true;
}

function addDetachedPieceBackToParent(detachedId) {
  const detached = getDetachedPieceById(detachedId);
  if (!detached) {
    return false;
  }

  const snippet = findSnippetById(detached.sourceSnippetId);
  if (!snippet) {
    return false;
  }
  const sourcePiece = (snippet.pieces || []).find((piece) => piece.id === detached.sourcePieceId);
  if (!sourcePiece) {
    return false;
  }

  const draft = ensureDraft(snippet);
  const selected = new Set(draft.selected?.pieces || []);
  selected.add(detached.sourcePieceId);
  draft.selected.pieces = [...selected];
  draft.selected.inPreview = true;

  const detachedTitle = String(detached.title || sourcePiece.title || "").trim() || sourcePiece.title;
  const detachedBodyMarkdown = String(detached.bodyMarkdown || "");
  const detachedBodyBlocks = Array.isArray(detached.bodyBlocks)
    ? deepClone(detached.bodyBlocks)
    : compileMarkdownBodyBlocks(detachedBodyMarkdown);
  const unchangedTitle = detachedTitle === String(sourcePiece.title || "").trim();
  const unchangedBody = detachedBodyMarkdown === String(sourcePiece.bodyMarkdown || "");
  const overrides = ensureSelectionOverrides(draft);
  if (unchangedTitle && unchangedBody) {
    delete overrides.pieces[detached.sourcePieceId];
  } else {
    overrides.pieces[detached.sourcePieceId] = {
      title: detachedTitle,
      bodyMarkdown: detachedBodyMarkdown,
      bodyBlocks: detachedBodyBlocks,
    };
  }

  const detachedLayout = state.previewCards?.[detachedId] ? deepClone(state.previewCards[detachedId]) : null;
  const hadParentLayout = Boolean(state.previewCards?.[snippet.id]);
  if (!hadParentLayout) {
    addSnippetToPreview(snippet.id, { page: detachedLayout?.page || 1 });
  }

  if (detachedLayout && state.previewCards?.[snippet.id]) {
    const parentLayout = state.previewCards[snippet.id];
    state.previewCards[snippet.id] = sanitizePreviewCardLayout(
      {
        ...parentLayout,
        page: detachedLayout.page,
        x: detachedLayout.x,
        y: detachedLayout.y,
        z: state.previewZCounter,
      },
      parentLayout,
      { cardId: snippet.id, minWidth: MIN_PREVIEW_CARD_WIDTH, minHeight: MIN_PREVIEW_CARD_HEIGHT }
    );
    state.previewZCounter = Math.max(state.previewZCounter, (state.previewCards[snippet.id]?.z || 1) + 1);
  }

  removeDetachedPiece(detachedId);
  return true;
}

function handlePreviewWorkspaceClick(event) {
  const addBtn = event.target.closest("[data-role='staged-add-snippet']");
  if (addBtn) {
    const snippetId = addBtn.dataset.snippetId || "";
    if (!snippetId) {
      return;
    }
    const added = addSnippetToPreview(snippetId, {});
    if (!added) {
      return;
    }
    pushPreviewHistorySnapshot(`Add staged snippet "${snippetId}" to canvas`);
    renderAll();
    return;
  }

  const addAllBtn = event.target.closest("#addAllStagedBtn");
  if (addAllBtn) {
    const stagedCount = getStagedPreviewEntries().length;
    if (!stagedCount) {
      return;
    }
    pushPreviewHistorySnapshot(`Add all ${stagedCount} staged snippets to canvas`);
    addAllStagedSnippets();
    renderAll();
  }
}

function handlePreviewWorkspaceDragStart(event) {
  const staged = event.target.closest("[data-role='staged-snippet']");
  if (!staged) {
    return;
  }
  const snippetId = staged.dataset.snippetId || "";
  if (!snippetId) {
    return;
  }

  previewWorkspaceDragState.stagedSnippetId = snippetId;
  event.dataTransfer?.setData(STAGED_SNIPPET_DRAG_MIME, snippetId);
  event.dataTransfer?.setData("text/plain", snippetId);
  event.dataTransfer.effectAllowed = "copy";
  staged.classList.add("is-dragging");
}

function handlePreviewWorkspaceDragEnd(event) {
  const staged = event.target.closest("[data-role='staged-snippet']");
  if (staged) {
    staged.classList.remove("is-dragging");
  }
  previewWorkspaceDragState.stagedSnippetId = "";
  clearPreviewDropTargets();
}

function resolveDroppedSnippetId(event) {
  return (
    previewWorkspaceDragState.stagedSnippetId ||
    event.dataTransfer?.getData(STAGED_SNIPPET_DRAG_MIME) ||
    event.dataTransfer?.getData("text/plain") ||
    ""
  );
}

function handlePreviewPageDragOver(event) {
  const snippetId = resolveDroppedSnippetId(event);
  if (!snippetId) {
    return;
  }
  event.preventDefault();
  const pageContent = event.currentTarget;
  clearPreviewDropTargets();
  pageContent?.classList.add("is-drop-target");
  if (event.dataTransfer) {
    event.dataTransfer.dropEffect = "copy";
  }
}

function handlePreviewPageDrop(event) {
  const snippetId = resolveDroppedSnippetId(event);
  if (!snippetId) {
    return;
  }

  const pageContent = event.currentTarget;
  const pageNumber = pageContent === refs.page2Content ? 2 : 1;

  event.preventDefault();
  clearPreviewDropTargets();
  const added = addSnippetToPreview(snippetId, {
    page: pageNumber,
    clientX: event.clientX,
    clientY: event.clientY,
  });
  if (!added) {
    return;
  }
  pushPreviewHistorySnapshot(`Drop staged snippet "${snippetId}" onto page ${pageNumber}`);
  renderAll();
}

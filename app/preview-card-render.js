function renderPreviewSummaryBlock(previewCardId, snippet) {
  if (!snippet.summary) {
    return "";
  }
  const layout = state.previewCards[previewCardId];
  const override = layout?.summaryOverride;
  const text = override !== undefined ? override : snippet.summary;
  if (text === "") {
    return "";
  }
  return `
    <div class="preview-item-block preview-summary-block">
      <div class="preview-item-actions">
        <button
          type="button"
          class="preview-mini-btn icon-only"
          data-role="preview-edit-summary"
          data-card-id="${escapeHtml(previewCardId)}"
          title="Edit summary"
          aria-label="Edit summary"
        ><span aria-hidden="true">&#9998;</span></button>
        <button
          type="button"
          class="preview-mini-btn danger icon-only"
          data-role="preview-delete-summary"
          data-card-id="${escapeHtml(previewCardId)}"
          title="Hide summary"
          aria-label="Hide summary"
        ><span aria-hidden="true">&#10005;</span></button>
      </div>
      <p class="preview-item-note">${renderInlineCode(text)}</p>
    </div>
  `;
}

function buildPreviewCard(entry, layout, isOverflow = false) {
  const { previewId, snippet, selectionsByCard } = entry;
  const selection = selectionsByCard[snippet.id];
  const selectedSet = new Set(selection?.selected?.pieces || []);
  const selectedPieces = snippet.pieces.filter((piece) => selectedSet.has(piece.id));
  if (!selectedPieces.length) {
    return null;
  }

  const locked = Boolean(layout?.locked);
  const displayTitle = getPreviewCardTitle(entry, layout);
  const lockTitle = locked ? "Unlock card position and size" : "Lock card position and size";
  const lockAria = locked ? "Unlock card position and size" : "Lock card position and size";
  const lockIcon = locked ? "&#128275;" : "&#128274;";
  const headTitle = locked ? "Card locked: unlock to move or resize" : "Drag to move this card";
  const dragHint = locked ? "&#128274;" : "&#8942;";
  const dragHintTitle = locked ? "Card locked" : "Drag card";
  const parentThemeId = getParentTopicThemeId(snippet);

  const cardElement = document.createElement("article");
  const overflowClass = isOverflow ? " is-overflow" : "";
  cardElement.className = `preview-card${locked ? " is-locked" : ""}${overflowClass}`;
  cardElement.dataset.cardId = previewId;
  cardElement.dataset.locked = String(locked);
  if (parentThemeId) {
    cardElement.dataset.parentTheme = parentThemeId;
  }

  cardElement.innerHTML = `
    <div class="preview-card-head" title="${headTitle}">
      <h4>${renderInlineCode(displayTitle)}</h4>
      <div class="preview-card-head-actions">
        <button
          type="button"
          class="preview-head-btn icon-only"
          data-role="preview-edit-card-title"
          data-card-id="${escapeHtml(previewId)}"
          title="Edit card title"
          aria-label="Edit card title"
        >
          <span aria-hidden="true">&#9998;</span>
        </button>
        <button
          type="button"
          class="preview-head-btn icon-only"
          data-role="preview-toggle-lock"
          data-card-id="${escapeHtml(previewId)}"
          data-locked="${String(locked)}"
          title="${lockTitle}"
          aria-label="${lockAria}"
        >
          <span aria-hidden="true">${lockIcon}</span>
        </button>
        <button
          type="button"
          class="preview-head-btn danger icon-only"
          data-role="preview-delete-card"
          data-card-id="${escapeHtml(previewId)}"
          title="Remove card from cheat sheet"
          aria-label="Remove card from cheat sheet"
        >
          <span aria-hidden="true">&#10005;</span>
        </button>
        <span class="preview-drag-hint" aria-hidden="true" title="${dragHintTitle}">${dragHint}</span>
      </div>
    </div>
    <div class="preview-body">
      <p class="preview-source-title"><strong>${renderInlineCode(snippet.subtopicTitle)}</strong></p>
      ${renderPreviewSummaryBlock(previewId, snippet)}
      ${selectedPieces.map((piece) => renderPreviewPiece(previewId, snippet, selection, piece)).join("")}
    </div>
    <button type="button" class="preview-resize-bottom" data-role="preview-resize-bottom" aria-label="Resize card height"></button>
    <button type="button" class="preview-resize-corner" data-role="preview-resize-corner" aria-label="Resize card"></button>
  `;

  return cardElement;
}

function renderPreviewItemActions(previewCardId, sourceCardId, pieceId, itemType) {
  return `
    <div class="preview-item-actions">
      <button
        type="button"
        class="preview-mini-btn icon-only"
        data-role="preview-edit-item"
        data-card-id="${escapeHtml(previewCardId || "")}"
        data-source-card-id="${escapeHtml(sourceCardId || "")}"
        data-piece-id="${escapeHtml(pieceId)}"
        data-item-type="${escapeHtml(itemType || "piece")}"
        title="Edit item"
        aria-label="Edit item"
      >
        <span aria-hidden="true">&#9998;</span>
      </button>
      <button
        type="button"
        class="preview-mini-btn danger icon-only"
        data-role="preview-delete-item"
        data-card-id="${escapeHtml(previewCardId || "")}"
        data-source-card-id="${escapeHtml(sourceCardId || "")}"
        data-piece-id="${escapeHtml(pieceId)}"
        data-item-type="${escapeHtml(itemType || "piece")}"
        title="Delete item"
        aria-label="Delete item"
      >
        <span aria-hidden="true">&#10005;</span>
      </button>
    </div>
  `;
}

function renderPreviewPiece(previewCardId, snippet, selection, piece) {
  const effective = getPieceOverride(selection, piece);
  const presentation = getPiecePresentation(effective);
  const emphasis = presentation?.emphasis || "";
  return `
    <div class="preview-item-block preview-piece-block${emphasis ? ` is-${escapeHtml(emphasis)}` : ""}"${
      emphasis ? ` data-piece-emphasis="${escapeHtml(emphasis)}"` : ""
    }>
      ${renderPreviewItemActions(previewCardId, snippet.id, piece.id, piece.kind)}
      <p class="preview-piece-title">${renderPiecePresentationBadge(presentation)}<strong>${renderInlineCode(
        effective.title || piece.title
      )}</strong></p>
      ${renderMarkdownBodyBlocks(effective.bodyBlocks || [], effective.bodyMarkdown || "")}
    </div>
  `;
}

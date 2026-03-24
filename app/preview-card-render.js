function buildPreviewCard(entry, layout) {
  const { previewId, card, cards, selectionsByCard } = entry;
  const sections = [];
  const locked = Boolean(layout?.locked);
  const displayTitle = getPreviewCardTitle(entry, layout);
  const lockTitle = locked ? "Unlock card position and size" : "Lock card position and size";
  const lockAria = locked ? "Unlock card position and size" : "Lock card position and size";
  const lockIcon = locked ? "&#128275;" : "&#128274;";
  const headTitle = locked ? "Card locked: unlock to move or resize" : "Drag to move this card";
  const dragHint = locked ? "&#128274;" : "&#8942;";
  const dragHintTitle = locked ? "Card locked" : "Drag card";

  cards.forEach((sourceCard) => {
    const selection = selectionsByCard[sourceCard.id];
    if (!selection) {
      return;
    }

    getExamCardSections(sourceCard).forEach((section) => {
      const snippetBlocks = section.snippets
        .map((snippet) => renderPreviewSnippetBlock(previewId, sourceCard, selection, section, snippet))
        .filter(Boolean);

      if (snippetBlocks.length) {
        sections.push({
          label: section.title,
          content: snippetBlocks.join(""),
        });
      }
    });
  });

  if (!sections.length) {
    return null;
  }

  const sectionHtml = sections
    .map((section) => (sections.length > 1 ? `<div class="section-title">${section.label}</div>${section.content}` : section.content))
    .join("");

  const cardElement = document.createElement("article");
  cardElement.className = `preview-card${locked ? " is-locked" : ""}`;
  cardElement.dataset.cardId = previewId;
  cardElement.dataset.locked = String(locked);

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
    <div class="preview-body">${sectionHtml}</div>
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

function renderPreviewSnippetBlock(previewCardId, sourceCard, selection, section, snippet) {
  const selectedSet = new Set(selection.selected?.pieces || []);
  const selectedPieces = snippet.pieces.filter((piece) => selectedSet.has(piece.id));
  if (!selectedPieces.length) {
    return "";
  }

  return `
    <div class="preview-source-item preview-item-block">
      <p class="preview-source-title"><strong>${renderInlineCode(snippet.title)}</strong></p>
      ${snippet.snippetType === "past_exam_question" ? `<p class="preview-item-note">Past exam</p>` : ""}
      ${selectedPieces.map((piece) => renderPreviewPiece(previewCardId, sourceCard, selection, section, snippet, piece)).join("")}
    </div>
  `;
}

function renderPreviewPiece(previewCardId, sourceCard, selection, section, snippet, piece) {
  const effective = getPieceOverride(selection, piece);
  return `
    <div class="preview-item-block preview-piece-block">
      ${renderPreviewItemActions(previewCardId, sourceCard.id, piece.id, piece.pieceType)}
      <p class="preview-piece-title"><strong>${renderInlineCode(effective.title || piece.title)}</strong></p>
      ${renderPreviewPieceBody(effective)}
    </div>
  `;
}

function renderPreviewPieceBody(piece) {
  const content = piece.content || {};

  if (piece.pieceType === "reference_table") {
    const text = String(content.text || "").trim();
    const table = {
      headers: Array.isArray(content.headers) ? content.headers : [],
      rows: Array.isArray(content.rows) ? content.rows : [],
    };
    return `
      ${text ? `<p>${renderInlineCode(text)}</p>` : ""}
      ${table.headers.length && table.rows.length ? renderPreviewTable(table) : ""}
    `;
  }

  if (piece.pieceType === "code_example") {
    return `
      ${content.text ? `<p>${renderInlineCode(content.text)}</p>` : ""}
      ${content.code ? renderCodeBlock(content.code) : ""}
      ${content.output ? `<p><strong>Output:</strong></p>${renderOutputBlock(content.output)}` : ""}
    `;
  }

  if (piece.pieceType === "past_exam_piece") {
    return `
      ${renderQuestionContent(content.question || "", content.code_context || "")}
      ${renderOptions(content.options || {})}
      ${content.correct ? `<p class="answer-chip">Correct: ${escapeHtml(String(content.correct).toUpperCase())}</p>` : ""}
      ${content.explanation ? `<p>${renderInlineCode(content.explanation)}</p>` : ""}
    `;
  }

  const text = normalizeTruncatedDisplayText(String(content.text || "").trim());
  return text ? `<p>${renderInlineCode(text)}</p>` : "";
}

function renderPreviewTable(table) {
  const headHtml = table.headers.map((header) => `<th>${renderInlineCode(header)}</th>`).join("");
  const rowsHtml = table.rows
    .map((row) => `<tr>${row.map((cell) => `<td>${renderInlineCode(cell)}</td>`).join("")}</tr>`)
    .join("");

  return `
    <div class="preview-table-wrap">
      <table class="preview-table">
        <thead><tr>${headHtml}</tr></thead>
        <tbody>${rowsHtml}</tbody>
      </table>
    </div>
  `;
}

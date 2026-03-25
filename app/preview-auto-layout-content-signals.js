function getSelectedPiecesForEntry(entry) {
  const snippet = entry?.snippet;
  if (!snippet || !Array.isArray(snippet.pieces)) {
    return [];
  }
  const selection = entry.selectionsByCard?.[snippet.id] || {};
  const selectedSet = new Set(selection?.selected?.pieces || []);
  return snippet.pieces.filter((piece) => selectedSet.size === 0 || selectedSet.has(piece.id));
}

function getAutoEntryContentStats(entry) {
  const pieces = getSelectedPiecesForEntry(entry);
  const stats = {
    pieceCount: pieces.length,
    blockCount: 0,
    codeBlockCount: 0,
    tableBlockCount: 0,
    maxCodeLineLength: 0,
    maxTableColumns: 0,
    longestTokenLength: 0,
    textChars: 0,
  };

  const updateLongestToken = (text) => {
    const tokens = String(text || "").split(/\s+/).map((token) => token.trim()).filter(Boolean);
    tokens.forEach((token) => {
      stats.longestTokenLength = Math.max(stats.longestTokenLength, token.length);
    });
  };

  pieces.forEach((piece) => {
    const title = String(piece?.title || "");
    stats.textChars += title.length;
    updateLongestToken(title);
    const bodyMarkdown = String(piece?.bodyMarkdown || "").trim();
    const blocks = Array.isArray(piece?.bodyBlocks) && piece.bodyBlocks.length ? piece.bodyBlocks : compileMarkdownBodyBlocks(bodyMarkdown);
    if (!blocks.length) {
      stats.textChars += bodyMarkdown.length;
      updateLongestToken(bodyMarkdown);
      return;
    }

    blocks.forEach((block) => {
      stats.blockCount += 1;
      if (block?.type === "code") {
        stats.codeBlockCount += 1;
        const lines = String(block.code || "").replace(/\r\n/g, "\n").split("\n");
        lines.forEach((line) => {
          const lineValue = String(line || "");
          stats.maxCodeLineLength = Math.max(stats.maxCodeLineLength, lineValue.length);
          stats.textChars += lineValue.length;
          updateLongestToken(lineValue);
        });
        return;
      }
      if (block?.type === "table") {
        stats.tableBlockCount += 1;
        const headers = Array.isArray(block.headers) ? block.headers : [];
        const rows = Array.isArray(block.rows) ? block.rows : [];
        const rowWidths = rows.map((row) => (Array.isArray(row) ? row.length : 0));
        stats.maxTableColumns = Math.max(stats.maxTableColumns, headers.length, ...rowWidths, 0);
        headers.forEach((cell) => {
          const cellText = String(cell || "");
          stats.textChars += cellText.length;
          updateLongestToken(cellText);
        });
        rows.forEach((row) => {
          if (!Array.isArray(row)) {
            return;
          }
          row.forEach((cell) => {
            const cellText = String(cell || "");
            stats.textChars += cellText.length;
            updateLongestToken(cellText);
          });
        });
        return;
      }
      if (block?.type === "list") {
        const items = Array.isArray(block.items) ? block.items : [];
        items.forEach((item) => {
          const itemText = String(item || "");
          stats.textChars += itemText.length;
          updateLongestToken(itemText);
        });
        return;
      }
      if (block?.type === "paragraph") {
        const paragraph = String(block.text || "");
        stats.textChars += paragraph.length;
        updateLongestToken(paragraph);
      }
    });
  });

  return stats;
}

function estimatePreferredCardSpan(entry, pageState, maxSpan = AUTO_MAX_CARD_SPAN) {
  if (!pageState || pageState.columns <= 1) {
    return 1;
  }
  const stats = getAutoEntryContentStats(entry);
  const safeMaxSpan = clamp(Math.floor(Number(maxSpan) || 1), 1, pageState.columns);
  let desiredWidth = pageState.columnWidth;

  if (stats.codeBlockCount > 0) {
    const codeWidthNeed = 84 + stats.maxCodeLineLength * 4.1;
    desiredWidth = Math.max(desiredWidth, codeWidthNeed);
  }
  if (stats.tableBlockCount > 0) {
    const tableWidthNeed = 88 + stats.maxTableColumns * 64;
    desiredWidth = Math.max(desiredWidth, tableWidthNeed);
  }
  if (stats.longestTokenLength > 20) {
    const tokenWidthNeed = 90 + stats.longestTokenLength * 3.2;
    desiredWidth = Math.max(desiredWidth, tokenWidthNeed);
  }

  const spanRaw = (desiredWidth + pageState.gap) / Math.max(1, pageState.columnWidth + pageState.gap);
  let span = clamp(Math.round(spanRaw), 1, safeMaxSpan);
  if (span > 1 && stats.codeBlockCount === 0 && stats.tableBlockCount === 0 && stats.longestTokenLength < 28) {
    span = 1;
  }
  return span;
}

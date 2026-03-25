const AUTO_LAYOUT_TARGET_OCCUPIED_RATIO = 0.45;
const AUTO_CARD_EXTREME_HEIGHT_RATIO = 0.78;
const AUTO_RESIZE_ROOM_PX = 64;
const AUTO_MIN_CARD_HEIGHT_PX = 130;
const AUTO_MAX_CARD_SPAN = 3;

function getAutoGridGap() {
  return clamp(Number(state.layout.cardGap) || 0, 0, 24);
}

function getAutoHeightCapForPage(pageState) {
  if (!pageState || !Number.isFinite(pageState.pageHeight)) {
    return AUTO_MIN_CARD_HEIGHT_PX;
  }

  const absoluteCap = Math.floor(pageState.pageHeight * AUTO_CARD_EXTREME_HEIGHT_RATIO);
  const minHeadroom = Math.max(AUTO_RESIZE_ROOM_PX, Math.max(1, Math.floor(pageState.pageHeight * 0.07)));
  const roomCap = Math.max(1, pageState.pageHeight - minHeadroom);
  return Math.max(AUTO_MIN_CARD_HEIGHT_PX, Math.min(absoluteCap, roomCap));
}

function getAutoCappedHeight(rawHeight, pageState, fallback) {
  const cap = Number.isFinite(Number(fallback)) ? Math.max(AUTO_MIN_CARD_HEIGHT_PX, Number(fallback)) : getAutoHeightCapForPage(pageState);
  return clamp(Math.round(rawHeight), AUTO_MIN_CARD_HEIGHT_PX, cap);
}

function getAutoPageState(page, columns, gap) {
  const safeColumns = Math.max(1, Math.floor(Number(columns) || 1));
  const pageSize = getPreviewPageSize(page);
  const usableWidth = Math.max(0, pageSize.width - gap * Math.max(0, safeColumns - 1));
  const columnWidth = Math.max(1, Math.floor(usableWidth / safeColumns));
  const columnIntervals = Array.from({ length: safeColumns }, () => []);

  return {
    page,
    pageWidth: pageSize.width,
    pageHeight: pageSize.height,
    columns: safeColumns,
    gap,
    columnWidth,
    columnIntervals,
  };
}

function getAutoCardWidthForSpan(pageState, span) {
  const safeSpan = clamp(Math.floor(Number(span) || 1), 1, pageState.columns);
  return Math.max(1, Math.round(pageState.columnWidth * safeSpan + pageState.gap * Math.max(0, safeSpan - 1)));
}

function getAutoColumnsForRect(pageState, layout) {
  const result = [];
  const x1 = layout.x;
  const x2 = layout.x + layout.width;

  for (let col = 0; col < pageState.columns; col += 1) {
    const colX = col * (pageState.columnWidth + pageState.gap);
    const colX2 = colX + pageState.columnWidth;
    if (x1 < colX2 && x2 > colX) {
      result.push(col);
    }
  }

  return result;
}

function addInterval(intervals, nextStart, nextEnd, pageHeight, gap) {
  const start = clamp(Number(nextStart), 0, pageHeight);
  const end = clamp(Number(nextEnd), 0, pageHeight);
  if (end <= start) {
    return intervals;
  }

  const paddedEnd = clamp(end + gap, 0, pageHeight);
  const merged = [...intervals, [start, paddedEnd]].sort((a, b) => a[0] - b[0]);
  intervals.length = 0;

  for (let i = 0; i < merged.length; i += 1) {
    const current = merged[i];
    const last = intervals[intervals.length - 1];
    if (!last || current[0] > last[1]) {
      intervals.push(current);
    } else {
      last[1] = Math.max(last[1], current[1]);
    }
  }

  return intervals;
}

function findFirstYInIntervals(intervals, pageHeight, height) {
  const maxY = pageHeight - Math.max(1, height);
  let cursorY = 0;

  for (let i = 0; i < intervals.length; i += 1) {
    const [start, end] = intervals[i];
    const candidateY = Math.min(cursorY, start);
    if (candidateY + height <= start) {
      return candidateY;
    }
    cursorY = Math.max(cursorY, end);
    if (cursorY > maxY) {
      return null;
    }
  }

  if (cursorY + height <= pageHeight) {
    return cursorY;
  }
  return null;
}

function mergeSortedIntervals(intervals) {
  if (!intervals.length) {
    return [];
  }
  const merged = [[intervals[0][0], intervals[0][1]]];
  for (let i = 1; i < intervals.length; i += 1) {
    const current = intervals[i];
    const last = merged[merged.length - 1];
    if (current[0] <= last[1]) {
      last[1] = Math.max(last[1], current[1]);
    } else {
      merged.push([current[0], current[1]]);
    }
  }
  return merged;
}

function getMergedIntervalsForSpan(pageState, startCol, span) {
  const safeSpan = clamp(Math.floor(Number(span) || 1), 1, pageState.columns);
  const start = clamp(Math.floor(Number(startCol) || 0), 0, Math.max(0, pageState.columns - safeSpan));
  const intervals = [];
  for (let col = start; col < start + safeSpan; col += 1) {
    const colIntervals = pageState.columnIntervals[col] || [];
    for (let i = 0; i < colIntervals.length; i += 1) {
      intervals.push([colIntervals[i][0], colIntervals[i][1]]);
    }
  }
  if (!intervals.length) {
    return [];
  }
  intervals.sort((a, b) => a[0] - b[0]);
  return mergeSortedIntervals(intervals);
}

function findFirstYForSpan(pageState, startCol, span, height) {
  const intervals = getMergedIntervalsForSpan(pageState, startCol, span);
  return findFirstYInIntervals(intervals, pageState.pageHeight, height);
}

function getMaxOccupiedBottomForSpan(pageState, startCol, span) {
  const intervals = getMergedIntervalsForSpan(pageState, startCol, span);
  if (!intervals.length) {
    return 0;
  }
  return intervals[intervals.length - 1][1];
}

function reservePageIntervalForCard(pageState, layout) {
  const columnIndices = getAutoColumnsForRect(pageState, layout);
  if (!columnIndices.length) {
    return;
  }

  for (let i = 0; i < columnIndices.length; i += 1) {
    const col = columnIndices[i];
    const intervals = pageState.columnIntervals[col];
    if (!intervals) {
      continue;
    }
    addInterval(intervals, layout.y, layout.y + layout.height, pageState.pageHeight, pageState.gap);
  }
}

function getAutoPlacementCandidate(pageState, cardHeight, options = {}) {
  const span = clamp(Math.floor(Number(options.span) || 1), 1, pageState.columns);
  const fallbackHeightRef = Number.isFinite(Number(options.fallbackHeightRef)) ? Number(options.fallbackHeightRef) : null;
  let best = null;

  for (let col = 0; col <= pageState.columns - span; col += 1) {
    const y = findFirstYForSpan(pageState, col, span, cardHeight);
    if (y !== null) {
      const candidate = {
        page: pageState.page,
        x: Math.round(col * (pageState.columnWidth + pageState.gap)),
        y: Math.round(y),
        width: getAutoCardWidthForSpan(pageState, span),
        height: Math.round(cardHeight),
        z: 0,
      };
      if (
        !best ||
        candidate.y < best.y ||
        (candidate.y === best.y && (col < best.col || (col === best.col && span < best.span)))
      ) {
        best = { ...candidate, col, span };
      }
      continue;
    }

    if (fallbackHeightRef !== null) {
      const occupiedBottom = getMaxOccupiedBottomForSpan(pageState, col, span);
      const remaining = Math.max(0, pageState.pageHeight - occupiedBottom);
      if (remaining <= 0) {
        continue;
      }
      const height = Math.min(fallbackHeightRef, remaining);
      if (height < 1) {
        continue;
      }
      const candidate = {
        page: pageState.page,
        x: Math.round(col * (pageState.columnWidth + pageState.gap)),
        y: Math.round(occupiedBottom),
        width: getAutoCardWidthForSpan(pageState, span),
        height: Math.round(height),
        z: 0,
      };
      if (
        !best ||
        candidate.y < best.y ||
        (candidate.y === best.y && (col < best.col || (col === best.col && span < best.span)))
      ) {
        best = { ...candidate, col, span, isOverflow: true };
      }
    }
  }

  return best;
}

function estimateTextLines(text, width, fontPx, fallbackLineHeight) {
  const value = String(text || "").trim();
  if (!value) {
    return 0;
  }
  const normalized = sanitizeDisplayText(value).replace(/\s+/g, " ");
  const avgCharWidth = Math.max(1.8, fontPx * 0.55);
  const charsPerLine = Math.max(12, Math.floor(Math.max(6, width) / avgCharWidth));
  const lineCount = Math.max(1, Math.ceil(normalized.length / charsPerLine));
  return lineCount * Math.max(1, fallbackLineHeight);
}

function estimateWrappedLineCountFromWidths(lines, maxCharsPerLine) {
  if (!Array.isArray(lines) || !lines.length) {
    return 1;
  }
  let wrapped = 0;
  const safeChars = Math.max(6, Math.floor(maxCharsPerLine));
  lines.forEach((line) => {
    const value = String(line || "");
    wrapped += Math.max(1, Math.ceil(Math.max(1, value.length) / safeChars));
  });
  return Math.max(1, wrapped);
}

function estimateBlockHeight(block, width, metrics) {
  if (!block || typeof block !== "object") {
    return 0;
  }
  if (block.type === "paragraph") {
    return estimateTextLines(block.text, width, metrics.bodyFont, metrics.lineHeightScale) * metrics.linePx;
  }

  if (block.type === "list") {
    const items = Array.isArray(block.items) ? block.items : [];
    if (!items.length) {
      return metrics.pieceGap + metrics.linePx;
    }

    let listLines = 0;
    items.forEach((item) => {
      const itemText = String(item || "").trim();
      if (!itemText) {
        return;
      }
      listLines += estimateTextLines(` ${itemText}`, width - 24, metrics.bodyFont, metrics.lineHeightScale);
    });

    return listLines * metrics.linePx + metrics.pieceGap * 1.2;
  }

  if (block.type === "code") {
    const source = String(block.code || "").replace(/\r\n/g, "\n");
    const sourceLines = source.trim() ? source.split("\n") : [""];
    const innerWidth = Math.max(24, width - metrics.codeBlockPadding * 2 - 6);
    const codeAvgCharWidth = Math.max(2.4, metrics.codeFont * 0.58);
    const codeCharsPerLine = Math.max(8, Math.floor(innerWidth / codeAvgCharWidth));
    const wrappedCodeLines = estimateWrappedLineCountFromWidths(sourceLines, codeCharsPerLine);
    return wrappedCodeLines * metrics.codeLinePx + metrics.codeBlockPadding * 2 + 4;
  }

  if (block.type === "table") {
    const headers = Array.isArray(block.headers) ? block.headers : [];
    const rows = Array.isArray(block.rows) ? block.rows : [];
    const columnCount = Math.max(headers.length, ...rows.map((row) => (Array.isArray(row) ? row.length : 0)), 1);
    const tableInnerWidth = Math.max(40, width - metrics.tablePadding * 2);
    const columnWidth = Math.max(14, tableInnerWidth / columnCount);
    const tableCharWidth = Math.max(2, metrics.tableFont * 0.55);
    const charsPerCellLine = Math.max(6, Math.floor(columnWidth / tableCharWidth));
    const estimateRowLines = (row) => {
      if (!Array.isArray(row) || !row.length) {
        return 1;
      }
      let maxLines = 1;
      row.forEach((cell) => {
        const cellText = sanitizeDisplayText(String(cell || "")).replace(/\s+/g, " ").trim();
        if (!cellText) {
          return;
        }
        maxLines = Math.max(maxLines, Math.ceil(cellText.length / charsPerCellLine));
      });
      return maxLines;
    };

    let totalRowLines = 0;
    if (headers.length) {
      totalRowLines += estimateRowLines(headers);
    }
    rows.forEach((row) => {
      totalRowLines += estimateRowLines(row);
    });
    totalRowLines = Math.max(1, totalRowLines);
    return totalRowLines * metrics.tableLinePx + metrics.tablePadding * 2;
  }

  return 0;
}

function estimateCardHeight(entry, cardWidth) {
  const contentWidth = Math.max(40, cardWidth - Number(state.layout.cardPadding || 5) * 2);
  const metrics = {
    bodyFont: Number(state.layout.fontSize) || 8.5,
    lineHeightScale: Number(state.layout.lineHeight) || 1.0,
    linePx: Math.max(6, (Number(state.layout.fontSize) || 8.5) * (Number(state.layout.lineHeight) || 1.0)),
    pieceFont: Number(state.layout.fontSize) || 8.5,
    pieceGap: Number(state.layout.pieceGap) || 2,
    codeFont: Math.max(6, (Number(state.layout.fontSize) || 8.5) * 0.8),
    codeLinePx: Math.max(6, (Number(state.layout.fontSize) || 8.5) * 0.8 * 1.34),
    codeBlockPadding: Number(state.layout.codeBlockPadding) || 4,
    tableFont: Number(state.layout.tableSize) || 7,
    tableLinePx: Math.max(6, (Number(state.layout.tableSize) || 7) * 1.22),
    tablePadding: Number(state.layout.cardPadding) || 5,
    summaryFontScale: 0.79,
    noteLineHeightScale: Number(state.layout.lineHeight) || 1.0,
  };

  const snippet = entry.snippet;
  const pieces = getSelectedPiecesForEntry(entry);

  let estimated = 0;
  const headerHeight = Math.max(6, Number(state.layout.titleSize) || 9.5);

  estimated += metrics.linePx;
  estimated += headerHeight + metrics.pieceGap;

  if (String(snippet.summary || "").trim()) {
    const summaryLines = estimateTextLines(snippet.summary, contentWidth, metrics.bodyFont * metrics.summaryFontScale, metrics.noteLineHeightScale);
    estimated += summaryLines * Math.max(5, metrics.bodyFont * metrics.summaryFontScale * metrics.noteLineHeightScale) + metrics.pieceGap;
  }

  if (String(snippet.subtopicTitle || "").trim()) {
    const title = estimateTextLines(snippet.subtopicTitle, contentWidth, metrics.bodyFont, metrics.lineHeightScale);
    estimated += title * Math.max(5, metrics.bodyFont * metrics.lineHeightScale) + metrics.pieceGap;
  }

  pieces.forEach((piece) => {
    const bodyMarkdown = String(piece.bodyMarkdown || "").trim();
    const blocks = Array.isArray(piece.bodyBlocks) && piece.bodyBlocks.length ? piece.bodyBlocks : compileMarkdownBodyBlocks(bodyMarkdown);

    const pieceTitle = `${piece.title || ""}`;
    if (pieceTitle) {
      const pieceTitleLines = estimateTextLines(pieceTitle, contentWidth, metrics.pieceFont, metrics.lineHeightScale);
      estimated += pieceTitleLines * Math.max(4, metrics.pieceFont * metrics.lineHeightScale) + metrics.pieceGap;
    }

    if (!blocks.length) {
      const fallbackLines = estimateTextLines(bodyMarkdown, contentWidth, metrics.bodyFont, metrics.lineHeightScale);
      estimated += fallbackLines * Math.max(4, metrics.bodyFont * metrics.lineHeightScale);
      return;
    }

    blocks.forEach((block) => {
      estimated += estimateBlockHeight(block, contentWidth, metrics);
    });
  });

  estimated += Number(state.layout.cardPadding) * 2;

  if (!pieces.length) {
    estimated = Math.max(estimated, 130);
  }

  return Math.max(130, Math.round(estimated));
}

function getAutoColumnIndexForLayout(pageState, layout) {
  const columns = getAutoColumnsForRect(pageState, layout);
  return columns.length === 1 ? columns[0] : -1;
}

function collectAutoColumnCards(pageState, layoutPlan) {
  const columns = Array.from({ length: pageState.columns }, () => []);
  layoutPlan.forEach((item, cardId) => {
    if (!item?.layout || item.isLocked || item.overflow) {
      return;
    }
    const layout = item.layout;
    if (layout.page !== pageState.page) {
      return;
    }
    const col = getAutoColumnIndexForLayout(pageState, layout);
    if (col < 0) {
      return;
    }
    columns[col].push({
      cardId,
      layout,
    });
  });

  columns.forEach((cards) => cards.sort((a, b) => a.layout.y - b.layout.y || a.layout.x - b.layout.x));

  return columns;
}

function getEffectiveGridSettings(totalCards) {
  if (!state.layout.autoGrid) {
    return {
      columns: state.layout.gridColumns,
      rows: state.layout.gridRows,
    };
  }

  let columns = 1;
  if (totalCards > 24) {
    columns = 4;
  } else if (totalCards > 12) {
    columns = 3;
  } else if (totalCards > 5) {
    columns = 2;
  }

  if (state.layout.fontSize >= 11.5) {
    columns = Math.max(1, columns - 1);
  }
  if (state.layout.fontSize <= 8.5) {
    columns = Math.min(4, columns + 1);
  }

  let rows = Math.ceil(Math.max(1, totalCards) / (2 * columns));
  rows = clamp(rows, 3, 14);

  if (state.layout.lineHeight <= 1.0 && rows < 14) {
    rows += 1;
  }
  if (state.layout.lineHeight >= 1.35 && rows > 3) {
    rows -= 1;
  }

  return {
    columns,
    rows,
  };
}

function getDefaultPreviewLayout(index, grid) {
  const columns = Math.max(1, Number(grid.columns) || 1);
  const rows = Math.max(1, Number(grid.rows) || 1);
  const capacityPerPage = columns * rows;
  const page = index < capacityPerPage ? 1 : 2;
  const localIndex = index % capacityPerPage;
  const col = localIndex % columns;
  const row = Math.floor(localIndex / columns);

  const pageSize = getPreviewPageSize(page);
  const gap = clamp(Number(state.layout.cardGap) || 0, 0, 24);
  const cellWidth = (pageSize.width - gap * (columns - 1)) / columns;
  const cellHeight = (pageSize.height - gap * (rows - 1)) / rows;

  return {
    page,
    x: Math.round(col * (cellWidth + gap)),
    y: Math.round(row * (cellHeight + gap)),
    width: Math.round(cellWidth),
    height: Math.round(cellHeight),
    z: index + 1,
  };
}

function renderPreview() {
  syncPreviewUndoAvailability();
  refs.page1Content.innerHTML = "";
  refs.page2Content.innerHTML = "";
  refs.page1Content.classList.remove("is-empty");
  refs.page2Content.classList.remove("is-empty");
  refs.previewOrderList.innerHTML = "";

  const previewEntries = buildMergedPreviewEntries();
  state.previewEntries = Object.fromEntries(previewEntries.map((entry) => [entry.previewId, entry]));

  previewEntries.forEach((entry) => {
    const li = document.createElement("li");
    li.textContent = `${entry.snippet.title} · ${entry.snippet.subtopicTitle}`;
    refs.previewOrderList.appendChild(li);
  });

  const previewCardCount = previewEntries.length;
  const grid = getEffectiveGridSettings(previewCardCount);
  const capacityPerPage = Math.max(1, grid.columns * grid.rows);

  if (!previewCardCount) {
    state.previewEntries = {};
    prunePreviewCardLayouts(new Set());
    refs.page1Content.classList.add("is-empty");
    refs.page2Content.classList.add("is-empty");
    refs.page1Content.innerHTML = `<div class="empty-state"><p>No selected content yet.</p><p>Choose exact snippet pieces in the topic explorer before opening Preview & Export.</p></div>`;
    refs.page2Content.innerHTML = `<div class="empty-state"><p>Page 2 is empty.</p></div>`;
    refs.overflowNotice.classList.add("hidden");
    syncGridControls(grid);
    schedulePersistState();
    syncPreviewUndoAvailability();
    return;
  }

  const validCardIds = new Set(previewEntries.map((entry) => entry.previewId));
  prunePreviewCardLayouts(validCardIds);

  previewEntries.forEach((entry, index) => {
    const fallback = getDefaultPreviewLayout(index, grid);
    const layout = ensurePreviewCardLayout(entry.previewId, fallback);
    const cardElement = buildPreviewCard(entry, layout);
    if (!cardElement) {
      return;
    }
    applyPreviewCardLayout(cardElement, layout);
    getPreviewPageContent(layout.page).appendChild(cardElement);
  });

  if (!refs.page1Content.querySelector(".preview-card")) {
    refs.page1Content.classList.add("is-empty");
    refs.page1Content.innerHTML = `<div class="empty-state"><p>Page 1 is empty.</p></div>`;
  }
  if (!refs.page2Content.querySelector(".preview-card")) {
    refs.page2Content.classList.add("is-empty");
    refs.page2Content.innerHTML = `<div class="empty-state"><p>Page 2 is empty.</p></div>`;
  }

  const overflowCards = Math.max(0, previewCardCount - capacityPerPage * 2);
  if (overflowCards > 0) {
    refs.overflowNotice.classList.remove("hidden");
    refs.overflowNotice.textContent = `${overflowCards} selected snippet card(s) exceed the default grid. They were added on page 2 and may overlap; drag or resize to arrange.`;
  } else {
    refs.overflowNotice.classList.add("hidden");
  }

  syncGridControls(grid);
  schedulePersistState();
  syncPreviewUndoAvailability();
}

function syncGridControls(effectiveGrid) {
  refs.autoGridToggle.checked = state.layout.autoGrid;
  refs.gridColumnsRange.disabled = state.layout.autoGrid;
  refs.gridRowsRange.disabled = state.layout.autoGrid;
  refs.gridColumnsRange.value = String(state.layout.gridColumns);
  refs.gridRowsRange.value = String(state.layout.gridRows);
  refs.gridColumnsValue.textContent = state.layout.autoGrid ? `${effectiveGrid.columns} (auto)` : String(state.layout.gridColumns);
  refs.gridRowsValue.textContent = state.layout.autoGrid ? `${effectiveGrid.rows} (auto)` : String(state.layout.gridRows);
}

function buildMergedPreviewEntries() {
  return getSelectedPreviewEntries()
    .map(({ snippet, selection }) => ({
      previewId: snippet.id,
      card: snippet,
      snippet,
      selectionsByCard: {
        [snippet.id]: selection,
      },
    }))
    .sort((a, b) => {
      if (a.snippet.topicTitle !== b.snippet.topicTitle) {
        return a.snippet.topicTitle.localeCompare(b.snippet.topicTitle);
      }
      if (a.snippet.subtopicTitle !== b.snippet.subtopicTitle) {
        return a.snippet.subtopicTitle.localeCompare(b.snippet.subtopicTitle);
      }
      return a.snippet.sortOrder - b.snippet.sortOrder || a.snippet.title.localeCompare(b.snippet.title);
    });
}

function getPreviewCardTitle(entry, layout) {
  const manualTitle = String(layout?.title || "").trim();
  if (manualTitle) {
    return manualTitle;
  }
  return derivePreviewCardTitle(entry);
}

function derivePreviewCardTitle(entry) {
  return summarizePreviewLabel(entry.snippet.title, entry.snippet.title);
}

function summarizePreviewLabel(text, fallback) {
  const plain = sanitizeDisplayText(text || "").replace(/`/g, "").replace(/\s+/g, " ").trim();
  if (!plain) {
    return fallback;
  }
  return plain.length > 52 ? `${plain.slice(0, 52).replace(/\s+\S*$/, "").trim()}…` : plain;
}

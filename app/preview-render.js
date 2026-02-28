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
  state.acceptedOrder.forEach((cardId) => {
    const card = state.cards.find((entry) => entry.id === cardId);
    if (!card) {
      return;
    }
    const li = document.createElement("li");
    li.textContent = humanizeTopic(card.topic);
    refs.previewOrderList.appendChild(li);
  });

  const acceptedCards = state.acceptedOrder
    .map((id) => state.cards.find((card) => card.id === id))
    .filter((card) => card && state.decisions[card.id]?.status === "accepted");

  const grid = getEffectiveGridSettings(acceptedCards.length);
  const capacityPerPage = Math.max(1, grid.columns * grid.rows);

  if (!acceptedCards.length) {
    prunePreviewCardLayouts(new Set());
    refs.page1Content.classList.add("is-empty");
    refs.page2Content.classList.add("is-empty");
    refs.page1Content.innerHTML = `<div class="empty-state"><p>No accepted topics yet.</p><p>Go to Swipe Mode and add cards first.</p></div>`;
    refs.page2Content.innerHTML = `<div class="empty-state"><p>Page 2 is empty.</p></div>`;
    refs.overflowNotice.classList.add("hidden");
    syncGridControls(grid);
    schedulePersistState();
    syncPreviewUndoAvailability();
    return;
  }

  const validCardIds = new Set(acceptedCards.map((card) => card.id));
  prunePreviewCardLayouts(validCardIds);

  let renderedCount = 0;
  acceptedCards.forEach((card, index) => {
    const selection = state.decisions[card.id]?.selection;
    if (!selection) {
      return;
    }
    const fallback = getDefaultPreviewLayout(index, grid);
    const layout = ensurePreviewCardLayout(card.id, fallback);
    const cardElement = buildPreviewCard(card, selection, layout);
    applyPreviewCardLayout(cardElement, layout);
    const pageContent = getPreviewPageContent(layout.page);
    pageContent.appendChild(cardElement);
    renderedCount += 1;
  });

  if (!renderedCount) {
    refs.page1Content.classList.add("is-empty");
    refs.page2Content.classList.add("is-empty");
    refs.page1Content.innerHTML = `<div class="empty-state"><p>No accepted topics yet.</p><p>Go to Swipe Mode and add cards first.</p></div>`;
    refs.page2Content.innerHTML = `<div class="empty-state"><p>Page 2 is empty.</p></div>`;
    refs.overflowNotice.classList.add("hidden");
    syncGridControls(grid);
    schedulePersistState();
    syncPreviewUndoAvailability();
    return;
  }

  if (!refs.page1Content.querySelector(".preview-card")) {
    refs.page1Content.classList.add("is-empty");
    refs.page1Content.innerHTML = `<div class="empty-state"><p>Page 1 is empty.</p></div>`;
  }
  if (!refs.page2Content.querySelector(".preview-card")) {
    refs.page2Content.classList.add("is-empty");
    refs.page2Content.innerHTML = `<div class="empty-state"><p>Page 2 is empty.</p></div>`;
  }

  const overflowCards = Math.max(0, acceptedCards.length - capacityPerPage * 2);
  if (overflowCards > 0) {
    refs.overflowNotice.classList.remove("hidden");
    refs.overflowNotice.textContent = `${overflowCards} topic(s) exceed the default grid. They were added on page 2 and may overlap; drag/resize to arrange.`;
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

  refs.gridColumnsValue.textContent = state.layout.autoGrid
    ? `${effectiveGrid.columns} (auto)`
    : String(state.layout.gridColumns);
  refs.gridRowsValue.textContent = state.layout.autoGrid
    ? `${effectiveGrid.rows} (auto)`
    : String(state.layout.gridRows);
}

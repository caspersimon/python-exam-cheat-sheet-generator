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

  const autoPlan = state.layout.autoGrid ? buildAutoPreviewLayoutPlan(previewEntries, grid) : null;
  let overflowCardCount = 0;
  const entryIndexById = new Map(previewEntries.map((entry, index) => [entry.previewId, index]));
  const renderEntries = state.layout.autoGrid
    ? [...previewEntries].sort((a, b) => {
      const planA = autoPlan?.layoutPlan?.get(a.previewId);
      const planB = autoPlan?.layoutPlan?.get(b.previewId);
      const layoutA = planA?.layout;
      const layoutB = planB?.layout;

      if (layoutA && layoutB) {
        if (layoutA.page !== layoutB.page) {
          return layoutA.page - layoutB.page;
        }
        if (layoutA.y !== layoutB.y) {
          return layoutA.y - layoutB.y;
        }
        if (layoutA.x !== layoutB.x) {
          return layoutA.x - layoutB.x;
        }
        return (layoutA.z || 0) - (layoutB.z || 0);
      }

      if (!layoutA && !layoutB) {
        return (entryIndexById.get(a.previewId) || 0) - (entryIndexById.get(b.previewId) || 0);
      }
      if (!layoutA) {
        return 1;
      }
      return -1;
    })
    : previewEntries;

  renderEntries.forEach((entry) => {
    const isAuto = Boolean(state.layout.autoGrid);
    const index = entryIndexById.get(entry.previewId) || 0;
    const fallback = getDefaultPreviewLayout(index, grid);
    const autoCardPlan = isAuto ? autoPlan?.layoutPlan?.get(entry.previewId) : null;
    let layout;

    if (isAuto) {
      layout = autoPlan?.layoutPlan.get(entry.previewId)?.layout;
      if (!layout) {
        layout = ensurePreviewCardLayout(entry.previewId, fallback, { force: true, sanitizeOptions: { minHeight: MIN_PREVIEW_CARD_HEIGHT } });
      }
      if (autoCardPlan?.overflow) {
        overflowCardCount += 1;
      }
    } else {
      layout = ensurePreviewCardLayout(entry.previewId, fallback, { force: false });
    }

    const cardElement = buildPreviewCard(entry, layout, Boolean(autoCardPlan?.overflow));
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

  if (overflowCardCount > 0) {
    refs.overflowNotice.classList.remove("hidden");
    refs.overflowNotice.textContent = `${overflowCardCount} selected snippet card(s) overflowed the two-page auto-pack layout. They were placed page-2-first with reduced fit. Densest cards may keep internal body scroll for full content.`;
  } else {
    refs.overflowNotice.classList.add("hidden");
  }

  syncGridControls(grid);
  schedulePersistState();
  syncPreviewUndoAvailability();
}

function syncGridControls(effectiveGrid) {
  if (refs.autoGridToggle) {
    refs.autoGridToggle.checked = Boolean(state.layout.autoGrid);
  }
  if (refs.gridColumnsRange) {
    refs.gridColumnsRange.disabled = false;
    refs.gridColumnsRange.value = String(state.layout.gridColumns);
  }
  if (refs.gridRowsRange) {
    refs.gridRowsRange.disabled = false;
    refs.gridRowsRange.value = String(state.layout.gridRows);
  }
  if (refs.gridColumnsValue) {
    refs.gridColumnsValue.textContent = String(state.layout.gridColumns);
  }
  if (refs.gridRowsValue) {
    refs.gridRowsValue.textContent = String(state.layout.gridRows);
  }
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

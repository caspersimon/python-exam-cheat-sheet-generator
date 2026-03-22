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
    li.textContent = `${humanizeTopic(entry.card.topic)}${entry.cards.length > 1 ? ` ×${entry.cards.length}` : ""}`;
    refs.previewOrderList.appendChild(li);
  });

  const previewTopicCount = previewEntries.length;
  const grid = getEffectiveGridSettings(previewTopicCount);
  const capacityPerPage = Math.max(1, grid.columns * grid.rows);

  if (!previewTopicCount) {
    state.previewEntries = {};
    prunePreviewCardLayouts(new Set());
    refs.page1Content.classList.add("is-empty");
    refs.page2Content.classList.add("is-empty");
    refs.page1Content.innerHTML = `<div class="empty-state"><p>No selected content yet.</p><p>Choose specific items in Topic Explorer before opening Preview & Export.</p></div>`;
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

  const overflowCards = Math.max(0, previewTopicCount - capacityPerPage * 2);
  if (overflowCards > 0) {
    refs.overflowNotice.classList.remove("hidden");
    refs.overflowNotice.textContent = `${overflowCards} selected topic card(s) exceed the default grid. They were added on page 2 and may overlap; drag/resize to arrange.`;
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
  const groups = new Map();

  getSelectedPreviewEntries().forEach(({ card, selection }) => {
    const key = normalizeTopicMergeKey(card);
    if (!groups.has(key)) {
      groups.set(key, {
        key,
        previewId: card.id,
        card,
        cards: [],
        selectionsByCard: {},
      });
    }

    const group = groups.get(key);
    group.cards.push(card);
    group.selectionsByCard[card.id] = selection;

    if (group.cards.length > 1) {
      group.previewId = `merged-${key.replace(/[^a-z0-9]+/g, "-") || card.id}`;
      if ((card.exam_stats?.total_hits || 0) > (group.card.exam_stats?.total_hits || 0)) {
        group.card = card;
      }
    }
  });

  return [...groups.values()].sort((a, b) => {
    const hitDelta = (b.card.exam_stats?.total_hits || 0) - (a.card.exam_stats?.total_hits || 0);
    if (hitDelta !== 0) {
      return hitDelta;
    }
    return humanizeTopic(a.card.topic).localeCompare(humanizeTopic(b.card.topic));
  });
}

function normalizeTopicMergeKey(card) {
  return String(card?.canonical_topic || card?.topic || "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, " ")
    .trim();
}

function getPreviewCardTitle(entry, layout) {
  const manualTitle = String(layout?.title || "").trim();
  if (manualTitle) {
    return manualTitle;
  }
  return derivePreviewCardTitle(entry);
}

function derivePreviewCardTitle(entry) {
  const focusQuestion = getFirstSelectedAIQuestion(entry);
  if (focusQuestion) {
    return summarizeCommonQuestionTitle(focusQuestion.summary);
  }

  const focusKeyPoint = getFirstSelectedKeyPoint(entry);
  if (focusKeyPoint) {
    return summarizePreviewLabel(focusKeyPoint.text, humanizeTopic(entry.card.topic));
  }

  const focusExample = getFirstSelectedAIExample(entry);
  if (focusExample?.title) {
    return summarizePreviewLabel(focusExample.title, humanizeTopic(entry.card.topic));
  }

  return humanizeTopic(entry.card.topic);
}

function getFirstSelectedAIQuestion(entry) {
  for (const sourceCard of entry.cards) {
    const selection = entry.selectionsByCard[sourceCard.id];
    if (!selection?.sections?.aiQuestions) {
      continue;
    }
    const selectedIds = new Set(selection.selected.aiQuestions || []);
    const match = commonQuestionItems(sourceCard).find((item) => selectedIds.has(item.id));
    if (match) {
      return match;
    }
  }
  return null;
}

function getFirstSelectedKeyPoint(entry) {
  for (const sourceCard of entry.cards) {
    const selection = entry.selectionsByCard[sourceCard.id];
    if (!selection?.sections?.keyPoints) {
      continue;
    }
    const selectedIds = new Set(selection.selected.keyPoints || []);
    const match = keyPointGroups(sourceCard).find((group) => selectedIds.has(group.id));
    if (match) {
      return match;
    }
  }
  return null;
}

function getFirstSelectedAIExample(entry) {
  for (const sourceCard of entry.cards) {
    const selection = entry.selectionsByCard[sourceCard.id];
    if (!selection?.sections?.aiExamples) {
      continue;
    }
    const selectedIds = new Set(selection.selected.aiExamples || []);
    const match = usefulAIExamples(sourceCard).find((item) => selectedIds.has(item.id));
    if (match) {
      return match;
    }
  }
  return null;
}

function summarizeCommonQuestionTitle(summary) {
  const plain = sanitizeDisplayText(summary || "").replace(/`/g, "").trim();
  const lower = plain.toLowerCase();

  if ((lower.includes("{}") || lower.includes("empty set")) && lower.includes("dict")) {
    return "Set vs. dict";
  }
  if (lower.includes("==") && /\bis\b/.test(lower)) {
    return "== vs is";
  }
  if (lower.includes("mutable") && lower.includes("default")) {
    return "Mutable defaults";
  }
  if (lower.includes("slice")) {
    return "Slicing rules";
  }
  if (lower.includes("membership") || lower.includes(" in {") || lower.includes("dictionary checks keys")) {
    return "dict membership";
  }
  if (lower.includes("print") && lower.includes("return")) {
    return "print vs return";
  }
  if (lower.includes("loc") && lower.includes("iloc")) {
    return ".loc vs .iloc";
  }
  if (lower.includes("strftime") && lower.includes("strptime")) {
    return "strftime vs strptime";
  }

  return summarizePreviewLabel(
    plain.replace(/^(why does|why is|what is|what does|how does|when does|which)\s+/i, "").replace(/\?+$/, ""),
    "Exam note"
  );
}

function summarizePreviewLabel(text, fallback) {
  const plain = sanitizeDisplayText(text || "").replace(/`/g, "").replace(/\s+/g, " ").trim();
  if (!plain) {
    return fallback;
  }
  return plain.length > 34 ? `${plain.slice(0, 34).replace(/\s+\S*$/, "").trim()}…` : plain;
}

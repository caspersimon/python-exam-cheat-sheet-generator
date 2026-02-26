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
    const cardElement = buildPreviewCard(card, selection);
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

function buildPreviewCard(card, selection) {
  const sectionHtml = [];

  if (selection.sections.keyPoints) {
    const groups = getSelectedKeyPointGroups(card, selection);
    if (groups.length) {
      sectionHtml.push(`<div class="section-title">Key Points for Reference</div>`);
      sectionHtml.push(renderPreviewKeyPoints(groups));
    }
  }

  if (selection.sections.aiExamples) {
    const aiExamples = usefulAIExamples(card).filter((item) => selection.selected.aiExamples.includes(item.id));
    if (aiExamples.length) {
      sectionHtml.push(`<div class="section-title">Code Examples</div>`);
      aiExamples.forEach((item) => {
        const kindLabel = item.kind === "incorrect" ? "Incorrect" : "Correct";
        sectionHtml.push(`<p><strong>${escapeHtml(kindLabel)} • ${renderInlineCode(item.title || "Code example")}</strong></p>`);
        sectionHtml.push(`<pre>${escapeHtml(item.code || "")}</pre>`);
        if (item.why) {
          sectionHtml.push(`<p>${renderInlineCode(normalizeTruncatedDisplayText(item.why))}</p>`);
        }
      });
    }
  }

  if (selection.sections.recommended) {
    const recommended = getSelectedSourceItemsForPreview(card, selection, "recommended");
    if (recommended.length) {
      sectionHtml.push(`<div class="section-title">Recommended</div>`);
      recommended.forEach((sourceItem) => {
        sectionHtml.push(renderPreviewSourceItem(sourceItem));
      });
    }
  }

  if (selection.sections.additional) {
    const additional = getSelectedSourceItemsForPreview(card, selection, "additional");
    if (additional.length) {
      sectionHtml.push(`<div class="section-title">Additional</div>`);
      additional.forEach((sourceItem) => {
        sectionHtml.push(renderPreviewSourceItem(sourceItem));
      });
    }
  }

  if (!sectionHtml.length) {
    sectionHtml.push(`<p class="preview-empty-copy">No selected details for this topic.</p>`);
  }

  const cardElement = document.createElement("article");
  cardElement.className = "preview-card";
  cardElement.dataset.cardId = card.id;

  cardElement.innerHTML = `
    <div class="preview-card-head" title="Drag to move this card">
      <h4>${escapeHtml(humanizeTopic(card.topic))}</h4>
      <span class="preview-drag-hint" aria-hidden="true">&#8942;&#8942;</span>
    </div>
    <div class="preview-body">${sectionHtml.join("")}</div>
    <button type="button" class="preview-resize-bottom" data-role="preview-resize-bottom" aria-label="Resize card height"></button>
    <button type="button" class="preview-resize-corner" data-role="preview-resize-corner" aria-label="Resize card"></button>
  `;

  return cardElement;
}

function getSelectedSourceItemsForPreview(card, selection, sectionKey) {
  const split = getSourceSplit(card);
  const selectedIds = new Set(selection.selected[sectionKey] || []);
  const bucket = sectionKey === "recommended" ? split.recommended : split.additional;
  return bucket.filter((item) => selectedIds.has(item.id));
}

function getSelectedKeyPointGroups(card, selection) {
  const selectedIds = new Set(selection.selected.keyPoints || []);
  return keyPointGroups(card)
    .map((group) => {
      const selectedDetails = group.details.filter((detail) => selectedIds.has(detail.id));
      const pointSelected = selectedIds.has(group.id);
      if (!pointSelected && !selectedDetails.length) {
        return null;
      }
      return {
        ...group,
        pointSelected,
        selectedDetails,
      };
    })
    .filter(Boolean);
}

function renderPreviewKeyPoints(groups) {
  const blocks = groups
    .map((group) => {
      const title = group.pointSelected
        ? `<p class="preview-kp-main">${renderInlineCode(group.text)}</p>`
        : `<p class="preview-kp-main"><span class="preview-kp-ref">Reference:</span> ${renderInlineCode(group.text)}</p>`;

      const detailHtml = group.selectedDetails.length
        ? `<div class="preview-kp-details">${group.selectedDetails.map((detail) => renderPreviewKeyPointDetail(detail)).join("")}</div>`
        : "";

      return `<div class="preview-kp-group">${title}${detailHtml}</div>`;
    })
    .join("");
  return `<div class="preview-kp-list">${blocks}</div>`;
}

function renderPreviewKeyPointDetail(detail) {
  if (detail.table) {
    return `
      <div class="preview-kp-detail-block">
        <p class="preview-kp-detail-title"><strong>${escapeHtml(detail.title || "Table detail")}</strong></p>
        ${renderPreviewTable(detail.table)}
      </div>
    `;
  }
  if (detail.code) {
    return `
      <div class="preview-kp-detail-block">
        <p class="preview-kp-detail-title"><strong>${escapeHtml(detail.title || "Code detail")}</strong></p>
        <pre>${escapeHtml(detail.code)}</pre>
      </div>
    `;
  }
  const text = normalizeTruncatedDisplayText(detail.text || detail.title || "Optional detail");
  return `
    <p class="preview-kp-detail">
      ${detail.title ? `<strong>${escapeHtml(detail.title)}:</strong> ` : ""}
      ${renderInlineCode(text)}
    </p>
  `;
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

function renderPreviewSourceItem(sourceItem) {
  const body = renderSourceItemBody(sourceItem);
  return `
    <div class="preview-source-item">
      <p class="preview-source-title"><strong>${escapeHtml(sourceItem.header)}</strong></p>
      ${body}
    </div>
  `;
}


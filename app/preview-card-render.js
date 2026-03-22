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

  const keyPointBlocks = [];
  const aiQuestionBlocks = [];
  const exampleBlocks = [];
  const recommendedBlocks = [];
  const additionalBlocks = [];

  cards.forEach((sourceCard) => {
    const selection = selectionsByCard[sourceCard.id];
    if (!selection) {
      return;
    }
    ensureSelectionOverrides(selection);

    if (selection.sections.aiQuestions) {
      commonQuestionItems(sourceCard)
        .filter((item) => (selection.selected.aiQuestions || []).includes(item.id))
        .forEach((item) => {
          aiQuestionBlocks.push(renderPreviewCommonQuestion(previewId, sourceCard, selection, item));
        });
    }

    if (selection.sections.keyPoints) {
      getSelectedKeyPointGroups(sourceCard, selection).forEach((group) => {
        keyPointBlocks.push(renderPreviewKeyPointGroup(sourceCard, selection, group));
      });
    }

    if (selection.sections.aiExamples) {
      usefulAIExamples(sourceCard)
        .filter((item) => selection.selected.aiExamples.includes(item.id))
        .forEach((item) => {
          const effective = getPreviewAIExampleOverride(selection, item.id, item);
          const kindLabel = item.kind === "incorrect" ? "Incorrect" : "Correct";
          exampleBlocks.push(`
            <div class="preview-item-block">
              ${renderPreviewItemActions(previewId, sourceCard.id, "aiExample", item.id, "aiExamples")}
              <p><strong>${escapeHtml(kindLabel)} • ${renderInlineCode(effective.title || "Code example")}</strong></p>
              ${renderCodeBlock(effective.code || "")}
              ${effective.output ? `<p><strong>Output / Result:</strong></p>${renderOutputBlock(effective.output || "")}` : ""}
            </div>
          `);
        });
    }

    if (selection.sections.recommended) {
      getSelectedSourceItemsForPreview(sourceCard, selection, "recommended").forEach((sourceItem) => {
        recommendedBlocks.push(renderPreviewSourceItem(previewId, sourceCard, selection, sourceItem, "recommended"));
      });
    }

    if (selection.sections.additional) {
      getSelectedSourceItemsForPreview(sourceCard, selection, "additional").forEach((sourceItem) => {
        additionalBlocks.push(renderPreviewSourceItem(previewId, sourceCard, selection, sourceItem, "additional"));
      });
    }
  });

  if (keyPointBlocks.length) {
    sections.push({
      label: "Key Points for Reference",
      content: `<div class="preview-kp-list">${keyPointBlocks.join("")}</div>`,
    });
  }

  if (aiQuestionBlocks.length) {
    sections.push({
      label: "Common Exam Questions",
      content: aiQuestionBlocks.join(""),
    });
  }

  if (exampleBlocks.length) {
    sections.push({
      label: "Code Examples",
      content: exampleBlocks.join(""),
    });
  }

  if (recommendedBlocks.length) {
    sections.push({
      label: "Recommended",
      content: recommendedBlocks.join(""),
    });
  }

  if (additionalBlocks.length) {
    sections.push({
      label: "Additional",
      content: additionalBlocks.join(""),
    });
  }

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

function renderPreviewItemActions(previewCardId, sourceCardId, itemType, itemId, sectionKey) {
  return `
    <div class="preview-item-actions">
      <button
        type="button"
        class="preview-mini-btn icon-only"
        data-role="preview-edit-item"
        data-card-id="${escapeHtml(previewCardId || "")}"
        data-source-card-id="${escapeHtml(sourceCardId || "")}"
        data-item-type="${escapeHtml(itemType)}"
        data-item-id="${escapeHtml(itemId)}"
        data-section="${escapeHtml(sectionKey)}"
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
        data-item-type="${escapeHtml(itemType)}"
        data-item-id="${escapeHtml(itemId)}"
        data-section="${escapeHtml(sectionKey)}"
        title="Delete item"
        aria-label="Delete item"
      >
        <span aria-hidden="true">&#10005;</span>
      </button>
    </div>
  `;
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

function renderPreviewKeyPointGroup(sourceCard, selection, group) {
  const keyPointText = getPreviewKeyPointOverride(selection, group.id, group.text);
  const title = group.pointSelected
    ? `<p class="preview-kp-main">${renderInlineCode(keyPointText)}</p>`
    : `<p class="preview-kp-main"><span class="preview-kp-ref">Reference:</span> ${renderInlineCode(keyPointText)}</p>`;

  const detailHtml = group.selectedDetails.length
    ? `<div class="preview-kp-details">${group.selectedDetails
        .map((detail) => renderPreviewKeyPointDetail(sourceCard.id, selection, detail))
        .join("")}</div>`
    : "";

  return `
    <div class="preview-kp-group preview-item-block">
      ${renderPreviewItemActions(sourceCard.id, sourceCard.id, "keyPoint", group.id, "keyPoints")}
      ${title}
      ${detailHtml}
    </div>
  `;
}

function renderPreviewCommonQuestion(previewCardId, sourceCard, selection, item) {
  const effective = getPreviewAIQuestionOverride(selection, item.id, item);
  return `
    <div class="preview-item-block preview-question-block">
      ${renderPreviewItemActions(previewCardId, sourceCard.id, "aiQuestion", item.id, "aiQuestions")}
      <p class="preview-kp-main"><strong>${renderInlineCode(effective.summary)}</strong></p>
      ${effective.detail ? `<p>${renderInlineCode(effective.detail)}</p>` : ""}
      ${effective.extra ? `<p>${renderInlineCode(effective.extra)}</p>` : ""}
      ${effective.table ? renderPreviewTable(effective.table) : ""}
      ${effective.code ? renderCodeBlock(effective.code) : ""}
    </div>
  `;
}

function renderPreviewKeyPointDetail(sourceCardId, selection, detail) {
  const overridden = getPreviewKeyPointDetailOverride(selection, detail.id);
  if (overridden) {
    return `
      <div class="preview-kp-detail-block preview-item-block">
        ${renderPreviewItemActions(sourceCardId, sourceCardId, "keyPointDetail", detail.id, "keyPoints")}
        <p class="preview-kp-detail"><strong>${escapeHtml(detail.title || "Detail")}:</strong> ${renderInlineCode(overridden)}</p>
      </div>
    `;
  }

  const actions = renderPreviewItemActions(sourceCardId, sourceCardId, "keyPointDetail", detail.id, "keyPoints");
  if (detail.table) {
    return `
      <div class="preview-kp-detail-block preview-item-block">
        ${actions}
        <p class="preview-kp-detail-title"><strong>${escapeHtml(detail.title || "Table detail")}</strong></p>
        ${renderPreviewTable(detail.table)}
      </div>
    `;
  }
  if (detail.code) {
    return `
      <div class="preview-kp-detail-block preview-item-block">
        ${actions}
        <p class="preview-kp-detail-title"><strong>${escapeHtml(detail.title || "Code detail")}</strong></p>
        ${renderCodeBlock(detail.code)}
      </div>
    `;
  }
  const text = normalizeTruncatedDisplayText(detail.text || detail.title || "Optional detail");
  return `
    <p class="preview-kp-detail preview-item-block">
      ${actions}
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

function renderPreviewSourceItem(previewCardId, sourceCard, selection, sourceItem, sectionKey) {
  const override = getPreviewSourceOverride(selection, sourceItem.id, sourceItem.header);
  const header = override?.header || sourceItem.header;
  const body = override?.body ? renderAutoBlock(override.body) : renderSourceItemBody(sourceItem);
  return `
    <div class="preview-source-item preview-item-block">
      ${renderPreviewItemActions(previewCardId, sourceCard.id, "sourceItem", sourceItem.id, sectionKey)}
      <p class="preview-source-title"><strong>${escapeHtml(header)}</strong></p>
      ${body}
    </div>
  `;
}

function ensureSelectionOverrides(selection) {
  if (!selection || typeof selection !== "object") {
    return { aiQuestions: {}, keyPoints: {}, keyPointDetails: {}, aiExamples: {}, sources: {} };
  }
  if (!selection.overrides || typeof selection.overrides !== "object") {
    selection.overrides = {};
  }
  const overrides = selection.overrides;
  if (!overrides.aiQuestions || typeof overrides.aiQuestions !== "object") {
    overrides.aiQuestions = {};
  }
  if (!overrides.keyPoints || typeof overrides.keyPoints !== "object") {
    overrides.keyPoints = {};
  }
  if (!overrides.keyPointDetails || typeof overrides.keyPointDetails !== "object") {
    overrides.keyPointDetails = {};
  }
  if (!overrides.aiExamples || typeof overrides.aiExamples !== "object") {
    overrides.aiExamples = {};
  }
  if (!overrides.sources || typeof overrides.sources !== "object") {
    overrides.sources = {};
  }
  return overrides;
}

function getPreviewAIQuestionOverride(selection, itemId, fallback) {
  const overrides = ensureSelectionOverrides(selection);
  const value = overrides.aiQuestions[itemId];
  if (!value || typeof value !== "object") {
    return fallback;
  }
  return {
    ...fallback,
    summary: typeof value.summary === "string" && value.summary.trim() ? value.summary.trim() : fallback.summary,
    detail: typeof value.detail === "string" && value.detail.trim() ? value.detail.trim() : fallback.detail,
    extra: typeof value.extra === "string" && value.extra.trim() ? value.extra.trim() : fallback.extra,
    table: fallback.table || null,
    code: typeof value.code === "string" && value.code.trim() ? value.code : fallback.code,
  };
}

function getPreviewKeyPointOverride(selection, keyPointId, fallbackText) {
  const overrides = ensureSelectionOverrides(selection);
  const value = overrides.keyPoints[keyPointId];
  if (typeof value === "string" && value.trim()) {
    return value.trim();
  }
  return fallbackText;
}

function getPreviewKeyPointDetailOverride(selection, detailId) {
  const overrides = ensureSelectionOverrides(selection);
  const value = overrides.keyPointDetails[detailId];
  if (typeof value === "string" && value.trim()) {
    return value.trim();
  }
  return "";
}

function getPreviewAIExampleOverride(selection, exampleId, fallback) {
  const overrides = ensureSelectionOverrides(selection);
  const value = overrides.aiExamples[exampleId];
  if (!value || typeof value !== "object") {
    return fallback;
  }
  return {
    ...fallback,
    title: typeof value.title === "string" && value.title.trim() ? value.title.trim() : fallback.title,
    code: typeof value.code === "string" && value.code.trim() ? value.code : fallback.code,
    output: typeof value.output === "string" && value.output.trim() ? value.output : fallback.output,
    why: typeof value.why === "string" && value.why.trim() ? value.why.trim() : fallback.why,
  };
}

function getPreviewSourceOverride(selection, itemId, fallbackHeader) {
  const overrides = ensureSelectionOverrides(selection);
  const value = overrides.sources[itemId];
  if (!value || typeof value !== "object") {
    return null;
  }
  const header = typeof value.header === "string" && value.header.trim() ? value.header.trim() : fallbackHeader;
  const body = typeof value.body === "string" && value.body.trim() ? value.body : "";
  if (!body && header === fallbackHeader) {
    return null;
  }
  return { header, body };
}

const MIN_PREVIEW_CARD_WIDTH = 56;
const MIN_PREVIEW_CARD_HEIGHT = 130;
const MIN_DETACHED_PREVIEW_CARD_HEIGHT = 64;

function isDetachedPreviewCard(cardId) {
  if (!cardId) {
    return false;
  }
  if (String(cardId).startsWith("detached__")) {
    return true;
  }
  return state.previewEntries?.[cardId]?.entryType === "detached-piece";
}

function getMinimumPreviewCardHeight(cardId, baseMinHeight = MIN_PREVIEW_CARD_HEIGHT) {
  const normalizedBase = Number.isFinite(Number(baseMinHeight)) ? Math.max(1, Number(baseMinHeight)) : MIN_PREVIEW_CARD_HEIGHT;
  if (!isDetachedPreviewCard(cardId)) {
    return normalizedBase;
  }
  return Math.min(normalizedBase, MIN_DETACHED_PREVIEW_CARD_HEIGHT);
}

function getPreviewPageContent(page) {
  return page === 2 ? refs.page2Content : refs.page1Content;
}

function getPreviewPageNumberForClientPoint(clientX, clientY) {
  const page1Rect = refs.page1Content.getBoundingClientRect();
  if (clientX >= page1Rect.left && clientX <= page1Rect.right && clientY >= page1Rect.top && clientY <= page1Rect.bottom) {
    return 1;
  }
  const page2Rect = refs.page2Content.getBoundingClientRect();
  if (clientX >= page2Rect.left && clientX <= page2Rect.right && clientY >= page2Rect.top && clientY <= page2Rect.bottom) {
    return 2;
  }
  return 0;
}

function getPreviewPageSize(page) {
  const pageContent = getPreviewPageContent(page);
  return {
    width: pageContent.clientWidth || DEFAULT_PAGE_INNER_WIDTH,
    height: pageContent.clientHeight || DEFAULT_PAGE_INNER_HEIGHT,
  };
}

function sanitizePreviewCardLayout(rawLayout, fallback = {}, options = {}) {
  const cardId = String(options.cardId || rawLayout?.id || fallback?.id || "");
  const page = rawLayout?.page === 2 ? 2 : 1;
  const pageSize = getPreviewPageSize(page);
  const sanitizeMinWidth = Number.isFinite(Number(options.minWidth))
    ? Math.max(1, Number(options.minWidth))
    : MIN_PREVIEW_CARD_WIDTH;
  const requestedMinHeight = Number.isFinite(Number(options.minHeight))
    ? Math.max(1, Number(options.minHeight))
    : MIN_PREVIEW_CARD_HEIGHT;
  const sanitizeMinHeight = getMinimumPreviewCardHeight(cardId, requestedMinHeight);
  const widthRaw = Number(rawLayout?.width ?? fallback.width ?? 160);
  const heightRaw = Number(rawLayout?.height ?? fallback.height ?? 220);
  const width = clamp(Number.isFinite(widthRaw) ? widthRaw : 160, sanitizeMinWidth, pageSize.width);
  const height = clamp(Number.isFinite(heightRaw) ? heightRaw : 220, sanitizeMinHeight, pageSize.height);
  const xRaw = Number(rawLayout?.x ?? fallback.x ?? 0);
  const yRaw = Number(rawLayout?.y ?? fallback.y ?? 0);
  const x = clamp(Number.isFinite(xRaw) ? xRaw : 0, 0, Math.max(0, pageSize.width - width));
  const y = clamp(Number.isFinite(yRaw) ? yRaw : 0, 0, Math.max(0, pageSize.height - height));
  const zRaw = Number(rawLayout?.z ?? fallback.z ?? 1);
  const z = clamp(Number.isFinite(zRaw) ? zRaw : 1, 1, 9999);
  const locked = Boolean(rawLayout?.locked ?? fallback.locked ?? false);
  const title = String(rawLayout?.title ?? fallback.title ?? "").trim();
  const summaryOverride = 'summaryOverride' in (rawLayout || {}) ? rawLayout.summaryOverride : ('summaryOverride' in (fallback || {}) ? fallback.summaryOverride : undefined);
  const result = { page, x, y, width, height, z, locked, title };
  if (summaryOverride !== undefined) {
    result.summaryOverride = summaryOverride;
  }
  return result;
}

function ensurePreviewCardLayout(cardId, fallback, options = {}) {
  const force = Boolean(options.force);
  const sanitizeOptions = { ...(options.sanitizeOptions || {}), cardId };
  const existing = state.previewCards[cardId];
  if (existing && (!force || existing.locked)) {
    const sanitized = sanitizePreviewCardLayout(existing, fallback, sanitizeOptions);
    state.previewCards[cardId] = sanitized;
    state.previewZCounter = Math.max(state.previewZCounter, sanitized.z + 1);
    return sanitized;
  }
  const next = sanitizePreviewCardLayout(
    {
      ...fallback,
      z: state.previewZCounter,
    },
    fallback,
    sanitizeOptions
  );
  state.previewCards[cardId] = next;
  state.previewZCounter = Math.max(state.previewZCounter, next.z + 1);
  return next;
}

function prunePreviewCardLayouts(validCardIds) {
  Object.keys(state.previewCards).forEach((cardId) => {
    if (!validCardIds.has(cardId)) {
      delete state.previewCards[cardId];
    }
  });
}

function normalizePreviewCardZOrder() {
  const ordered = Object.entries(state.previewCards || {}).sort((a, b) => {
    const zA = Number(a?.[1]?.z) || 0;
    const zB = Number(b?.[1]?.z) || 0;
    return zA - zB || a[0].localeCompare(b[0]);
  });
  ordered.forEach(([cardId], index) => {
    if (state.previewCards[cardId]) {
      state.previewCards[cardId].z = index + 1;
    }
  });
  state.previewZCounter = ordered.length + 1;
}

function bringPreviewCardToFront(cardId) {
  const layout = state.previewCards[cardId];
  if (!layout) {
    return;
  }
  if (state.previewZCounter >= 9990) {
    normalizePreviewCardZOrder();
  }
  layout.z = state.previewZCounter;
  state.previewZCounter += 1;
}

function sendPreviewCardToBack(cardId) {
  const layout = state.previewCards[cardId];
  if (!layout) {
    return;
  }
  layout.z = 0;
  normalizePreviewCardZOrder();
}

function applyPreviewCardLayout(cardElement, layout) {
  cardElement.style.left = `${layout.x}px`;
  cardElement.style.top = `${layout.y}px`;
  cardElement.style.width = `${layout.width}px`;
  cardElement.style.height = `${layout.height}px`;
  cardElement.style.zIndex = String(layout.z || 1);
}

function handlePreviewPointerDown(event) {
  if (state.view !== "preview" || event.button !== 0) {
    return;
  }
  if (event.target.closest(".preview-item-actions, .preview-card-head-actions")) {
    return;
  }
  const card = event.target.closest(".preview-card");
  if (!card) {
    return;
  }

  let mode = "";
  if (event.target.closest("[data-role='preview-resize-corner']")) {
    mode = "resize-corner";
  } else if (event.target.closest("[data-role='preview-resize-bottom']")) {
    mode = "resize-bottom";
  } else if (event.target.closest(".preview-card-head")) {
    mode = "drag";
  } else {
    return;
  }

  const cardId = card.dataset.cardId;
  const layout = state.previewCards[cardId];
  if (!cardId || !layout || card.classList.contains("is-locked") || layout.locked) {
    return;
  }

  event.preventDefault();
  bringPreviewCardToFront(cardId);
  applyPreviewCardLayout(card, layout);

  const pageContent = getPreviewPageContent(layout.page);
  const pageRect = pageContent.getBoundingClientRect();

  previewPointerState.active = true;
  previewPointerState.pointerId = event.pointerId;
  previewPointerState.mode = mode;
  previewPointerState.cardId = cardId;
  previewPointerState.cardEl = card;
  previewPointerState.startX = event.clientX;
  previewPointerState.startY = event.clientY;
  previewPointerState.startLeft = layout.x;
  previewPointerState.startTop = layout.y;
  previewPointerState.startWidth = layout.width;
  previewPointerState.startHeight = layout.height;
  previewPointerState.grabOffsetX = event.clientX - pageRect.left - layout.x;
  previewPointerState.grabOffsetY = event.clientY - pageRect.top - layout.y;

  card.classList.add(mode === "drag" ? "dragging" : "resizing");
  card.setPointerCapture?.(event.pointerId);
}

function handlePreviewPointerMove(event) {
  if (!previewPointerState.active || previewPointerState.pointerId !== event.pointerId) {
    return;
  }

  const layout = state.previewCards[previewPointerState.cardId];
  const cardElement = previewPointerState.cardEl;
  if (!layout || !cardElement) {
    return;
  }

  if (previewPointerState.mode === "drag") {
    const hoveredPage = getPreviewPageNumberForClientPoint(event.clientX, event.clientY) || layout.page;
    layout.page = hoveredPage;
    const pageContent = getPreviewPageContent(layout.page);
    const pageRect = pageContent.getBoundingClientRect();
    const pageSize = getPreviewPageSize(layout.page);
    const nextX = event.clientX - pageRect.left - previewPointerState.grabOffsetX;
    const nextY = event.clientY - pageRect.top - previewPointerState.grabOffsetY;
    layout.x = clamp(nextX, 0, Math.max(0, pageSize.width - layout.width));
    layout.y = clamp(nextY, 0, Math.max(0, pageSize.height - layout.height));

    if (cardElement.parentElement !== pageContent) {
      pageContent.appendChild(cardElement);
    }
    applyPreviewCardLayout(cardElement, layout);
    return;
  }

  const pageSize = getPreviewPageSize(layout.page);
  const dx = event.clientX - previewPointerState.startX;
  const dy = event.clientY - previewPointerState.startY;
  const minHeight = getMinimumPreviewCardHeight(previewPointerState.cardId);

  if (previewPointerState.mode === "resize-corner") {
    const maxWidth = Math.max(MIN_PREVIEW_CARD_WIDTH, pageSize.width - layout.x);
    const maxHeight = Math.max(minHeight, pageSize.height - layout.y);
    layout.width = clamp(previewPointerState.startWidth + dx, MIN_PREVIEW_CARD_WIDTH, maxWidth);
    layout.height = clamp(previewPointerState.startHeight + dy, minHeight, maxHeight);
  } else if (previewPointerState.mode === "resize-bottom") {
    const maxHeight = Math.max(minHeight, pageSize.height - layout.y);
    layout.height = clamp(previewPointerState.startHeight + dy, minHeight, maxHeight);
  }

  applyPreviewCardLayout(cardElement, layout);
}

function finishPreviewPointerAction(event) {
  if (!previewPointerState.active) {
    return;
  }
  if (event && previewPointerState.pointerId !== event.pointerId) {
    return;
  }

  const cardElement = previewPointerState.cardEl;
  if (cardElement) {
    cardElement.classList.remove("dragging", "resizing");
    if (previewPointerState.pointerId !== null && cardElement.hasPointerCapture?.(previewPointerState.pointerId)) {
      cardElement.releasePointerCapture(previewPointerState.pointerId);
    }
  }

  previewPointerState.active = false;
  previewPointerState.pointerId = null;
  previewPointerState.mode = "";
  previewPointerState.cardId = "";
  previewPointerState.cardEl = null;
  schedulePersistState();
}

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

function sanitizePreviewCardLayout(rawLayout, fallback = {}) {
  const page = rawLayout?.page === 2 ? 2 : 1;
  const pageSize = getPreviewPageSize(page);
  const widthRaw = Number(rawLayout?.width ?? fallback.width ?? 260);
  const heightRaw = Number(rawLayout?.height ?? fallback.height ?? 220);
  const width = clamp(Number.isFinite(widthRaw) ? widthRaw : 260, 170, pageSize.width);
  const height = clamp(Number.isFinite(heightRaw) ? heightRaw : 220, 130, pageSize.height);
  const xRaw = Number(rawLayout?.x ?? fallback.x ?? 0);
  const yRaw = Number(rawLayout?.y ?? fallback.y ?? 0);
  const x = clamp(Number.isFinite(xRaw) ? xRaw : 0, 0, Math.max(0, pageSize.width - width));
  const y = clamp(Number.isFinite(yRaw) ? yRaw : 0, 0, Math.max(0, pageSize.height - height));
  const zRaw = Number(rawLayout?.z ?? fallback.z ?? 1);
  const z = clamp(Number.isFinite(zRaw) ? zRaw : 1, 1, 9999);
  return { page, x, y, width, height, z };
}

function ensurePreviewCardLayout(cardId, fallback) {
  const existing = state.previewCards[cardId];
  if (existing) {
    const sanitized = sanitizePreviewCardLayout(existing, fallback);
    state.previewCards[cardId] = sanitized;
    state.previewZCounter = Math.max(state.previewZCounter, sanitized.z + 1);
    return sanitized;
  }
  const next = sanitizePreviewCardLayout(
    {
      ...fallback,
      z: state.previewZCounter,
    },
    fallback
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

function bringPreviewCardToFront(cardId) {
  const layout = state.previewCards[cardId];
  if (!layout) {
    return;
  }
  layout.z = state.previewZCounter;
  state.previewZCounter += 1;
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
  if (!cardId || !layout) {
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

  if (previewPointerState.mode === "resize-corner") {
    const maxWidth = Math.max(170, pageSize.width - layout.x);
    const maxHeight = Math.max(130, pageSize.height - layout.y);
    layout.width = clamp(previewPointerState.startWidth + dx, 170, maxWidth);
    layout.height = clamp(previewPointerState.startHeight + dy, 130, maxHeight);
  } else if (previewPointerState.mode === "resize-bottom") {
    const maxHeight = Math.max(130, pageSize.height - layout.y);
    layout.height = clamp(previewPointerState.startHeight + dy, 130, maxHeight);
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


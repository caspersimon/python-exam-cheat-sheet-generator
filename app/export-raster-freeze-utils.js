const EXPORT_TARGET_DPI = 300;
const EXPORT_PAGE_PIXELS = Object.freeze({
  portrait: { width: 2480, height: 3508 },
  landscape: { width: 3508, height: 2480 },
});
const EXPORT_DEBUG_STORE_KEY = "__pythonCheatsheetExportDebug";
const EXPORT_FONT_TIMEOUT_MS = 8000;
const EXPORT_CHROME_SELECTOR = [
  ".preview-card-head-actions",
  ".preview-item-actions",
  ".preview-resize-bottom",
  ".preview-resize-corner",
  ".preview-drag-hint",
  ".support-prompt-overlay",
  ".preview-edit-modal",
  ".staged-sidebar",
].join(", ");
const EXPORT_LAYOUT_FREEZE_SELECTOR = [
  ".sheet-page",
  ".page-content",
  ".preview-card",
  ".preview-card-head",
  ".preview-body",
  ".preview-table-wrap",
  ".preview-table",
  ".kp-mini-table",
  "pre",
  "code",
  ".inline-code",
  "p",
  "li",
  "ul",
  "ol",
  "table",
  "thead",
  "tbody",
  "tr",
  "th",
  "td",
  ".section-title",
  ".preview-piece-title",
  ".preview-item-note",
].join(", ");
const EXPORT_STYLE_PROPERTIES = [
  "font-family", "font-size", "font-weight", "font-style", "line-height", "letter-spacing", "word-spacing",
  "text-transform", "text-indent", "text-rendering", "font-feature-settings", "font-variant-ligatures",
  "font-kerning", "font-stretch", "font-variant", "white-space", "word-break", "overflow-wrap", "hyphens",
  "tab-size", "text-wrap", "text-align", "color", "background", "background-color", "background-image",
  "background-size", "background-position", "background-repeat", "border", "border-top", "border-right",
  "border-bottom", "border-left", "border-radius", "box-shadow", "box-sizing", "display", "position",
  "overflow", "overflow-x", "overflow-y", "opacity", "visibility", "padding-top", "padding-right",
  "padding-bottom", "padding-left", "margin-top", "margin-right", "margin-bottom", "margin-left", "gap",
  "row-gap", "column-gap", "justify-content", "align-items", "align-content", "justify-items", "flex",
  "flex-grow", "flex-shrink", "flex-basis", "flex-direction", "flex-wrap", "grid-template-columns",
  "grid-template-rows", "grid-auto-columns", "grid-auto-rows", "grid-column", "grid-row", "grid-area",
  "place-items", "place-content", "transform", "transform-origin",
];

function getExportDebugStore() {
  if (!window[EXPORT_DEBUG_STORE_KEY] || typeof window[EXPORT_DEBUG_STORE_KEY] !== "object") {
    window[EXPORT_DEBUG_STORE_KEY] = { history: [] };
  }
  if (!Array.isArray(window[EXPORT_DEBUG_STORE_KEY].history)) {
    window[EXPORT_DEBUG_STORE_KEY].history = [];
  }
  return window[EXPORT_DEBUG_STORE_KEY];
}

function recordExportDebug(entry) {
  const store = getExportDebugStore();
  store.lastRun = entry;
  store.history.push(entry);
  if (store.history.length > 40) {
    store.history.splice(0, store.history.length - 40);
  }
}

function getExportDebugSnapshot() {
  return getExportDebugStore();
}

function getExportPageRenderSpec(pageElement, targetDpi = EXPORT_TARGET_DPI) {
  const isLandscape = Boolean(pageElement?.classList?.contains("is-landscape"));
  const targetPixels = isLandscape ? EXPORT_PAGE_PIXELS.landscape : EXPORT_PAGE_PIXELS.portrait;
  const rect = pageElement?.getBoundingClientRect?.() || { width: 0, height: 0 };
  const sourceWidthPx = Math.round(rect.width || (isLandscape ? DEFAULT_PAGE_INNER_HEIGHT : DEFAULT_PAGE_INNER_WIDTH));
  const sourceHeightPx = Math.round(rect.height || (isLandscape ? DEFAULT_PAGE_INNER_WIDTH : DEFAULT_PAGE_INNER_HEIGHT));
  return {
    orientation: isLandscape ? "landscape" : "portrait",
    widthMm: isLandscape ? 297 : 210,
    heightMm: isLandscape ? 210 : 297,
    targetWidthPx: targetPixels.width,
    targetHeightPx: targetPixels.height,
    sourceWidthPx,
    sourceHeightPx,
    rasterScale: Math.max(targetPixels.width / Math.max(1, sourceWidthPx), targetPixels.height / Math.max(1, sourceHeightPx)),
    targetDpi,
  };
}

function isExportChromeNode(node) {
  return Boolean(node?.matches?.(EXPORT_CHROME_SELECTOR));
}

function shouldFreezeLayoutNode(node) {
  return Boolean(node?.matches?.(EXPORT_LAYOUT_FREEZE_SELECTOR));
}

function copyComputedStyles(sourceNode, cloneNode) {
  if (!(sourceNode instanceof Element) || !(cloneNode instanceof Element)) {
    return;
  }
  const computed = window.getComputedStyle(sourceNode);
  EXPORT_STYLE_PROPERTIES.forEach((property) => {
    const value = computed.getPropertyValue(property);
    if (value) cloneNode.style.setProperty(property, value);
  });
}

function freezeNodeBoxMetrics(sourceNode, cloneNode, pageRect, clonePageElement) {
  if (!(sourceNode instanceof Element) || !(cloneNode instanceof Element)) {
    return;
  }
  const sourceRect = sourceNode.getBoundingClientRect();
  const cloneRect = cloneNode.getBoundingClientRect();
  const sourceStyle = window.getComputedStyle(sourceNode);
  if (sourceNode === clonePageElement.__sourcePageRef) {
    cloneNode.style.width = `${pageRect.width}px`;
    cloneNode.style.height = `${pageRect.height}px`;
    cloneNode.style.minWidth = `${pageRect.width}px`;
    cloneNode.style.maxWidth = `${pageRect.width}px`;
    cloneNode.style.minHeight = `${pageRect.height}px`;
    cloneNode.style.maxHeight = `${pageRect.height}px`;
    cloneNode.style.margin = "0";
    cloneNode.style.borderRadius = "0";
    cloneNode.style.boxShadow = "none";
    cloneNode.style.border = "none";
    return;
  }
  if (sourceStyle.position === "absolute" || sourceStyle.position === "fixed") {
    cloneNode.style.position = "absolute";
    cloneNode.style.left = `${sourceRect.left - pageRect.left}px`;
    cloneNode.style.top = `${sourceRect.top - pageRect.top}px`;
    cloneNode.style.width = `${sourceRect.width}px`;
    cloneNode.style.height = `${sourceRect.height}px`;
  } else if (shouldFreezeLayoutNode(sourceNode)) {
    const currentWidth = sourceRect.width || cloneRect.width;
    const currentHeight = sourceRect.height || cloneRect.height;
    if (currentWidth > 0) cloneNode.style.width = `${currentWidth}px`;
    if (currentHeight > 0) cloneNode.style.height = `${currentHeight}px`;
  }
  if (sourceNode.scrollTop) cloneNode.scrollTop = sourceNode.scrollTop;
  if (sourceNode.scrollLeft) cloneNode.scrollLeft = sourceNode.scrollLeft;
}

function traverseSourceAndClone(sourceNode, cloneNode, visitor) {
  visitor(sourceNode, cloneNode);
  const sourceChildren = Array.from(sourceNode.children || []);
  const cloneChildren = Array.from(cloneNode.children || []);
  const pairCount = Math.min(sourceChildren.length, cloneChildren.length);
  for (let index = 0; index < pairCount; index += 1) {
    traverseSourceAndClone(sourceChildren[index], cloneChildren[index], visitor);
  }
}

function hideExportChromeInClone(sourceNode, cloneNode) {
  if (!isExportChromeNode(sourceNode)) return;
  cloneNode.style.setProperty("display", "none", "important");
  cloneNode.style.setProperty("visibility", "hidden", "important");
  cloneNode.style.setProperty("opacity", "0", "important");
  cloneNode.style.setProperty("pointer-events", "none", "important");
}

async function waitForExportFontsReady(timeoutMs = EXPORT_FONT_TIMEOUT_MS) {
  if (!document.fonts?.ready) {
    return { ready: false, status: "unsupported" };
  }
  try {
    const result = await Promise.race([
      document.fonts.ready,
      new Promise((resolve) => {
        window.setTimeout(() => resolve("timeout"), timeoutMs);
      }),
    ]);
    if (result === "timeout") {
      const unresolved = Array.from(document.fonts).filter((fontFace) => fontFace.status !== "loaded").length;
      return { ready: false, status: "timeout", unresolvedCount: unresolved };
    }
  } catch {
    return { ready: false, status: "error" };
  }
  const unresolved = Array.from(document.fonts).filter((fontFace) => fontFace.status !== "loaded").length;
  return { ready: true, status: unresolved === 0 ? "loaded" : "ready", unresolvedCount: unresolved };
}

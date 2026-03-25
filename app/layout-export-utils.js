function applyLayoutVariables() {
  refs.sheetStage.style.setProperty("--sheet-font", state.layout.fontFamily);
  refs.sheetStage.style.setProperty("--sheet-font-size", `${state.layout.fontSize}px`);
  refs.sheetStage.style.setProperty("--sheet-title-size", `${state.layout.titleSize}px`);
  refs.sheetStage.style.setProperty("--sheet-line-height", String(state.layout.lineHeight));
  refs.sheetStage.style.setProperty("--sheet-letter-spacing", `${state.layout.letterSpacing}px`);
  refs.sheetStage.style.setProperty("--sheet-card-gap", `${state.layout.cardGap}px`);
  refs.sheetStage.style.setProperty("--sheet-card-padding", `${state.layout.cardPadding}px`);
  refs.sheetStage.style.setProperty("--sheet-code-block-padding", `${state.layout.codeBlockPadding}px`);
  refs.sheetStage.style.setProperty("--sheet-code-block-margin", `${state.layout.codeBlockMargin}px`);
  refs.sheetStage.style.setProperty("--sheet-table-font-size", `${state.layout.tableSize}px`);
  refs.sheetStage.style.setProperty("--sheet-piece-gap", `${state.layout.pieceGap}px`);
  refs.sheetStage.style.setProperty("--sheet-title-margin", `${state.layout.titleMargin}px`);

  refs.page1Content?.closest(".sheet-page")?.classList.toggle("is-landscape", Boolean(state.layout.page1Landscape));
  refs.page2Content?.closest(".sheet-page")?.classList.toggle("is-landscape", Boolean(state.layout.page2Landscape));

  refs.fontFamilySelect.value = state.layout.fontFamily;
  refs.fontSizeRange.value = String(state.layout.fontSize);
  refs.titleSizeRange.value = String(state.layout.titleSize);
  refs.lineHeightRange.value = String(state.layout.lineHeight);
  refs.letterSpacingRange.value = String(state.layout.letterSpacing);
  refs.cardGapRange.value = String(state.layout.cardGap);
  refs.cardPaddingRange.value = String(state.layout.cardPadding);
  refs.codeBlockPaddingRange.value = String(state.layout.codeBlockPadding);
  refs.codeBlockMarginRange.value = String(state.layout.codeBlockMargin);
  refs.tableSizeRange.value = String(state.layout.tableSize);
  refs.pieceGapRange.value = String(state.layout.pieceGap);
  refs.titleMarginRange.value = String(state.layout.titleMargin);

  refs.fontSizeValue.textContent = String(state.layout.fontSize);
  refs.titleSizeValue.textContent = String(state.layout.titleSize);
  refs.lineHeightValue.textContent = String(state.layout.lineHeight);
  refs.letterSpacingValue.textContent = String(state.layout.letterSpacing);
  refs.cardGapValue.textContent = String(state.layout.cardGap);
  refs.cardPaddingValue.textContent = String(state.layout.cardPadding);
  refs.codeBlockPaddingValue.textContent = String(state.layout.codeBlockPadding);
  refs.codeBlockMarginValue.textContent = String(state.layout.codeBlockMargin);
  refs.tableSizeValue.textContent = String(state.layout.tableSize);
  refs.pieceGapValue.textContent = String(state.layout.pieceGap);
  refs.titleMarginValue.textContent = String(state.layout.titleMargin);

  if (refs.page1LandscapeToggle) refs.page1LandscapeToggle.checked = Boolean(state.layout.page1Landscape);
  if (refs.page2LandscapeToggle) refs.page2LandscapeToggle.checked = Boolean(state.layout.page2Landscape);
}

async function exportPng() {
  setView("preview");

  if (typeof window.html2canvas !== "function") {
    alert("PNG export library not loaded. Use Print as fallback.");
    return;
  }

  const pages = getNonEmptyPageElements();
  if (!pages.length) {
    alert("No content to export.");
    return;
  }

  const originalText = refs.exportPngBtn.textContent;
  refs.exportPngBtn.textContent = "Exporting...";
  refs.exportPngBtn.disabled = true;

  try {
    for (let idx = 0; idx < pages.length; idx += 1) {
      const page = pages[idx];
      const canvas = await renderExportPageToCanvas(page);

      const url = canvas.toDataURL("image/png");
      const link = document.createElement("a");
      link.href = url;
      link.download = `python-cheatsheet-page-${idx + 1}.png`;
      link.click();
    }
  } finally {
    refs.exportPngBtn.textContent = originalText;
    refs.exportPngBtn.disabled = false;
  }
}

function getNonEmptyPageElements() {
  const pages = [];
  const page1Has = refs.page1Content.querySelector(".preview-card");
  const page2Has = refs.page2Content.querySelector(".preview-card");

  if (page1Has) {
    pages.push(refs.page1Content.parentElement);
  }
  if (page2Has) {
    pages.push(refs.page2Content.parentElement);
  }
  return pages;
}

function getExportRenderOptions(options = {}) {
  const scale = Number(options.scale);
  const docEl = document.documentElement;
  const body = document.body;
  const windowWidth = Math.max(docEl?.clientWidth || 0, docEl?.scrollWidth || 0, body?.scrollWidth || 0);
  const windowHeight = Math.max(docEl?.clientHeight || 0, docEl?.scrollHeight || 0, body?.scrollHeight || 0);
  return {
    scale: Number.isFinite(scale) && scale > 0 ? scale : 2,
    useCORS: true,
    backgroundColor: "#ffffff",
    logging: false,
    foreignObjectRendering: options.useForeignObject !== false,
    windowWidth,
    windowHeight,
    scrollX: 0,
    scrollY: 0,
    removeContainer: true,
    onclone: (clonedDoc) => {
      clonedDoc.body.classList.add("export-snapshot-mode");
    },
  };
}

function isCanvasLikelyBlank(canvas) {
  if (!canvas || canvas.width < 8 || canvas.height < 8) {
    return true;
  }

  const ctx = canvas.getContext("2d", { willReadFrequently: true });
  if (!ctx) {
    return false;
  }

  const sampleCols = 18;
  const sampleRows = 24;
  const minX = Math.max(0, Math.floor(canvas.width * 0.02));
  const minY = Math.max(0, Math.floor(canvas.height * 0.02));
  const maxX = Math.max(minX + 1, Math.ceil(canvas.width * 0.98));
  const maxY = Math.max(minY + 1, Math.ceil(canvas.height * 0.98));
  const stepX = Math.max(1, Math.floor((maxX - minX) / sampleCols));
  const stepY = Math.max(1, Math.floor((maxY - minY) / sampleRows));

  for (let y = minY; y < maxY; y += stepY) {
    for (let x = minX; x < maxX; x += stepX) {
      const [r, g, b, a] = ctx.getImageData(x, y, 1, 1).data;
      if (a > 8 && (r < 246 || g < 246 || b < 246)) {
        return false;
      }
    }
  }

  return true;
}

async function renderExportPageToCanvas(page, options = {}) {
  if (!page) {
    throw new Error("Export page element is missing.");
  }
  if (typeof window.html2canvas !== "function") {
    throw new Error("html2canvas is not available.");
  }

  // Prefer raster mode for stable full-page captures. ForeignObject mode can
  // clip tall content in some browser/PDF combinations.
  const primary = await window.html2canvas(page, getExportRenderOptions({ ...options, useForeignObject: false }));
  if (!isCanvasLikelyBlank(primary)) {
    return primary;
  }

  const fallback = await window.html2canvas(page, getExportRenderOptions({ ...options, useForeignObject: true }));
  if (isCanvasLikelyBlank(fallback)) {
    throw new Error("Export rendering resulted in a blank page.");
  }
  return fallback;
}

function smartFitLayout() {
  const entries = buildMergedPreviewEntries();
  const N = entries.length;
  if (N === 0) {
    return;
  }

  // Estimate content per card
  let totalChars = 0;
  entries.forEach(({ snippet, selectionsByCard }) => {
    const selection = selectionsByCard[snippet.id];
    const selectedSet = new Set(selection?.selected?.pieces || []);
    snippet.pieces
      .filter((p) => selectedSet.has(p.id))
      .forEach((p) => {
        totalChars += String(p.text || p.body || p.bodyMarkdown || p.summary || "").length;
      });
  });
  const avgCharsPerCard = totalChars / N;

  // Get effective page dimensions (accounting for landscape)
  const page1Landscape = Boolean(state.layout.page1Landscape);
  const page2Landscape = Boolean(state.layout.page2Landscape);
  const p1w = page1Landscape ? DEFAULT_PAGE_INNER_HEIGHT : DEFAULT_PAGE_INNER_WIDTH;
  const p1h = page1Landscape ? DEFAULT_PAGE_INNER_WIDTH : DEFAULT_PAGE_INNER_HEIGHT;
  const p2w = page2Landscape ? DEFAULT_PAGE_INNER_HEIGHT : DEFAULT_PAGE_INNER_WIDTH;
  const p2h = page2Landscape ? DEFAULT_PAGE_INNER_WIDTH : DEFAULT_PAGE_INNER_HEIGHT;

  // Find best grid: maximize cell area while fitting all cards in 2 pages
  // Constraint: cell must be at least 80px tall and 100px wide to be readable
  const MIN_CELL_HEIGHT = 80;
  const MIN_CELL_WIDTH = 100;
  const GAP = 4; // use tight gap for smart fit

  let bestCols = 2;
  let bestRows = 6;
  let bestScore = -Infinity;

  for (let cols = 1; cols <= 4; cols++) {
    for (let rows = 3; rows <= 14; rows++) {
      const capacity = cols * rows * 2;
      if (capacity < N) {
        continue;
      }

      // Check cell dimensions for both pages
      const cellW1 = (p1w - GAP * (cols - 1)) / cols;
      const cellH1 = (p1h - GAP * (rows - 1)) / rows;
      const cellW2 = (p2w - GAP * (cols - 1)) / cols;
      const cellH2 = (p2h - GAP * (rows - 1)) / rows;

      if (cellH1 < MIN_CELL_HEIGHT || cellW1 < MIN_CELL_WIDTH) continue;
      if (cellH2 < MIN_CELL_HEIGHT || cellW2 < MIN_CELL_WIDTH) continue;

      // Score: prefer large cells, penalize wasted space
      const avgCellArea = ((cellW1 * cellH1) + (cellW2 * cellH2)) / 2;
      const waste = (capacity - N) / capacity;
      const score = avgCellArea * (1 - waste * 0.3);

      if (score > bestScore) {
        bestScore = score;
        bestCols = cols;
        bestRows = rows;
      }
    }
  }

  // Determine font size based on resulting cell height and content density
  const avgCellH = ((p1h - GAP * (bestRows - 1)) / bestRows + (p2h - GAP * (bestRows - 1)) / bestRows) / 2;
  // chars per pixel of cell height: higher = denser content
  const contentDensity = avgCharsPerCard / avgCellH;

  let fontSize, titleSize, cardPadding, codeBlockPadding, codeBlockMargin, lineHeight;

  if (contentDensity < 1.5 && avgCellH > 180) {
    fontSize = 9.5; titleSize = 10.5; cardPadding = 6; codeBlockPadding = 5; codeBlockMargin = 2; lineHeight = 1.1;
  } else if (contentDensity < 2.5 && avgCellH > 130) {
    fontSize = 9; titleSize = 10; cardPadding = 5; codeBlockPadding = 4; codeBlockMargin = 1; lineHeight = 1.08;
  } else if (contentDensity < 4 || avgCellH > 100) {
    fontSize = 8.5; titleSize = 9.5; cardPadding = 5; codeBlockPadding = 4; codeBlockMargin = 1; lineHeight = 1.08;
  } else if (contentDensity < 6) {
    fontSize = 8; titleSize = 9; cardPadding = 4; codeBlockPadding = 3; codeBlockMargin = 1; lineHeight = 1.06;
  } else {
    fontSize = 7.5; titleSize = 8.5; cardPadding = 4; codeBlockPadding = 2; codeBlockMargin = 1; lineHeight = 1.04;
  }

  state.layout.autoGrid = false;
  state.layout.gridColumns = bestCols;
  state.layout.gridRows = bestRows;
  state.layout.fontSize = fontSize;
  state.layout.titleSize = titleSize;
  state.layout.cardGap = GAP;
  state.layout.cardPadding = cardPadding;
  state.layout.codeBlockPadding = codeBlockPadding;
  state.layout.codeBlockMargin = codeBlockMargin;
  state.layout.lineHeight = lineHeight;
  state.layout.letterSpacing = 0;

  // Clear manual position overrides so the new grid takes effect
  state.previewCards = {};

  applyLayoutVariables();
  renderPreview();
}

function formatExamLabel(label) {
  return EXAM_LABELS[label] || label || "Unknown exam";
}

function normalizeTruncatedDisplayText(text) {
  const value = normalizeNewlines(String(text || "")).trim();
  if (!value) {
    return "";
  }

  if (!/(?:\.\.\.|…)\s*$/.test(value)) {
    return value;
  }

  let trimmed = value.replace(/(?:\.\.\.|…)\s*$/, "").trim();
  trimmed = trimmed.replace(/\b(a|an|the|to|of|for|in|on|at|by|with|and|or|but|if|when|while|before|after|via|into|from)\s*$/i, "").trim();

  return trimmed || value;
}

function trimWords(text, maxWords) {
  if (!text) {
    return "";
  }
  const words = text.trim().split(/\s+/);
  if (words.length <= maxWords) {
    return text.trim();
  }
  return `${words.slice(0, maxWords).join(" ")}…`;
}

function trimLines(text, maxLines) {
  if (!text) {
    return "";
  }
  const lines = text.split("\n");
  if (lines.length <= maxLines) {
    return text;
  }
  return `${lines.slice(0, maxLines).join("\n")}\n# ...`;
}

function humanizeTopic(topic) {
  const raw = String(topic || "").trim();
  if (!raw) {
    return "";
  }

  const cleaned = raw.replace(/_/g, " ").replace(/\s+/g, " ").trim();
  if (cleaned !== cleaned.toLowerCase()) {
    return cleaned;
  }

  const smallWords = new Set(["and", "or", "of", "vs", "in", "to", "for", "on", "with"]);
  return cleaned
    .split(" ")
    .map((word, index) => {
      if (index > 0 && smallWords.has(word)) {
        return word;
      }
      return word.charAt(0).toUpperCase() + word.slice(1);
    })
    .join(" ");
}

function looksCodeLike(text) {
  const value = (text || "").trim();
  if (!value) {
    return false;
  }

  if (value.includes("\n")) {
    return true;
  }

  const codeSignals = ["=", "(", ")", "[", "]", "{", "}", ":", "+", "-", "*", "/", "%", "."];
  const codeKeywords = ["print", "for ", "if ", "while ", "def ", "return", "import ", "from ", "lambda", "range", "len", "sorted"];
  const lower = value.toLowerCase();

  return codeSignals.some((signal) => value.includes(signal)) || codeKeywords.some((kw) => lower.startsWith(kw) || lower.includes(` ${kw}`));
}

function isLowValueSnippet(text) {
  const value = (text || "").trim();
  if (!value) {
    return true;
  }

  if (value.includes("\n")) {
    return false;
  }

  const lower = value.toLowerCase();
  if (lower.startsWith("#") || lower.startsWith("##") || lower.startsWith("###")) {
    return true;
  }

  const lowPhrases = [
    "below you will find",
    "the following",
    "function definitions start",
    "you call functions",
    "dictionaries are",
    "global and local names",
  ];

  if (lowPhrases.some((phrase) => lower.includes(phrase)) && !looksCodeLike(value)) {
    return true;
  }

  if (!looksCodeLike(value) && value.split(/\s+/).length <= 8) {
    return true;
  }

  return false;
}

function clamp(value, min, max) {
  return Math.min(max, Math.max(min, value));
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function deepClone(value) {
  return JSON.parse(JSON.stringify(value));
}

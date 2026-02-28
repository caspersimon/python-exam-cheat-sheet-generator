function applyLayoutVariables() {
  refs.sheetStage.style.setProperty("--sheet-font", state.layout.fontFamily);
  refs.sheetStage.style.setProperty("--sheet-font-size", `${state.layout.fontSize}px`);
  refs.sheetStage.style.setProperty("--sheet-line-height", String(state.layout.lineHeight));
  refs.sheetStage.style.setProperty("--sheet-letter-spacing", `${state.layout.letterSpacing}px`);
  refs.sheetStage.style.setProperty("--sheet-card-gap", `${state.layout.cardGap}px`);
  refs.sheetStage.style.setProperty("--sheet-card-padding", `${state.layout.cardPadding}px`);

  refs.fontFamilySelect.value = state.layout.fontFamily;
  refs.fontSizeRange.value = String(state.layout.fontSize);
  refs.lineHeightRange.value = String(state.layout.lineHeight);
  refs.letterSpacingRange.value = String(state.layout.letterSpacing);
  refs.cardGapRange.value = String(state.layout.cardGap);
  refs.cardPaddingRange.value = String(state.layout.cardPadding);

  refs.fontSizeValue.textContent = String(state.layout.fontSize);
  refs.lineHeightValue.textContent = String(state.layout.lineHeight);
  refs.letterSpacingValue.textContent = String(state.layout.letterSpacing);
  refs.cardGapValue.textContent = String(state.layout.cardGap);
  refs.cardPaddingValue.textContent = String(state.layout.cardPadding);
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
    const renderOptions = getExportRenderOptions();
    for (let idx = 0; idx < pages.length; idx += 1) {
      const page = pages[idx];
      const canvas = await window.html2canvas(page, renderOptions);

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

function getExportRenderOptions() {
  return {
    scale: 2,
    useCORS: true,
    backgroundColor: "#ffffff",
    foreignObjectRendering: true,
    removeContainer: true,
    onclone: (clonedDoc) => {
      clonedDoc.body.classList.add("export-snapshot-mode");
    },
  };
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

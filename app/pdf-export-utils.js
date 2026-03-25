const SUPPORT_PAGE_URL =
  "https://buymeacoffee.com/caspersimon/?utm_source=cheatsheet_app&utm_medium=support_prompt&utm_campaign=post_export_support";
const SUPPORT_PROMPT_SNOOZE_KEY = "python_midterm_support_prompt_snooze_v1";
const SUPPORT_PROMPT_SNOOZE_DAYS = 14;
const PDF_EXPORT_SCALE = 3;
const PDF_IMAGE_COMPRESSION = "MEDIUM";

const supportPromptState = {
  overlay: null,
  acceptBtn: null,
  declineBtn: null,
  closeBtn: null,
  active: false,
  eventsBound: false,
};

function readSupportPromptSuppression() {
  try {
    return localStorage.getItem(SUPPORT_PROMPT_SNOOZE_KEY) || "";
  } catch {
    return "";
  }
}

function writeSupportPromptSuppression(value) {
  try {
    localStorage.setItem(SUPPORT_PROMPT_SNOOZE_KEY, value);
  } catch {
    // Ignore write issues in private/incognito contexts.
  }
}

function suppressSupportPromptForever() {
  writeSupportPromptSuppression("never");
}

function suppressSupportPromptForDays(days) {
  const ms = Math.max(1, Number(days) || 1) * 24 * 60 * 60 * 1000;
  writeSupportPromptSuppression(String(Date.now() + ms));
}

function isSupportPromptSuppressed() {
  const marker = readSupportPromptSuppression();
  if (!marker) {
    return false;
  }
  if (marker === "never") {
    return true;
  }
  const until = Number(marker);
  return Number.isFinite(until) && until > Date.now();
}

function isPdfExportReady() {
  return typeof window.html2canvas === "function" && !!window.jspdf && !!window.jspdf.jsPDF;
}

function getPdfPageRenderSpec(pageElement) {
  const isLandscape = Boolean(pageElement?.classList?.contains("is-landscape"));
  return isLandscape
    ? { orientation: "landscape", widthMm: 297, heightMm: 210 }
    : { orientation: "portrait", widthMm: 210, heightMm: 297 };
}

async function buildPdfDocumentFromPages(pages) {
  const { jsPDF } = window.jspdf;
  if (!Array.isArray(pages) || pages.length === 0) {
    throw new Error("No pages available for PDF generation.");
  }
  const firstSpec = getPdfPageRenderSpec(pages[0]);
  const pdf = new jsPDF({ orientation: firstSpec.orientation, unit: "mm", format: "a4" });

  for (let idx = 0; idx < pages.length; idx += 1) {
    const page = pages[idx];
    const pageSpec = getPdfPageRenderSpec(page);
    const canvas = await renderExportPageToCanvas(page, { scale: PDF_EXPORT_SCALE });
    if (!canvas || canvas.width < 10 || canvas.height < 10) {
      throw new Error("Generated canvas is invalid.");
    }
    const imageData = canvas.toDataURL("image/png");
    if (idx > 0) {
      pdf.addPage("a4", pageSpec.orientation);
    }
    pdf.addImage(imageData, "PNG", 0, 0, pageSpec.widthMm, pageSpec.heightMm, undefined, PDF_IMAGE_COMPRESSION);
  }

  return pdf;
}

function queueSupportPrompt() {
  window.setTimeout(() => {
    if (typeof window.showSupportPrompt === "function") {
      window.showSupportPrompt({ force: true });
      return;
    }
    showSupportPrompt({ force: true });
  }, 260);
}

async function exportPdf() {
  setView("preview");

  if (!isPdfExportReady()) {
    alert("PDF export libraries not loaded. Use browser Print as fallback.");
    return;
  }

  const pages = getNonEmptyPageElements();
  if (!pages.length) {
    alert("No content to export.");
    return;
  }

  const originalText = refs.exportPdfBtn.textContent;
  refs.exportPdfBtn.textContent = "Exporting...";
  refs.exportPdfBtn.disabled = true;

  let exported = false;
  try {
    const pdf = await buildPdfDocumentFromPages(pages);
    const blob = pdf.output("blob");
    if (!(blob instanceof Blob) || blob.size < 1024) {
      throw new Error("Generated PDF is unexpectedly empty.");
    }
    pdf.save("python-midterm-cheatsheet.pdf");
    exported = true;
  } catch (error) {
    alert(`Could not export PDF: ${error?.message || "unknown error"}`);
  } finally {
    refs.exportPdfBtn.textContent = originalText;
    refs.exportPdfBtn.disabled = false;
  }

  if (exported) {
    queueSupportPrompt();
  }
}

function createHiddenPrintFrame(url) {
  const frame = document.createElement("iframe");
  frame.style.position = "fixed";
  frame.style.width = "0";
  frame.style.height = "0";
  frame.style.opacity = "0";
  frame.style.pointerEvents = "none";
  frame.style.border = "0";
  frame.src = url;
  document.body.appendChild(frame);
  return frame;
}

function waitForFrameLoad(frame) {
  return new Promise((resolve, reject) => {
    const cleanup = () => {
      frame.onload = null;
      frame.onerror = null;
    };
    frame.onload = () => {
      cleanup();
      resolve();
    };
    frame.onerror = () => {
      cleanup();
      reject(new Error("Failed to load printable PDF frame."));
    };
  });
}

function waitForPrintDialogClose(printWindow) {
  return new Promise((resolve) => {
    let settled = false;
    const finish = () => {
      if (settled) {
        return;
      }
      settled = true;
      try {
        printWindow.removeEventListener("afterprint", finish);
      } catch {
        // Ignore removal issues for cross-browser print windows.
      }
      resolve();
    };

    try {
      printWindow.addEventListener("afterprint", finish, { once: true });
    } catch {
      // Ignore browsers that do not allow binding this listener.
    }

    window.setTimeout(finish, 1800);
    printWindow.focus?.();
    printWindow.print?.();
  });
}

function cleanupFrameAndUrl(frame, url) {
  window.setTimeout(() => {
    if (frame?.parentNode) {
      frame.parentNode.removeChild(frame);
    }
    if (url) {
      URL.revokeObjectURL(url);
    }
  }, 3000);
}

async function printGeneratedPdf() {
  setView("preview");

  if (!isPdfExportReady()) {
    alert("PDF export libraries not loaded. Use browser Print as fallback.");
    return;
  }

  const pages = getNonEmptyPageElements();
  if (!pages.length) {
    alert("No content to print.");
    return;
  }

  const originalText = refs.printBtn.textContent;
  refs.printBtn.textContent = "Preparing PDF...";
  refs.printBtn.disabled = true;

  let frame = null;
  let url = "";
  let printTriggered = false;
  try {
    const pdf = await buildPdfDocumentFromPages(pages);
    const blob = pdf.output("blob");
    if (!(blob instanceof Blob) || blob.size < 1024) {
      throw new Error("Generated PDF is unexpectedly empty.");
    }

    url = URL.createObjectURL(blob);
    frame = createHiddenPrintFrame(url);
    await waitForFrameLoad(frame);

    const printWindow = frame.contentWindow;
    if (!printWindow) {
      throw new Error("Could not open printable PDF frame.");
    }
    await waitForPrintDialogClose(printWindow);
    printTriggered = true;
  } catch (error) {
    alert(`Could not generate printable PDF: ${error?.message || "unknown error"}`);
  } finally {
    refs.printBtn.textContent = originalText;
    refs.printBtn.disabled = false;
    cleanupFrameAndUrl(frame, url);
  }

  if (printTriggered) {
    queueSupportPrompt();
  }
}

function ensureSupportPromptModal() {
  if (supportPromptState.overlay) {
    return supportPromptState;
  }

  const overlay = document.getElementById("supportPromptOverlay");
  const acceptBtn = document.getElementById("supportPromptAcceptBtn");
  const declineBtn = document.getElementById("supportPromptDeclineBtn");
  const closeBtn = document.getElementById("supportPromptCloseBtn");
  if (!overlay || !acceptBtn || !declineBtn || !closeBtn) {
    return null;
  }

  supportPromptState.overlay = overlay;
  supportPromptState.acceptBtn = acceptBtn;
  supportPromptState.declineBtn = declineBtn;
  supportPromptState.closeBtn = closeBtn;

  if (!supportPromptState.eventsBound) {
    supportPromptState.eventsBound = true;

    const dismiss = () => {
      suppressSupportPromptForDays(SUPPORT_PROMPT_SNOOZE_DAYS);
      hideSupportPrompt();
    };
    closeBtn.addEventListener("click", dismiss);
    declineBtn.addEventListener("click", dismiss);
    overlay.addEventListener("click", (event) => {
      if (event.target === overlay) {
        dismiss();
      }
    });

    acceptBtn.addEventListener("click", () => {
      suppressSupportPromptForever();
      hideSupportPrompt();
      window.open(SUPPORT_PAGE_URL, "_blank", "noopener,noreferrer");
    });

    document.addEventListener("keydown", (event) => {
      if (!supportPromptState.active) {
        return;
      }
      if (event.key === "Escape") {
        event.preventDefault();
        dismiss();
      }
    });
  }

  return supportPromptState;
}

function showSupportPrompt(options = {}) {
  const force = Boolean(options?.force);
  const modal = ensureSupportPromptModal();
  if (!modal || modal.active) {
    return;
  }
  if (!force && isSupportPromptSuppressed()) {
    return;
  }

  modal.active = true;
  modal.overlay.classList.remove("hidden");
  document.body.classList.add("support-prompt-open");
  window.setTimeout(() => {
    modal.acceptBtn?.focus();
  }, 0);
}

function hideSupportPrompt() {
  if (!supportPromptState.active) {
    return;
  }
  supportPromptState.active = false;
  supportPromptState.overlay?.classList.add("hidden");
  document.body.classList.remove("support-prompt-open");
}

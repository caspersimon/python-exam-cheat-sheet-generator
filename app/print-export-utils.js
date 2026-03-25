const PRINT_EXPORT_STORAGE_PREFIX = "python_midterm_print_job_v1__";
const PRINT_EXPORT_MAX_JOBS = 8;
const PRINT_EXPORT_EVENT_TYPE = "python-cheatsheet-print-attempt";
const PRINT_EXPORT_STYLE_VARS = [
  "--sheet-font",
  "--sheet-font-size",
  "--sheet-title-size",
  "--sheet-line-height",
  "--sheet-letter-spacing",
  "--sheet-card-gap",
  "--sheet-card-padding",
  "--sheet-code-block-padding",
  "--sheet-code-block-margin",
  "--sheet-table-font-size",
  "--sheet-piece-gap",
  "--sheet-title-margin",
];

function pruneOldPrintJobs() {
  try {
    const jobs = [];
    for (let index = 0; index < window.localStorage.length; index += 1) {
      const key = window.localStorage.key(index);
      if (!key || !key.startsWith(PRINT_EXPORT_STORAGE_PREFIX)) {
        continue;
      }
      const raw = window.localStorage.getItem(key) || "";
      let createdAt = 0;
      try {
        createdAt = Number(JSON.parse(raw)?.createdAt || 0);
      } catch {
        createdAt = 0;
      }
      jobs.push({ key, createdAt });
    }
    jobs.sort((a, b) => b.createdAt - a.createdAt);
    jobs.slice(PRINT_EXPORT_MAX_JOBS).forEach((job) => {
      window.localStorage.removeItem(job.key);
    });
  } catch {
    // Ignore storage pruning failures.
  }
}

function collectPrintExportVariables() {
  const style = window.getComputedStyle(refs.sheetStage);
  return Object.fromEntries(
    PRINT_EXPORT_STYLE_VARS.map((name) => [name, style.getPropertyValue(name).trim() || refs.sheetStage.style.getPropertyValue(name).trim()])
  );
}

function buildPrintExportPages() {
  return getNonEmptyPageElements().map((pageElement, index) => {
    const rect = pageElement.getBoundingClientRect();
    return {
      pageNumber: index + 1,
      html: pageElement.outerHTML,
      logicalLandscape: Boolean(pageElement.classList.contains("is-landscape")),
      widthPx: Math.round(rect.width || 0),
      heightPx: Math.round(rect.height || 0),
    };
  });
}

function buildPrintExportPayload() {
  return {
    createdAt: Date.now(),
    sourcePath: window.location.pathname,
    title: document.title,
    styleVars: collectPrintExportVariables(),
    pages: buildPrintExportPages(),
  };
}

function storePrintExportPayload(payload) {
  const jobId = `${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
  const storageKey = `${PRINT_EXPORT_STORAGE_PREFIX}${jobId}`;
  window.localStorage.setItem(storageKey, JSON.stringify(payload));
  pruneOldPrintJobs();
  return storageKey;
}

function ensurePrintSupportPromptListener() {
  if (window.__printSupportPromptListenerBound) {
    return;
  }
  window.__printSupportPromptListenerBound = true;
  window.__pendingPrintSupportJobs = new Set();
  window.addEventListener("message", (event) => {
    if (event.origin !== window.location.origin) {
      return;
    }
    if (event.data?.type !== PRINT_EXPORT_EVENT_TYPE) {
      return;
    }
    const jobKey = String(event.data?.jobKey || "").trim();
    if (!jobKey || !window.__pendingPrintSupportJobs?.has(jobKey)) {
      return;
    }
    window.__pendingPrintSupportJobs.delete(jobKey);
    if (typeof queueSupportPrompt === "function") {
      queueSupportPrompt();
    }
  });
}

function openPrintView() {
  setView("preview");

  const pages = getNonEmptyPageElements();
  if (!pages.length) {
    alert("No content to print.");
    return;
  }

  const originalText = refs.printBtn.textContent;
  refs.printBtn.textContent = "Opening print view...";
  refs.printBtn.disabled = true;

  let storageKey = "";
  try {
    ensurePrintSupportPromptListener();
    const payload = buildPrintExportPayload();
    storageKey = storePrintExportPayload(payload);
    const printUrl = `./print.html?job=${encodeURIComponent(storageKey)}&autoprint=1`;
    const popup = window.open(printUrl, "_blank");
    if (!popup) {
      throw new Error("Popup blocked. Please allow popups for this site and try again.");
    }
    window.__pendingPrintSupportJobs?.add(storageKey);
  } catch (error) {
    if (storageKey) {
      try {
        window.localStorage.removeItem(storageKey);
      } catch {
        // Ignore cleanup failures.
      }
    }
    alert(`Could not open print view: ${error?.message || "unknown error"}`);
  } finally {
    refs.printBtn.textContent = originalText;
    refs.printBtn.disabled = false;
  }
}

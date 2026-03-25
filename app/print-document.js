const PRINT_AUTOPRINT_DELAY_MS = 220;
const PRINT_EXPORT_EVENT_TYPE = "python-cheatsheet-print-attempt";
const printDocumentState = {
  ready: false,
  autoPrintAttempted: false,
  sheetsRendered: 0,
  logicalLandscapePages: 0,
  jobKey: "",
};

function getPrintDocumentRefs() {
  return {
    host: document.getElementById("printDocumentHost"),
    status: document.getElementById("printDocumentStatus"),
    manualBtn: document.getElementById("printDocumentManualBtn"),
    shell: document.querySelector(".print-document-shell"),
  };
}

function readPrintJobKey() {
  const params = new URLSearchParams(window.location.search);
  return String(params.get("job") || "").trim();
}

function shouldAutoPrint() {
  const params = new URLSearchParams(window.location.search);
  return params.get("autoprint") === "1";
}

function readPrintPayload(jobKey) {
  if (!jobKey) {
    return null;
  }
  try {
    const raw = window.localStorage.getItem(jobKey);
    if (!raw) {
      return null;
    }
    window.localStorage.removeItem(jobKey);
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

function applyPrintStyleVariables(styleVars) {
  const root = document.documentElement;
  Object.entries(styleVars || {}).forEach(([name, value]) => {
    if (name && value) {
      root.style.setProperty(name, String(value));
    }
  });
}

function buildPrintSheet(pageData) {
  const sheet = document.createElement("section");
  sheet.className = "print-sheet";
  sheet.dataset.pageNumber = String(pageData.pageNumber || 0);

  const viewport = document.createElement("div");
  viewport.className = "print-sheet__viewport";
  if (pageData.logicalLandscape) {
    viewport.classList.add("is-logical-landscape");
  }

  const temp = document.createElement("div");
  temp.innerHTML = String(pageData.html || "");
  const pageNode = temp.firstElementChild;
  if (!(pageNode instanceof HTMLElement)) {
    return null;
  }

  if (pageData.logicalLandscape) {
    const rotated = document.createElement("div");
    rotated.className = "print-sheet__rotated";
    rotated.style.setProperty("--print-rotate-shift", `${pageData.heightPx || 794}px`);
    rotated.appendChild(pageNode);
    viewport.appendChild(rotated);
  } else {
    viewport.appendChild(pageNode);
  }

  sheet.appendChild(viewport);
  return sheet;
}

async function waitForPrintFontsReady() {
  if (!document.fonts?.ready) {
    return;
  }
  try {
    await document.fonts.ready;
  } catch {
    // Ignore font readiness failures and still show the print view.
  }
}

function notifyOpenerBeforePrint() {
  try {
    if (window.opener && !window.opener.closed) {
      window.opener.postMessage(
        {
          type: PRINT_EXPORT_EVENT_TYPE,
          jobKey: printDocumentState.jobKey,
        },
        window.location.origin
      );
    }
  } catch {
    // Ignore cross-window notification issues.
  }
}

function attemptAutoPrint() {
  printDocumentState.autoPrintAttempted = true;
  window.__printDocumentState = { ...printDocumentState };
  notifyOpenerBeforePrint();
  window.setTimeout(() => {
    window.print();
  }, PRINT_AUTOPRINT_DELAY_MS);
}

async function initPrintDocument() {
  const refs = getPrintDocumentRefs();
  const jobKey = readPrintJobKey();
  printDocumentState.jobKey = jobKey;
  window.__printDocumentState = { ...printDocumentState };

  refs.manualBtn?.addEventListener("click", () => {
    refs.status.textContent = "Opening the browser print dialog...";
    attemptAutoPrint();
  });

  const payload = readPrintPayload(jobKey);
  if (!payload || !Array.isArray(payload.pages) || payload.pages.length === 0) {
    refs.status.textContent = "Could not load the print payload. Go back to the app and try Print again.";
    return;
  }

  applyPrintStyleVariables(payload.styleVars || {});
  refs.host.innerHTML = "";

  payload.pages.forEach((pageData) => {
    const sheet = buildPrintSheet(pageData);
    if (!sheet) {
      return;
    }
    refs.host.appendChild(sheet);
  });

  await waitForPrintFontsReady();

  printDocumentState.ready = true;
  printDocumentState.sheetsRendered = refs.host.querySelectorAll(".print-sheet").length;
  printDocumentState.logicalLandscapePages = payload.pages.filter((page) => page.logicalLandscape).length;
  window.__printDocumentState = { ...printDocumentState };

  refs.shell?.classList.add("is-ready");
  refs.status.textContent = shouldAutoPrint()
    ? "If the print dialog does not appear, use the button on the right or press Cmd/Ctrl+P."
    : "Use the button on the right or press Cmd/Ctrl+P to print this clean view.";

  if (shouldAutoPrint()) {
    attemptAutoPrint();
  }
}

initPrintDocument();

#!/usr/bin/env node
const fs = require("fs");
const path = require("path");
const http = require("http");
const { chromium } = require("playwright");
const ROOT = path.resolve(__dirname, "..");

const MIME = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "application/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".pdf": "application/pdf",
  ".txt": "text/plain; charset=utf-8",
};

function startStaticServer(rootDir) {
  const server = http.createServer((req, res) => {
    try {
      const reqPath = decodeURIComponent((req.url || "/").split("?")[0]);
      const normalized = path.normalize(reqPath).replace(/^\/+/, "");
      let filePath = path.join(rootDir, normalized || "index.html");

      if (!filePath.startsWith(rootDir)) {
        res.writeHead(403, { "Content-Type": "text/plain; charset=utf-8" });
        res.end("Forbidden");
        return;
      }

      if (fs.existsSync(filePath) && fs.statSync(filePath).isDirectory()) {
        filePath = path.join(filePath, "index.html");
      }

      if (!fs.existsSync(filePath) || !fs.statSync(filePath).isFile()) {
        res.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
        res.end("Not found");
        return;
      }

      const ext = path.extname(filePath).toLowerCase();
      const type = MIME[ext] || "application/octet-stream";
      res.writeHead(200, { "Content-Type": type });
      fs.createReadStream(filePath).pipe(res);
    } catch (error) {
      res.writeHead(500, { "Content-Type": "text/plain; charset=utf-8" });
      res.end(`Server error: ${error.message}`);
    }
  });

  return new Promise((resolve, reject) => {
    server.on("error", reject);
    server.listen(0, "127.0.0.1", () => {
      const addr = server.address();
      resolve({ server, port: addr.port });
    });
  });
}

function toInt(text) {
  const n = parseInt(String(text || "").trim(), 10);
  return Number.isFinite(n) ? n : 0;
}

async function acceptNextDialog(page, action) {
  await Promise.all([
    page.waitForEvent("dialog", { timeout: 7000 }).then((dialog) => dialog.accept()),
    action(),
  ]);
}

async function installExportFlowStubs(page) {
  await page.evaluate(() => {
    window.__smokeExport = { supportPrompts: 0, saveCalls: 0, printCalls: 0, events: [], html2canvasModes: [] };
    window.showSupportPrompt = () => {
      window.__smokeExport.supportPrompts += 1;
      window.__smokeExport.events.push("support");
    };

    window.html2canvas = async (_node, options = {}) => {
      window.__smokeExport.html2canvasModes.push(Boolean(options.foreignObjectRendering));
      return {
        width: 100,
        height: 100,
        getContext: () => ({ getImageData: () => ({ data: [0, 0, 0, 255] }) }),
        toDataURL: () => "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADElEQVR4nGP4//8/AAX+Av5B7A7NAAAAAElFTkSuQmCC",
      };
    };
    window.jspdf = { jsPDF: function jsPDF() {} };

    window.buildPdfDocumentFromPages = async () => ({
      save: () => {
        window.__smokeExport.saveCalls += 1;
        window.__smokeExport.events.push("save");
      },
      output: () => new Blob([new Uint8Array(2400)], { type: "application/pdf" }),
    });

    const originalCreateElement = document.createElement.bind(document);
    document.createElement = function patchedCreateElement(tagName, ...rest) {
      const element = originalCreateElement(tagName, ...rest);
      if (String(tagName).toLowerCase() !== "iframe") {
        return element;
      }

      Object.defineProperty(element, "contentWindow", {
        configurable: true,
        value: {
          focus() {},
          print() {
            window.__smokeExport.printCalls += 1;
            window.__smokeExport.events.push("print");
          },
        },
      });

      queueMicrotask(() => {
        if (typeof element.onload === "function") {
          element.onload();
        }
      });
      return element;
    };

    window.URL.createObjectURL = () => "about:blank";
    window.URL.revokeObjectURL = () => {};
  });
}

async function collectDensityProbe(page) {
  return page.evaluate(() => {
    const card = document.querySelector(".preview-card");
    if (!card) {
      return null;
    }

    const head = card.querySelector(".preview-card-head");
    const body = card.querySelector(".preview-body");
    if (!head || !body) {
      return null;
    }

    const cardRect = card.getBoundingClientRect();
    const headRect = head.getBoundingClientRect();
    const bodyStyle = window.getComputedStyle(body);
    const headStyle = window.getComputedStyle(head);

    const sectionTitles = Array.from(card.querySelectorAll(".section-title"));
    const actionButtons = Array.from(card.querySelectorAll(".preview-mini-btn, .preview-head-btn"));
    const iconButtonsOnly = actionButtons.every((button) => {
      const text = button.textContent.replace(/\s+/g, "");
      return text.length <= 2;
    });

    const visibleActions = Array.from(card.querySelectorAll(".preview-item-actions")).filter((element) => {
      const style = window.getComputedStyle(element);
      return style.display !== "none" && style.visibility !== "hidden" && Number(style.opacity || "1") > 0.05;
    });
    const actionsAreaPx = visibleActions.reduce((sum, element) => {
      const rect = element.getBoundingClientRect();
      return sum + rect.width * rect.height;
    }, 0);

    const avg = (values) => {
      if (!values.length) {
        return 0;
      }
      return values.reduce((sum, value) => sum + value, 0) / values.length;
    };

    return {
      cardHeightPx: Number(cardRect.height.toFixed(2)),
      cardWidthPx: Number(cardRect.width.toFixed(2)),
      headerHeightPx: Number(headRect.height.toFixed(2)),
      headerRatio: Number((headRect.height / Math.max(1, cardRect.height)).toFixed(4)),
      headerPaddingTopPx: Number.parseFloat(headStyle.paddingTop || "0"),
      headerPaddingBottomPx: Number.parseFloat(headStyle.paddingBottom || "0"),
      bodyPaddingTopPx: Number.parseFloat(bodyStyle.paddingTop || "0"),
      sectionTitleMarginTopAvgPx: Number(
        avg(sectionTitles.map((element) => Number.parseFloat(window.getComputedStyle(element).marginTop || "0"))).toFixed(2)
      ),
      sectionTitleMarginBottomAvgPx: Number(
        avg(sectionTitles.map((element) => Number.parseFloat(window.getComputedStyle(element).marginBottom || "0"))).toFixed(2)
      ),
      actionsAreaRatio: Number((actionsAreaPx / Math.max(1, cardRect.width * cardRect.height)).toFixed(4)),
      iconButtonsOnly,
    };
  });
}

async function probeExportSnapshotLayout(page) {
  return page.evaluate(() => {
    const measure = () => {
      const card = document.querySelector(".preview-card");
      const head = card?.querySelector(".preview-card-head");
      const body = card?.querySelector(".preview-body");
      const cardRect = card?.getBoundingClientRect();
      const headRect = head?.getBoundingClientRect();
      const bodyRect = body?.getBoundingClientRect();
      return {
        cardHeightPx: Number((cardRect?.height || 0).toFixed(2)),
        cardWidthPx: Number((cardRect?.width || 0).toFixed(2)),
        headHeightPx: Number((headRect?.height || 0).toFixed(2)),
        bodyHeightPx: Number((bodyRect?.height || 0).toFixed(2)),
      };
    };

    const before = measure();
    document.body.classList.add("export-snapshot-mode");
    const isVisible = (element) => {
      if (!element) {
        return false;
      }
      const style = window.getComputedStyle(element);
      return style.display !== "none" && style.visibility !== "hidden" && Number(style.opacity || "1") > 0;
    };
    const hasVisible = (selector) => Array.from(document.querySelectorAll(selector)).some(isVisible);
    const head = document.querySelector(".preview-card-head");
    const card = document.querySelector(".preview-card");
    const body = document.querySelector(".preview-body");
    const after = measure();
    const headStyle = head ? window.getComputedStyle(head) : null;
    const headRect = head?.getBoundingClientRect();
    const cardRect = card?.getBoundingClientRect();
    const cardHeightDeltaPx = Number((after.cardHeightPx - before.cardHeightPx).toFixed(2));
    const cardWidthDeltaPx = Number((after.cardWidthPx - before.cardWidthPx).toFixed(2));
    const headHeightDeltaPx = Number((after.headHeightPx - before.headHeightPx).toFixed(2));
    const probe = {
      controlsHidden:
        !hasVisible(".preview-card-head-actions") &&
        !hasVisible(".preview-item-actions") &&
        !hasVisible(".preview-resize-bottom") &&
        !hasVisible(".preview-resize-corner"),
      layoutStable:
        Math.abs(cardHeightDeltaPx) <= 0.5 && Math.abs(cardWidthDeltaPx) <= 0.5 && Math.abs(headHeightDeltaPx) <= 0.5,
      cardHeightDeltaPx,
      cardWidthDeltaPx,
      headHeightDeltaPx,
      compactHeader:
        Number.parseFloat(headStyle?.paddingTop || "99") <= 2.5 &&
        Number.parseFloat(headStyle?.paddingBottom || "99") <= 2.5 &&
        Number.parseFloat(headStyle?.borderBottomWidth || "99") <= 0.5,
      headerRatio: Number(((headRect?.height || 0) / Math.max(1, cardRect?.height || 1)).toFixed(4)),
      bodyPaddingTopPx: Number.parseFloat(window.getComputedStyle(body || document.body).paddingTop || "0"),
    };
    return probe;
  });
}

async function run() {
  const artifactDir = path.join(ROOT, "data", "test_reports", "artifacts");
  fs.mkdirSync(artifactDir, { recursive: true });
  const { server, port } = await startStaticServer(ROOT);
  const url = `http://127.0.0.1:${port}/index.html`;
  const modifierKey = process.platform === "darwin" ? "Meta" : "Control";
  const undoShortcut = `${modifierKey}+z`;
  const consoleErrors = [];

  try {
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
    const page = await context.newPage();

    page.on("console", (msg) => {
      if (msg.type() === "error") {
        consoleErrors.push(msg.text());
      }
    });

    await page.goto(url, { waitUntil: "domcontentloaded", timeout: 60000 });
    await page.waitForSelector("#cardHost", { timeout: 20000 });
    await page.waitForFunction(
      () => !document.querySelector("#cardHost")?.textContent?.includes("Loading topic cards..."),
      { timeout: 30000 }
    );

    const title = await page.title();
    if (!title.includes("Python Midterm Cheat Sheet Builder")) {
      throw new Error(`Unexpected page title: ${title}`);
    }

    const splashVisible = await page.locator("#splashOverlay:not(.hidden)").count();
    if (splashVisible > 0) {
      await page.click("#getStartedBtn", { timeout: 5000 });
    }

    const selectableItems = page.locator("#cardHost [data-role='item-toggle']");
    if ((await selectableItems.count()) > 0) {
      await selectableItems.first().click({ timeout: 5000 });
    }

    const acceptedBefore = toInt(await page.textContent("#acceptedCount"));
    await page.click("#acceptBtn", { timeout: 5000 });
    await page.waitForTimeout(500);
    const acceptedAfter = toInt(await page.textContent("#acceptedCount"));
    if (acceptedAfter < acceptedBefore + 1) {
      throw new Error(`Accept action did not increment accepted count (${acceptedBefore} -> ${acceptedAfter})`);
    }

    await page.click("#goToPreviewBtn", { timeout: 5000 });
    await page.waitForSelector("#previewView.active", { timeout: 10000 });

    const previewCards = await page.locator(".preview-card").count();
    if (previewCards < 1) {
      throw new Error("Preview did not render any preview cards after accepting a topic");
    }
    const firstPreviewCard = page.locator(".preview-card").first();
    const lockBtn = firstPreviewCard.locator("[data-role='preview-toggle-lock']");
    if ((await lockBtn.count()) < 1) throw new Error("Preview card lock button was not found.");
    await firstPreviewCard.hover({ timeout: 5000 });
    const posBeforeLock = await firstPreviewCard.evaluate((el) => ({ left: el.style.left, top: el.style.top }));
    await lockBtn.click({ timeout: 5000 });
    await page.waitForFunction(() => document.querySelector(".preview-card")?.classList.contains("is-locked"), { timeout: 7000 });
    const lockedHeadBox = await firstPreviewCard.locator(".preview-card-head").boundingBox();
    if (!lockedHeadBox) throw new Error("Could not read locked card header bounds.");
    await page.mouse.move(lockedHeadBox.x + 24, lockedHeadBox.y + 12);
    await page.mouse.down();
    await page.mouse.move(lockedHeadBox.x + 132, lockedHeadBox.y + 72);
    await page.mouse.up();
    await page.waitForTimeout(150);
    const posAfterLockDrag = await firstPreviewCard.evaluate((el) => ({ left: el.style.left, top: el.style.top }));
    if (posBeforeLock.left !== posAfterLockDrag.left || posBeforeLock.top !== posAfterLockDrag.top) throw new Error("Locked preview card still moved during drag attempt.");
    await lockBtn.click({ timeout: 5000 });
    await page.waitForFunction(() => !document.querySelector(".preview-card")?.classList.contains("is-locked"), { timeout: 7000 });

    const firstEditButton = page.locator("[data-role='preview-edit-item']").first();
    if ((await firstEditButton.count()) < 1) {
      throw new Error("No editable preview item found.");
    }
    await page.locator(".preview-item-block").filter({ has: firstEditButton }).first().hover({ timeout: 5000 });
    const editableType = await firstEditButton.getAttribute("data-item-type");
    if (!editableType) {
      throw new Error("Editable preview item is missing data-item-type.");
    }

    const editedMarker = "[smoke] edited key point";
    await page.evaluate(() => {
      window.__useNativePromptEditing = false;
    });
    await firstEditButton.click({ timeout: 5000 });
    await page.waitForSelector("#previewEditModal:not(.hidden)", { timeout: 7000 });

    const modalInput = page.locator("#previewEditModal [data-preview-edit-input='true']").first();
    if ((await modalInput.count()) < 1) {
      throw new Error("Preview edit modal did not render editable input fields.");
    }

    const undoProbeSuffix = " [undo-probe]";
    await modalInput.focus({ timeout: 3000 });
    await page.keyboard.press("End");
    await page.keyboard.type(undoProbeSuffix);
    const typedValue = await modalInput.inputValue();
    if (!typedValue.endsWith(undoProbeSuffix)) {
      throw new Error("Preview edit modal input did not update before text undo check.");
    }
    await page.keyboard.press(undoShortcut);
    await page.waitForTimeout(120);
    const restoredValue = await modalInput.inputValue();
    if (restoredValue === typedValue) {
      throw new Error("Text undo inside preview edit modal was intercepted by app-level undo.");
    }

    await modalInput.fill(editedMarker);
    await page.click("#previewEditModalSaveBtn", { timeout: 5000 });
    await page.waitForSelector("#previewEditModal", { state: "hidden", timeout: 7000 });
    await page.waitForFunction((marker) => document.body.textContent.includes(marker), editedMarker, { timeout: 8000 });

    await page.keyboard.press(undoShortcut);
    await page.waitForFunction((marker) => !document.body.textContent.includes(marker), editedMarker, { timeout: 8000 });

    const typedDeleteSelector = `[data-role='preview-delete-item'][data-item-type='${editableType}']`;
    const deleteButtonsBefore = await page.locator(typedDeleteSelector).count();
    if (deleteButtonsBefore < 1) {
      throw new Error(`No deletable preview item found for type: ${editableType}`);
    }
    await page.locator(".preview-item-block").filter({ has: page.locator(typedDeleteSelector).first() }).first().hover({
      timeout: 5000,
    });
    await page.click(typedDeleteSelector, { timeout: 5000 });
    await page.waitForTimeout(300);
    const deleteButtonsAfter = await page.locator(typedDeleteSelector).count();
    if (deleteButtonsAfter >= deleteButtonsBefore) {
      throw new Error(`Preview item delete failed for type=${editableType} (${deleteButtonsBefore} -> ${deleteButtonsAfter}).`);
    }

    await page.click("#previewUndoBtn", { timeout: 5000 });
    await page.waitForTimeout(350);
    const deleteButtonsAfterUndo = await page.locator(typedDeleteSelector).count();
    if (deleteButtonsAfterUndo < deleteButtonsBefore) {
      throw new Error(
        `Preview undo did not restore item count for type=${editableType} (${deleteButtonsBefore} -> ${deleteButtonsAfterUndo}).`
      );
    }

    await page.locator(".preview-card").first().hover({ timeout: 5000 });
    await acceptNextDialog(page, async () => {
      await page.click("[data-role='preview-delete-card']", { timeout: 5000 });
    });
    await page.waitForTimeout(350);
    const previewAfterDelete = await page.locator(".preview-card").count();
    if (previewAfterDelete >= previewCards) {
      throw new Error("Preview delete action did not remove a card.");
    }

    await page.click("#previewUndoBtn", { timeout: 5000 });
    await page.waitForTimeout(300);
    const previewAfterUndo = await page.locator(".preview-card").count();
    if (previewAfterUndo < previewCards) {
      throw new Error("Preview undo did not restore the removed card.");
    }

    const densityProbe = await collectDensityProbe(page);
    if (!densityProbe) {
      throw new Error("Could not collect density probe from preview card.");
    }

    const realPdfByteSize = await page.evaluate(async () => ((await buildPdfDocumentFromPages(getNonEmptyPageElements())).output("blob")?.size || 0));
    if (realPdfByteSize < 1500) throw new Error(`Generated PDF blob looks empty (${realPdfByteSize} bytes).`);

    await installExportFlowStubs(page);
    await page.evaluate(async () => { const pages = getNonEmptyPageElements(); if (pages.length) await renderExportPageToCanvas(pages[0]); });
    await page.click("#exportPdfBtn", { timeout: 7000 });
    await page.waitForFunction(
      () => { const p = window.__smokeExport; const e = p?.events || []; const i = e.indexOf("save"); return !!p && p.saveCalls >= 1 && p.supportPrompts >= 1 && i >= 0 && e.indexOf("support") > i; },
      { timeout: 12000 }
    );

    await page.click("#printBtn", { timeout: 7000 });
    await page.waitForFunction(
      () => { const p = window.__smokeExport; const e = p?.events || []; const i = e.lastIndexOf("print"); return !!p && p.printCalls >= 1 && p.supportPrompts >= 2 && i >= 0 && e.slice(i + 1).includes("support"); },
      { timeout: 12000 }
    );
    await page.waitForFunction(() => (window.__smokeExport?.html2canvasModes || []).includes(false), { timeout: 8000 });

    const screenshotPath = path.join(ROOT, "docs", "smoke-preview.png");
    await page.screenshot({ path: screenshotPath, fullPage: true });
    const previewArtifactPath = path.join(artifactDir, "smoke-preview.png");
    await page.screenshot({ path: previewArtifactPath, fullPage: true });

    const exportStyleProbe = await probeExportSnapshotLayout(page);
    if (!exportStyleProbe.controlsHidden) {
      throw new Error("Export snapshot still contains editing/resize controls.");
    }
    if (!exportStyleProbe.layoutStable) {
      throw new Error(
        `Export snapshot changed card geometry (cardH=${exportStyleProbe.cardHeightDeltaPx}, cardW=${exportStyleProbe.cardWidthDeltaPx}, headH=${exportStyleProbe.headHeightDeltaPx}).`
      );
    }
    if (!exportStyleProbe.compactHeader) {
      throw new Error("Export snapshot header is not compact enough.");
    }

    const exportScreenshotPath = path.join(ROOT, "docs", "smoke-export-preview.png");
    await page.screenshot({ path: exportScreenshotPath, fullPage: true });
    const exportArtifactPath = path.join(artifactDir, "smoke-export-preview.png");
    await page.screenshot({ path: exportArtifactPath, fullPage: true });
    await page.evaluate(() => {
      document.body.classList.remove("export-snapshot-mode");
    });

    const blockingErrors = consoleErrors.filter(
      (line) => !line.includes("html2canvas") && !line.includes("jspdf")
    );
    if (blockingErrors.length > 0) {
      throw new Error(`Console errors detected: ${blockingErrors.slice(0, 3).join(" | ")}`);
    }

    const exportProbe = await page.evaluate(() => window.__smokeExport || null);
    await browser.close();
    console.log(
      JSON.stringify(
        {
          ok: true,
          url,
          previewCards,
          densityProbe,
          realPdfByteSize,
          exportProbe,
          exportStyleProbe,
          screenshotPath,
          exportScreenshotPath,
          previewArtifactPath,
          exportArtifactPath,
        },
        null,
        2
      )
    );
  } finally {
    server.close();
  }
}

run().catch((error) => {
  console.error(error.stack || error.message);
  process.exit(1);
});

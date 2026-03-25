#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");
const {
  addAllStagedSnippetsToCanvas,
  acceptCards,
  acceptNextDialog,
  dismissSplash,
  installExportFlowStubs,
  installPrintDialogStub,
  startStaticServer,
} = require("./lib/ui_playwright_common");
const {
  collectDensityProbe,
  probeExportSnapshotLayout,
} = require("./lib/ui_playwright_metrics");

const ROOT = path.resolve(__dirname, "..");
const ARTIFACT_DIR = path.join(ROOT, "data", "test_reports", "artifacts");

async function run() {
  fs.mkdirSync(ARTIFACT_DIR, { recursive: true });
  const { server, port } = await startStaticServer(ROOT);
  const url = `http://127.0.0.1:${port}/index.html`;
  const modifierKey = process.platform === "darwin" ? "Meta" : "Control";
  const undoShortcut = `${modifierKey}+z`;
  const consoleErrors = [];

  try {
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
    await installPrintDialogStub(context);
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
    if (!title.includes("Python Exam Cheat Sheet Builder")) {
      throw new Error(`Unexpected page title: ${title}`);
    }

    await dismissSplash(page);
    await page.waitForSelector(".topic-nav-item", { state: "attached", timeout: 20000 });

    const accepted = await acceptCards(page, 3);
    if (accepted < 2) {
      throw new Error(`Could not select enough topics for smoke test (${accepted}).`);
    }

    await page.click("#goToPreviewBtn", { timeout: 5000 });
    await page.waitForSelector("#previewView.active", { timeout: 10000 });
    await addAllStagedSnippetsToCanvas(page);

    const previewCards = await page.locator(".preview-card").count();
    if (previewCards < 1) {
      throw new Error("Preview did not render any preview cards after selecting content.");
    }
    if ((await page.locator(".preview-empty-copy").count()) > 0) {
      throw new Error("Preview rendered empty placeholder copy inside a card.");
    }

    const firstPreviewCard = page.locator(".preview-card").first();
    const lockBtn = firstPreviewCard.locator("[data-role='preview-toggle-lock']");
    if ((await lockBtn.count()) < 1) {
      throw new Error("Preview card lock button was not found.");
    }
    const firstCardHead = firstPreviewCard.locator(".preview-card-head");
    await firstCardHead.hover({ timeout: 5000 });
    const posBeforeLock = await firstPreviewCard.evaluate((el) => ({ left: el.style.left, top: el.style.top }));
    await lockBtn.click({ timeout: 5000, force: true });
    await page.waitForFunction(() => document.querySelector(".preview-card")?.classList.contains("is-locked"), { timeout: 7000 });
    const lockedHeadBox = await firstPreviewCard.locator(".preview-card-head").boundingBox();
    if (!lockedHeadBox) {
      throw new Error("Could not read locked card header bounds.");
    }
    await page.mouse.move(lockedHeadBox.x + 24, lockedHeadBox.y + 12);
    await page.mouse.down();
    await page.mouse.move(lockedHeadBox.x + 132, lockedHeadBox.y + 72);
    await page.mouse.up();
    await page.waitForTimeout(150);
    const posAfterLockDrag = await firstPreviewCard.evaluate((el) => ({ left: el.style.left, top: el.style.top }));
    if (posBeforeLock.left !== posAfterLockDrag.left || posBeforeLock.top !== posAfterLockDrag.top) {
      throw new Error("Locked preview card still moved during drag attempt.");
    }
    await firstCardHead.hover({ timeout: 5000 });
    await lockBtn.click({ timeout: 5000, force: true });
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
    await page.locator(".preview-item-block").filter({ has: page.locator(typedDeleteSelector).first() }).first().hover({ timeout: 5000 });
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
      throw new Error(`Preview undo did not restore item count for type=${editableType} (${deleteButtonsBefore} -> ${deleteButtonsAfterUndo}).`);
    }

    const deleteTargetCard = page.locator(".preview-card").first();
    const deleteTargetHead = deleteTargetCard.locator(".preview-card-head");
    await deleteTargetHead.hover({ timeout: 5000 });
    await acceptNextDialog(page, async () => {
      await deleteTargetHead.hover({ timeout: 5000 });
      await deleteTargetCard.locator("[data-role='preview-delete-card']").click({ timeout: 5000 });
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
    if (realPdfByteSize < 1500) {
      throw new Error(`Generated PDF blob looks empty (${realPdfByteSize} bytes).`);
    }

    await installExportFlowStubs(page, "__smokeExport", { pdfBlobSize: 2400 });
    await page.evaluate(async () => {
      const pages = getNonEmptyPageElements();
      if (pages.length) {
        await renderExportPageToCanvas(pages[0]);
      }
    });
    await page.click("#exportPdfBtn", { timeout: 7000 });
    await page.waitForFunction(
      () => {
        const probe = window.__smokeExport;
        const events = probe?.events || [];
        const saveIndex = events.indexOf("save");
        return !!probe && probe.saveCalls >= 1 && probe.supportPrompts >= 1 && saveIndex >= 0 && events.indexOf("support") > saveIndex;
      },
      { timeout: 12000 }
    );

    const [printPopup] = await Promise.all([
      page.waitForEvent("popup", { timeout: 12000 }),
      page.click("#printBtn", { timeout: 7000 }),
    ]);
    await printPopup.waitForLoadState("domcontentloaded", { timeout: 12000 });
    await printPopup.waitForSelector("#printDocumentHost .print-sheet", { timeout: 12000 });
    await printPopup.waitForFunction(() => window.__printDocumentState?.ready === true, { timeout: 12000 });
    await printPopup.waitForFunction(() => window.__printStubCalls >= 1, { timeout: 12000 });
    await page.waitForFunction(
      () => {
        const probe = window.__smokeExport;
        const events = probe?.events || [];
        const supportCount = probe?.supportPrompts || 0;
        return !!probe && supportCount >= 2;
      },
      { timeout: 12000 }
    );
    await page.waitForFunction(() => (window.__smokeExport?.html2canvasModes || []).includes(false), { timeout: 8000 });
    const printDocumentProbe = await printPopup.evaluate(() => ({
      state: window.__printDocumentState || null,
      printCalls: window.__printStubCalls || 0,
      url: window.location.pathname,
    }));
    if (!String(printDocumentProbe.url || "").includes("/print.html")) {
      throw new Error(`Print popup opened unexpected route: ${printDocumentProbe.url}`);
    }
    if ((printDocumentProbe.state?.sheetsRendered || 0) !== 1) {
      throw new Error(`Expected 1 print sheet, found ${printDocumentProbe.state?.sheetsRendered || 0}.`);
    }
    await page.evaluate(() => {
      if (window.__smokeExport) {
        window.__smokeExport.printCalls += 1;
        window.__smokeExport.events.push("print");
      }
    });
    await printPopup.close();

    const screenshotPath = path.join(ROOT, "docs", "smoke-preview.png");
    await page.screenshot({ path: screenshotPath, fullPage: true });
    const previewArtifactPath = path.join(ARTIFACT_DIR, "smoke-preview.png");
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
    const exportArtifactPath = path.join(ARTIFACT_DIR, "smoke-export-preview.png");
    await page.screenshot({ path: exportArtifactPath, fullPage: true });
    await page.evaluate(() => {
      document.body.classList.remove("export-snapshot-mode");
    });

    const blockingErrors = consoleErrors.filter((line) => !line.includes("html2canvas") && !line.includes("jspdf"));
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
          printDocumentProbe,
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

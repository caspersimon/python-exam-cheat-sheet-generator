#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");
const {
  acceptCards,
  acceptNextDialog,
  dismissSplash,
  installExportFlowStubs,
  startStaticServer,
} = require("./lib/ui_playwright_common");
const {
  collectLegibilityProbe,
  collectPreviewMetrics,
  probeExportSnapshotLayout,
} = require("./lib/ui_playwright_metrics");

const ROOT = path.resolve(__dirname, "..");
const ARTIFACT_DIR = path.join(ROOT, "data", "test_reports", "artifacts", "full-ui");
const TARGET_ACCEPTED_CARDS = 14;
const MIN_OCCUPIED_AREA_RATIO = 0.45;
const MAX_OVERLAP_AREA_RATIO = 0.02;
const MAX_HEADER_RATIO = 0.16;
const MIN_FONT_SIZE_PX = 6.5;
const MIN_LINE_HEIGHT = 0.95;

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
    const page = await context.newPage();

    page.on("console", (msg) => {
      if (msg.type() === "error") {
        consoleErrors.push(msg.text());
      }
    });

    await page.goto(url, { waitUntil: "domcontentloaded", timeout: 60000 });
    await page.waitForSelector("#cardHost", { timeout: 25000 });
    await page.waitForFunction(() => !document.querySelector("#cardHost")?.textContent?.includes("Loading topic cards..."), {
      timeout: 30000,
    });

    const title = await page.title();
    if (!title.includes("Python Exam Cheat Sheet Builder")) {
      throw new Error(`Unexpected page title: ${title}`);
    }

    await dismissSplash(page);
    await page.waitForSelector(".topic-nav-item", { state: "attached", timeout: 20000 });

    const accepted = await acceptCards(page, TARGET_ACCEPTED_CARDS);
    if (accepted < TARGET_ACCEPTED_CARDS) {
      throw new Error(`Could not select enough topics for full UI tests (selected=${accepted}).`);
    }

    await page.click("#goToPreviewBtn", { timeout: 7000 });
    await page.waitForSelector("#previewView.active", { timeout: 12000 });

    await page.evaluate(() => {
      const applyRange = (id, value) => {
        const element = document.getElementById(id);
        if (!element) return;
        element.value = String(value);
        element.dispatchEvent(new Event("input", { bubbles: true }));
      };
      applyRange("fontSizeRange", 8.5);
      applyRange("lineHeightRange", 1.05);
      applyRange("cardGapRange", 5);
      applyRange("cardPaddingRange", 6);
      applyRange("codeBlockPaddingRange", 7);
      applyRange("codeBlockMarginRange", 2);
      if (typeof state !== "undefined" && state && typeof state === "object") {
        state.previewCards = {};
        state.previewZCounter = 1;
      }
      if (typeof renderPreview === "function") {
        renderPreview();
      }
    });
    await page.waitForTimeout(200);

    const previewCards = await page.locator(".preview-card").count();
    if (previewCards < TARGET_ACCEPTED_CARDS) {
      throw new Error(`Expected at least ${TARGET_ACCEPTED_CARDS} preview cards, found ${previewCards}.`);
    }
    if ((await page.locator(".preview-empty-copy").count()) > 0) {
      throw new Error("Preview still rendered empty placeholder copy.");
    }

    const firstPreviewCard = page.locator(".preview-card").first();
    const lockBtn = firstPreviewCard.locator("[data-role='preview-toggle-lock']");
    if ((await lockBtn.count()) < 1) {
      throw new Error("Preview card lock button was not found.");
    }
    const firstCardBounds = await firstPreviewCard.boundingBox();
    if (!firstCardBounds) {
      throw new Error("Could not measure first preview card.");
    }

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
    const lockedAfterDrag = await firstPreviewCard.boundingBox();
    if (!lockedAfterDrag) {
      throw new Error("Could not remeasure locked preview card.");
    }
    if (Math.abs(lockedAfterDrag.x - firstCardBounds.x) > 0.5 || Math.abs(lockedAfterDrag.y - firstCardBounds.y) > 0.5) {
      throw new Error("Locked preview card still moved during drag attempt.");
    }

    await lockBtn.click({ timeout: 5000, force: true });
    await page.waitForFunction(() => !document.querySelector(".preview-card")?.classList.contains("is-locked"), { timeout: 7000 });

    const resizeHandle = firstPreviewCard.locator("[data-role='preview-resize-corner']");
    const resizeBox = await resizeHandle.boundingBox();
    if (!resizeBox) {
      throw new Error("Could not read resize handle bounds.");
    }
    await page.mouse.move(resizeBox.x + 4, resizeBox.y + 4);
    await page.mouse.down();
    await page.mouse.move(resizeBox.x + 64, resizeBox.y + 48);
    await page.mouse.up();
    await page.waitForTimeout(150);
    const resizedCardBox = await firstPreviewCard.boundingBox();
    if (!resizedCardBox) {
      throw new Error("Could not remeasure resized preview card.");
    }
    if (resizedCardBox.width <= firstCardBounds.width || resizedCardBox.height <= firstCardBounds.height) {
      throw new Error("Preview card resize did not increase card size.");
    }

    const firstEditButton = page.locator("[data-role='preview-edit-item']").first();
    if ((await firstEditButton.count()) < 1) {
      throw new Error("No editable preview item found.");
    }
    await page.locator(".preview-item-block").filter({ has: firstEditButton }).first().hover({ timeout: 5000 });
    const editableType = await firstEditButton.getAttribute("data-item-type");
    if (!editableType) {
      throw new Error("Editable preview item is missing data-item-type.");
    }

    const editedMarker = "[full-ui] edited key point";
    await page.evaluate(() => {
      window.__useNativePromptEditing = false;
    });
    await firstEditButton.click({ timeout: 5000 });
    await page.waitForSelector("#previewEditModal:not(.hidden)", { timeout: 7000 });

    const modalInput = page.locator("#previewEditModal [data-preview-edit-input='true']").first();
    if ((await modalInput.count()) < 1) {
      throw new Error("Preview edit modal did not render editable input fields.");
    }

    await modalInput.focus({ timeout: 3000 });
    await page.keyboard.press("End");
    await page.keyboard.type(" [undo-probe]");
    const typedValue = await modalInput.inputValue();
    if (!typedValue.endsWith("[undo-probe]")) {
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
      throw new Error(`Preview item delete failed for type=${editableType}`);
    }

    await page.click("#previewUndoBtn", { timeout: 5000 });
    await page.waitForTimeout(350);
    const deleteButtonsAfterUndo = await page.locator(typedDeleteSelector).count();
    if (deleteButtonsAfterUndo < deleteButtonsBefore) {
      throw new Error(`Preview undo did not restore item count for type=${editableType}.`);
    }

    const firstDeleteTargetCard = page.locator(".preview-card").first();
    const firstDeleteTargetHead = firstDeleteTargetCard.locator(".preview-card-head");
    await firstDeleteTargetHead.hover({ timeout: 5000 });
    await acceptNextDialog(page, async () => {
      await firstDeleteTargetHead.hover({ timeout: 5000 });
      await firstDeleteTargetCard.locator("[data-role='preview-delete-card']").click({ timeout: 5000 });
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

    const previewMetrics = await collectPreviewMetrics(page);
    const legibilityProbe = await collectLegibilityProbe(page);
    let realPdfByteSize = 0;
    try {
      realPdfByteSize = await page.evaluate(async () => ((await buildPdfDocumentFromPages(getNonEmptyPageElements())).output("blob")?.size || 0));
    } catch (error) {
      realPdfByteSize = 0;
    }

    const previewArtifactPath = path.join(ARTIFACT_DIR, "dense-preview.png");
    await page.screenshot({ path: previewArtifactPath, fullPage: true });

    await installExportFlowStubs(page, "__fullUiExport", { pdfBlobSize: 2600 });
    await page.evaluate(async () => {
      const pages = getNonEmptyPageElements();
      if (pages.length) {
        await renderExportPageToCanvas(pages[0]);
      }
    });
    await page.click("#exportPdfBtn", { timeout: 7000 });
    await page.waitForFunction(
      () => {
        const probe = window.__fullUiExport;
        const events = probe?.events || [];
        const saveIndex = events.indexOf("save");
        return !!probe && probe.saveCalls >= 1 && probe.supportPrompts >= 1 && saveIndex >= 0 && events.indexOf("support") > saveIndex;
      },
      { timeout: 12000 }
    );

    await page.click("#printBtn", { timeout: 7000 });
    await page.waitForFunction(
      () => {
        const probe = window.__fullUiExport;
        const events = probe?.events || [];
        const printIndex = events.lastIndexOf("print");
        return !!probe && probe.printCalls >= 1 && probe.supportPrompts >= 2 && printIndex >= 0 && events.slice(printIndex + 1).includes("support");
      },
      { timeout: 12000 }
    );
    await page.waitForFunction(() => (window.__fullUiExport?.html2canvasModes || []).includes(false), { timeout: 8000 });

    const exportStyleProbe = await probeExportSnapshotLayout(page);
    if (!exportStyleProbe.controlsHidden) {
      throw new Error("Export snapshot still contains editing/resize controls.");
    }
    if (!exportStyleProbe.layoutStable) {
      throw new Error("Export snapshot changed card geometry.");
    }
    if (!exportStyleProbe.compactHeader) {
      throw new Error("Export snapshot header is not compact enough.");
    }

    const exportArtifactPath = path.join(ARTIFACT_DIR, "dense-export-snapshot.png");
    await page.screenshot({ path: exportArtifactPath, fullPage: true });
    const exportProbe = await page.evaluate(() => window.__fullUiExport || null);

    const blockingErrors = consoleErrors.filter((line) => !line.includes("html2canvas") && !line.includes("jspdf"));
    if (blockingErrors.length > 0) {
      throw new Error(`Console errors detected: ${blockingErrors.slice(0, 3).join(" | ")}`);
    }

    const overflowCards = legibilityProbe.overflowCards;
    const occupiedAreaRatio = previewMetrics.occupiedAreaRatio;
    const overlapAreaRatio = previewMetrics.overlapAreaRatio;
    const minFontSizePx = legibilityProbe.minFontSizePx;
    const minLineHeight = legibilityProbe.minLineHeight;
    const minHeaderRatio = previewMetrics.headerRatioAvg;

    if (previewMetrics.outOfBoundsCount !== 0) {
      throw new Error(`Preview cards exceeded page bounds (${previewMetrics.outOfBoundsCount}).`);
    }
    if (occupiedAreaRatio < MIN_OCCUPIED_AREA_RATIO) {
      throw new Error(`Occupied area ratio too low (${occupiedAreaRatio}).`);
    }
    if (overlapAreaRatio > MAX_OVERLAP_AREA_RATIO) {
      throw new Error(`Overlap area ratio too high (${overlapAreaRatio}).`);
    }
    if (minHeaderRatio > MAX_HEADER_RATIO) {
      throw new Error(`Header ratio too high (${minHeaderRatio}).`);
    }
    if (minFontSizePx < MIN_FONT_SIZE_PX) {
      throw new Error(`Text too small for legibility (${minFontSizePx}px).`);
    }
    if (minLineHeight < MIN_LINE_HEIGHT) {
      throw new Error(`Line height too tight (${minLineHeight}).`);
    }
    if (overflowCards > 0) {
      throw new Error(`Some preview cards overflowed their bodies (${overflowCards}).`);
    }

    await browser.close();
    console.log(
      JSON.stringify(
        {
          ok: true,
          url,
          acceptedCards: accepted,
          previewCards,
          previewMetrics,
          legibilityProbe,
          realPdfByteSize,
          exportProbe,
          exportStyleProbe,
          previewArtifactPath,
          exportArtifactPath,
          summary: {
            occupiedAreaRatio,
            overlapAreaRatio,
            headerRatioAvg: previewMetrics.headerRatioAvg,
            minFontSizePx,
            minLineHeight,
            overflowCards,
            exportControlsHidden: exportStyleProbe.controlsHidden,
            exportLayoutStable: exportStyleProbe.layoutStable,
            exportHeaderRatio: exportStyleProbe.headerRatio,
          },
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

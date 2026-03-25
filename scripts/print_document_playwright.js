#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");
const {
  addAllStagedSnippetsToCanvas,
  acceptCards,
  dismissSplash,
  installPrintDialogStub,
  startStaticServer,
} = require("./lib/ui_playwright_common");

const ROOT = path.resolve(__dirname, "..");
const ARTIFACT_DIR = path.join(ROOT, "data", "test_reports", "artifacts", "print-document");

async function seedMixedOrientationLayout(page) {
  await page.evaluate(() => {
    const ids = Object.keys(state.previewCards || {});
    if (ids.length < 2) {
      throw new Error("Need at least two preview cards for print-document probe.");
    }
    const first = state.previewCards[ids[0]];
    const second = state.previewCards[ids[1]];
    if (!first || !second) {
      throw new Error("Missing preview card layouts for print-document probe.");
    }
    first.page = 1;
    first.x = 24;
    first.y = 28;
    second.page = 2;
    second.x = 34;
    second.y = 42;
    state.layout.page1Landscape = false;
    state.layout.page2Landscape = true;
    applyLayoutVariables();
    renderPreview();
  });
  await page.waitForTimeout(150);
}

async function run() {
  fs.mkdirSync(ARTIFACT_DIR, { recursive: true });
  const { server, port } = await startStaticServer(ROOT);
  const url = `http://127.0.0.1:${port}/index.html`;

  try {
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
    await installPrintDialogStub(context);
    const page = await context.newPage();

    await page.goto(url, { waitUntil: "domcontentloaded", timeout: 60000 });
    await page.waitForSelector("#cardHost", { timeout: 25000 });
    await page.waitForFunction(() => !document.querySelector("#cardHost")?.textContent?.includes("Loading topic cards..."), {
      timeout: 30000,
    });
    await dismissSplash(page);
    await page.waitForSelector(".topic-nav-item", { state: "attached", timeout: 20000 });

    const accepted = await acceptCards(page, 4, { itemsPerTopic: 2 });
    if (accepted < 2) {
      throw new Error(`Could not select enough topics for print document test (${accepted}).`);
    }

    await page.click("#goToPreviewBtn", { timeout: 7000 });
    await page.waitForSelector("#previewView.active", { timeout: 12000 });
    await addAllStagedSnippetsToCanvas(page);
    await seedMixedOrientationLayout(page);

    const [popup] = await Promise.all([
      page.waitForEvent("popup", { timeout: 12000 }),
      page.click("#printBtn", { timeout: 7000 }),
    ]);
    await popup.waitForLoadState("domcontentloaded", { timeout: 12000 });
    await popup.waitForSelector("#printDocumentHost .print-sheet", { timeout: 12000 });
    await popup.waitForFunction(() => window.__printDocumentState?.ready === true, { timeout: 12000 });
    await popup.waitForFunction(() => window.__printStubCalls >= 1, { timeout: 12000 });

    const probe = await popup.evaluate(() => ({
      state: window.__printDocumentState || null,
      printCalls: window.__printStubCalls || 0,
      sheetCount: document.querySelectorAll(".print-sheet").length,
      logicalLandscapeCount: document.querySelectorAll(".print-sheet__viewport.is-logical-landscape").length,
      rotatedCount: document.querySelectorAll(".print-sheet__rotated").length,
      hiddenControls: [
        ".preview-card-head-actions",
        ".preview-item-actions",
        ".preview-resize-bottom",
        ".preview-resize-corner",
      ].every((selector) => Array.from(document.querySelectorAll(selector)).every((node) => getComputedStyle(node).display === "none")),
      route: window.location.pathname,
    }));

    if (!String(probe.route || "").includes("/print.html")) {
      throw new Error(`Unexpected print route: ${probe.route}`);
    }
    if (probe.sheetCount !== 2) {
      throw new Error(`Expected exactly 2 print sheets, found ${probe.sheetCount}.`);
    }
    if (probe.logicalLandscapeCount !== 1 || probe.rotatedCount !== 1) {
      throw new Error(`Expected one rotated logical landscape page, got landscape=${probe.logicalLandscapeCount}, rotated=${probe.rotatedCount}.`);
    }
    if (!probe.hiddenControls) {
      throw new Error("Print document still renders edit/resize controls.");
    }

    const artifactPath = path.join(ARTIFACT_DIR, "print-document-mixed-orientation.png");
    await popup.screenshot({ path: artifactPath, fullPage: true });
    await popup.close();
    await browser.close();

    console.log(
      JSON.stringify(
        {
          ok: true,
          url,
          probe,
          artifactPath,
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

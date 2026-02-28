#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
const http = require("http");
const { chromium } = require("playwright");

const ROOT = path.resolve(__dirname, "..");
const ARTIFACT_DIR = path.join(ROOT, "data", "test_reports", "artifacts", "stress");

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

const SCENARIOS = [
  { name: "auto_default", autoGrid: true, fontSize: 9.5, lineHeight: 1.1, cardGap: 6, cardPadding: 7, letterSpacing: 0 },
  { name: "auto_dense_small", autoGrid: true, fontSize: 8.0, lineHeight: 1.0, cardGap: 4, cardPadding: 5, letterSpacing: -0.05 },
  { name: "auto_large_text", autoGrid: true, fontSize: 11.5, lineHeight: 1.3, cardGap: 5, cardPadding: 6, letterSpacing: 0.02 },
  { name: "auto_tight_lines", autoGrid: true, fontSize: 9.0, lineHeight: 0.95, cardGap: 5, cardPadding: 6, letterSpacing: 0 },
  { name: "auto_loose_lines", autoGrid: true, fontSize: 9.0, lineHeight: 1.35, cardGap: 5, cardPadding: 6, letterSpacing: 0 },
  { name: "manual_2x3", autoGrid: false, columns: 2, rows: 3, fontSize: 9.0, lineHeight: 1.05, cardGap: 5, cardPadding: 6, letterSpacing: 0 },
  { name: "manual_3x3", autoGrid: false, columns: 3, rows: 3, fontSize: 8.5, lineHeight: 1.0, cardGap: 4, cardPadding: 5, letterSpacing: 0 },
  { name: "manual_2x4", autoGrid: false, columns: 2, rows: 4, fontSize: 8.5, lineHeight: 1.0, cardGap: 4, cardPadding: 5, letterSpacing: 0 },
  { name: "manual_padding_high", autoGrid: false, columns: 2, rows: 3, fontSize: 9.0, lineHeight: 1.1, cardGap: 5, cardPadding: 12, letterSpacing: 0 },
  { name: "manual_padding_low", autoGrid: false, columns: 2, rows: 3, fontSize: 9.0, lineHeight: 1.1, cardGap: 4, cardPadding: 4, letterSpacing: 0 },
];

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
      res.writeHead(200, { "Content-Type": MIME[ext] || "application/octet-stream" });
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

async function dismissSplash(page) {
  const splashVisible = await page.locator("#splashOverlay:not(.hidden)").count();
  if (splashVisible > 0) {
    await page.click("#getStartedBtn", { timeout: 5000 });
  }
}

async function ensureCurrentCardHasSelection(page) {
  const selectable = page.locator("#cardHost [data-role='item-toggle']");
  if ((await selectable.count()) > 0) {
    const first = selectable.first();
    if (!(await first.isChecked().catch(() => false))) {
      await first.click({ timeout: 5000 });
    }
  }
}

async function acceptCards(page, target) {
  let loop = 0;
  while (loop < 180) {
    loop += 1;
    const activeCards = await page.locator("#activeTopicCard").count();
    const accepted = toInt(await page.textContent("#acceptedCount"));
    if (!activeCards || accepted >= target) {
      return accepted;
    }
    await ensureCurrentCardHasSelection(page);
    await page.click("#acceptBtn", { timeout: 6000 });
    await page.waitForTimeout(140);
  }
  return toInt(await page.textContent("#acceptedCount"));
}

async function applyScenario(page, scenario) {
  await page.evaluate((cfg) => {
    const setRange = (id, value) => {
      const element = document.getElementById(id);
      if (!element) {
        return;
      }
      element.value = String(value);
      element.dispatchEvent(new Event("input", { bubbles: true }));
    };
    const setToggle = (id, checked) => {
      const element = document.getElementById(id);
      if (!element) {
        return;
      }
      element.checked = Boolean(checked);
      element.dispatchEvent(new Event("change", { bubbles: true }));
    };

    setToggle("autoGridToggle", cfg.autoGrid);
    if (!cfg.autoGrid) {
      setRange("gridColumnsRange", cfg.columns || 2);
      setRange("gridRowsRange", cfg.rows || 3);
    }
    setRange("fontSizeRange", cfg.fontSize);
    setRange("lineHeightRange", cfg.lineHeight);
    setRange("cardGapRange", cfg.cardGap);
    setRange("cardPaddingRange", cfg.cardPadding);
    setRange("letterSpacingRange", cfg.letterSpacing);

    // Force a fresh grid placement for each scenario so metrics reflect the
    // current controls, not persisted drag/resize coordinates from a prior run.
    if (typeof state !== "undefined" && state && typeof state === "object") {
      state.previewCards = {};
      state.previewZCounter = 1;
    }
    if (typeof renderPreview === "function") {
      renderPreview();
    }
  }, scenario);
  await page.waitForTimeout(260);
}

async function collectLayoutMetrics(page) {
  return page.evaluate(() => {
    const pageContents = [document.querySelector("#page1Content"), document.querySelector("#page2Content")];
    const metrics = {
      totalCards: 0,
      outOfBoundsCount: 0,
      totalCardArea: 0,
      totalOverlapArea: 0,
      totalPageArea: 0,
      headerRatioSum: 0,
      headerRatioSamples: 0,
      pageBreakdown: [],
    };

    const overlapArea = (a, b) => {
      const x = Math.max(0, Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x));
      const y = Math.max(0, Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y));
      return x * y;
    };

    pageContents.forEach((pageEl, index) => {
      if (!pageEl) {
        return;
      }
      const pageRect = pageEl.getBoundingClientRect();
      const cards = Array.from(pageEl.querySelectorAll(".preview-card"));
      const rects = [];
      let pageCardArea = 0;
      let pageOverlapArea = 0;
      let pageOut = 0;

      cards.forEach((card) => {
        const rect = card.getBoundingClientRect();
        const x = rect.left - pageRect.left;
        const y = rect.top - pageRect.top;
        const w = rect.width;
        const h = rect.height;

        const clippedW = Math.max(0, Math.min(rect.right, pageRect.right) - Math.max(rect.left, pageRect.left));
        const clippedH = Math.max(0, Math.min(rect.bottom, pageRect.bottom) - Math.max(rect.top, pageRect.top));
        pageCardArea += clippedW * clippedH;
        rects.push({ x, y, w, h });

        if (x < -0.5 || y < -0.5 || x + w > pageRect.width + 0.5 || y + h > pageRect.height + 0.5) {
          pageOut += 1;
        }

        const header = card.querySelector(".preview-card-head");
        if (header) {
          metrics.headerRatioSum += header.getBoundingClientRect().height / Math.max(1, rect.height);
          metrics.headerRatioSamples += 1;
        }
      });

      for (let i = 0; i < rects.length; i += 1) {
        for (let j = i + 1; j < rects.length; j += 1) {
          pageOverlapArea += overlapArea(rects[i], rects[j]);
        }
      }

      const pageArea = pageRect.width * pageRect.height;
      metrics.totalCards += cards.length;
      metrics.outOfBoundsCount += pageOut;
      metrics.totalCardArea += pageCardArea;
      metrics.totalOverlapArea += pageOverlapArea;
      metrics.totalPageArea += pageArea;
      metrics.pageBreakdown.push({
        page: index + 1,
        cards: cards.length,
        outOfBoundsCount: pageOut,
        occupiedRatio: Number((pageCardArea / Math.max(1, pageArea)).toFixed(4)),
        overlapRatio: Number((pageOverlapArea / Math.max(1, pageArea)).toFixed(4)),
      });
    });

    const anyVisible = (selector) =>
      Array.from(document.querySelectorAll(selector)).some((el) => {
        const style = window.getComputedStyle(el);
        return style.display !== "none" && style.visibility !== "hidden" && Number(style.opacity || "1") > 0.05;
      });

    return {
      ...metrics,
      occupiedAreaRatio: Number((metrics.totalCardArea / Math.max(1, metrics.totalPageArea)).toFixed(4)),
      overlapAreaRatio: Number((metrics.totalOverlapArea / Math.max(1, metrics.totalPageArea)).toFixed(4)),
      headerRatioAvg: Number((metrics.headerRatioSum / Math.max(1, metrics.headerRatioSamples)).toFixed(4)),
      editChromeVisible: anyVisible(".preview-item-actions,.preview-card-head-actions"),
      activeControls: {
        autoGrid: document.getElementById("autoGridToggle")?.checked ?? null,
        gridColumnsLabel: document.getElementById("gridColumnsValue")?.textContent?.trim() || "",
        gridRowsLabel: document.getElementById("gridRowsValue")?.textContent?.trim() || "",
        fontSize: document.getElementById("fontSizeValue")?.textContent?.trim() || "",
        lineHeight: document.getElementById("lineHeightValue")?.textContent?.trim() || "",
        cardGap: document.getElementById("cardGapValue")?.textContent?.trim() || "",
        cardPadding: document.getElementById("cardPaddingValue")?.textContent?.trim() || "",
      },
    };
  });
}

function evaluateScenarioFailures(metrics) {
  const failures = [];
  if (metrics.outOfBoundsCount > 0) {
    failures.push(`out_of_bounds=${metrics.outOfBoundsCount}`);
  }
  if (metrics.overlapAreaRatio > 0.01) {
    failures.push(`overlap_ratio=${metrics.overlapAreaRatio}`);
  }
  if (metrics.occupiedAreaRatio < 0.42) {
    failures.push(`occupied_ratio=${metrics.occupiedAreaRatio}`);
  }
  if (metrics.headerRatioAvg > 0.16) {
    failures.push(`header_ratio=${metrics.headerRatioAvg}`);
  }
  return failures;
}

async function collectExportSnapshotProbe(page) {
  return page.evaluate(() => {
    document.body.classList.add("export-snapshot-mode");
    const isVisible = (selector) =>
      Array.from(document.querySelectorAll(selector)).some((el) => {
        const style = window.getComputedStyle(el);
        return style.display !== "none" && style.visibility !== "hidden" && Number(style.opacity || "1") > 0.05;
      });
    const head = document.querySelector(".preview-card-head");
    const card = document.querySelector(".preview-card");
    const headRect = head?.getBoundingClientRect();
    const cardRect = card?.getBoundingClientRect();
    return {
      controlsHidden:
        !isVisible(".preview-card-head-actions") &&
        !isVisible(".preview-item-actions") &&
        !isVisible(".preview-resize-bottom") &&
        !isVisible(".preview-resize-corner"),
      headerRatio: Number(((headRect?.height || 0) / Math.max(1, cardRect?.height || 1)).toFixed(4)),
    };
  });
}

async function run() {
  fs.mkdirSync(ARTIFACT_DIR, { recursive: true });
  const { server, port } = await startStaticServer(ROOT);
  const url = `http://127.0.0.1:${port}/index.html`;

  try {
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
    const page = await context.newPage();

    await page.goto(url, { waitUntil: "domcontentloaded", timeout: 60000 });
    await page.waitForSelector("#cardHost", { timeout: 25000 });
    await page.waitForFunction(() => !document.querySelector("#cardHost")?.textContent?.includes("Loading topic cards..."), {
      timeout: 30000,
    });
    await dismissSplash(page);

    const accepted = await acceptCards(page, 10);
    if (accepted < 8) {
      throw new Error(`Could not accept enough cards for stress tests (accepted=${accepted}).`);
    }
    await page.click("#goToPreviewBtn", { timeout: 7000 });
    await page.waitForSelector("#previewView.active", { timeout: 12000 });

    const scenarioResults = [];
    for (let idx = 0; idx < SCENARIOS.length; idx += 1) {
      const scenario = SCENARIOS[idx];
      await applyScenario(page, scenario);
      const metrics = await collectLayoutMetrics(page);
      const failures = evaluateScenarioFailures(metrics);
      const screenshotPath = path.join(ARTIFACT_DIR, `stress-${String(idx + 1).padStart(2, "0")}-${scenario.name}.png`);
      await page.screenshot({ path: screenshotPath, fullPage: true });
      scenarioResults.push({
        name: scenario.name,
        metrics,
        failures,
        screenshotPath,
      });
    }

    const exportSnapshotProbe = await collectExportSnapshotProbe(page);
    const exportScreenshotPath = path.join(ARTIFACT_DIR, "stress-export-snapshot.png");
    await page.screenshot({ path: exportScreenshotPath, fullPage: true });

    const minOccupiedAreaRatio = Math.min(...scenarioResults.map((item) => item.metrics.occupiedAreaRatio));
    const maxOverlapAreaRatio = Math.max(...scenarioResults.map((item) => item.metrics.overlapAreaRatio));
    const maxOutOfBounds = Math.max(...scenarioResults.map((item) => item.metrics.outOfBoundsCount));
    const failedScenarios = scenarioResults.filter((item) => item.failures.length > 0);
    const worstByUtilization = [...scenarioResults].sort((a, b) => a.metrics.occupiedAreaRatio - b.metrics.occupiedAreaRatio)[0];

    const payload = {
      ok: failedScenarios.length === 0,
      url,
      acceptedCards: accepted,
      scenarios: scenarioResults,
      summary: {
        scenariosRun: scenarioResults.length,
        scenariosFailed: failedScenarios.length,
        minOccupiedAreaRatio,
        maxOverlapAreaRatio,
        maxOutOfBounds,
        worstByUtilization: {
          name: worstByUtilization?.name || "",
          occupiedAreaRatio: worstByUtilization?.metrics?.occupiedAreaRatio || 0,
          screenshotPath: worstByUtilization?.screenshotPath || "",
        },
      },
      exportSnapshotProbe: {
        ...exportSnapshotProbe,
        screenshotPath: exportScreenshotPath,
      },
      artifactDir: ARTIFACT_DIR,
    };

    await browser.close();
    console.log(JSON.stringify(payload, null, 2));
    if (!payload.ok) {
      process.exit(1);
    }
  } finally {
    server.close();
  }
}

run().catch((error) => {
  console.error(error.stack || error.message);
  process.exit(1);
});

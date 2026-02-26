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
  const value = String(text || "").trim();
  const n = parseInt(value, 10);
  return Number.isFinite(n) ? n : 0;
}

async function run() {
  const { server, port } = await startStaticServer(ROOT);
  const url = `http://127.0.0.1:${port}/index.html`;
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

    const screenshotPath = path.join(ROOT, "docs", "smoke-preview.png");
    await page.screenshot({ path: screenshotPath, fullPage: true });

    const blockingErrors = consoleErrors.filter(
      (line) => !line.includes("html2canvas") && !line.includes("jspdf")
    );
    if (blockingErrors.length > 0) {
      throw new Error(`Console errors detected: ${blockingErrors.slice(0, 3).join(" | ")}`);
    }

    await browser.close();
    console.log(JSON.stringify({ ok: true, url, previewCards, screenshotPath }, null, 2));
  } finally {
    server.close();
  }
}

run().catch((error) => {
  console.error(error.stack || error.message);
  process.exit(1);
});

#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
const http = require("http");
const { chromium } = require("playwright");

const ROOT = path.resolve(__dirname, "..");
const ARTIFACT_DIR = path.join(ROOT, "data", "test_reports", "artifacts");

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

function toFilePathFromDataUrl(dataUrl, targetPath) {
  const marker = "base64,";
  const index = String(dataUrl || "").indexOf(marker);
  if (index < 0) {
    throw new Error("Expected base64 PNG data URL.");
  }
  const b64 = dataUrl.slice(index + marker.length);
  fs.writeFileSync(targetPath, Buffer.from(b64, "base64"));
}

async function collectCanvasProbe(page) {
  return page.evaluate(async () => {
    const pages = getNonEmptyPageElements();
    const results = [];

    for (let idx = 0; idx < pages.length; idx += 1) {
      const canvas = await renderExportPageToCanvas(pages[idx]);
      const ctx = canvas.getContext("2d", { willReadFrequently: true });
      if (!ctx) {
        throw new Error("Canvas 2D context unavailable for export probe.");
      }

      const w = canvas.width;
      const h = canvas.height;
      const step = Math.max(1, Math.floor(Math.min(w, h) / 700));
      let ink = 0;
      let bottomInk = 0;
      let minX = w;
      let minY = h;
      let maxX = -1;
      let maxY = -1;

      const bottomStart = Math.floor(h * 0.8);
      for (let y = 0; y < h; y += step) {
        for (let x = 0; x < w; x += step) {
          const [r, g, b, a] = ctx.getImageData(x, y, 1, 1).data;
          const isInk = a > 8 && (r < 246 || g < 246 || b < 246);
          if (!isInk) {
            continue;
          }
          ink += 1;
          if (y >= bottomStart) {
            bottomInk += 1;
          }
          if (x < minX) minX = x;
          if (y < minY) minY = y;
          if (x > maxX) maxX = x;
          if (y > maxY) maxY = y;
        }
      }

      const sampled = Math.max(1, Math.ceil(w / step) * Math.ceil(h / step));
      const bboxHeightRatio = maxY >= 0 ? (maxY - minY + 1) / Math.max(1, h) : 0;
      const bottomInkRatio = ink > 0 ? bottomInk / ink : 0;

      results.push({
        page: idx + 1,
        width: w,
        height: h,
        sampleStep: step,
        sampledPixels: sampled,
        sampledInkPixels: ink,
        sampledInkRatio: Number((ink / sampled).toFixed(5)),
        bboxHeightRatio: Number(bboxHeightRatio.toFixed(5)),
        bottomInkRatio: Number(bottomInkRatio.toFixed(5)),
        dataUrl: canvas.toDataURL("image/png"),
      });
    }

    const minBBoxHeightRatio = results.length ? Math.min(...results.map((item) => item.bboxHeightRatio)) : 0;
    const minBottomInkRatio = results.length ? Math.min(...results.map((item) => item.bottomInkRatio)) : 0;

    return {
      pagesDetected: pages.length,
      minBBoxHeightRatio: Number(minBBoxHeightRatio.toFixed(5)),
      minBottomInkRatio: Number(minBottomInkRatio.toFixed(5)),
      pages: results,
    };
  });
}

async function collectInlineWrapProbe(page) {
  return page.evaluate(async () => {
    const pageEl = refs.page1Content?.parentElement;
    if (!pageEl) {
      throw new Error("Page 1 element unavailable for inline-wrap probe.");
    }

    const wrapCases = [
      {
        id: "short_dictionary",
        width: 300,
        prefix: "Direct iteration over a dictionary (e.g.",
        code: "for key in dict_name",
        suffix: ") iterates over its keys.",
      },
      {
        id: "long_sorted_items",
        width: 230,
        prefix: "Use deterministic iteration when needed:",
        code: "for key, value in sorted(my_dictionary.items())",
        suffix: "to keep output stable.",
      },
      {
        id: "membership_chain",
        width: 210,
        prefix: "Membership checks can be chained with readability in mind:",
        code: "if user_id in active_users and role in allowed_roles",
        suffix: "before returning permissions.",
      },
    ];

    const host = document.createElement("div");
    host.id = "exportInlineWrapProbeHost";
    host.style.position = "absolute";
    host.style.left = "14px";
    host.style.top = "14px";
    host.style.width = "330px";
    host.style.padding = "3px 4px";
    host.style.background = "#fff";
    host.style.zIndex = "9999";
    host.style.pointerEvents = "none";
    host.innerHTML = wrapCases
      .map(
        (item, idx) => `
          <p
            class="export-inline-wrap-case"
            data-case-id="${item.id}"
            style="margin:${idx === 0 ? 0 : 8}px 0 0; line-height:1.18; width:${item.width}px;"
          >
            ${item.prefix}
            <code class="inline-code">${item.code}</code>
            ${item.suffix}
          </p>
        `
      )
      .join("");
    refs.page1Content.appendChild(host);

    try {
      const caseEls = Array.from(host.querySelectorAll(".export-inline-wrap-case"));
      const codeEl = host.querySelector("code.inline-code");
      if (!caseEls.length || !codeEl) {
        throw new Error("Inline-wrap probe host did not render expected elements.");
      }
      const readInlineStyle = () => {
        const style = window.getComputedStyle(codeEl);
        return {
          backgroundColor: style.backgroundColor,
          borderTopColor: style.borderTopColor,
          borderTopWidth: style.borderTopWidth,
          borderTopStyle: style.borderTopStyle,
          borderRadius: style.borderRadius,
          paddingTop: style.paddingTop,
          paddingRight: style.paddingRight,
          paddingBottom: style.paddingBottom,
          paddingLeft: style.paddingLeft,
          whiteSpace: style.whiteSpace,
          overflowWrap: style.overflowWrap,
          fontFamily: style.fontFamily,
          fontSize: style.fontSize,
        };
      };
      const norm = (value) => String(value || "").replace(/\s+/g, " ").trim().toLowerCase();
      const normalStyle = readInlineStyle();
      document.body.classList.add("export-snapshot-mode");
      const exportStyle = readInlineStyle();
      document.body.classList.remove("export-snapshot-mode");
      const styleParityKeys = [
        "backgroundColor",
        "borderTopColor",
        "borderTopWidth",
        "borderTopStyle",
        "borderRadius",
        "paddingTop",
        "paddingRight",
        "paddingBottom",
        "paddingLeft",
        "whiteSpace",
        "overflowWrap",
      ];
      const styleMismatches = styleParityKeys
        .filter((key) => norm(normalStyle[key]) !== norm(exportStyle[key]))
        .map((key) => ({
          key,
          normal: normalStyle[key],
          export: exportStyle[key],
        }));
      const styleParityOk = styleMismatches.length === 0;

      const pageRect = pageEl.getBoundingClientRect();
      const canvas = await renderExportPageToCanvas(pageEl, { scale: 2 });
      const ctx = canvas.getContext("2d", { willReadFrequently: true });
      if (!ctx) {
        throw new Error("Canvas 2D context unavailable for inline-wrap probe.");
      }

      const scaleX = canvas.width / Math.max(1, pageRect.width);
      const scaleY = canvas.height / Math.max(1, pageRect.height);

      const sampleInkRatio = (rx, ry, rw, rh) => {
        const step = Math.max(1, Math.floor(Math.min(rw, rh) / 80));
        let sampled = 0;
        let ink = 0;
        const maxX = Math.min(canvas.width, rx + rw);
        const maxY = Math.min(canvas.height, ry + rh);
        for (let py = ry; py < maxY; py += step) {
          for (let px = rx; px < maxX; px += step) {
            sampled += 1;
            const [r, g, b, a] = ctx.getImageData(px, py, 1, 1).data;
            if (a > 8 && (r < 246 || g < 246 || b < 246)) {
              ink += 1;
            }
          }
        }
        return { sampled: Math.max(1, sampled), ink, ratio: ink / Math.max(1, sampled) };
      };

      const caseResults = caseEls.map((element) => {
        const rect = element.getBoundingClientRect();
        const relX = rect.left - pageRect.left;
        const relY = rect.top - pageRect.top;
        const relW = rect.width;
        const relH = rect.height;
        const x = Math.max(0, Math.floor(relX * scaleX));
        const y = Math.max(0, Math.floor(relY * scaleY));
        const w = Math.max(10, Math.floor(relW * scaleX));
        const h = Math.max(10, Math.floor(relH * scaleY));
        const full = sampleInkRatio(x, y, w, h);
        const topLeft = sampleInkRatio(x, y, Math.max(10, Math.floor(w * 0.5)), Math.max(8, Math.floor(h * 0.55)));
        const bottom = sampleInkRatio(x, y + Math.floor(h * 0.45), w, Math.max(8, Math.floor(h * 0.55)));
        const ok = full.ratio >= 0.03 && topLeft.ratio >= 0.015 && bottom.ratio >= 0.01;
        return {
          id: element.getAttribute("data-case-id") || "",
          ok,
          fullInkRatio: Number(full.ratio.toFixed(5)),
          topLeftInkRatio: Number(topLeft.ratio.toFixed(5)),
          bottomInkRatio: Number(bottom.ratio.toFixed(5)),
          paragraphCanvasBox: { x, y, w, h },
        };
      });
      const minFullInkRatio = caseResults.length ? Math.min(...caseResults.map((item) => item.fullInkRatio)) : 0;
      const minTopLeftInkRatio = caseResults.length ? Math.min(...caseResults.map((item) => item.topLeftInkRatio)) : 0;
      const minBottomInkRatio = caseResults.length ? Math.min(...caseResults.map((item) => item.bottomInkRatio)) : 0;
      const wrapCasesOk = caseResults.every((item) => item.ok);
      const ok = styleParityOk && wrapCasesOk;

      return {
        ok,
        styleParityOk,
        wrapCasesOk,
        caseResults,
        styleMismatches,
        styleSample: { normal: normalStyle, export: exportStyle },
        minFullInkRatio: Number(minFullInkRatio.toFixed(5)),
        minTopLeftInkRatio: Number(minTopLeftInkRatio.toFixed(5)),
        minBottomInkRatio: Number(minBottomInkRatio.toFixed(5)),
        thresholds: {
          styleParityOk: true,
          fullInkRatio: 0.03,
          topLeftInkRatio: 0.015,
          bottomInkRatio: 0.01,
        },
        artifactDataUrl: canvas.toDataURL("image/png"),
      };
    } finally {
      host.remove();
    }
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
    await page.waitForFunction(
      () => !document.querySelector("#cardHost")?.textContent?.includes("Loading topic cards..."),
      { timeout: 30000 }
    );

    if ((await page.locator("#splashOverlay:not(.hidden)").count()) > 0) {
      await page.click("#getStartedBtn", { timeout: 5000 });
    }

    const selectableItems = page.locator("#cardHost [data-role='item-toggle']");
    if ((await selectableItems.count()) > 0) {
      await selectableItems.first().click({ timeout: 5000 });
    }
    await page.click("#acceptBtn", { timeout: 5000 });
    await page.waitForTimeout(350);
    await page.click("#goToPreviewBtn", { timeout: 5000 });
    await page.waitForSelector("#previewView.active", { timeout: 10000 });

    const previewCards = await page.locator(".preview-card").count();
    if (previewCards < 1) {
      throw new Error("No preview cards available for export canvas guard.");
    }

    const probe = await collectCanvasProbe(page);
    const inlineWrapProbe = await collectInlineWrapProbe(page);
    const artifactPaths = [];
    for (const item of probe.pages) {
      const artifactPath = path.join(ARTIFACT_DIR, `export-canvas-page-${item.page}.png`);
      toFilePathFromDataUrl(item.dataUrl, artifactPath);
      artifactPaths.push(artifactPath);
      delete item.dataUrl;
      item.artifactPath = artifactPath;
    }
    const inlineWrapArtifactPath = path.join(ARTIFACT_DIR, "export-inline-wrap-probe.png");
    toFilePathFromDataUrl(inlineWrapProbe.artifactDataUrl, inlineWrapArtifactPath);
    delete inlineWrapProbe.artifactDataUrl;
    inlineWrapProbe.artifactPath = inlineWrapArtifactPath;

    const ok =
      probe.pagesDetected >= 1 &&
      probe.minBBoxHeightRatio >= 0.55 &&
      probe.minBottomInkRatio >= 0.02 &&
      inlineWrapProbe.ok;

    await browser.close();
    console.log(
      JSON.stringify(
        {
          ok,
          url,
          thresholds: {
            minBBoxHeightRatio: 0.55,
            minBottomInkRatio: 0.02,
          },
          probe,
          inlineWrapProbe,
          artifactPaths,
          inlineWrapArtifactPath,
          primaryArtifactPath: artifactPaths[0] || "",
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

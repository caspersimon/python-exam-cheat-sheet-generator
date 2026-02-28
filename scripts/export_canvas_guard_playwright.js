#!/usr/bin/env node
const fs = require("fs");
const http = require("http");
const path = require("path");
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
      resolve({ server, port: server.address().port });
    });
  });
}
function toFilePathFromDataUrl(dataUrl, targetPath) {
  const marker = "base64,";
  const index = String(dataUrl || "").indexOf(marker);
  if (index < 0) {
    throw new Error("Expected base64 PNG data URL.");
  }
  fs.writeFileSync(targetPath, Buffer.from(dataUrl.slice(index + marker.length), "base64"));
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
          if (!isInk) continue;
          ink += 1;
          if (y >= bottomStart) bottomInk += 1;
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
    const pageContent = refs.page1Content;
    if (!pageEl || !pageContent) {
      throw new Error("Page 1 element unavailable for inline-wrap probe.");
    }
    const wrapCases = [
      {
        id: "short_dictionary",
        width: 284,
        prefix: "Direct iteration over a dictionary (e.g.",
        code: "for key in dict_name",
        suffix: ") iterates over its keys.",
        minCodeLines: 1,
      },
      {
        id: "long_sorted_items",
        width: 238,
        prefix: "Use deterministic iteration when needed:",
        code: "for key, value in sorted(my_dictionary.items())",
        suffix: "to keep output stable.",
        minCodeLines: 2,
      },
      {
        id: "membership_chain",
        width: 226,
        prefix: "Membership checks can be chained with readability in mind:",
        code: "if user_id in active_users and role in allowed_roles",
        suffix: "before returning permissions.",
        minCodeLines: 2,
      },
    ];
    const host = document.createElement("article");
    host.id = "exportInlineWrapProbeHost";
    host.className = "preview-card";
    Object.assign(host.style, {
      position: "absolute",
      left: "14px",
      top: "14px",
      width: "372px",
      minHeight: "0",
      background: "#fff",
      zIndex: "9999",
      pointerEvents: "none",
      borderRadius: "8px",
    });
    const body = document.createElement("div");
    body.className = "preview-body";
    body.style.paddingTop = "4px";
    body.style.paddingBottom = "5px";
    body.innerHTML = wrapCases
      .map(
        (item, idx) => `
          ${idx === 0 ? '<div class="section-title" style="margin-top:0;">Inline Wrap Probe</div>' : ""}
          <p class="section-paragraph export-inline-wrap-case" data-case-id="${item.id}" style="margin:${idx === 0 ? 2 : 8}px 0 0; width:${item.width}px;">
            <span class="export-inline-wrap-prefix">${item.prefix}</span>
            <code class="inline-code">${item.code}</code>
            <span class="export-inline-wrap-suffix">${item.suffix}</span>
          </p>
        `
      )
      .join("");
    host.appendChild(body);
    pageContent.appendChild(host);
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
          display: style.display,
          paddingTop: style.paddingTop,
          paddingRight: style.paddingRight,
          paddingBottom: style.paddingBottom,
          paddingLeft: style.paddingLeft,
          whiteSpace: style.whiteSpace,
          wordBreak: style.wordBreak,
          overflowWrap: style.overflowWrap,
          boxDecorationBreak: style.boxDecorationBreak,
          hyphens: style.hyphens,
        };
      };
      const norm = (value) => String(value || "").replace(/\s+/g, " ").trim().toLowerCase();
      const normalStyle = readInlineStyle();
      document.body.classList.add("export-snapshot-mode");
      const exportStyle = readInlineStyle();
      document.body.classList.remove("export-snapshot-mode");
      const styleKeys = [
        "backgroundColor",
        "borderTopColor",
        "borderTopWidth",
        "borderTopStyle",
        "borderRadius",
        "display",
        "paddingTop",
        "paddingRight",
        "paddingBottom",
        "paddingLeft",
        "whiteSpace",
        "wordBreak",
        "overflowWrap",
        "boxDecorationBreak",
        "hyphens",
      ];
      const styleMismatches = styleKeys
        .filter((key) => norm(normalStyle[key]) !== norm(exportStyle[key]))
        .map((key) => ({ key, normal: normalStyle[key], export: exportStyle[key] }));
      const styleParityOk = styleMismatches.length === 0;
      const pageRect = pageEl.getBoundingClientRect();
      const canvas = await renderExportPageToCanvas(pageEl, { scale: 2 });
      const ctx = canvas.getContext("2d", { willReadFrequently: true });
      if (!ctx) {
        throw new Error("Canvas 2D context unavailable for inline-wrap probe.");
      }
      const scaleX = canvas.width / Math.max(1, pageRect.width);
      const scaleY = canvas.height / Math.max(1, pageRect.height);
      const toRelative = (rect) => ({
        x: rect.left - pageRect.left,
        y: rect.top - pageRect.top,
        w: rect.width,
        h: rect.height,
      });
      const sampleRect = (rect, padX = 0, padY = 0) => {
        const relX = Math.max(0, rect.x - padX);
        const relY = Math.max(0, rect.y - padY);
        const relW = Math.max(6, rect.w + padX * 2);
        const relH = Math.max(6, rect.h + padY * 2);
        const rx = Math.max(0, Math.floor(relX * scaleX));
        const ry = Math.max(0, Math.floor(relY * scaleY));
        const rw = Math.max(6, Math.floor(relW * scaleX));
        const rh = Math.max(6, Math.floor(relH * scaleY));
        const step = Math.max(1, Math.floor(Math.min(rw, rh) / 80));
        const image = ctx.getImageData(rx, ry, rw, rh).data;
        let sampled = 0;
        let ink = 0;
        let tint = 0;
        let minInkX = rw;
        let sawInk = false;
        for (let localY = 0; localY < rh; localY += step) {
          for (let localX = 0; localX < rw; localX += step) {
            const idx = (localY * rw + localX) * 4;
            sampled += 1;
            const r = image[idx];
            const g = image[idx + 1];
            const b = image[idx + 2];
            const a = image[idx + 3];
            const isInk = a > 8 && (r < 246 || g < 246 || b < 246);
            if (isInk) {
              ink += 1;
              sawInk = true;
              if (localX < minInkX) minInkX = localX;
            }
            const spread = Math.max(r, g, b) - Math.min(r, g, b);
            const isCodeTint = a > 8 && r >= 220 && g >= 220 && b >= 220 && r <= 252 && g <= 252 && b <= 252 && spread <= 18;
            if (isCodeTint) tint += 1;
          }
        }
        const denom = Math.max(1, sampled);
        return {
          sampled: denom,
          inkRatio: ink / denom,
          tintRatio: tint / denom,
          minInkXRatio: sawInk ? minInkX / Math.max(1, rw) : 1,
          canvasBox: { x: rx, y: ry, w: rw, h: rh },
        };
      };
      const sampleOutsideTintRatio = (paragraphBox, codeBox) => {
        const px = Math.max(0, Math.floor(paragraphBox.x));
        const py = Math.max(0, Math.floor(paragraphBox.y));
        const pw = Math.max(6, Math.floor(paragraphBox.w));
        const ph = Math.max(6, Math.floor(paragraphBox.h));
        const step = Math.max(1, Math.floor(Math.min(pw, ph) / 80));
        const image = ctx.getImageData(px, py, pw, ph).data;
        const codeLeft = Math.floor(codeBox.x);
        const codeTop = Math.floor(codeBox.y);
        const codeRight = codeLeft + Math.floor(codeBox.w);
        const codeBottom = codeTop + Math.floor(codeBox.h);
        let sampledOutside = 0;
        let tintedOutside = 0;
        for (let localY = 0; localY < ph; localY += step) {
          const globalY = py + localY;
          for (let localX = 0; localX < pw; localX += step) {
            const globalX = px + localX;
            const inCode = globalX >= codeLeft && globalX < codeRight && globalY >= codeTop && globalY < codeBottom;
            if (inCode) continue;
            sampledOutside += 1;
            const idx = (localY * pw + localX) * 4;
            const r = image[idx];
            const g = image[idx + 1];
            const b = image[idx + 2];
            const a = image[idx + 3];
            const spread = Math.max(r, g, b) - Math.min(r, g, b);
            const isCodeTint = a > 8 && r >= 220 && g >= 220 && b >= 220 && r <= 252 && g <= 252 && b <= 252 && spread <= 18;
            if (isCodeTint) tintedOutside += 1;
          }
        }
        if (sampledOutside < 1) return 0;
        return tintedOutside / sampledOutside;
      };
      const caseResults = caseEls.map((element) => {
        const caseId = element.getAttribute("data-case-id") || "";
        const config = wrapCases.find((item) => item.id === caseId) || wrapCases[0];
        const code = element.querySelector("code.inline-code");
        const prefix = element.querySelector(".export-inline-wrap-prefix");
        const suffix = element.querySelector(".export-inline-wrap-suffix");
        if (!code || !prefix || !suffix) {
          return { id: caseId, ok: false, error: "Expected probe spans are missing." };
        }
        const range = document.createRange();
        range.selectNodeContents(code);
        const lineRectsRaw = Array.from(range.getClientRects()).filter((lineRect) => lineRect.width > 1 && lineRect.height > 1);
        const lineRects = (lineRectsRaw.length ? lineRectsRaw : [code.getBoundingClientRect()]).map(toRelative);
        const codeRect = toRelative(code.getBoundingClientRect());
        const prefixRect = toRelative(prefix.getBoundingClientRect());
        const suffixRect = toRelative(suffix.getBoundingClientRect());
        const paragraphRect = toRelative(element.getBoundingClientRect());
        const codeMetrics = sampleRect(codeRect, 2, 2);
        const prefixMetrics = sampleRect(prefixRect, 1, 1);
        const suffixMetrics = sampleRect(suffixRect, 1, 1);
        const paragraphMetrics = sampleRect(paragraphRect, 1, 1);
        const outsideTintRatio = sampleOutsideTintRatio(paragraphMetrics.canvasBox, codeMetrics.canvasBox);
        const minStarts = lineRects.map((lineRect) => sampleRect(lineRect, 1, 1).minInkXRatio);
        const firstLineStart = minStarts[0] ?? 1;
        const lineStartDrift = minStarts.length > 1 ? Math.max(...minStarts) - Math.min(...minStarts) : 0;
        const hasExpectedWrap = lineRects.length >= (config.minCodeLines || 1);
        const ok =
          hasExpectedWrap &&
          codeMetrics.inkRatio >= 0.02 &&
          prefixMetrics.inkRatio >= 0.008 &&
          suffixMetrics.inkRatio >= 0.008 &&
          outsideTintRatio <= 0.45 &&
          (lineRects.length < 2 || firstLineStart <= 0.6) &&
          (lineRects.length < 2 || lineStartDrift <= 0.55);
        return {
          id: caseId,
          ok,
          minCodeLines: config.minCodeLines || 1,
          actualCodeLines: lineRects.length,
          codeInkRatio: Number(codeMetrics.inkRatio.toFixed(5)),
          prefixInkRatio: Number(prefixMetrics.inkRatio.toFixed(5)),
          suffixInkRatio: Number(suffixMetrics.inkRatio.toFixed(5)),
          outsideTintRatio: Number(outsideTintRatio.toFixed(5)),
          firstLineStartRatio: Number(firstLineStart.toFixed(5)),
          maxLineStartDrift: Number(lineStartDrift.toFixed(5)),
          paragraphCanvasBox: paragraphMetrics.canvasBox,
        };
      });
      const wrapCasesOk = caseResults.every((item) => item.ok);
      const ok = styleParityOk && wrapCasesOk;
      const minCodeInkRatio = caseResults.length ? Math.min(...caseResults.map((item) => item.codeInkRatio || 0)) : 0;
      const minPrefixInkRatio = caseResults.length ? Math.min(...caseResults.map((item) => item.prefixInkRatio || 0)) : 0;
      const minSuffixInkRatio = caseResults.length ? Math.min(...caseResults.map((item) => item.suffixInkRatio || 0)) : 0;
      const maxFirstLineStartRatio = caseResults.length ? Math.max(...caseResults.map((item) => item.firstLineStartRatio || 0)) : 0;
      const maxLineStartDrift = caseResults.length ? Math.max(...caseResults.map((item) => item.maxLineStartDrift || 0)) : 0;
      return {
        ok,
        styleParityOk,
        wrapCasesOk,
        passingCases: caseResults.filter((item) => item.ok).length,
        totalCases: caseResults.length,
        caseResults,
        styleMismatches,
        minCodeInkRatio: Number(minCodeInkRatio.toFixed(5)),
        minPrefixInkRatio: Number(minPrefixInkRatio.toFixed(5)),
        minSuffixInkRatio: Number(minSuffixInkRatio.toFixed(5)),
        maxFirstLineStartRatio: Number(maxFirstLineStartRatio.toFixed(5)),
        maxLineStartDrift: Number(maxLineStartDrift.toFixed(5)),
        thresholds: {
          styleParityOk: true,
          minCodeInkRatio: 0.02,
          minPrefixInkRatio: 0.008,
          minSuffixInkRatio: 0.008,
          outsideTintRatio: 0.45,
          firstLineStartRatio: 0.6,
          lineStartDrift: 0.55,
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
    if ((await page.locator(".preview-card").count()) < 1) {
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

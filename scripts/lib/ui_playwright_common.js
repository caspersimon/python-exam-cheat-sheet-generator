const fs = require("fs");
const http = require("http");
const path = require("path");

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

      res.writeHead(200, { "Content-Type": MIME[path.extname(filePath).toLowerCase()] || "application/octet-stream" });
      fs.createReadStream(filePath).pipe(res);
    } catch (error) {
      res.writeHead(500, { "Content-Type": "text/plain; charset=utf-8" });
      res.end(`Server error: ${error.message}`);
    }
  });

  return new Promise((resolve, reject) => {
    server.on("error", reject);
    server.listen(0, "127.0.0.1", () => resolve({ server, port: server.address().port }));
  });
}

function toInt(text) {
  const n = parseInt(String(text || "").trim(), 10);
  return Number.isFinite(n) ? n : 0;
}

async function acceptNextDialog(page, action) {
  await Promise.all([page.waitForEvent("dialog", { timeout: 7000 }).then((dialog) => dialog.accept()), action()]);
}

async function dismissSplash(page) {
  if ((await page.locator("#splashOverlay:not(.hidden)").count()) > 0) {
    await page.click("#getStartedBtn", { timeout: 5000 });
  }
}

async function expandAllWeeks(page) {
  const toggles = page.locator(".topic-week-toggle");
  const count = await toggles.count();
  for (let index = 0; index < count; index += 1) {
    const toggle = toggles.nth(index);
    const expanded = await toggle.getAttribute("aria-expanded");
    if (expanded !== "true") {
      await toggle.click({ timeout: 5000 });
      await page.waitForTimeout(50);
    }
  }
}

async function openTopicAtIndex(page, index) {
  const topic = page.locator(".topic-nav-item:visible").nth(index);
  if ((await topic.count()) < 1) {
    return false;
  }
  await topic.click({ timeout: 5000 });
  await page.waitForSelector(".topic-detail-card", { timeout: 10000 });
  await page.waitForTimeout(80);
  return true;
}

async function selectItemsInCurrentTopic(page, maxItems = 1) {
  const toggles = page.locator(".topic-detail-card [data-role='item-toggle']");
  const count = await toggles.count();
  let selected = 0;
  for (let index = 0; index < count && selected < maxItems; index += 1) {
    const toggle = toggles.nth(index);
    if (!(await toggle.isChecked().catch(() => false))) {
      await toggle.click({ timeout: 5000 });
      selected += 1;
      await page.waitForTimeout(40);
    }
  }
  return selected;
}

async function acceptCards(page, target, options = {}) {
  const itemsPerTopic = Math.max(1, Number(options.itemsPerTopic) || 1);
  await expandAllWeeks(page);
  const topicButtons = page.locator(".topic-nav-item:visible");
  const totalTopics = await topicButtons.count();

  for (let index = 0; index < totalTopics; index += 1) {
    const selectedTopics = toInt(await page.textContent("#acceptedCount"));
    if (selectedTopics >= target) {
      return selectedTopics;
    }
    const opened = await openTopicAtIndex(page, index);
    if (!opened) {
      break;
    }
    await selectItemsInCurrentTopic(page, itemsPerTopic);
  }

  return toInt(await page.textContent("#acceptedCount"));
}

async function addAllStagedSnippetsToCanvas(page) {
  const addAllButton = page.locator("#addAllStagedBtn");
  if ((await addAllButton.count()) < 1) {
    return 0;
  }

  const stagedCountBefore = toInt(await page.textContent("#stagedSnippetCount").catch(() => "0"));
  if (stagedCountBefore < 1) {
    return 0;
  }

  await addAllButton.click({ timeout: 5000 });
  await page.waitForFunction(
    () => {
      const staged = Number.parseInt(document.querySelector("#stagedSnippetCount")?.textContent || "0", 10);
      const cards = document.querySelectorAll(".preview-card").length;
      return cards > 0 || staged === 0;
    },
    { timeout: 10000 }
  );

  return stagedCountBefore;
}

async function installExportFlowStubs(page, namespace, options = {}) {
  const pdfBlobSize = Number(options.pdfBlobSize) || 2400;
  await page.evaluate(
    ({ namespace: ns, pdfBlobSize: blobSize }) => {
      window[ns] = { supportPrompts: 0, saveCalls: 0, printCalls: 0, events: [], html2canvasModes: [] };
      const bucket = window[ns];
      window.showSupportPrompt = () => {
        bucket.supportPrompts += 1;
        bucket.events.push("support");
      };
      window.html2canvas = async (_node, renderOptions = {}) => {
        bucket.html2canvasModes.push(Boolean(renderOptions.foreignObjectRendering));
        return {
          width: 100,
          height: 100,
          getContext: () => ({ getImageData: () => ({ data: [0, 0, 0, 255] }) }),
          toDataURL: () =>
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADElEQVR4nGP4//8/AAX+Av5B7A7NAAAAAElFTkSuQmCC",
        };
      };
      window.jspdf = { jsPDF: function jsPDF() {} };
      window.buildPdfDocumentFromPages = async () => ({
        save: () => {
          bucket.saveCalls += 1;
          bucket.events.push("save");
        },
        output: () => new Blob([new Uint8Array(blobSize)], { type: "application/pdf" }),
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
              bucket.printCalls += 1;
              bucket.events.push("print");
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
    },
    { namespace, pdfBlobSize }
  );
}

async function installPrintDialogStub(context) {
  await context.addInitScript(() => {
    window.__printStubCalls = 0;
    const originalPrint = window.print ? window.print.bind(window) : null;
    window.print = function patchedPrint() {
      window.__printStubCalls += 1;
      return undefined;
    };
    window.__originalPrintForTests = originalPrint;
  });
}

module.exports = {
  addAllStagedSnippetsToCanvas,
  acceptCards,
  acceptNextDialog,
  dismissSplash,
  expandAllWeeks,
  installExportFlowStubs,
  installPrintDialogStub,
  openTopicAtIndex,
  selectItemsInCurrentTopic,
  startStaticServer,
  toInt,
};

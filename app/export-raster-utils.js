function getExportHost() {
  let host = document.getElementById("exportRenderHost");
  if (host) {
    return host;
  }

  host = document.createElement("div");
  host.id = "exportRenderHost";
  Object.assign(host.style, {
    position: "fixed",
    left: "-20000px",
    top: "0",
    width: "0",
    height: "0",
    overflow: "hidden",
    opacity: "0",
    pointerEvents: "none",
    zIndex: "-1",
    contain: "layout style paint",
  });
  document.body.appendChild(host);
  return host;
}

function buildFrozenExportPage(pageElement, options = {}) {
  if (!pageElement) {
    throw new Error("Export page element is missing.");
  }

  const pageRect = pageElement.getBoundingClientRect();
  if (pageRect.width < 10 || pageRect.height < 10) {
    throw new Error("Export page is not visible or has invalid dimensions.");
  }

  const pageSpec = getExportPageRenderSpec(pageElement, options.targetDpi);
  const host = getExportHost();
  host.innerHTML = "";

  const wrapper = document.createElement("div");
  wrapper.className = "export-frozen-page-wrapper";
  Object.assign(wrapper.style, {
    position: "relative",
    width: `${pageRect.width}px`,
    height: `${pageRect.height}px`,
    overflow: "hidden",
    background: "#ffffff",
  });

  const clonePage = pageElement.cloneNode(true);
  clonePage.__sourcePageRef = pageElement;
  clonePage.setAttribute("data-export-frozen", "true");
  clonePage.classList.add("export-frozen-page");
  Object.assign(clonePage.style, {
    position: "relative",
    width: `${pageRect.width}px`,
    height: `${pageRect.height}px`,
    overflow: "hidden",
    margin: "0",
    border: "none",
    borderRadius: "0",
    boxShadow: "none",
    background: "#fffefb",
  });

  wrapper.appendChild(clonePage);
  host.appendChild(wrapper);

  traverseSourceAndClone(pageElement, clonePage, (sourceNode, cloneNode) => {
    hideExportChromeInClone(sourceNode, cloneNode);
    copyComputedStyles(sourceNode, cloneNode);
    freezeNodeBoxMetrics(sourceNode, cloneNode, pageRect, clonePage);
  });

  const clonePageContent = clonePage.querySelector(".page-content");
  if (clonePageContent) {
    clonePageContent.style.width = `${pageRect.width}px`;
    clonePageContent.style.height = `${pageRect.height}px`;
    clonePageContent.style.minWidth = `${pageRect.width}px`;
    clonePageContent.style.minHeight = `${pageRect.height}px`;
  }

  return {
    host,
    wrapper,
    page: clonePage,
    pageSpec,
    cleanup() {
      host.innerHTML = "";
    },
  };
}

function getHtml2CanvasRenderOptions(pageSpec, options = {}) {
  return {
    scale: Number.isFinite(options.scale) && options.scale > 0 ? options.scale : pageSpec.rasterScale,
    useCORS: true,
    backgroundColor: "#ffffff",
    logging: false,
    foreignObjectRendering: Boolean(options.foreignObjectRendering),
    scrollX: 0,
    scrollY: 0,
    removeContainer: true,
    width: pageSpec.sourceWidthPx,
    height: pageSpec.sourceHeightPx,
    windowWidth: pageSpec.sourceWidthPx,
    windowHeight: pageSpec.sourceHeightPx,
  };
}

function isCanvasLikelyBlank(canvas) {
  if (!canvas || canvas.width < 8 || canvas.height < 8) {
    return true;
  }

  const ctx = canvas.getContext("2d", { willReadFrequently: true });
  if (!ctx) {
    return false;
  }

  const sampleCols = 18;
  const sampleRows = 24;
  const minX = Math.max(0, Math.floor(canvas.width * 0.02));
  const minY = Math.max(0, Math.floor(canvas.height * 0.02));
  const maxX = Math.max(minX + 1, Math.ceil(canvas.width * 0.98));
  const maxY = Math.max(minY + 1, Math.ceil(canvas.height * 0.98));
  const stepX = Math.max(1, Math.floor((maxX - minX) / sampleCols));
  const stepY = Math.max(1, Math.floor((maxY - minY) / sampleRows));

  for (let y = minY; y < maxY; y += stepY) {
    for (let x = minX; x < maxX; x += stepX) {
      const [r, g, b, a] = ctx.getImageData(x, y, 1, 1).data;
      if (a > 8 && (r < 246 || g < 246 || b < 246)) {
        return false;
      }
    }
  }

  return true;
}

function normalizeCanvasToTargetSize(sourceCanvas, pageSpec) {
  if (!sourceCanvas) {
    throw new Error("Missing source canvas for export normalization.");
  }
  if (
    sourceCanvas.width === pageSpec.targetWidthPx &&
    sourceCanvas.height === pageSpec.targetHeightPx
  ) {
    return sourceCanvas;
  }

  const normalized = document.createElement("canvas");
  normalized.width = pageSpec.targetWidthPx;
  normalized.height = pageSpec.targetHeightPx;
  const ctx = normalized.getContext("2d");
  if (!ctx) {
    throw new Error("Could not create normalized export canvas context.");
  }

  const isDrawableCanvas =
    typeof HTMLCanvasElement !== "undefined" && sourceCanvas instanceof HTMLCanvasElement;
  if (!isDrawableCanvas) {
    if (typeof sourceCanvas.width === "number") {
      sourceCanvas.width = pageSpec.targetWidthPx;
    }
    if (typeof sourceCanvas.height === "number") {
      sourceCanvas.height = pageSpec.targetHeightPx;
    }
    return sourceCanvas;
  }

  ctx.fillStyle = "#ffffff";
  ctx.fillRect(0, 0, normalized.width, normalized.height);
  ctx.drawImage(sourceCanvas, 0, 0, normalized.width, normalized.height);
  return normalized;
}

async function renderExportPageToCanvas(page, options = {}) {
  if (!page) {
    throw new Error("Export page element is missing.");
  }
  if (typeof window.html2canvas !== "function") {
    throw new Error("html2canvas is not available.");
  }

  const frozen = buildFrozenExportPage(page, options);
  const pageSpec = frozen.pageSpec;
  const fontStatus = await waitForExportFontsReady();
  const startedAt = performance.now();
  let methodUsed = "html2canvas-raster";

  try {
    const primary = await window.html2canvas(
      frozen.page,
      getHtml2CanvasRenderOptions(pageSpec, { scale: pageSpec.rasterScale, foreignObjectRendering: false })
    );

    let canvasToUse = primary;
    if (isCanvasLikelyBlank(primary)) {
      methodUsed = "html2canvas-foreignObject";
      const fallback = await window.html2canvas(
        frozen.page,
        getHtml2CanvasRenderOptions(pageSpec, { scale: pageSpec.rasterScale, foreignObjectRendering: true })
      );
      if (isCanvasLikelyBlank(fallback)) {
        throw new Error("Export rendering resulted in a blank page.");
      }
      canvasToUse = fallback;
    }

    const normalizedCanvas = normalizeCanvasToTargetSize(canvasToUse, pageSpec);
    const debugEntry = {
      orientation: pageSpec.orientation,
      targetWidthPx: pageSpec.targetWidthPx,
      targetHeightPx: pageSpec.targetHeightPx,
      sourceWidthPx: pageSpec.sourceWidthPx,
      sourceHeightPx: pageSpec.sourceHeightPx,
      targetDpi: pageSpec.targetDpi,
      rasterScale: Number(pageSpec.rasterScale.toFixed(5)),
      fontReady: Boolean(fontStatus.ready),
      fontStatus: fontStatus.status || "unknown",
      unresolvedFontCount: Number(fontStatus.unresolvedCount || 0),
      captureMethod: methodUsed,
      renderTimeMs: Number((performance.now() - startedAt).toFixed(2)),
    };
    normalizedCanvas.__exportDebug = debugEntry;
    recordExportDebug(debugEntry);
    return normalizedCanvas;
  } finally {
    frozen.cleanup();
  }
}

async function renderExportPagesToCanvases(pages, options = {}) {
  const renderedPages = [];
  for (let idx = 0; idx < pages.length; idx += 1) {
    const page = pages[idx];
    const canvas = await renderExportPageToCanvas(page, options);
    renderedPages.push({
      page,
      canvas,
      pageSpec: getExportPageRenderSpec(page, options.targetDpi),
      debug: canvas.__exportDebug || null,
    });
  }
  return renderedPages;
}

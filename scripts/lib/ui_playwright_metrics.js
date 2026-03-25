async function collectDensityProbe(page) {
  return page.evaluate(() => {
    const card = document.querySelector(".preview-card");
    if (!card) return null;

    const head = card.querySelector(".preview-card-head");
    const body = card.querySelector(".preview-body");
    if (!head || !body) return null;

    const cardRect = card.getBoundingClientRect();
    const headRect = head.getBoundingClientRect();
    const bodyStyle = window.getComputedStyle(body);
    const headStyle = window.getComputedStyle(head);
    const sectionTitles = Array.from(card.querySelectorAll(".section-title"));
    const actionButtons = Array.from(card.querySelectorAll(".preview-mini-btn, .preview-head-btn"));
    const iconButtonsOnly = actionButtons.every((button) => button.textContent.replace(/\s+/g, "").length <= 2);
    const visibleActions = Array.from(card.querySelectorAll(".preview-item-actions")).filter((element) => {
      const style = window.getComputedStyle(element);
      return style.display !== "none" && style.visibility !== "hidden" && Number(style.opacity || "1") > 0.05;
    });
    const actionsAreaPx = visibleActions.reduce((sum, element) => {
      const rect = element.getBoundingClientRect();
      return sum + rect.width * rect.height;
    }, 0);
    const avg = (values) => (values.length ? values.reduce((sum, value) => sum + value, 0) / values.length : 0);

    return {
      cardHeightPx: Number(cardRect.height.toFixed(2)),
      cardWidthPx: Number(cardRect.width.toFixed(2)),
      headerHeightPx: Number(headRect.height.toFixed(2)),
      headerRatio: Number((headRect.height / Math.max(1, cardRect.height)).toFixed(4)),
      headerPaddingTopPx: Number.parseFloat(headStyle.paddingTop || "0"),
      headerPaddingBottomPx: Number.parseFloat(headStyle.paddingBottom || "0"),
      bodyPaddingTopPx: Number.parseFloat(bodyStyle.paddingTop || "0"),
      sectionTitleMarginTopAvgPx: Number(avg(sectionTitles.map((element) => Number.parseFloat(window.getComputedStyle(element).marginTop || "0"))).toFixed(2)),
      sectionTitleMarginBottomAvgPx: Number(avg(sectionTitles.map((element) => Number.parseFloat(window.getComputedStyle(element).marginBottom || "0"))).toFixed(2)),
      actionsAreaRatio: Number((actionsAreaPx / Math.max(1, cardRect.width * cardRect.height)).toFixed(4)),
      iconButtonsOnly,
    };
  });
}

async function collectPreviewMetrics(page) {
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
    };
    const overlapArea = (a, b) => {
      const x = Math.max(0, Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x));
      const y = Math.max(0, Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y));
      return x * y;
    };

    pageContents.forEach((pageEl) => {
      if (!pageEl) return;
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
        pageCardArea += Math.max(0, Math.min(rect.right, pageRect.right) - Math.max(rect.left, pageRect.left)) * Math.max(0, Math.min(rect.bottom, pageRect.bottom) - Math.max(rect.top, pageRect.top));
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

      metrics.totalCards += cards.length;
      metrics.outOfBoundsCount += pageOut;
      metrics.totalCardArea += pageCardArea;
      metrics.totalOverlapArea += pageOverlapArea;
      metrics.totalPageArea += pageRect.width * pageRect.height;
    });

    return {
      totalCards: metrics.totalCards,
      outOfBoundsCount: metrics.outOfBoundsCount,
      occupiedAreaRatio: Number((metrics.totalCardArea / Math.max(1, metrics.totalPageArea)).toFixed(4)),
      overlapAreaRatio: Number((metrics.totalOverlapArea / Math.max(1, metrics.totalPageArea)).toFixed(4)),
      headerRatioAvg: Number((metrics.headerRatioSum / Math.max(1, metrics.headerRatioSamples)).toFixed(4)),
    };
  });
}

async function collectLegibilityProbe(page) {
  return page.evaluate(() => {
    const isVisible = (element) => {
      if (!element) return false;
      const style = window.getComputedStyle(element);
      return style.display !== "none" && style.visibility !== "hidden" && Number(style.opacity || "1") > 0.05;
    };
    const elements = Array.from(
      document.querySelectorAll(
        ".preview-card .preview-card-head h4, .preview-card .section-title, .preview-card .preview-body p, .preview-card .preview-body li, .preview-card .preview-body pre, .preview-card .preview-body .inline-code"
      )
    ).filter(isVisible);
    const fontSizes = elements.map((element) => Number.parseFloat(window.getComputedStyle(element).fontSize || "0")).filter(Boolean);
    const lineHeights = elements.map((element) => {
      const value = window.getComputedStyle(element).lineHeight || "";
      const parsed = Number.parseFloat(value);
      return Number.isFinite(parsed) ? parsed : 0;
    }).filter(Boolean);
    const overflowCards = Array.from(document.querySelectorAll(".preview-card")).filter((card) => {
      const body = card.querySelector(".preview-body");
      return body && body.scrollHeight > body.clientHeight + 6;
    }).length;
    return {
      minFontSizePx: Number((fontSizes.length ? Math.min(...fontSizes) : 0).toFixed(2)),
      minLineHeight: Number((lineHeights.length ? Math.min(...lineHeights) : 0).toFixed(2)),
      overflowCards,
      textElementCount: elements.length,
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
    const sourcePage = document.querySelector(".sheet-page");
    if (!sourcePage || typeof buildFrozenExportPage !== "function") {
      return {
        controlsHidden: false,
        layoutStable: false,
        cardHeightDeltaPx: 0,
        cardWidthDeltaPx: 0,
        headHeightDeltaPx: 0,
        compactHeader: false,
        headerRatio: 0,
        bodyPaddingTopPx: 0,
      };
    }

    const frozen = buildFrozenExportPage(sourcePage);
    try {
      const isVisible = (element) => {
        if (!element) return false;
        const style = window.getComputedStyle(element);
        return style.display !== "none" && style.visibility !== "hidden" && Number(style.opacity || "1") > 0;
      };
      const hasVisible = (root, selector) => Array.from(root.querySelectorAll(selector)).some(isVisible);
      const card = frozen.page.querySelector(".preview-card");
      const head = card?.querySelector(".preview-card-head");
      const body = card?.querySelector(".preview-body");
      const cardRect = card?.getBoundingClientRect();
      const headRect = head?.getBoundingClientRect();
      const after = {
        cardHeightPx: Number((cardRect?.height || 0).toFixed(2)),
        cardWidthPx: Number((cardRect?.width || 0).toFixed(2)),
        headHeightPx: Number((headRect?.height || 0).toFixed(2)),
        bodyHeightPx: Number((body?.getBoundingClientRect?.().height || 0).toFixed(2)),
      };
      const headStyle = head ? window.getComputedStyle(head) : null;
      return {
        controlsHidden:
          !hasVisible(frozen.page, ".preview-card-head-actions") &&
          !hasVisible(frozen.page, ".preview-item-actions") &&
          !hasVisible(frozen.page, ".preview-resize-bottom") &&
          !hasVisible(frozen.page, ".preview-resize-corner"),
        layoutStable:
          Math.abs(after.cardHeightPx - before.cardHeightPx) <= 0.5 &&
          Math.abs(after.cardWidthPx - before.cardWidthPx) <= 0.5 &&
          Math.abs(after.headHeightPx - before.headHeightPx) <= 0.5,
        cardHeightDeltaPx: Number((after.cardHeightPx - before.cardHeightPx).toFixed(2)),
        cardWidthDeltaPx: Number((after.cardWidthPx - before.cardWidthPx).toFixed(2)),
        headHeightDeltaPx: Number((after.headHeightPx - before.headHeightPx).toFixed(2)),
        compactHeader:
          Number.parseFloat(headStyle?.paddingTop || "99") <= 2.5 &&
          Number.parseFloat(headStyle?.paddingBottom || "99") <= 2.5 &&
          Number.parseFloat(headStyle?.borderBottomWidth || "99") <= 0.5,
        headerRatio: Number(((headRect?.height || 0) / Math.max(1, cardRect?.height || 1)).toFixed(4)),
        bodyPaddingTopPx: Number.parseFloat(window.getComputedStyle(body || document.body).paddingTop || "0"),
      };
    } finally {
      frozen.cleanup();
    }
  });
}

module.exports = {
  collectDensityProbe,
  collectLegibilityProbe,
  collectPreviewMetrics,
  probeExportSnapshotLayout,
};

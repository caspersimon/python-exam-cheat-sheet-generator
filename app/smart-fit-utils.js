function getSmartFitContentProfile(entries) {
  const stats = {
    cardCount: entries.length,
    totalChars: 0,
    totalPieces: 0,
    codeBlocks: 0,
    tableBlocks: 0,
    longestCodeLine: 0,
    longestToken: 0,
  };

  entries.forEach((entry) => {
    const entryStats = getAutoEntryContentStats(entry);
    stats.totalChars += Number(entryStats.textChars) || 0;
    stats.totalPieces += Number(entryStats.pieceCount) || 0;
    stats.codeBlocks += Number(entryStats.codeBlockCount) || 0;
    stats.tableBlocks += Number(entryStats.tableBlockCount) || 0;
    stats.longestCodeLine = Math.max(stats.longestCodeLine, Number(entryStats.maxCodeLineLength) || 0);
    stats.longestToken = Math.max(stats.longestToken, Number(entryStats.longestTokenLength) || 0);
  });

  const cardCount = Math.max(1, stats.cardCount);
  const pieceCount = Math.max(1, stats.totalPieces);
  return {
    ...stats,
    avgCharsPerCard: stats.totalChars / cardCount,
    avgPiecesPerCard: stats.totalPieces / cardCount,
    codeBlocksPerPiece: stats.codeBlocks / pieceCount,
    tableBlocksPerPiece: stats.tableBlocks / pieceCount,
  };
}

function buildSmartFitPresets(contentProfile) {
  const dense = contentProfile.avgCharsPerCard >= 620 || contentProfile.avgPiecesPerCard >= 4.2;
  const veryDense = contentProfile.avgCharsPerCard >= 760 || contentProfile.avgPiecesPerCard >= 5.1;
  const wideHeavy = contentProfile.longestCodeLine >= 70 || contentProfile.tableBlocks >= Math.max(3, Math.floor(contentProfile.cardCount * 0.2));
  const tokenHeavy = contentProfile.longestToken >= 28;

  const basePresets = [
    {
      id: "comfortable",
      fontSize: 9.6,
      titleSize: 10.8,
      lineHeight: 1.18,
      letterSpacing: 0.02,
      cardGap: 5,
      cardPadding: 6,
      codeBlockPadding: 5,
      codeBlockMargin: 2,
      tableSize: 8,
      pieceGap: 3,
      titleMargin: 2,
    },
    {
      id: "balanced",
      fontSize: 9.1,
      titleSize: 10.2,
      lineHeight: 1.12,
      letterSpacing: 0.01,
      cardGap: 4,
      cardPadding: 5,
      codeBlockPadding: 4,
      codeBlockMargin: 1,
      tableSize: 7.6,
      pieceGap: 2,
      titleMargin: 1,
    },
    {
      id: "compact",
      fontSize: 8.6,
      titleSize: 9.8,
      lineHeight: 1.08,
      letterSpacing: 0,
      cardGap: 4,
      cardPadding: 5,
      codeBlockPadding: 4,
      codeBlockMargin: 1,
      tableSize: 7.2,
      pieceGap: 2,
      titleMargin: 1,
    },
    {
      id: "dense",
      fontSize: 8.2,
      titleSize: 9.3,
      lineHeight: 1.05,
      letterSpacing: 0,
      cardGap: 3,
      cardPadding: 4,
      codeBlockPadding: 3,
      codeBlockMargin: 1,
      tableSize: 6.8,
      pieceGap: 1,
      titleMargin: 1,
    },
    {
      id: "tight",
      fontSize: 7.8,
      titleSize: 8.9,
      lineHeight: 1.02,
      letterSpacing: 0,
      cardGap: 3,
      cardPadding: 4,
      codeBlockPadding: 3,
      codeBlockMargin: 1,
      tableSize: 6.5,
      pieceGap: 1,
      titleMargin: 1,
    },
  ];

  const presets = basePresets.map((preset) => {
    const next = { ...preset };
    if (wideHeavy || tokenHeavy) {
      next.codeBlockPadding = Math.max(next.codeBlockPadding, 4);
      next.cardPadding = Math.max(next.cardPadding, 5);
      next.tableSize = Math.max(next.tableSize, 7);
    }
    if (veryDense) {
      next.cardGap = Math.max(2, next.cardGap - 1);
      next.lineHeight = Math.max(1.02, next.lineHeight - 0.02);
      next.tableSize = Math.max(6.2, next.tableSize - 0.2);
    } else if (!dense) {
      next.lineHeight = Math.min(1.2, next.lineHeight + 0.02);
      next.pieceGap = Math.min(3, next.pieceGap + 1);
    }
    return next;
  });

  return dense ? presets.slice(1) : presets.slice(0, 4);
}

function evaluateSmartFitPreset(entries, contentProfile, preset, baseline) {
  const restoreLayout = deepClone(baseline.layout);
  const restorePreviewCards = deepClone(baseline.previewCards);
  const restoreZCounter = baseline.previewZCounter;

  try {
    Object.assign(state.layout, preset, { autoGrid: true });
    state.previewCards = deepClone(restorePreviewCards);
    state.previewZCounter = restoreZCounter;
    clearUnlockedPreviewCardLayouts();

    const grid = getEffectiveGridSettings(entries.length);
    const plan = buildAutoPreviewLayoutPlan(entries, grid);
    const page1 = getPreviewPageSize(1);
    const page2 = getPreviewPageSize(2);
    const totalPageArea = Math.max(1, page1.width * page1.height + page2.width * page2.height);

    let occupiedArea = 0;
    plan.layoutPlan.forEach((item) => {
      if (!item?.layout) {
        return;
      }
      occupiedArea += Math.max(1, item.layout.width) * Math.max(1, item.layout.height);
    });

    const occupancyRatio = occupiedArea / totalPageArea;
    const cardCount = Math.max(1, entries.length);
    const targetOccupancy = clamp(0.57 + Math.min(0.16, cardCount * 0.008), 0.58, 0.73);
    const overflowPenalty = (Number(plan.overflowCardCount) || 0) * 390;
    const compressionPenalty = (Number(plan.compressedCardCount) || 0) * 54 + Math.max(0, 0.92 - (Number(plan.averageCompression) || 1)) * 840;
    const occupancyPenalty = Math.abs(occupancyRatio - targetOccupancy) * 320;
    const readabilityPenalty =
      Math.max(0, 8.1 - preset.fontSize) * 150 +
      Math.max(0, 1.04 - preset.lineHeight) * 180 +
      Math.max(0, 6.7 - preset.tableSize) * 80;
    const gapPenalty = Math.max(0, 1 - preset.pieceGap) * 24;

    const wideDemand = (contentProfile.codeBlocks + contentProfile.tableBlocks) > 0 || contentProfile.longestToken >= 24;
    const wideReward = Math.min(
      120,
      (Number(plan.wideCardCount) || 0) * (wideDemand ? 24 : 9) + Math.max(0, contentProfile.longestCodeLine - 56) * 0.35
    );

    const score = 1000 - overflowPenalty - compressionPenalty - occupancyPenalty - readabilityPenalty - gapPenalty + wideReward;

    return {
      preset,
      grid,
      plan,
      score,
      occupancyRatio,
    };
  } finally {
    Object.assign(state.layout, restoreLayout);
    state.previewCards = restorePreviewCards;
    state.previewZCounter = restoreZCounter;
  }
}

function rebalanceAutoLayoutDensity(layoutPlan, pageStates) {
  const pages = [1, 2];
  let occupiedArea = 0;
  const totalPageArea = pages.reduce((sum, page) => sum + (pageStates[page] ? pageStates[page].pageWidth * pageStates[page].pageHeight : 0), 0);
  const targetArea = totalPageArea * AUTO_LAYOUT_TARGET_OCCUPIED_RATIO;

  layoutPlan.forEach((item) => {
    if (item?.layout) {
      occupiedArea += item.layout.width * item.layout.height;
    }
  });

  let neededArea = Math.floor(Math.max(0, targetArea - occupiedArea));
  if (neededArea <= 0) {
    return;
  }

  const growthGroups = [];
  pages.forEach((page) => {
    const pageState = pageStates[page];
    if (!pageState) {
      return;
    }

    const columns = collectAutoColumnCards(pageState, layoutPlan);
    columns.forEach((cards) => {
      if (!cards.length) {
        return;
      }

      let segmentStart = 0;
      while (segmentStart < cards.length) {
        while (segmentStart < cards.length && layoutPlan.get(cards[segmentStart].cardId)?.isLocked) {
          segmentStart += 1;
        }
        if (segmentStart >= cards.length) {
          break;
        }

        let segmentEnd = segmentStart;
        while (segmentEnd < cards.length && !layoutPlan.get(cards[segmentEnd].cardId)?.isLocked) {
          segmentEnd += 1;
        }

        const segmentCards = cards.slice(segmentStart, segmentEnd);
        if (!segmentCards.length) {
          segmentStart = segmentEnd + 1;
          continue;
        }

        const lockedBoundaryCard = cards[segmentEnd];
        const segmentBottomY = lockedBoundaryCard && layoutPlan.get(lockedBoundaryCard.cardId)?.isLocked
          ? lockedBoundaryCard.layout.y
          : pageState.pageHeight;

        const tailCard = segmentCards[segmentCards.length - 1];
        const availableHeight = Math.max(0, Math.floor(segmentBottomY - (tailCard.layout.y + tailCard.layout.height)));
        const maxSegmentGrowArea = availableHeight * Math.max(1, Math.round(tailCard.layout.width || pageState.columnWidth));
        if (maxSegmentGrowArea <= 0) {
          segmentStart = segmentEnd + 1;
          continue;
        }

        const adjustableCards = [];
        let totalWeight = 0;
        segmentCards.forEach((item) => {
          const cardId = item.cardId;
          const candidate = layoutPlan.get(cardId);
          const candidateLayout = candidate?.layout;
          if (!candidateLayout) {
            return;
          }

          const cardMaxHeight = Math.max(candidateLayout.height, Number(candidate?.maxHeightPx) || candidateLayout.height);
          const maxGrowHeight = Math.max(0, cardMaxHeight - candidateLayout.height);
          if (maxGrowHeight <= 0) {
            return;
          }

          const width = Math.max(1, Math.round(candidateLayout.width || pageState.columnWidth));
          const maxGrowArea = maxGrowHeight * width;
          if (maxGrowArea <= 0) {
            return;
          }

          const weight = Math.max(1, Math.round(Number(candidate?.densityWeight) || candidateLayout.height || 1));
          totalWeight += weight;
          adjustableCards.push({
            cardId,
            layout: candidateLayout,
            width,
            maxGrowArea,
            usedGrowArea: 0,
            weight,
          });
        });

        if (!adjustableCards.length || totalWeight <= 0) {
          segmentStart = segmentEnd;
          continue;
        }

        growthGroups.push({
          cards: segmentCards.map(({ cardId, layout }) => ({ cardId, layout })),
          adjustableCards,
          maxColumnGrowArea: maxSegmentGrowArea,
          remainingColumnGrowArea: maxSegmentGrowArea,
          totalWeight,
        });

        segmentStart = segmentEnd;
      }
    });
  });

  if (!growthGroups.length) {
    return;
  }

  let loops = 0;
  while (neededArea > 0 && loops < 24) {
    loops += 1;
    let totalGrowthWeight = 0;
    growthGroups.forEach((group) => {
      if (group.remainingColumnGrowArea <= 0) {
        group.totalWeight = 0;
        return;
      }

      let activeWeight = 0;
      group.adjustableCards.forEach((card) => {
        if (card.maxGrowArea <= card.usedGrowArea) {
          return;
        }
        activeWeight += card.weight;
      });
      group.totalWeight = activeWeight;
      totalGrowthWeight += activeWeight;
    });

    if (totalGrowthWeight <= 0) {
      break;
    }

    let deltaThisRound = 0;

    growthGroups.forEach((group) => {
      if (!group.totalWeight || group.remainingColumnGrowArea <= 0) {
        return;
      }

      group.adjustableCards.forEach((card) => {
        if (card.maxGrowArea <= card.usedGrowArea || group.remainingColumnGrowArea <= 0) {
          return;
        }
        if (card.usedGrowArea >= card.maxGrowArea) {
          return;
        }

        const globalWeightShare = card.weight / totalGrowthWeight;
        const proposedArea = neededArea * globalWeightShare;
        const cardRemainingArea = Math.max(0, card.maxGrowArea - card.usedGrowArea);
        const maxAllowedArea = Math.min(cardRemainingArea, group.remainingColumnGrowArea);
        const growArea = Math.max(0, Math.min(proposedArea, maxAllowedArea));
        if (growArea <= 0) {
          return;
        }

        card.usedGrowArea += growArea;
        group.remainingColumnGrowArea -= growArea;
        deltaThisRound += growArea;
      });
    });

    if (deltaThisRound <= 0) {
      break;
    }

    neededArea -= deltaThisRound;
  }

  growthGroups.forEach((group) => {
    if (!group.adjustableCards.length) {
      return;
    }

    const growthById = new Map();
    group.adjustableCards.forEach((card) => {
      if (card.usedGrowArea > 0) {
        const growthPx = card.usedGrowArea / card.width;
        growthById.set(card.cardId, growthPx);
      }
    });

    let shiftY = 0;
    group.cards.forEach((item) => {
      const cardGrowthPx = growthById.get(item.cardId) || 0;
      if (shiftY) {
        item.layout.y += shiftY;
      }
      if (cardGrowthPx > 0) {
        item.layout.height += cardGrowthPx;
        shiftY += cardGrowthPx;
      }
    });
  });
}

function buildAutoPreviewLayoutPlan(previewEntries, grid) {
  const gap = getAutoGridGap();
  const columns = Math.max(1, Number(grid.columns) || 1);
  const pageStates = {
    1: getAutoPageState(1, columns, gap),
    2: getAutoPageState(2, columns, gap),
  };

  const minColumnWidth = Math.min(pageStates[1].columnWidth, pageStates[2].columnWidth);
  const layoutPlan = new Map();
  const candidateEntries = [];

  previewEntries.forEach((entry, index) => {
    const existing = state.previewCards[entry.previewId];
    const fallback = getDefaultPreviewLayout(index, grid);
    const isLocked = Boolean(existing?.locked);

    if (!isLocked) {
      const width1 = pageStates[1].columnWidth || minColumnWidth;
      const width2 = pageStates[2].columnWidth || minColumnWidth;
      const entryHeightOn1 = estimateCardHeight(entry, width1);
      const entryHeightOn2 = estimateCardHeight(entry, width2);
      const maxHeightOn1 = getAutoHeightCapForPage(pageStates[1]);
      const maxHeightOn2 = getAutoHeightCapForPage(pageStates[2]);
      const packedHeightOn1 = getAutoCappedHeight(entryHeightOn1, pageStates[1], maxHeightOn1);
      const packedHeightOn2 = getAutoCappedHeight(entryHeightOn2, pageStates[2], maxHeightOn2);
      candidateEntries.push({
        entry,
        estimatedHeights: {
          1: entryHeightOn1,
          2: entryHeightOn2,
        },
        packedHeights: {
          1: packedHeightOn1,
          2: packedHeightOn2,
        },
        maxHeights: {
          1: maxHeightOn1,
          2: maxHeightOn2,
        },
        densityWeight: Math.max(1, Math.round(Math.max(entryHeightOn1, entryHeightOn2))),
        sortKey: Math.max(entryHeightOn1, entryHeightOn2),
      });
      return;
    }

    const lockedLayout = ensurePreviewCardLayout(entry.previewId, fallback, {
      force: false,
    });
    reservePageIntervalForCard(pageStates[lockedLayout.page], lockedLayout);
    layoutPlan.set(entry.previewId, { layout: lockedLayout, isLocked: true, overflow: false });
  });

  candidateEntries.sort((a, b) => b.sortKey - a.sortKey || a.entry.previewId.localeCompare(b.entry.previewId));

  candidateEntries.forEach((item) => {
    const heightOn1 = item.packedHeights[1];
    const heightOn2 = item.packedHeights[2];
    const rawHeightOn1 = item.estimatedHeights[1];
    const rawHeightOn2 = item.estimatedHeights[2];
    const candidate1 = getAutoPlacementCandidate(pageStates[1], heightOn1);
    const candidate2 = getAutoPlacementCandidate(pageStates[2], heightOn2);

    let chosen = candidate1;
    if (!chosen || (candidate2 && (candidate2.y < chosen.y || (candidate2.y === chosen.y && candidate2.col < chosen.col)))) {
      chosen = candidate2;
    }

    if (!chosen) {
      const overflowCandidate2 = getAutoPlacementCandidate(pageStates[2], heightOn2, rawHeightOn2);
      const overflowCandidate1 = getAutoPlacementCandidate(pageStates[1], heightOn1, rawHeightOn1);
      chosen = overflowCandidate2 || overflowCandidate1;
      if (chosen) {
        chosen.isOverflow = true;
      }
    }

    if (!chosen) {
      const fallbackLayout = getDefaultPreviewLayout(layoutPlan.size, grid);
      const layout = ensurePreviewCardLayout(item.entry.previewId, fallbackLayout, {
        force: true,
        sanitizeOptions: {
          minHeight: 1,
          minWidth: 1,
        },
      });
      layoutPlan.set(item.entry.previewId, { layout, isLocked: false, overflow: true });
      reservePageIntervalForCard(pageStates[layout.page], layout);
      return;
    }

    const normalizedMinHeight = chosen.isOverflow
      ? 1
      : Math.min(AUTO_MIN_CARD_HEIGHT_PX, Math.max(1, Math.round(chosen.height)));

    const fitted = ensurePreviewCardLayout(
      item.entry.previewId,
      {
        page: chosen.page,
        x: chosen.x,
        y: chosen.y,
        width: chosen.width,
        height: chosen.height,
        z: layoutPlan.size + 1,
      },
      {
        force: true,
        sanitizeOptions: {
          minHeight: normalizedMinHeight,
          minWidth: chosen.width,
        },
      }
    );

    reservePageIntervalForCard(pageStates[fitted.page], fitted);
    layoutPlan.set(item.entry.previewId, {
      layout: fitted,
      isLocked: false,
      overflow: Boolean(chosen.isOverflow),
      densityWeight: Math.max(1, Math.round(item.densityWeight || item.sortKey || 1)),
      maxHeightPx: chosen.page === 1 ? item.maxHeights[1] : item.maxHeights[2],
    });
  });

  rebalanceAutoLayoutDensity(layoutPlan, pageStates);

  const pageHeights = {
    1: getPreviewPageSize(1).height,
    2: getPreviewPageSize(2).height,
  };

  let overflowCardCount = 0;
  layoutPlan.forEach((item) => {
    const layout = item.layout;
    if (!layout || !Number.isFinite(layout.x) || !Number.isFinite(layout.y) || !Number.isFinite(layout.width) || !Number.isFinite(layout.height)) {
      return;
    }

    const pageHeight = pageHeights[layout.page];
    if (!pageHeight || !Number.isFinite(pageHeight) || pageHeight <= 0) {
      return;
    }

    layout.y = clamp(layout.y, 0, Math.max(0, pageHeight - layout.height));
    const maxAllowedHeight = Math.max(1, pageHeight - layout.y);
    if (layout.height > maxAllowedHeight) {
      layout.height = maxAllowedHeight;
      item.overflow = true;
    }

    if (item.overflow) {
      overflowCardCount += 1;
    }
  });

  return { layoutPlan, overflowCardCount };
}

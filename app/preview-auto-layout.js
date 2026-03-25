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

function buildAutoPageSpanVariants(entry, pageState) {
  const maxSpan = Math.max(1, Math.min(pageState.columns, AUTO_MAX_CARD_SPAN));
  const preferredSpan = estimatePreferredCardSpan(entry, pageState, maxSpan);
  const spanSet = new Set([1, preferredSpan]);
  if (preferredSpan > 1) {
    spanSet.add(preferredSpan - 1);
  }
  if (preferredSpan < maxSpan) {
    spanSet.add(preferredSpan + 1);
  }
  if (maxSpan >= 2) {
    spanSet.add(2);
  }

  const variants = [...spanSet]
    .filter((span) => Number.isFinite(span) && span >= 1 && span <= maxSpan)
    .sort((a, b) => a - b)
    .map((span) => {
      const width = getAutoCardWidthForSpan(pageState, span);
      const rawHeight = estimateCardHeight(entry, width);
      const maxHeight = getAutoHeightCapForPage(pageState);
      const packedHeight = getAutoCappedHeight(rawHeight, pageState, maxHeight);
      return {
        page: pageState.page,
        span,
        preferredSpan,
        width,
        rawHeight,
        packedHeight,
        maxHeight,
      };
    });

  return variants.length ? variants : [{
    page: pageState.page,
    span: 1,
    preferredSpan: 1,
    width: pageState.columnWidth,
    rawHeight: estimateCardHeight(entry, pageState.columnWidth),
    packedHeight: getAutoCappedHeight(estimateCardHeight(entry, pageState.columnWidth), pageState, getAutoHeightCapForPage(pageState)),
    maxHeight: getAutoHeightCapForPage(pageState),
  }];
}

function compareAutoPlacementOption(a, b) {
  const aOverflow = Boolean(a?.candidate?.isOverflow);
  const bOverflow = Boolean(b?.candidate?.isOverflow);
  if (aOverflow !== bOverflow) {
    return aOverflow ? 1 : -1;
  }

  const ay = Number(a?.candidate?.y) || 0;
  const by = Number(b?.candidate?.y) || 0;
  if (ay !== by) {
    return ay - by;
  }

  const apage = Number(a?.candidate?.page) || 1;
  const bpage = Number(b?.candidate?.page) || 1;
  if (apage !== bpage) {
    return apage - bpage;
  }

  const aSpanPenalty = Math.abs((Number(a?.variant?.span) || 1) - (Number(a?.variant?.preferredSpan) || 1));
  const bSpanPenalty = Math.abs((Number(b?.variant?.span) || 1) - (Number(b?.variant?.preferredSpan) || 1));
  if (aSpanPenalty !== bSpanPenalty) {
    return aSpanPenalty - bSpanPenalty;
  }

  const aCompression = (Number(a?.variant?.packedHeight) || 1) / Math.max(1, Number(a?.variant?.rawHeight) || 1);
  const bCompression = (Number(b?.variant?.packedHeight) || 1) / Math.max(1, Number(b?.variant?.rawHeight) || 1);
  if (aCompression !== bCompression) {
    return bCompression - aCompression;
  }

  const aHeight = Number(a?.variant?.packedHeight) || 0;
  const bHeight = Number(b?.variant?.packedHeight) || 0;
  if (aHeight !== bHeight) {
    return aHeight - bHeight;
  }

  const ax = Number(a?.candidate?.x) || 0;
  const bx = Number(b?.candidate?.x) || 0;
  if (ax !== bx) {
    return ax - bx;
  }

  const aSpan = Number(a?.variant?.span) || 1;
  const bSpan = Number(b?.variant?.span) || 1;
  return aSpan - bSpan;
}

function buildAutoPreviewLayoutPlan(previewEntries, grid) {
  const gap = getAutoGridGap();
  const columns = Math.max(1, Number(grid.columns) || 1);
  const pageStates = {
    1: getAutoPageState(1, columns, gap),
    2: getAutoPageState(2, columns, gap),
  };

  const layoutPlan = new Map();
  const candidateEntries = [];

  previewEntries.forEach((entry, index) => {
    const existing = state.previewCards[entry.previewId];
    const fallback = getDefaultPreviewLayout(index, grid);
    const isLocked = Boolean(existing?.locked);

    if (!isLocked) {
      const pageVariants = {
        1: buildAutoPageSpanVariants(entry, pageStates[1]),
        2: buildAutoPageSpanVariants(entry, pageStates[2]),
      };
      const sortKey = Math.max(
        ...pageVariants[1].map((variant) => variant.rawHeight * variant.width),
        ...pageVariants[2].map((variant) => variant.rawHeight * variant.width)
      );
      const densityWeight = Math.max(
        ...pageVariants[1].map((variant) => variant.rawHeight * (1 + (variant.span - 1) * 0.35)),
        ...pageVariants[2].map((variant) => variant.rawHeight * (1 + (variant.span - 1) * 0.35))
      );

      candidateEntries.push({
        entry,
        pageVariants,
        densityWeight: Math.max(1, Math.round(densityWeight)),
        sortKey,
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
    const collectPlacementOptions = (useOverflowFallback = false) => {
      const options = [];
      [1, 2].forEach((page) => {
        const variants = item.pageVariants?.[page] || [];
        variants.forEach((variant) => {
          const candidate = getAutoPlacementCandidate(pageStates[page], variant.packedHeight, {
            span: variant.span,
            fallbackHeightRef: useOverflowFallback ? variant.rawHeight : null,
          });
          if (!candidate) {
            return;
          }
          options.push({
            candidate: {
              ...candidate,
              isOverflow: Boolean(candidate.isOverflow || useOverflowFallback),
            },
            variant,
          });
        });
      });
      return options;
    };

    const directOptions = collectPlacementOptions(false).sort(compareAutoPlacementOption);
    const chosenOption = directOptions[0] || collectPlacementOptions(true).sort(compareAutoPlacementOption)[0] || null;

    if (!chosenOption) {
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
    const chosen = chosenOption.candidate;
    const chosenVariant = chosenOption.variant;

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
    const estimatedHeightPx = Math.max(1, Math.round(chosenVariant.rawHeight || chosen.height || 1));
    const compressionRatio = Math.min(1, Math.max(0.35, fitted.height / estimatedHeightPx));
    layoutPlan.set(item.entry.previewId, {
      layout: fitted,
      isLocked: false,
      overflow: Boolean(chosen.isOverflow),
      densityWeight: Math.max(1, Math.round(item.densityWeight || item.sortKey || 1)),
      maxHeightPx: chosenVariant.maxHeight,
      span: chosenVariant.span,
      preferredSpan: chosenVariant.preferredSpan,
      estimatedHeightPx,
      compressionRatio,
    });
  });

  rebalanceAutoLayoutDensity(layoutPlan, pageStates);

  const pageHeights = {
    1: getPreviewPageSize(1).height,
    2: getPreviewPageSize(2).height,
  };

  let overflowCardCount = 0;
  let compressedCardCount = 0;
  let wideCardCount = 0;
  let compressionSum = 0;
  let compressionCount = 0;
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

    if ((Number(item.span) || 1) > 1) {
      wideCardCount += 1;
    }

    const estimatedHeight = Number(item.estimatedHeightPx);
    if (Number.isFinite(estimatedHeight) && estimatedHeight > 0) {
      const compressionRatio = Math.min(1, Math.max(0.35, layout.height / estimatedHeight));
      item.compressionRatio = compressionRatio;
      compressionSum += compressionRatio;
      compressionCount += 1;
      if (compressionRatio < 0.9) {
        compressedCardCount += 1;
      }
    }
  });

  return {
    layoutPlan,
    overflowCardCount,
    compressedCardCount,
    wideCardCount,
    averageCompression: compressionCount > 0 ? compressionSum / compressionCount : 1,
  };
}

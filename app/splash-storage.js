function setLoadingState() {
  refs.cardHost.innerHTML = `<div class="empty-state"><p>Loading exam topic explorer...</p></div>`;
}

function maybeShowSplash() {
  if (!refs.splashOverlay || !refs.getStartedBtn) {
    return;
  }
  if (hasSeenSplash()) {
    return;
  }
  refs.splashOverlay.classList.remove("hidden");
  document.body.classList.add("splash-open");
  window.setTimeout(() => refs.getStartedBtn?.focus(), 0);
}

function dismissSplash() {
  if (!refs.splashOverlay) {
    return;
  }
  refs.splashOverlay.classList.add("hidden");
  document.body.classList.remove("splash-open");
  markSplashSeen();
}

function isSplashVisible() {
  return Boolean(refs.splashOverlay && !refs.splashOverlay.classList.contains("hidden"));
}

function hasSeenSplash() {
  try {
    return window.localStorage.getItem(SPLASH_STORAGE_KEY) === "1";
  } catch {
    return true;
  }
}

function markSplashSeen() {
  try {
    window.localStorage.setItem(SPLASH_STORAGE_KEY, "1");
  } catch {
    // Ignore browsers that block storage.
  }
}

function resetSplashIntro() {
  try {
    window.localStorage.removeItem(SPLASH_STORAGE_KEY);
  } catch {
    // Ignore browsers that block storage.
  }
  maybeShowSplash();
}

function resetAppProgress() {
  const confirmed = window.confirm(
    "Reset all progress?\n\nThis will permanently remove your saved selections, filters, layout settings, and preview positions."
  );
  if (!confirmed) {
    return;
  }

  if (persistTimer) {
    window.clearTimeout(persistTimer);
    persistTimer = 0;
  }

  finishPreviewPointerAction();
  closeOpenInfoPopovers();
  closeDrawers();

  try {
    window.localStorage.removeItem(APP_STATE_STORAGE_KEY);
  } catch {
    // Ignore browsers that block storage.
  }
  lastPersistedPayload = "";

  state.filters.search = "";
  state.filters.weeks = new Set(CANONICAL_WEEK_ORDER);
  state.drafts = {};
  state.navigation = buildDefaultNavigationState();
  state.previewHistory = [];
  state.openDrawer = "";
  state.previewCards = {};
  state.previewEntries = {};
  state.previewZCounter = 1;
  state.layout = {
    fontFamily: "'Manrope', sans-serif",
    fontSize: 9.5,
    titleSize: 6.8,
    lineHeight: 1.1,
    letterSpacing: 0,
    cardGap: 6,
    cardPadding: 7,
    codeBlockPadding: 8,
    codeBlockMargin: 2,
    autoGrid: true,
    gridColumns: 2,
    gridRows: 6,
  };

  renderWeekFilterControls();
  syncFilterControls();
  applyLayoutVariables();
  ensureExplorerNavigation(getFilteredParentBundles());
  closeTopicSidebar();
  setView("swipe");
  renderAll();
  syncPreviewUndoAvailability();
}

function hydratePersistedState() {
  const raw = getPersistedRawState();
  if (!raw || typeof raw !== "object") {
    return;
  }

  const cardIds = new Set(state.cards.map((card) => card.id));
  const parentIds = new Set(state.parentTopics.map((parentTopic) => parentTopic.id));
  const validWeeks = new Set(CANONICAL_WEEK_ORDER);

  if (raw.layout && typeof raw.layout === "object") {
    const fontAliases = new Map([
      ["'Space Grotesk', sans-serif", "'Manrope', sans-serif"],
      ["'DM Sans', sans-serif", "'Manrope', sans-serif"],
      ["'Inter', sans-serif", "'Manrope', sans-serif"],
      ["'IBM Plex Sans', sans-serif", "'Manrope', sans-serif"],
      ["'Manrope', sans-serif", "'Manrope', sans-serif"],
      ["'Newsreader', serif", "'Manrope', sans-serif"],
      ["'Source Serif 4', serif", "'Manrope', sans-serif"],
    ]);
    const hydratedFont = fontAliases.get(raw.layout.fontFamily);
    if (hydratedFont) {
      state.layout.fontFamily = hydratedFont;
    }
    if (Number.isFinite(raw.layout.fontSize)) {
      state.layout.fontSize = clamp(Number(raw.layout.fontSize), 7, 14);
    }
    if (Number.isFinite(raw.layout.titleSize)) {
      state.layout.titleSize = clamp(Number(raw.layout.titleSize), 4.8, 12);
    }
    if (Number.isFinite(raw.layout.lineHeight)) {
      state.layout.lineHeight = clamp(Number(raw.layout.lineHeight), 0.9, 1.5);
    }
    if (Number.isFinite(raw.layout.letterSpacing)) {
      state.layout.letterSpacing = clamp(Number(raw.layout.letterSpacing), -0.2, 1.2);
    }
    if (Number.isFinite(raw.layout.cardGap)) {
      state.layout.cardGap = clamp(Number(raw.layout.cardGap), 2, 18);
    }
    if (Number.isFinite(raw.layout.cardPadding)) {
      state.layout.cardPadding = clamp(Number(raw.layout.cardPadding), 4, 16);
    }
    if (Number.isFinite(raw.layout.codeBlockPadding)) {
      state.layout.codeBlockPadding = clamp(Number(raw.layout.codeBlockPadding), 2, 10);
    }
    if (Number.isFinite(raw.layout.codeBlockMargin)) {
      state.layout.codeBlockMargin = clamp(Number(raw.layout.codeBlockMargin), 0, 8);
    }
    if (typeof raw.layout.autoGrid === "boolean") {
      state.layout.autoGrid = raw.layout.autoGrid;
    }
    if (Number.isFinite(raw.layout.gridColumns)) {
      state.layout.gridColumns = clamp(Number(raw.layout.gridColumns), 1, 4);
    }
    if (Number.isFinite(raw.layout.gridRows)) {
      state.layout.gridRows = clamp(Number(raw.layout.gridRows), 3, 14);
    }
  }

  if (raw.filters && typeof raw.filters === "object") {
    state.filters.search = typeof raw.filters.search === "string" ? raw.filters.search : state.filters.search;
    if (Array.isArray(raw.filters.weeks)) {
      const weeks = raw.filters.weeks
        .map((value) => Number(value))
        .filter((value) => validWeeks.has(value));
      if (weeks.length) {
        state.filters.weeks = new Set(weeks);
      }
    }
  }

  if (raw.drafts && typeof raw.drafts === "object") {
    const hydratedDrafts = {};
    Object.entries(raw.drafts).forEach(([cardId, draft]) => {
      if (!cardIds.has(cardId) || !draft || typeof draft !== "object") {
        return;
      }

      const card = state.cards.find((entry) => entry.id === cardId);
      const validPieceIds = new Set(getAllSelectablePieceIds(card));
      const selectedPieces = Array.isArray(draft.selected?.pieces)
        ? draft.selected.pieces.filter((pieceId) => validPieceIds.has(pieceId))
        : [];
      hydratedDrafts[cardId] = {
        ui: {
          expandedSections: deepClone(draft.ui?.expandedSections || {}),
        },
        selected: {
          pieces: [...new Set(selectedPieces)],
        },
        overrides: {
          pieces: deepClone(draft.overrides?.pieces || {}),
        },
      };
    });
    state.drafts = hydratedDrafts;
  }

  if (raw.navigation && typeof raw.navigation === "object") {
    const nextNavigation = buildDefaultNavigationState();
    const activeParentId = String(raw.navigation.activeParentId || "").trim();
    if (parentIds.has(activeParentId)) {
      nextNavigation.activeParentId = activeParentId;
    }
    const activeTopicId = String(raw.navigation.activeTopicId || "").trim();
    if (cardIds.has(activeTopicId)) {
      nextNavigation.activeTopicId = activeTopicId;
    }
    if (raw.navigation.expandedParents && typeof raw.navigation.expandedParents === "object") {
      state.parentTopics.forEach((parentTopic, index) => {
        const fallbackValue = index === 0;
        const persistedValue = raw.navigation.expandedParents[parentTopic.id];
        nextNavigation.expandedParents[parentTopic.id] =
          typeof persistedValue === "boolean" ? persistedValue : fallbackValue;
      });
    }
    if (typeof raw.navigation.mobileSidebarOpen === "boolean") {
      nextNavigation.mobileSidebarOpen = raw.navigation.mobileSidebarOpen;
    }
    state.navigation = nextNavigation;
  }

  if (raw.previewCards && typeof raw.previewCards === "object") {
    const hydratedLayouts = {};
    Object.entries(raw.previewCards).forEach(([cardId, layout]) => {
      if (!cardIds.has(cardId) || !layout || typeof layout !== "object") {
        return;
      }
      hydratedLayouts[cardId] = {
        page: layout.page === 2 ? 2 : 1,
        x: Number(layout.x) || 0,
        y: Number(layout.y) || 0,
        width: Number(layout.width) || 160,
        height: Number(layout.height) || 220,
        z: Number(layout.z) || 1,
        locked: Boolean(layout.locked),
        title: typeof layout.title === "string" ? layout.title.trim() : "",
      };
    });
    state.previewCards = hydratedLayouts;
  }

  if (Number.isFinite(raw.previewZCounter)) {
    state.previewZCounter = clamp(Number(raw.previewZCounter), 1, 99999);
  }
}

function getPersistedRawState() {
  try {
    const raw = window.localStorage.getItem(APP_STATE_STORAGE_KEY);
    if (!raw) {
      return null;
    }
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

function syncFilterControls() {
  refs.searchInput.value = state.filters.search;
  refs.weekFilterList?.querySelectorAll(".weekCheck").forEach((checkbox) => {
    const week = Number(checkbox.value);
    checkbox.checked = state.filters.weeks.has(week);
  });
}

function schedulePersistState() {
  if (persistTimer) {
    window.clearTimeout(persistTimer);
  }
  persistTimer = window.setTimeout(() => {
    persistTimer = 0;
    persistAppState();
  }, 120);
}

function persistAppState() {
  if (!state.cards.length) {
    return;
  }
  const payload = {
    filters: {
      search: state.filters.search,
      weeks: [...state.filters.weeks],
    },
    drafts: state.drafts,
    navigation: state.navigation,
    layout: state.layout,
    previewCards: state.previewCards,
    previewZCounter: state.previewZCounter,
  };
  const serialized = JSON.stringify(payload);
  if (serialized === lastPersistedPayload) {
    return;
  }
  try {
    window.localStorage.setItem(APP_STATE_STORAGE_KEY, serialized);
    lastPersistedPayload = serialized;
  } catch {
    // Ignore storage quota/privacy mode errors.
  }
}

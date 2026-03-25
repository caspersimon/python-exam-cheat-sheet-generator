function setLoadingState() {
  refs.cardHost.innerHTML = `<div class="empty-state"><p>Loading topic explorer...</p></div>`;
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
  } catch {}
}

function resetSplashIntro() {
  try {
    window.localStorage.removeItem(SPLASH_STORAGE_KEY);
  } catch {}
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
  } catch {}
  lastPersistedPayload = "";

  state.filters.search = "";
  state.filters.coursePhases = new Set(DEFAULT_COURSE_PHASES);
  state.filters.recurrenceLevels = new Set(DEFAULT_RECURRENCE_LEVELS);
  state.drafts = {};
  state.selectedPresetId = "";
  state.navigation = buildDefaultNavigationState();
  state.previewHistory = [];
  state.openDrawer = "";
  state.previewCards = {};
  state.previewEntries = {};
  state.previewZCounter = 1;
  state.layout = {
    fontFamily: DEFAULT_FONT_FAMILY,
    fontSize: 8.5,
    titleSize: 9.5,
    lineHeight: 1.08,
    letterSpacing: 0,
    cardGap: 4,
    cardPadding: 5,
    codeBlockPadding: 4,
    codeBlockMargin: 1,
    autoGrid: true,
    gridColumns: 2,
    gridRows: 6,
    page1Landscape: false,
    page2Landscape: false,
    tableSize: 7,
    pieceGap: 2,
    titleMargin: 1,
  };

  renderFilterControls(DEFAULT_COURSE_PHASES, DEFAULT_RECURRENCE_LEVELS);
  renderPresetSurfaces();
  syncFilterControls();
  applyLayoutVariables();
  ensureExplorerNavigation(getFilteredTopics());
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

  const snippetIds = new Set(state.snippets.map((snippet) => snippet.id));
  const topicIds = new Set(state.topics.map((topic) => topic.id));

  if (raw.layout && typeof raw.layout === "object") {
    const fontAliases = new Map([
      ["'Manrope', sans-serif", "'Manrope', sans-serif"],
      ["'Inter', sans-serif", "'Inter', sans-serif"],
      ["'Space Grotesk', sans-serif", "'Space Grotesk', sans-serif"],
      ["'DM Sans', sans-serif", "'DM Sans', sans-serif"],
      ["'Public Sans', sans-serif", "'Public Sans', sans-serif"],
      ["'IBM Plex Sans', sans-serif", "'IBM Plex Sans', sans-serif"],
      ["'Source Sans 3', sans-serif", "'Source Sans 3', sans-serif"],
      ["'Work Sans', sans-serif", "'Work Sans', sans-serif"],
      ["'Newsreader', serif", "'Newsreader', serif"],
      ["'Source Serif 4', serif", "'Source Serif 4', serif"],
      ["'Merriweather', serif", "'Merriweather', serif"],
      ["'Lora', serif", "'Lora', serif"],
    ]);
    const rawFontFamily = typeof raw.layout.fontFamily === "string" ? raw.layout.fontFamily : "";
    const hydratedFont = fontAliases.get(rawFontFamily) ?? rawFontFamily;
    if (FONT_FAMILY_VALUES.has(hydratedFont)) {
      state.layout.fontFamily = hydratedFont;
    } else {
      state.layout.fontFamily = DEFAULT_FONT_FAMILY;
    }
    if (Number.isFinite(raw.layout.fontSize)) state.layout.fontSize = clamp(Number(raw.layout.fontSize), 4, 20);
    if (Number.isFinite(raw.layout.titleSize)) {
      let titleSize = clamp(Number(raw.layout.titleSize), 4, 20);
      // Migrate: old default had titleSize < fontSize which is visually wrong
      if (titleSize < state.layout.fontSize * 0.9) {
        titleSize = Math.round(state.layout.fontSize * 1.12 * 10) / 10;
      }
      state.layout.titleSize = titleSize;
    }
    if (Number.isFinite(raw.layout.lineHeight)) state.layout.lineHeight = clamp(Number(raw.layout.lineHeight), 0.2, 3);
    if (Number.isFinite(raw.layout.letterSpacing))
      state.layout.letterSpacing = clamp(Number(raw.layout.letterSpacing), -1, 3);
    if (Number.isFinite(raw.layout.cardGap)) state.layout.cardGap = clamp(Number(raw.layout.cardGap), 0, 30);
    if (Number.isFinite(raw.layout.cardPadding)) state.layout.cardPadding = clamp(Number(raw.layout.cardPadding), 0, 30);
    if (Number.isFinite(raw.layout.codeBlockPadding))
      state.layout.codeBlockPadding = clamp(Number(raw.layout.codeBlockPadding), 0, 20);
    if (Number.isFinite(raw.layout.codeBlockMargin))
      state.layout.codeBlockMargin = clamp(Number(raw.layout.codeBlockMargin), 0, 16);
    if (typeof raw.layout.autoGrid === "boolean") state.layout.autoGrid = raw.layout.autoGrid;
    if (Number.isFinite(raw.layout.gridColumns)) state.layout.gridColumns = clamp(Number(raw.layout.gridColumns), 1, 4);
    if (Number.isFinite(raw.layout.gridRows)) state.layout.gridRows = clamp(Number(raw.layout.gridRows), 3, 14);
    if (typeof raw.layout.page1Landscape === "boolean") state.layout.page1Landscape = raw.layout.page1Landscape;
    if (typeof raw.layout.page2Landscape === "boolean") state.layout.page2Landscape = raw.layout.page2Landscape;
    if (Number.isFinite(raw.layout.tableSize)) state.layout.tableSize = clamp(Number(raw.layout.tableSize), 5, 12);
    if (Number.isFinite(raw.layout.pieceGap)) state.layout.pieceGap = clamp(Number(raw.layout.pieceGap), 0, 10);
    if (Number.isFinite(raw.layout.titleMargin)) state.layout.titleMargin = clamp(Number(raw.layout.titleMargin), 0, 8);
  }

  if (raw.filters && typeof raw.filters === "object") {
    state.filters.search = typeof raw.filters.search === "string" ? raw.filters.search : state.filters.search;
    if (Array.isArray(raw.filters.coursePhases)) {
      const values = raw.filters.coursePhases.map((value) => String(value || "").trim()).filter(Boolean);
      if (values.length) {
        state.filters.coursePhases = new Set(values);
      }
    }
    if (Array.isArray(raw.filters.recurrenceLevels)) {
      const values = raw.filters.recurrenceLevels.map((value) => String(value || "").trim()).filter(Boolean);
      if (values.length) {
        state.filters.recurrenceLevels = new Set(values);
      }
    }
  }

  if (raw.drafts && typeof raw.drafts === "object") {
    const hydratedDrafts = {};
    Object.entries(raw.drafts).forEach(([snippetId, draft]) => {
      if (!snippetIds.has(snippetId) || !draft || typeof draft !== "object") {
        return;
      }

      const snippet = findSnippetById(snippetId);
      const validPieceIds = new Set(getSnippetSelectablePieceIds(snippet));
      const selectedPieces = Array.isArray(draft.selected?.pieces)
        ? draft.selected.pieces.filter((pieceId) => validPieceIds.has(pieceId))
        : [];
      const rawOverrides = draft.overrides?.pieces && typeof draft.overrides.pieces === "object" ? draft.overrides.pieces : {};
      const cleanOverrides = {};
      Object.entries(rawOverrides).forEach(([pieceId, value]) => {
        if (validPieceIds.has(pieceId) && value && typeof value === "object") {
          cleanOverrides[pieceId] = deepClone(value);
        }
      });

      hydratedDrafts[snippetId] = {
        selected: { pieces: [...new Set(selectedPieces)] },
        overrides: { pieces: cleanOverrides },
      };
    });
    state.drafts = hydratedDrafts;
  }

  if (raw.navigation && typeof raw.navigation === "object") {
    const nextNavigation = buildDefaultNavigationState();
    const activeTopicId = String(raw.navigation.activeTopicId || "").trim();
    if (topicIds.has(activeTopicId)) {
      nextNavigation.activeTopicId = activeTopicId;
    }
    if (typeof raw.navigation.mobileSidebarOpen === "boolean") {
      nextNavigation.mobileSidebarOpen = raw.navigation.mobileSidebarOpen;
    }
    state.navigation = nextNavigation;
  }

  if (typeof raw.selectedPresetId === "string") {
    const presetId = raw.selectedPresetId.trim();
    if (presetId && state.presets.some((preset) => preset.id === presetId)) {
      state.selectedPresetId = presetId;
    }
  }

  if (raw.previewCards && typeof raw.previewCards === "object") {
    const hydratedLayouts = {};
    Object.entries(raw.previewCards).forEach(([snippetId, layout]) => {
      if (!snippetIds.has(snippetId) || !layout || typeof layout !== "object") {
        return;
      }
      hydratedLayouts[snippetId] = {
        page: layout.page === 2 ? 2 : 1,
        x: Number(layout.x) || 0,
        y: Number(layout.y) || 0,
        width: Number(layout.width) || 160,
        height: Number(layout.height) || 220,
        z: Number(layout.z) || 1,
        locked: Boolean(layout.locked),
        title: typeof layout.title === "string" ? layout.title.trim() : "",
        ...(layout.summaryOverride !== undefined ? { summaryOverride: String(layout.summaryOverride) } : {}),
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
  syncCheckboxFilterGroup(refs.coursePhaseFilterList, ".coursePhaseCheck", state.filters.coursePhases);
  syncCheckboxFilterGroup(refs.recurrenceFilterList, ".recurrenceCheck", state.filters.recurrenceLevels);
}

function syncCheckboxFilterGroup(host, selector, selectedValues) {
  host?.querySelectorAll(selector).forEach((checkbox) => {
    checkbox.checked = selectedValues.has(checkbox.value);
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
  if (!state.snippets.length) {
    return;
  }
  const payload = {
    filters: {
      search: state.filters.search,
      coursePhases: [...state.filters.coursePhases],
      recurrenceLevels: [...state.filters.recurrenceLevels],
    },
    drafts: state.drafts,
    navigation: state.navigation,
    selectedPresetId: state.selectedPresetId,
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
  } catch {}
}

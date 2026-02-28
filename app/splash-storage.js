function setLoadingState() {
  refs.cardHost.innerHTML = `<div class="empty-state"><p>Loading topic cards...</p></div>`;
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
    "Reset all progress?\n\nThis will permanently remove your saved decisions, selections, filters, layout settings, and preview positions."
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
  state.filters.onlyExam = true;
  state.filters.minHits = 0;
  state.filters.weeks = new Set([1, 2, 3]);

  state.drafts = {};
  state.decisions = {};
  state.acceptedOrder = [];
  state.history = [];
  state.previewHistory = [];
  state.openDrawer = "";
  state.previewCards = {};
  state.previewZCounter = 1;
  state.preferences = {
    sourceAutoSelectMode: "none",
  };
  state.layout = {
    fontFamily: "'Space Grotesk', sans-serif",
    fontSize: 9.5,
    lineHeight: 1.1,
    letterSpacing: 0,
    cardGap: 6,
    cardPadding: 7,
    autoGrid: true,
    gridColumns: 2,
    gridRows: 6,
  };

  syncFilterControls();
  applyLayoutVariables();
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

  if (raw.preferences && typeof raw.preferences === "object") {
    const mode = raw.preferences.sourceAutoSelectMode;
    if (mode === "recommended" || mode === "none") {
      state.preferences.sourceAutoSelectMode = mode;
    }
  }

  if (raw.layout && typeof raw.layout === "object") {
    const allowedFonts = new Set(["'Space Grotesk', sans-serif", "'DM Sans', sans-serif", "'Source Serif 4', serif"]);
    if (allowedFonts.has(raw.layout.fontFamily)) {
      state.layout.fontFamily = raw.layout.fontFamily;
    }
    if (Number.isFinite(raw.layout.fontSize)) {
      state.layout.fontSize = clamp(Number(raw.layout.fontSize), 7, 14);
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
    if (typeof raw.filters.onlyExam === "boolean") {
      state.filters.onlyExam = raw.filters.onlyExam;
    }
    if (Number.isFinite(raw.filters.minHits)) {
      state.filters.minHits = clamp(Number(raw.filters.minHits), 0, 3);
    }
    if (Array.isArray(raw.filters.weeks)) {
      const validWeeks = raw.filters.weeks
        .map((value) => Number(value))
        .filter((value) => [1, 2, 3].includes(value));
      if (validWeeks.length) {
        state.filters.weeks = new Set(validWeeks);
      }
    }
  }

  if (raw.decisions && typeof raw.decisions === "object") {
    const hydratedDecisions = {};
    Object.entries(raw.decisions).forEach(([cardId, entry]) => {
      if (!cardIds.has(cardId) || !entry || typeof entry !== "object") {
        return;
      }
      if (entry.status === "accepted" && entry.selection && typeof entry.selection === "object") {
        hydratedDecisions[cardId] = {
          status: "accepted",
          selection: deepClone(entry.selection),
        };
        return;
      }
      if (entry.status === "rejected") {
        hydratedDecisions[cardId] = { status: "rejected" };
      }
    });
    state.decisions = hydratedDecisions;
  }

  if (raw.drafts && typeof raw.drafts === "object") {
    const hydratedDrafts = {};
    Object.entries(raw.drafts).forEach(([cardId, draft]) => {
      if (!cardIds.has(cardId) || !draft || typeof draft !== "object") {
        return;
      }
      hydratedDrafts[cardId] = deepClone(draft);
    });
    state.drafts = hydratedDrafts;
  }

  if (Array.isArray(raw.acceptedOrder)) {
    const seen = new Set();
    state.acceptedOrder = raw.acceptedOrder.filter((cardId) => {
      if (!cardIds.has(cardId) || seen.has(cardId)) {
        return false;
      }
      if (state.decisions[cardId]?.status !== "accepted") {
        return false;
      }
      seen.add(cardId);
      return true;
    });

    Object.entries(state.decisions).forEach(([cardId, decision]) => {
      if (decision?.status === "accepted" && !seen.has(cardId)) {
        state.acceptedOrder.push(cardId);
        seen.add(cardId);
      }
    });
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
        width: Number(layout.width) || 260,
        height: Number(layout.height) || 220,
        z: Number(layout.z) || 1,
        locked: Boolean(layout.locked),
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
  refs.onlyExamToggle.checked = state.filters.onlyExam;
  refs.minHitsSelect.value = String(state.filters.minHits);
  refs.weekChecks.forEach((checkbox) => {
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
      onlyExam: state.filters.onlyExam,
      minHits: state.filters.minHits,
      weeks: [...state.filters.weeks],
    },
    drafts: state.drafts,
    decisions: state.decisions,
    acceptedOrder: state.acceptedOrder,
    preferences: state.preferences,
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

const SPLASH_STORAGE_KEY = "python_midterm_splash_seen_v3";
const APP_STATE_STORAGE_KEY = "python_midterm_app_state_v9";
const EXAM_BUILDER_DATASET_VERSION = "2026-03-24-manual-curation-hard-cut";
const CANONICAL_WEEK_ORDER = [1, 2, 3, 4, 5, 6];
const DEFAULT_PAGE_INNER_WIDTH = 758;
const DEFAULT_PAGE_INNER_HEIGHT = 1079;

function buildDefaultNavigationState() {
  return {
    activeTopicId: "",
    activeParentId: "",
    expandedParents: {},
    mobileSidebarOpen: false,
  };
}

const state = {
  parentTopics: [],
  cards: [],
  filters: {
    search: "",
    weeks: new Set(CANONICAL_WEEK_ORDER),
  },
  drafts: {},
  navigation: buildDefaultNavigationState(),
  previewHistory: [],
  view: "swipe",
  openDrawer: "",
  previewCards: {},
  previewEntries: {},
  previewZCounter: 1,
  layout: {
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
  },
};

const refs = {
  swipeView: document.getElementById("swipeView"),
  previewView: document.getElementById("previewView"),

  progressText: document.getElementById("progressText"),
  selectionShell: document.getElementById("selectionShell"),
  topicSidebar: document.getElementById("topicSidebar"),
  cardHost: document.getElementById("cardHost"),
  swipeHeaderActions: document.getElementById("swipeHeaderActions"),
  previewHeaderActions: document.getElementById("previewHeaderActions"),

  openTopicSidebarBtn: document.getElementById("openTopicSidebarBtn"),
  openFiltersBtn: document.getElementById("openFiltersBtn"),
  openStatsBtn: document.getElementById("openStatsBtn"),
  openLayoutBtn: document.getElementById("openLayoutBtn"),
  openOrderBtn: document.getElementById("openOrderBtn"),
  previewUndoBtn: document.getElementById("previewUndoBtn"),

  filtersDrawer: document.getElementById("filtersDrawer"),
  statsDrawer: document.getElementById("statsDrawer"),
  layoutDrawer: document.getElementById("layoutDrawer"),
  orderDrawer: document.getElementById("orderDrawer"),
  drawerBackdrop: document.getElementById("drawerBackdrop"),
  topicSidebarBackdrop: document.getElementById("topicSidebarBackdrop"),
  closeDrawerButtons: Array.from(document.querySelectorAll(".close-drawer-btn")),

  acceptedCount: document.getElementById("acceptedCount"),
  rejectedCount: document.getElementById("rejectedCount"),
  remainingCount: document.getElementById("remainingCount"),
  acceptedTopicsList: document.getElementById("acceptedTopicsList"),
  weekFilterList: document.getElementById("weekFilterList"),

  previewOrderList: document.getElementById("previewOrderList"),
  page1Content: document.getElementById("page1Content"),
  page2Content: document.getElementById("page2Content"),
  overflowNotice: document.getElementById("overflowNotice"),
  sheetStage: document.getElementById("sheetStage"),

  searchInput: document.getElementById("searchInput"),
  skipToPreviewBtn: document.getElementById("skipToPreviewBtn"),
  goToSwipeBtn: document.getElementById("goToSwipeBtn"),
  goToPreviewBtn: document.getElementById("goToPreviewBtn"),

  printBtn: document.getElementById("printBtn"),
  exportPngBtn: document.getElementById("exportPngBtn"),
  exportPdfBtn: document.getElementById("exportPdfBtn"),

  autoGridToggle: document.getElementById("autoGridToggle"),
  gridColumnsRange: document.getElementById("gridColumnsRange"),
  gridRowsRange: document.getElementById("gridRowsRange"),
  gridColumnsValue: document.getElementById("gridColumnsValue"),
  gridRowsValue: document.getElementById("gridRowsValue"),

  fontFamilySelect: document.getElementById("fontFamilySelect"),
  fontSizeRange: document.getElementById("fontSizeRange"),
  titleSizeRange: document.getElementById("titleSizeRange"),
  lineHeightRange: document.getElementById("lineHeightRange"),
  letterSpacingRange: document.getElementById("letterSpacingRange"),
  cardGapRange: document.getElementById("cardGapRange"),
  cardPaddingRange: document.getElementById("cardPaddingRange"),
  codeBlockPaddingRange: document.getElementById("codeBlockPaddingRange"),
  codeBlockMarginRange: document.getElementById("codeBlockMarginRange"),
  fontSizeValue: document.getElementById("fontSizeValue"),
  titleSizeValue: document.getElementById("titleSizeValue"),
  lineHeightValue: document.getElementById("lineHeightValue"),
  letterSpacingValue: document.getElementById("letterSpacingValue"),
  cardGapValue: document.getElementById("cardGapValue"),
  cardPaddingValue: document.getElementById("cardPaddingValue"),
  codeBlockPaddingValue: document.getElementById("codeBlockPaddingValue"),
  codeBlockMarginValue: document.getElementById("codeBlockMarginValue"),
  splashOverlay: document.getElementById("splashOverlay"),
  getStartedBtn: document.getElementById("getStartedBtn"),
};

const drawerMap = {
  filters: refs.filtersDrawer,
  stats: refs.statsDrawer,
  layout: refs.layoutDrawer,
  order: refs.orderDrawer,
};

let persistTimer = 0;
let lastPersistedPayload = "";
const previewPointerState = {
  active: false,
  pointerId: null,
  mode: "",
  cardId: "",
  cardEl: null,
  startX: 0,
  startY: 0,
  startLeft: 0,
  startTop: 0,
  startWidth: 0,
  startHeight: 0,
  grabOffsetX: 0,
  grabOffsetY: 0,
};

async function init() {
  bindEvents();
  syncViewButtons();
  applyLayoutVariables();
  setLoadingState();
  maybeShowSplash();

  try {
    const response = await fetch(`./data/exam_builder_topics.json?v=${encodeURIComponent(EXAM_BUILDER_DATASET_VERSION)}`);
    if (!response.ok) {
      throw new Error(`Failed to load exam_builder_topics.json (${response.status})`);
    }

    const payload = await response.json();
    const normalized = normalizeExamBuilderPayload(payload);
    state.parentTopics = normalized.parentTopics;
    state.cards = normalized.cards;

    renderWeekFilterControls();
    hydratePersistedState();
    ensureExplorerNavigation(getFilteredParentBundles());
    syncFilterControls();
    applyLayoutVariables();
    renderAll();
    if (getSelectedPreviewEntries().length > 0 && state.view === "preview") {
      setView("preview");
    }
  } catch (error) {
    refs.cardHost.innerHTML = `<div class="empty-state">
      <p><strong>Could not load <code>data/exam_builder_topics.json</code>.</strong></p>
      <p>${escapeHtml(error.message)}</p>
      <p>Refresh the manually curated dataset at <code>data/exam_builder_topics.json</code>, then serve the repo with <code>python3 -m http.server 4173</code>.</p>
    </div>`;
  }
}

function readClampedRangeValue(rangeInput) {
  const rawValue = Number(rangeInput?.value);
  const min = Number(rangeInput?.min);
  const max = Number(rangeInput?.max);
  const safeMin = Number.isFinite(min) ? min : rawValue;
  const safeMax = Number.isFinite(max) ? max : rawValue;
  const fallback = Number.isFinite(safeMin) ? safeMin : 0;
  if (!Number.isFinite(rawValue)) {
    return fallback;
  }
  return clamp(rawValue, Math.min(safeMin, safeMax), Math.max(safeMin, safeMax));
}

function bindEvents() {
  refs.searchInput.addEventListener("input", (event) => {
    state.filters.search = event.target.value.trim().toLowerCase();
    renderAll();
  });

  refs.skipToPreviewBtn.addEventListener("click", () => setView("preview"));
  refs.goToSwipeBtn.addEventListener("click", () => setView("swipe"));
  refs.goToPreviewBtn.addEventListener("click", () => setView("preview"));
  refs.openTopicSidebarBtn?.addEventListener("click", () => {
    state.navigation.mobileSidebarOpen = true;
    renderSwipe();
    schedulePersistState();
  });

  refs.openFiltersBtn.addEventListener("click", () => toggleDrawer("filters"));
  refs.openStatsBtn.addEventListener("click", () => toggleDrawer("stats"));
  refs.openLayoutBtn.addEventListener("click", () => toggleDrawer("layout"));
  refs.openOrderBtn.addEventListener("click", () => toggleDrawer("order"));

  refs.closeDrawerButtons.forEach((btn) => {
    btn.addEventListener("click", () => closeDrawers());
  });

  refs.drawerBackdrop.addEventListener("click", () => closeDrawers());
  refs.topicSidebarBackdrop?.addEventListener("click", () => {
    state.navigation.mobileSidebarOpen = false;
    renderSwipe();
    schedulePersistState();
  });

  if (refs.getStartedBtn) {
    refs.getStartedBtn.addEventListener("click", dismissSplash);
  }
  if (refs.splashOverlay) {
    refs.splashOverlay.addEventListener("click", (event) => {
      if (event.target === refs.splashOverlay) {
        dismissSplash();
      }
    });
  }

  refs.selectionShell?.addEventListener("change", handleCardInputChange);
  refs.selectionShell?.addEventListener("click", handleCardClick);
  refs.selectionShell?.addEventListener("mouseover", handleCardMouseOver);
  document.addEventListener("click", (event) => {
    if (event.target.closest("#selectionShell .info-chip")) {
      return;
    }
    closeOpenInfoPopovers();
  });

  document.addEventListener("keydown", (event) => {
    if (isSplashVisible()) {
      if (event.key === "Escape") {
        event.preventDefault();
        dismissSplash();
      }
      return;
    }

    if (event.key === "Escape") {
      closeOpenInfoPopovers();
      closeDrawers();
      return;
    }

    if (state.view !== "swipe") {
      const isUndoShortcut =
        (event.metaKey || event.ctrlKey) &&
        !event.altKey &&
        !event.shiftKey &&
        event.key.toLowerCase() === "z";
      if (state.view === "preview" && isUndoShortcut && !isEditableKeyTarget(event.target) && !isPreviewEditModalOpen()) {
        event.preventDefault();
        undoLastPreviewChange();
      }
      return;
    }

    if (isEditableKeyTarget(event.target)) {
      return;
    }
  });

  refs.autoGridToggle.addEventListener("change", (event) => {
    state.layout.autoGrid = Boolean(event.target.checked);
    applyLayoutVariables();
    renderPreview();
  });

  refs.gridColumnsRange.addEventListener("input", (event) => {
    state.layout.gridColumns = readClampedRangeValue(event.target);
    applyLayoutVariables();
    renderPreview();
  });

  refs.gridRowsRange.addEventListener("input", (event) => {
    state.layout.gridRows = readClampedRangeValue(event.target);
    applyLayoutVariables();
    renderPreview();
  });

  refs.fontFamilySelect.addEventListener("change", (event) => {
    state.layout.fontFamily = event.target.value;
    applyLayoutVariables();
    renderPreview();
  });

  refs.fontSizeRange.addEventListener("input", (event) => {
    state.layout.fontSize = readClampedRangeValue(event.target);
    applyLayoutVariables();
    renderPreview();
  });

  refs.titleSizeRange.addEventListener("input", (event) => {
    state.layout.titleSize = readClampedRangeValue(event.target);
    applyLayoutVariables();
    renderPreview();
  });

  refs.lineHeightRange.addEventListener("input", (event) => {
    state.layout.lineHeight = readClampedRangeValue(event.target);
    applyLayoutVariables();
    renderPreview();
  });

  refs.letterSpacingRange.addEventListener("input", (event) => {
    state.layout.letterSpacing = readClampedRangeValue(event.target);
    applyLayoutVariables();
    renderPreview();
  });

  refs.cardGapRange.addEventListener("input", (event) => {
    state.layout.cardGap = readClampedRangeValue(event.target);
    applyLayoutVariables();
    renderPreview();
  });

  refs.cardPaddingRange.addEventListener("input", (event) => {
    state.layout.cardPadding = readClampedRangeValue(event.target);
    applyLayoutVariables();
    renderPreview();
  });

  refs.codeBlockPaddingRange.addEventListener("input", (event) => {
    state.layout.codeBlockPadding = readClampedRangeValue(event.target);
    applyLayoutVariables();
    renderPreview();
  });

  refs.codeBlockMarginRange.addEventListener("input", (event) => {
    state.layout.codeBlockMargin = readClampedRangeValue(event.target);
    applyLayoutVariables();
    renderPreview();
  });

  refs.printBtn.addEventListener("click", printGeneratedPdf);
  refs.previewUndoBtn?.addEventListener("click", () => undoLastPreviewChange());
  refs.exportPngBtn.addEventListener("click", exportPng);
  refs.exportPdfBtn.addEventListener("click", exportPdf);

  refs.sheetStage.addEventListener("pointerdown", handlePreviewPointerDown);
  document.addEventListener("pointermove", handlePreviewPointerMove);
  document.addEventListener("pointerup", finishPreviewPointerAction);
  document.addEventListener("pointercancel", finishPreviewPointerAction);
}

function renderWeekFilterControls() {
  if (!refs.weekFilterList) {
    return;
  }

  refs.weekFilterList.innerHTML = CANONICAL_WEEK_ORDER.map((week) => {
    const checked = state.filters.weeks.has(week);
    return `<label><input class="weekCheck" type="checkbox" value="${week}" ${checked ? "checked" : ""} />W${week}</label>`;
  }).join("");

  refs.weekFilterList.querySelectorAll(".weekCheck").forEach((checkbox) => {
    checkbox.addEventListener("change", () => {
      const selected = Array.from(refs.weekFilterList.querySelectorAll(".weekCheck"))
        .filter((el) => el.checked)
        .map((el) => Number(el.value));
      state.filters.weeks = new Set(selected);
      renderAll();
    });
  });
}

function isEditableKeyTarget(target) {
  if (!(target instanceof Element)) {
    return false;
  }
  return Boolean(target.closest("input, textarea, select, [contenteditable='true']"));
}

function isPreviewEditModalOpen() {
  return document.body.classList.contains("preview-edit-modal-open");
}

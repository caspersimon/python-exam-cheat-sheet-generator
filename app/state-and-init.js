const SPLASH_STORAGE_KEY = "python_midterm_splash_seen_v3";
const APP_STATE_STORAGE_KEY = "python_midterm_app_state_v12";
const FRONTEND_BUNDLE_VERSION = "2026-03-25-new-database-hard-cut-presets";
const FRONTEND_BUNDLE_PATH = "./new_database/exports/frontend_bundle.json";
const DEFAULT_PAGE_INNER_WIDTH = 758;
const DEFAULT_PAGE_INNER_HEIGHT = 1079;
const DEFAULT_COURSE_PHASES = ["pre-midterm", "post-midterm", "mixed"];
const DEFAULT_RECURRENCE_LEVELS = ["signature", "very-common", "common", "occasional", "rare"];
const DEFAULT_FONT_FAMILY = "'Manrope', sans-serif";
const FONT_FAMILY_OPTIONS = Object.freeze([
  { label: "Manrope", value: "'Manrope', sans-serif" },
  { label: "Inter", value: "'Inter', sans-serif" },
  { label: "Space Grotesk", value: "'Space Grotesk', sans-serif" },
  { label: "DM Sans", value: "'DM Sans', sans-serif" },
  { label: "Public Sans", value: "'Public Sans', sans-serif" },
  { label: "IBM Plex Sans", value: "'IBM Plex Sans', sans-serif" },
  { label: "Source Sans 3", value: "'Source Sans 3', sans-serif" },
  { label: "Work Sans", value: "'Work Sans', sans-serif" },
  { label: "Newsreader", value: "'Newsreader', serif" },
  { label: "Source Serif 4", value: "'Source Serif 4', serif" },
  { label: "Merriweather", value: "'Merriweather', serif" },
  { label: "Lora", value: "'Lora', serif" },
]);
const FONT_FAMILY_VALUES = new Set(FONT_FAMILY_OPTIONS.map((option) => option.value));

function buildDefaultNavigationState() {
  return {
    activeTopicId: "",
    mobileSidebarOpen: false,
  };
}

const state = {
  topics: [],
  parentTopics: [],
  snippets: [],
  presets: [],
  cards: [],
  filters: {
    search: "",
    coursePhases: new Set(DEFAULT_COURSE_PHASES),
    recurrenceLevels: new Set(DEFAULT_RECURRENCE_LEVELS),
  },
  drafts: {},
  navigation: buildDefaultNavigationState(),
  selectedPresetId: "",
  previewHistory: [],
  view: "swipe",
  openDrawer: "",
  previewCards: {},
  previewEntries: {},
  previewZCounter: 1,
  detachedPieces: {},
  layout: {
    fontFamily: DEFAULT_FONT_FAMILY,
    fontSize: 8.5,
    titleSize: 9.5,
    lineHeight: 0.9,
    letterSpacing: 0,
    cardGap: 4,
    cardPadding: 5,
    codeBlockPadding: 4,
    codeBlockMargin: 1,
    tableSize: 7,
    pieceGap: 2,
    titleMargin: 1,
    autoGrid: false,
    gridColumns: 2,
    gridRows: 4,
    page1Landscape: false,
    page2Landscape: false,
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
  openPresetsBtn: document.getElementById("openPresetsBtn"),
  openStatsBtn: document.getElementById("openStatsBtn"),
  openLayoutBtn: document.getElementById("openLayoutBtn"),
  openOrderBtn: document.getElementById("openOrderBtn"),
  previewUndoBtn: document.getElementById("previewUndoBtn"),

  filtersDrawer: document.getElementById("filtersDrawer"),
  presetsDrawer: document.getElementById("presetsDrawer"),
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
  activePresetName: document.getElementById("activePresetName"),
  coursePhaseFilterList: document.getElementById("coursePhaseFilterList"),
  recurrenceFilterList: document.getElementById("recurrenceFilterList"),
  presetList: document.getElementById("presetList"),

  previewOrderList: document.getElementById("previewOrderList"),
  page1Content: document.getElementById("page1Content"),
  page2Content: document.getElementById("page2Content"),
  overflowNotice: document.getElementById("overflowNotice"),
  stagedSnippetCount: document.getElementById("stagedSnippetCount"),
  stagedSnippetList: document.getElementById("stagedSnippetList"),
  addAllStagedBtn: document.getElementById("addAllStagedBtn"),
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
  tableSizeRange: document.getElementById("tableSizeRange"),
  pieceGapRange: document.getElementById("pieceGapRange"),
  titleMarginRange: document.getElementById("titleMarginRange"),
  tableSizeValue: document.getElementById("tableSizeValue"),
  pieceGapValue: document.getElementById("pieceGapValue"),
  titleMarginValue: document.getElementById("titleMarginValue"),
  fontSizeValue: document.getElementById("fontSizeValue"),
  titleSizeValue: document.getElementById("titleSizeValue"),
  lineHeightValue: document.getElementById("lineHeightValue"),
  letterSpacingValue: document.getElementById("letterSpacingValue"),
  cardGapValue: document.getElementById("cardGapValue"),
  cardPaddingValue: document.getElementById("cardPaddingValue"),
  codeBlockPaddingValue: document.getElementById("codeBlockPaddingValue"),
  codeBlockMarginValue: document.getElementById("codeBlockMarginValue"),
  splashOverlay: document.getElementById("splashOverlay"),
  splashPresetList: document.getElementById("splashPresetList"),
  getStartedBtn: document.getElementById("getStartedBtn"),
  page1LandscapeToggle: document.getElementById("page1LandscapeToggle"),
  page2LandscapeToggle: document.getElementById("page2LandscapeToggle"),
  smartFitBtn: document.getElementById("smartFitBtn"),
};

const drawerMap = {
  filters: refs.filtersDrawer,
  presets: refs.presetsDrawer,
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
  populateFontFamilyOptions();
  bindEvents();
  bindPreviewEditingEvents();
  syncViewButtons();
  applyLayoutVariables();
  setLoadingState();
  maybeShowSplash();

  try {
    const response = await fetch(`${FRONTEND_BUNDLE_PATH}?v=${encodeURIComponent(FRONTEND_BUNDLE_VERSION)}`);
    if (!response.ok) {
      throw new Error(`Failed to load frontend bundle (${response.status})`);
    }

    const payload = await response.json();
    const normalized = normalizeSnippetBankPayload(payload);
    state.topics = normalized.topics;
    state.parentTopics = normalized.topics;
    state.snippets = normalized.snippets;
    state.presets = normalized.presets;
    state.cards = normalized.snippets;

    renderFilterControls(normalized.availableCoursePhases, normalized.availableRecurrenceLevels);
    hydratePersistedState();
    renderPresetSurfaces();
    ensureExplorerNavigation(getFilteredTopics());
    syncFilterControls();
    applyLayoutVariables();
    renderAll();
    if (getSelectedPreviewEntries().length > 0 && state.view === "preview") {
      setView("preview");
    }
  } catch (error) {
    refs.cardHost.innerHTML = `<div class="empty-state">
      <p><strong>Could not load <code>new_database/exports/frontend_bundle.json</code>.</strong></p>
      <p>${escapeHtml(error.message)}</p>
      <p>Rebuild the bundle with <code>python3 scripts/build_frontend_bundle.py</code>, then serve the repo with <code>python3 -m http.server 4173</code>.</p>
    </div>`;
  }
}

function populateFontFamilyOptions() {
  if (!refs.fontFamilySelect) {
    return;
  }
  refs.fontFamilySelect.innerHTML = FONT_FAMILY_OPTIONS.map(
    (option) => `<option value="${option.value}">${option.label}</option>`
  ).join("");
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

  refs.skipToPreviewBtn?.addEventListener("click", () => setView("preview"));
  refs.goToSwipeBtn.addEventListener("click", () => setView("swipe"));
  refs.goToPreviewBtn.addEventListener("click", () => setView("preview"));
  refs.openTopicSidebarBtn?.addEventListener("click", () => {
    state.navigation.mobileSidebarOpen = true;
    renderSwipe();
    schedulePersistState();
  });

  refs.openFiltersBtn.addEventListener("click", () => toggleDrawer("filters"));
  refs.openPresetsBtn?.addEventListener("click", () => toggleDrawer("presets"));
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
      handleCardClick(event);
      if (event.target === refs.splashOverlay) {
        dismissSplash();
      }
    });
  }

  refs.selectionShell?.addEventListener("change", handleCardInputChange);
  refs.selectionShell?.addEventListener("click", handleCardClick);
  refs.previewView?.addEventListener("click", handlePreviewWorkspaceClick);
  refs.previewView?.addEventListener("dragstart", handlePreviewWorkspaceDragStart);
  refs.previewView?.addEventListener("dragend", handlePreviewWorkspaceDragEnd);
  refs.page1Content?.addEventListener("dragover", handlePreviewPageDragOver);
  refs.page2Content?.addEventListener("dragover", handlePreviewPageDragOver);
  refs.page1Content?.addEventListener("drop", handlePreviewPageDrop);
  refs.page2Content?.addEventListener("drop", handlePreviewPageDrop);
  refs.presetsDrawer?.addEventListener("click", handleCardClick);
  refs.selectionShell?.addEventListener("mouseover", handleCardMouseOver);
  document.addEventListener("click", (event) => {
    if (event.target.closest("#selectionShell .info-chip")) {
      return;
    }
    closeOpenInfoPopovers();
  });

  bindGlobalKeyboardShortcuts();

  refs.autoGridToggle?.addEventListener("change", (event) => {
    state.layout.autoGrid = Boolean(event.target.checked);
    renderPreview();
  });

  refs.gridColumnsRange.addEventListener("input", (event) => {
    state.layout.gridColumns = readClampedRangeValue(event.target);
    renderPreview();
  });

  refs.gridRowsRange.addEventListener("input", (event) => {
    state.layout.gridRows = readClampedRangeValue(event.target);
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

  refs.tableSizeRange?.addEventListener("input", (event) => {
    state.layout.tableSize = readClampedRangeValue(event.target);
    applyLayoutVariables();
  });

  refs.pieceGapRange?.addEventListener("input", (event) => {
    state.layout.pieceGap = readClampedRangeValue(event.target);
    applyLayoutVariables();
  });

  refs.titleMarginRange?.addEventListener("input", (event) => {
    state.layout.titleMargin = readClampedRangeValue(event.target);
    applyLayoutVariables();
  });

  refs.page1LandscapeToggle?.addEventListener("change", (event) => {
    state.layout.page1Landscape = Boolean(event.target.checked);
    applyLayoutVariables();
    renderPreview();
  });
  refs.page2LandscapeToggle?.addEventListener("change", (event) => {
    state.layout.page2Landscape = Boolean(event.target.checked);
    applyLayoutVariables();
    renderPreview();
  });
  refs.smartFitBtn?.addEventListener("click", smartFitLayout);

  refs.printBtn.addEventListener("click", openPrintView);
  refs.previewUndoBtn?.addEventListener("click", () => undoLastPreviewChange());
  refs.exportPngBtn.addEventListener("click", exportPng);
  refs.exportPdfBtn.addEventListener("click", exportPdf);

  refs.sheetStage.addEventListener("pointerdown", handlePreviewPointerDown);
  document.addEventListener("pointermove", handlePreviewPointerMove);
  document.addEventListener("pointerup", finishPreviewPointerAction);
  document.addEventListener("pointercancel", finishPreviewPointerAction);
}

function renderFilterControls(coursePhases, recurrenceLevels) {
  renderCheckboxFilterGroup(
    refs.coursePhaseFilterList,
    "coursePhaseCheck",
    coursePhases.length ? coursePhases : DEFAULT_COURSE_PHASES,
    state.filters.coursePhases,
    "coursePhases"
  );
  renderCheckboxFilterGroup(
    refs.recurrenceFilterList,
    "recurrenceCheck",
    recurrenceLevels.length ? recurrenceLevels : DEFAULT_RECURRENCE_LEVELS,
    state.filters.recurrenceLevels,
    "recurrenceLevels"
  );
}

function renderCheckboxFilterGroup(host, inputClass, values, selectedSet, filterKey) {
  if (!host) {
    return;
  }
  host.innerHTML = values
    .map((value) => {
      const checked = selectedSet.has(value);
      return `<label><input class="${inputClass}" type="checkbox" value="${escapeHtml(value)}" ${checked ? "checked" : ""} />${escapeHtml(
        humanizeTopic(value)
      )}</label>`;
    })
    .join("");

  host.querySelectorAll(`.${inputClass}`).forEach((checkbox) => {
    checkbox.addEventListener("change", () => {
      const nextValues = Array.from(host.querySelectorAll(`.${inputClass}`))
        .filter((entry) => entry.checked)
        .map((entry) => entry.value);
      state.filters[filterKey] = new Set(nextValues);
      renderAll();
    });
  });
}

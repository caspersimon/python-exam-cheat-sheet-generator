const EXAM_LABELS = {
  trial_midterm: "Trial 24/25",
  midterm_2023: "Trial 22/23",
  midterm_2024: "Trial 23/24",
  extra_practice: "Extra Practice",
};

const AI_GENERATION_NOTE = "AI-generated from practice exam questions, lecture snippets, notebook snippets, and trap-pattern context.";
const KEY_POINTS_GENERATION_NOTE = "AI-generated key points and optional details, then filtered against available course materials.";
const SPLASH_STORAGE_KEY = "python_midterm_splash_seen_v1";
const APP_STATE_STORAGE_KEY = "python_midterm_app_state_v1";
const DEFAULT_PAGE_INNER_WIDTH = 758;
const DEFAULT_PAGE_INNER_HEIGHT = 1079;

const state = {
  cards: [],
  filters: {
    search: "",
    onlyExam: true,
    minHits: 0,
    weeks: new Set([1, 2, 3]),
  },
  drafts: {},
  decisions: {},
  acceptedOrder: [],
  history: [],
  previewHistory: [],
  view: "swipe",
  openDrawer: "",
  previewCards: {},
  previewZCounter: 1,
  preferences: {
    sourceAutoSelectMode: "none",
  },
  layout: {
    fontFamily: "'Space Grotesk', sans-serif",
    fontSize: 9.5,
    lineHeight: 1.1,
    letterSpacing: 0,
    cardGap: 6,
    cardPadding: 7,
    autoGrid: true,
    gridColumns: 2,
    gridRows: 6,
  },
};

const refs = {
  swipeView: document.getElementById("swipeView"),
  previewView: document.getElementById("previewView"),

  progressText: document.getElementById("progressText"),
  cardHost: document.getElementById("cardHost"),

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
  closeDrawerButtons: Array.from(document.querySelectorAll(".close-drawer-btn")),

  acceptedCount: document.getElementById("acceptedCount"),
  rejectedCount: document.getElementById("rejectedCount"),
  remainingCount: document.getElementById("remainingCount"),
  acceptedTopicsList: document.getElementById("acceptedTopicsList"),

  previewOrderList: document.getElementById("previewOrderList"),
  page1Content: document.getElementById("page1Content"),
  page2Content: document.getElementById("page2Content"),
  overflowNotice: document.getElementById("overflowNotice"),
  sheetStage: document.getElementById("sheetStage"),

  searchInput: document.getElementById("searchInput"),
  onlyExamToggle: document.getElementById("onlyExamToggle"),
  minHitsSelect: document.getElementById("minHitsSelect"),
  weekChecks: Array.from(document.querySelectorAll(".weekCheck")),

  rejectBtn: document.getElementById("rejectBtn"),
  acceptBtn: document.getElementById("acceptBtn"),
  undoBtn: document.getElementById("undoBtn"),
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
  lineHeightRange: document.getElementById("lineHeightRange"),
  letterSpacingRange: document.getElementById("letterSpacingRange"),
  cardGapRange: document.getElementById("cardGapRange"),
  cardPaddingRange: document.getElementById("cardPaddingRange"),
  fontSizeValue: document.getElementById("fontSizeValue"),
  lineHeightValue: document.getElementById("lineHeightValue"),
  letterSpacingValue: document.getElementById("letterSpacingValue"),
  cardGapValue: document.getElementById("cardGapValue"),
  cardPaddingValue: document.getElementById("cardPaddingValue"),
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
  applyLayoutVariables();
  setLoadingState();
  maybeShowSplash();

  try {
    const response = await fetch("./topic_cards.json");
    if (!response.ok) {
      throw new Error(`Failed to load topic_cards.json (${response.status})`);
    }
    const data = await response.json();
    state.cards = Array.isArray(data.cards) ? data.cards : [];
    hydratePersistedState();
    syncFilterControls();
    applyLayoutVariables();
    renderAll();
  } catch (error) {
    refs.cardHost.innerHTML = `<div class="empty-state">
      <p><strong>Could not load <code>topic_cards.json</code>.</strong></p>
      <p>${escapeHtml(error.message)}</p>
      <p>Serve this folder with <code>python3 -m http.server 8000</code> and open <code>http://localhost:8000</code>.</p>
    </div>`;
  }
}

function bindEvents() {
  refs.searchInput.addEventListener("input", (event) => {
    state.filters.search = event.target.value.trim().toLowerCase();
    renderAll();
  });

  refs.onlyExamToggle.addEventListener("change", (event) => {
    state.filters.onlyExam = Boolean(event.target.checked);
    renderAll();
  });

  refs.minHitsSelect.addEventListener("change", (event) => {
    state.filters.minHits = Number(event.target.value);
    renderAll();
  });

  refs.weekChecks.forEach((checkbox) => {
    checkbox.addEventListener("change", () => {
      const selected = refs.weekChecks
        .filter((el) => el.checked)
        .map((el) => Number(el.value));
      state.filters.weeks = new Set(selected);
      renderAll();
    });
  });

  refs.rejectBtn.addEventListener("click", () => triggerDecision("rejected"));
  refs.acceptBtn.addEventListener("click", () => triggerDecision("accepted"));
  refs.undoBtn.addEventListener("click", undoLastDecision);

  refs.skipToPreviewBtn.addEventListener("click", () => setView("preview"));
  refs.goToSwipeBtn.addEventListener("click", () => setView("swipe"));
  refs.goToPreviewBtn.addEventListener("click", () => setView("preview"));

  refs.openFiltersBtn.addEventListener("click", () => toggleDrawer("filters"));
  refs.openStatsBtn.addEventListener("click", () => toggleDrawer("stats"));
  refs.openLayoutBtn.addEventListener("click", () => toggleDrawer("layout"));
  refs.openOrderBtn.addEventListener("click", () => toggleDrawer("order"));

  refs.closeDrawerButtons.forEach((btn) => {
    btn.addEventListener("click", () => closeDrawers());
  });

  refs.drawerBackdrop.addEventListener("click", () => closeDrawers());

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

  refs.cardHost.addEventListener("change", handleCardInputChange);
  refs.cardHost.addEventListener("click", handleCardClick);
  refs.cardHost.addEventListener("mouseover", handleCardMouseOver);
  document.addEventListener("click", (event) => {
    if (event.target.closest("#cardHost .info-chip")) {
      return;
    }
    closeOpenInfoPopovers();
  });
  const repositionOpenPopovers = () => {
    document.querySelectorAll(".info-chip.open").forEach((chip) => positionInfoPopover(chip));
  };
  window.addEventListener("resize", repositionOpenPopovers);
  window.addEventListener("scroll", repositionOpenPopovers, true);

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
      if (state.view === "preview" && isUndoShortcut) {
        event.preventDefault();
        undoLastPreviewChange();
      }
      return;
    }

    const activeTag = document.activeElement?.tagName;
    if (["INPUT", "TEXTAREA", "SELECT"].includes(activeTag)) {
      return;
    }

    const isSwipeUndoShortcut =
      (event.metaKey || event.ctrlKey) && !event.altKey && !event.shiftKey && event.key.toLowerCase() === "z";
    if (isSwipeUndoShortcut) {
      event.preventDefault();
      undoLastDecision();
      return;
    }

    if (event.key === "ArrowRight") {
      event.preventDefault();
      triggerDecision("accepted");
    } else if (event.key === "ArrowLeft") {
      event.preventDefault();
      triggerDecision("rejected");
    }
  });

  refs.autoGridToggle.addEventListener("change", (event) => {
    state.layout.autoGrid = Boolean(event.target.checked);
    applyLayoutVariables();
    renderPreview();
  });

  refs.gridColumnsRange.addEventListener("input", (event) => {
    state.layout.gridColumns = Number(event.target.value);
    applyLayoutVariables();
    renderPreview();
  });

  refs.gridRowsRange.addEventListener("input", (event) => {
    state.layout.gridRows = Number(event.target.value);
    applyLayoutVariables();
    renderPreview();
  });

  refs.fontFamilySelect.addEventListener("change", (event) => {
    state.layout.fontFamily = event.target.value;
    applyLayoutVariables();
    renderPreview();
  });

  refs.fontSizeRange.addEventListener("input", (event) => {
    state.layout.fontSize = Number(event.target.value);
    applyLayoutVariables();
    renderPreview();
  });

  refs.lineHeightRange.addEventListener("input", (event) => {
    state.layout.lineHeight = Number(event.target.value);
    applyLayoutVariables();
    renderPreview();
  });

  refs.letterSpacingRange.addEventListener("input", (event) => {
    state.layout.letterSpacing = Number(event.target.value);
    applyLayoutVariables();
    renderPreview();
  });

  refs.cardGapRange.addEventListener("input", (event) => {
    state.layout.cardGap = Number(event.target.value);
    applyLayoutVariables();
    renderPreview();
  });

  refs.cardPaddingRange.addEventListener("input", (event) => {
    state.layout.cardPadding = Number(event.target.value);
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

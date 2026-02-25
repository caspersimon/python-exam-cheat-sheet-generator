const EXAM_LABELS = {
  trial_midterm: "Trial 24/25",
  midterm_2023: "Trial 22/23",
  midterm_2024: "Trial 23/24",
  extra_practice: "Extra Practice",
};

const AI_GENERATION_NOTE = "AI-generated from practice exam questions, lecture snippets, notebook snippets, and trap-pattern context.";
const KEY_POINTS_GENERATION_NOTE = "AI-generated key points and optional details, then filtered against available course materials.";
const SPLASH_STORAGE_KEY = "python_midterm_splash_seen_v1";

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
  view: "swipe",
  openDrawer: "",
  previewDragId: null,
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

init();

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
  window.addEventListener("resize", () => {
    refs.cardHost.querySelectorAll(".info-chip.open").forEach((chip) => positionInfoPopover(chip));
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
      return;
    }

    const activeTag = document.activeElement?.tagName;
    if (["INPUT", "TEXTAREA", "SELECT"].includes(activeTag)) {
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

  refs.printBtn.addEventListener("click", () => {
    setView("preview");
    window.print();
  });

  refs.exportPngBtn.addEventListener("click", exportPng);
  refs.exportPdfBtn.addEventListener("click", exportPdf);

  refs.sheetStage.addEventListener("dragstart", (event) => {
    const card = event.target.closest(".preview-card");
    if (!card) {
      return;
    }
    state.previewDragId = card.dataset.cardId;
    event.dataTransfer.effectAllowed = "move";
  });

  refs.sheetStage.addEventListener("dragover", (event) => {
    const targetCard = event.target.closest(".preview-card");
    if (!targetCard || !state.previewDragId) {
      return;
    }
    event.preventDefault();
    refs.sheetStage.querySelectorAll(".preview-card.drag-over").forEach((el) => el.classList.remove("drag-over"));
    if (targetCard.dataset.cardId !== state.previewDragId) {
      targetCard.classList.add("drag-over");
    }
  });

  refs.sheetStage.addEventListener("dragleave", (event) => {
    const targetCard = event.target.closest(".preview-card");
    if (targetCard) {
      targetCard.classList.remove("drag-over");
    }
  });

  refs.sheetStage.addEventListener("drop", (event) => {
    event.preventDefault();
    const targetCard = event.target.closest(".preview-card");
    refs.sheetStage.querySelectorAll(".preview-card.drag-over").forEach((el) => el.classList.remove("drag-over"));

    if (!targetCard || !state.previewDragId) {
      state.previewDragId = null;
      return;
    }

    const draggedId = state.previewDragId;
    const targetId = targetCard.dataset.cardId;
    state.previewDragId = null;

    if (draggedId === targetId) {
      return;
    }

    const from = state.acceptedOrder.indexOf(draggedId);
    const to = state.acceptedOrder.indexOf(targetId);
    if (from === -1 || to === -1) {
      return;
    }

    const updated = [...state.acceptedOrder];
    updated.splice(from, 1);
    updated.splice(to, 0, draggedId);
    state.acceptedOrder = updated;
    renderPreview();
  });
}

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

function toggleDrawer(name) {
  if (state.openDrawer === name) {
    closeDrawers();
    return;
  }

  closeDrawers();
  const drawer = drawerMap[name];
  if (!drawer) {
    return;
  }

  drawer.classList.remove("hidden");
  refs.drawerBackdrop.classList.remove("hidden");
  state.openDrawer = name;
}

function closeDrawers() {
  Object.values(drawerMap).forEach((drawer) => {
    if (drawer) {
      drawer.classList.add("hidden");
    }
  });
  refs.drawerBackdrop.classList.add("hidden");
  state.openDrawer = "";
}

function setView(viewName) {
  state.view = viewName;
  refs.swipeView.classList.toggle("active", viewName === "swipe");
  refs.previewView.classList.toggle("active", viewName === "preview");
  closeDrawers();
  renderPreview();
}

function renderAll() {
  renderSwipe();
  renderPreview();
}

function getFilteredDeck() {
  const search = state.filters.search;

  return state.cards.filter((card) => {
    if (state.filters.onlyExam && card.exam_stats.total_hits === 0) {
      return false;
    }

    if (card.exam_stats.total_hits < state.filters.minHits) {
      return false;
    }

    const weeks = Array.isArray(card.weeks) ? card.weeks : [];
    if (state.filters.weeks.size > 0 && !weeks.some((week) => state.filters.weeks.has(week))) {
      return false;
    }

    if (!search) {
      return true;
    }

    const haystack = [
      card.topic,
      card.canonical_topic,
      ...(card.related_topics || []),
      ...(card.trap_patterns || []).map((trap) => trap.pattern),
    ]
      .join(" ")
      .toLowerCase();

    return haystack.includes(search);
  });
}

function getPendingCards(filteredDeck) {
  return filteredDeck.filter((card) => !state.decisions[card.id]);
}

function getCurrentCard(filteredDeck) {
  const pending = getPendingCards(filteredDeck);
  return pending.length > 0 ? pending[0] : null;
}

function usefulLectureSnippets(card) {
  const snippets = card.sections.lecture_snippets || [];
  return snippets
    .map((snippet) => {
      const filteredCode = (snippet.code_examples || []).filter((example) => !isLowValueSnippet(example.code || ""));
      return {
        ...snippet,
        code_examples: filteredCode,
      };
    })
    .filter((snippet) => {
      return Boolean(snippet.explanation || snippet.question || (snippet.code_examples || []).length);
    });
}

function usefulNotebookSnippets(card) {
  return (card.sections.notebook_snippets || []).filter((snippet) => !isLowValueSnippet(snippet.source || ""));
}

function usefulAIExamples(card) {
  return (card.sections.ai_examples || []).filter((item) => (item.code || "").trim().length > 0);
}

function normalizeKeyPointDetails(baseId, details) {
  return (details || [])
    .map((detail, idx) => {
      const id = String(detail?.id || `${baseId}-d${idx + 1}`).trim();
      const kindRaw = String(detail?.kind || "example").trim().toLowerCase();
      const kind = ["example", "table", "commands", "explanation"].includes(kindRaw) ? kindRaw : "example";
      const title = String(detail?.title || "Optional detail").trim();
      const text = String(detail?.text || "").trim();
      const code = normalizeNewlines(detail?.code || "").trim();
      const table = normalizeMiniTable(detail?.table);

      if (!id || (!text && !code && !table)) {
        return null;
      }

      return {
        id,
        kind,
        title,
        text,
        code,
        table,
      };
    })
    .filter(Boolean);
}

function normalizeMiniTable(rawTable) {
  if (!rawTable || typeof rawTable !== "object") {
    return null;
  }

  const headers = Array.isArray(rawTable.headers)
    ? rawTable.headers.map((value) => String(value || "").trim()).filter((value) => value.length > 0)
    : [];

  const rows = Array.isArray(rawTable.rows)
    ? rawTable.rows
        .map((row) => (Array.isArray(row) ? row.map((value) => String(value || "").trim()) : []))
        .filter((row) => row.length > 0 && row.some((cell) => cell.length > 0))
    : [];

  if (!headers.length || !rows.length) {
    return null;
  }

  return { headers, rows };
}

function keyPointGroups(card) {
  return (card.sections.key_points_to_remember || [])
    .filter((item) => item && (item.text || "").trim().length > 0)
    .map((item, idx) => {
      const id = String(item.id || `kp-${idx + 1}`).trim();
      const text = String(item.text || "").trim();
      return {
        id,
        text,
        details: normalizeKeyPointDetails(id, item.details || []),
      };
    });
}

function keyPointSelectableIds(card) {
  const ids = [];
  keyPointGroups(card).forEach((group) => {
    ids.push(group.id);
    group.details.forEach((detail) => ids.push(detail.id));
  });
  return ids;
}

function buildSourceItems(card) {
  const items = [];

  (card.sections.exam_questions || []).forEach((item) => {
    items.push({
      id: item.id,
      sourceType: "exam",
      priority: 0,
      header: `Exam • Q${item.number || "?"} • ${formatExamLabel(item.exam_label)}`,
      item,
    });
  });

  usefulLectureSnippets(card).forEach((item) => {
    items.push({
      id: item.id,
      sourceType: "lecture",
      priority: 1,
      header: `Lecture • ${item.topic || "snippet"} • W${item.week || "?"}`,
      item,
    });
  });

  usefulNotebookSnippets(card).forEach((item) => {
    items.push({
      id: item.id,
      sourceType: "notebook",
      priority: 2,
      header: `Notebook • W${item.week || "?"} cell ${item.cell_index || "?"} • ${item.topic || ""}`,
      item,
    });
  });

  items.sort((a, b) => a.priority - b.priority);
  return items;
}

function getSourceSplit(card) {
  const allItems = buildSourceItems(card);
  const byId = new Map(allItems.map((item) => [item.id, item]));
  const recommendedIdsRaw = card.sections.recommended_ids || [];
  const recommendedIds = recommendedIdsRaw.filter((id) => byId.has(id));

  const recommended = [];
  recommendedIds.forEach((id) => {
    if (!recommended.some((item) => item.id === id)) {
      recommended.push(byId.get(id));
    }
  });

  if (!recommended.length && allItems.length) {
    const fallback = allItems.filter((item) => item.sourceType === "exam").slice(0, 4);
    const extra = allItems
      .filter((item) => item.sourceType !== "exam")
      .slice(0, Math.max(0, 6 - fallback.length));
    recommended.push(...fallback, ...extra);
  }

  const recSet = new Set(recommended.map((item) => item.id));
  const additional = allItems.filter((item) => !recSet.has(item.id));

  return { recommended, additional };
}

function ensureDraft(card) {
  if (state.drafts[card.id]) {
    return state.drafts[card.id];
  }

  const split = getSourceSplit(card);
  const recommendedIds = split.recommended.map((item) => item.id);
  const additionalIds = split.additional.map((item) => item.id);
  const aiExampleIds = usefulAIExamples(card).map((item) => item.id);
  const keyPointIds = keyPointSelectableIds(card);

  const autoSelectRecommended = state.preferences.sourceAutoSelectMode === "recommended";

  state.drafts[card.id] = {
    ui: {
      settingsOpen: false,
    },
    sections: {
      aiSummary: Boolean(card.sections.ai_summary?.content),
      aiQuestions: (card.sections.ai_common_questions?.bullets || []).length > 0,
      keyPoints: keyPointIds.length > 0,
      aiExamples: aiExampleIds.length > 0,
      recommended: recommendedIds.length > 0,
      additional: additionalIds.length > 0,
    },
    selected: {
      aiExamples: [],
      keyPoints: [],
      recommended: autoSelectRecommended ? [...recommendedIds] : [],
      additional: [],
    },
  };

  return state.drafts[card.id];
}

function cloneDraft(draft) {
  return {
    ui: {
      settingsOpen: Boolean(draft.ui?.settingsOpen),
    },
    sections: { ...draft.sections },
    selected: {
      aiExamples: [...draft.selected.aiExamples],
      keyPoints: [...draft.selected.keyPoints],
      recommended: [...draft.selected.recommended],
      additional: [...draft.selected.additional],
    },
  };
}

function renderSwipe() {
  const filteredDeck = getFilteredDeck();
  const pendingCards = getPendingCards(filteredDeck);
  const currentCard = getCurrentCard(filteredDeck);

  const acceptedCount = Object.values(state.decisions).filter((entry) => entry.status === "accepted").length;
  const rejectedCount = Object.values(state.decisions).filter((entry) => entry.status === "rejected").length;

  refs.acceptedCount.textContent = String(acceptedCount);
  refs.rejectedCount.textContent = String(rejectedCount);
  refs.remainingCount.textContent = String(pendingCards.length);

  const decidedInFilter = filteredDeck.filter((card) => state.decisions[card.id]).length;
  refs.progressText.textContent = `${decidedInFilter}/${filteredDeck.length} decided in current filter • ${acceptedCount} accepted`;

  refs.acceptedTopicsList.innerHTML = "";
  state.acceptedOrder.slice(0, 40).forEach((cardId) => {
    const card = state.cards.find((entry) => entry.id === cardId);
    if (!card) {
      return;
    }
    const li = document.createElement("li");
    li.textContent = humanizeTopic(card.topic);
    refs.acceptedTopicsList.appendChild(li);
  });

  if (!currentCard) {
    refs.cardHost.innerHTML = `<div class="empty-state">
      <p><strong>No more cards in this filter.</strong></p>
      <p>Adjust filters or open preview/export.</p>
      <p>Accepted topics: ${acceptedCount}</p>
    </div>`;
    return;
  }

  const draft = ensureDraft(currentCard);
  refs.cardHost.innerHTML = renderTopicCard(currentCard, draft);
  attachCardSwipeHandlers();
}

function renderTopicCard(card, draft) {
  const weeksText = card.weeks.length ? card.weeks.map((week) => `W${week}`).join(" • ") : "Week unknown";
  const examSources = Object.entries(card.exam_stats.by_exam || {})
    .map(([exam, count]) => `${formatExamLabel(exam)} × ${count}`)
    .join(", ");
  const split = getSourceSplit(card);
  const keyPointGroupsForCard = keyPointGroups(card);
  const keyPointItemCount = keyPointGroupsForCard.reduce((count, group) => count + 1 + group.details.length, 0);
  const examSourceInfo = examSources || "No detailed exam-source mapping is available yet.";

  const totalHitsPill = card.exam_stats.total_hits > 0
    ? `<span class="pill hot exam-count-pill">
         <span>${card.exam_stats.total_hits} exam question${card.exam_stats.total_hits === 1 ? "" : "s"}</span>
         ${renderInfoChip("?", "Exam question sources", `Questions sourced from: ${examSourceInfo}`, "help")}
       </span>`
    : `<span class="pill">Not tested in exams</span>`;

  return `
    <article class="topic-card" data-card-id="${escapeHtml(card.id)}" id="activeTopicCard">
      <div class="card-head">
        <div>
          <h3>${escapeHtml(humanizeTopic(card.topic))}</h3>
          <div class="meta-pill-row">
            <span class="pill">${escapeHtml(weeksText)}</span>
            ${totalHitsPill}
          </div>
        </div>
        <div class="meta-column">
          <span>Swipe / arrow keys to decide</span>
          <button class="ghost-btn compact-btn icon-btn" type="button" data-role="toggle-card-settings" aria-expanded="${draft.ui?.settingsOpen ? "true" : "false"}" title="Card settings">
            <span aria-hidden="true">&#9881;</span>
            <span class="visually-hidden">Card settings</span>
          </button>
        </div>
      </div>

      <section class="card-settings-panel ${draft.ui?.settingsOpen ? "" : "hidden"}">
        <p class="muted settings-hint">Choose section visibility and defaults for new cards.</p>
        <label class="field settings-row">
          <span>Default source selection</span>
          <select data-role="default-selection-mode">
            <option value="none" ${state.preferences.sourceAutoSelectMode === "none" ? "selected" : ""}>Manual (select nothing)</option>
            <option value="recommended" ${state.preferences.sourceAutoSelectMode === "recommended" ? "selected" : ""}>Auto-select recommended</option>
          </select>
        </label>
        <div class="section-toggle-grid">
          ${renderSectionToggle("aiSummary", "Summary", 1, draft.sections.aiSummary, true)}
          ${renderSectionToggle("aiQuestions", "Common Questions", (card.sections.ai_common_questions?.bullets || []).length, draft.sections.aiQuestions, true)}
          ${renderSectionToggle("keyPoints", "Key Points for Reference", keyPointItemCount, draft.sections.keyPoints, true)}
          ${renderSectionToggle("aiExamples", "Code Examples", usefulAIExamples(card).length, draft.sections.aiExamples, true)}
          ${renderSectionToggle("recommended", "Recommended for Cheat Sheet", split.recommended.length, draft.sections.recommended)}
          ${renderSectionToggle("additional", "Additional Snippets", split.additional.length, draft.sections.additional)}
        </div>
      </section>

      ${renderAISummarySection(card, draft)}
      ${renderAIQuestionsSection(card, draft)}
      ${renderKeyPointsSection(card, draft)}
      ${renderAIExamplesSection(card, draft)}
      ${renderSourceSection(card, draft, "recommended", "Recommended for Cheat Sheet", split.recommended)}
      ${renderSourceSection(card, draft, "additional", "Additional Snippets", split.additional)}
    </article>
  `;
}

function renderSectionToggle(section, label, count, checked, isAI = false) {
  void isAI;
  return `
    <label>
      <input type="checkbox" data-role="section-toggle" data-section="${section}" ${checked ? "checked" : ""} />
      <span>${escapeHtml(label)} (${count})</span>
    </label>
  `;
}

function renderInfoChip(iconHtml, label, text, variant = "") {
  const variantClass = variant ? ` ${variant}` : "";
  return `
    <span class="info-chip${variantClass}">
      <button type="button" class="info-icon-btn" data-role="toggle-info" aria-label="${escapeHtml(label)}" title="${escapeHtml(label)}">
        <span aria-hidden="true">${iconHtml}</span>
      </button>
      <span class="info-popover" role="tooltip">${escapeHtml(text)}</span>
    </span>
  `;
}

function renderSparkleInfo(text, label = "AI-generated details") {
  return renderInfoChip("&#10024;", label, text, "sparkle");
}

function renderSectionHeader(title, countText = "", sparkleText = "", sparkleLabel = "AI-generated details") {
  const hasTitle = Boolean(title);
  const countHtml = countText ? `<span class="section-count">${escapeHtml(countText)}</span>` : "";
  return `
    <div class="section-header ${hasTitle ? "" : "section-header-meta-only"}">
      <div class="section-title-row">
        ${hasTitle ? `<strong>${escapeHtml(title)}</strong>` : ""}
        ${sparkleText ? renderSparkleInfo(sparkleText, sparkleLabel) : ""}
      </div>
      ${countHtml}
    </div>
  `;
}

function renderAISummarySection(card, draft) {
  const summary = card.sections.ai_summary?.content || "";
  const hiddenClass = draft.sections.aiSummary ? "" : "hidden";
  return `
    <section class="section-block ${hiddenClass}" data-section-block="aiSummary">
      <div class="summary-meta">
        ${renderSparkleInfo(AI_GENERATION_NOTE, "How this summary was generated")}
      </div>
      <div class="section-items">
        <p class="section-paragraph">${renderInlineCode(summary)}</p>
      </div>
    </section>
  `;
}

function renderAIQuestionsSection(card, draft) {
  const bullets = card.sections.ai_common_questions?.bullets || [];
  const hiddenClass = draft.sections.aiQuestions ? "" : "hidden";

  return `
    <section class="section-block ${hiddenClass}" data-section-block="aiQuestions">
      ${renderSectionHeader("Common Questions", String(bullets.length), AI_GENERATION_NOTE, "How these questions were generated")}
      <div class="section-items">
        <ul class="plain-bullets">
          ${bullets.map((bullet) => `<li>${renderInlineCode(bullet)}</li>`).join("")}
        </ul>
      </div>
    </section>
  `;
}

function renderKeyPointsSection(card, draft) {
  const groups = keyPointGroups(card);
  const hiddenClass = draft.sections.keyPoints ? "" : "hidden";
  const selectedSet = new Set(draft.selected.keyPoints || []);
  const selectableIds = new Set(keyPointSelectableIds(card));
  const selectedCount = [...selectedSet].filter((id) => selectableIds.has(id)).length;
  const totalCount = selectableIds.size;

  const pointHtml = groups.length
    ? groups
        .map((group) => {
          const checked = selectedSet.has(group.id);
          const detailsHtml = group.details.length
            ? `
              <div class="key-point-details">
                ${group.details
                  .map((detail) => {
                    const detailChecked = selectedSet.has(detail.id);
                    const kindLabel = detail.kind.charAt(0).toUpperCase() + detail.kind.slice(1);
                    return `
                      <div class="kp-detail-item">
                        <label class="item-select kp-detail-select">
                          <input
                            type="checkbox"
                            data-role="item-toggle"
                            data-section="keyPoints"
                            data-item-id="${escapeHtml(detail.id)}"
                            ${detailChecked ? "checked" : ""}
                          />
                          <span class="kp-detail-label">
                            <strong>${escapeHtml(detail.title)}</strong>
                            <span class="kp-detail-kind">${escapeHtml(kindLabel)}</span>
                          </span>
                        </label>
                        <div class="kp-detail-body">
                          ${detail.text ? `<p class="item-note">${renderInlineCode(detail.text)}</p>` : ""}
                          ${detail.table ? renderMiniTable(detail.table) : ""}
                          ${detail.code ? `<pre>${escapeHtml(detail.code)}</pre>` : ""}
                        </div>
                      </div>
                    `;
                  })
                  .join("")}
              </div>
            `
            : "";

          return `
            <div class="item-card key-point-group">
              <label class="item-select">
                <input
                  type="checkbox"
                  data-role="item-toggle"
                  data-section="keyPoints"
                  data-item-id="${escapeHtml(group.id)}"
                  ${checked ? "checked" : ""}
                />
                <strong>${renderInlineCode(group.text)}</strong>
              </label>
              ${detailsHtml}
            </div>
          `;
        })
        .join("")
    : `<p class="muted">No key points available.</p>`;

  return `
    <section class="section-block ${hiddenClass}" data-section-block="keyPoints">
      ${renderSectionHeader("Key Points for Reference", `${selectedCount}/${totalCount} selected`, KEY_POINTS_GENERATION_NOTE, "How these key points were generated")}
      <div class="section-items">${pointHtml}</div>
    </section>
  `;
}

function renderMiniTable(table) {
  const headHtml = table.headers.map((header) => `<th>${renderInlineCode(header)}</th>`).join("");
  const rowsHtml = table.rows
    .map((row) => `<tr>${row.map((cell) => `<td>${renderInlineCode(cell)}</td>`).join("")}</tr>`)
    .join("");
  return `
    <div class="kp-mini-table-wrap">
      <table class="kp-mini-table">
        <thead><tr>${headHtml}</tr></thead>
        <tbody>${rowsHtml}</tbody>
      </table>
    </div>
  `;
}

function renderAIExamplesSection(card, draft) {
  const items = usefulAIExamples(card);
  const hiddenClass = draft.sections.aiExamples ? "" : "hidden";

  const itemHtml = items.length
    ? items
        .map((item) => {
          const checked = draft.selected.aiExamples.includes(item.id);
          const kindLabel = item.kind === "incorrect" ? "Incorrect" : "Correct";
          return `
            <div class="item-card">
              <label class="item-select">
                <input
                  type="checkbox"
                  data-role="item-toggle"
                  data-section="aiExamples"
                  data-item-id="${escapeHtml(item.id)}"
                  ${checked ? "checked" : ""}
                />
                <strong>${escapeHtml(kindLabel)} • ${renderInlineCode(item.title || "Code example")}</strong>
              </label>
              <pre>${escapeHtml(item.code || "")}</pre>
              <p class="item-note">${renderInlineCode(item.why || "")}</p>
            </div>
          `;
        })
        .join("")
    : `<p class="muted">No code examples available.</p>`;

  return `
    <section class="section-block ${hiddenClass}" data-section-block="aiExamples">
      ${renderSectionHeader("Code Examples", `${draft.selected.aiExamples.length}/${items.length} selected`, AI_GENERATION_NOTE, "How these examples were generated")}
      <div class="section-items">${itemHtml}</div>
    </section>
  `;
}

function renderSourceSection(card, draft, sectionKey, title, items) {
  const hiddenClass = draft.sections[sectionKey] ? "" : "hidden";
  const selectedIds = draft.selected[sectionKey] || [];
  const selectedCount = items.filter((item) => selectedIds.includes(item.id)).length;

  const itemHtml = items.length
    ? items
        .map((sourceItem) => {
          const checked = selectedIds.includes(sourceItem.id);
          return `
            <div class="item-card">
              <label class="item-select">
                <input
                  type="checkbox"
                  data-role="item-toggle"
                  data-section="${sectionKey}"
                  data-item-id="${escapeHtml(sourceItem.id)}"
                  ${checked ? "checked" : ""}
                />
                <strong>${escapeHtml(sourceItem.header)}</strong>
              </label>
              <div class="item-body">
                ${renderSourceItemBody(sourceItem)}
              </div>
            </div>
          `;
        })
        .join("")
    : `<p class="muted">No snippets in this category.</p>`;

  return `
    <section class="section-block ${hiddenClass}" data-section-block="${sectionKey}">
      ${renderSectionHeader(title, `${selectedCount}/${items.length} selected`)}
      <div class="section-items">${itemHtml}</div>
    </section>
  `;
}

function renderSourceItemBody(sourceItem) {
  const item = sourceItem.item;
  if (sourceItem.sourceType === "exam") {
    return `
      ${renderQuestionContent(item.question, item.code_context)}
      ${renderOptions(item.options)}
      ${item.correct ? `<p class="answer-chip">Correct: ${escapeHtml(String(item.correct))}</p>` : ""}
      ${item.explanation ? `<p>${renderInlineCode(item.explanation)}</p>` : ""}
    `;
  }

  if (sourceItem.sourceType === "lecture") {
    const codeExamples = (item.code_examples || [])
      .map(
        (example) => `
          <p><strong>${renderInlineCode(example.description || "Code")}</strong></p>
          <pre>${escapeHtml(example.code || "")}</pre>
        `
      )
      .join("");

    const lectureQ = item.question
      ? `
        ${renderQuestionContent(item.question, "", "Lecture question")}
        ${renderOptions(item.options)}
        ${item.correct ? `<p class="answer-chip">Correct: ${escapeHtml(String(item.correct))}</p>` : ""}
      `
      : "";

    return `
      ${item.explanation ? `<p>${renderInlineCode(item.explanation)}</p>` : ""}
      ${lectureQ}
      ${codeExamples}
    `;
  }

  const outText = (item.outputs || []).join("\\n");
  return `
    <pre>${escapeHtml(item.source || "")}</pre>
    ${outText ? `<p><strong>Output:</strong></p><pre>${escapeHtml(outText)}</pre>` : ""}
  `;
}

function renderOptions(options = {}) {
  const entries = Object.entries(options);
  if (!entries.length) {
    return "";
  }

  const sorted = entries.sort(([a], [b]) => a.localeCompare(b));
  return `
    <ul class="option-list">
      ${sorted
        .map(
          ([key, value]) => `
            <li class="option-item">
              <strong>${escapeHtml(String(key).toUpperCase())}:</strong>
              ${renderOptionValue(value)}
            </li>
          `
        )
        .join("")}
    </ul>
  `;
}

function renderOptionValue(value) {
  const text = normalizeNewlines(String(value ?? "")).trim();
  if (!text) {
    return '<span class="option-text">-</span>';
  }

  if (text.includes("\n") || isCodeBlockLikely(text)) {
    return `<pre class="option-code">${escapeHtml(text)}</pre>`;
  }

  return `<span class="option-text">${renderInlineCode(text)}</span>`;
}

function renderQuestionContent(question, codeContext = "", label = "") {
  const parsed = splitPromptAndCode(question);
  const parts = [];

  if (parsed.prompt) {
    const labelPrefix = label ? `<strong>${escapeHtml(label)}:</strong> ` : "";
    parts.push(`<p class="question-text">${labelPrefix}${renderInlineCode(parsed.prompt)}</p>`);
  }

  const codeBlocks = [];
  if (parsed.code) {
    codeBlocks.push(parsed.code);
  }

  const contextText = normalizeNewlines(codeContext || "").trim();
  if (contextText && !codeBlocks.some((existing) => existing.trim() === contextText)) {
    codeBlocks.push(contextText);
  }

  codeBlocks.forEach((block) => {
    parts.push(`<pre class="question-code">${escapeHtml(block)}</pre>`);
  });

  if (!parts.length) {
    const fallback = normalizeNewlines(question || "").trim();
    if (fallback) {
      parts.push(`<p class="question-text">${renderInlineCode(fallback)}</p>`);
    }
  }

  return parts.join("");
}

function splitPromptAndCode(rawQuestion) {
  const text = normalizeNewlines(rawQuestion || "").trim();
  if (!text) {
    return { prompt: "", code: "" };
  }

  const chunks = text.split(/\n{2,}/);
  if (chunks.length >= 2) {
    const prompt = chunks[0].trim();
    const tail = chunks.slice(1).join("\n\n").trim();
    if (isCodeBlockLikely(tail)) {
      return { prompt, code: tail };
    }
  }

  const lines = text.split("\n");
  if (lines.length > 1) {
    const codeStart = lines.findIndex((line) => isCodeLineLikely(line));
    if (codeStart > 0) {
      const prompt = lines.slice(0, codeStart).join("\n").trim();
      const code = lines.slice(codeStart).join("\n").trim();
      if (isCodeBlockLikely(code)) {
        return { prompt, code };
      }
    }
  }

  return { prompt: text, code: "" };
}

function isCodeBlockLikely(block) {
  const lines = normalizeNewlines(block || "")
    .split("\n")
    .map((line) => line.trimEnd())
    .filter((line) => line.trim().length > 0);

  if (!lines.length) {
    return false;
  }

  const codeLineCount = lines.filter((line) => isCodeLineLikely(line)).length;
  return codeLineCount >= Math.max(2, Math.ceil(lines.length * 0.45));
}

function isCodeLineLikely(line) {
  const raw = String(line || "");
  const trimmed = raw.trim();
  if (!trimmed) {
    return false;
  }

  if (/^\s{2,}\S/.test(raw)) {
    return true;
  }

  if (/^(for|while|if|elif|else|def|class|return|print|from|import|with|try|except|finally)\b/.test(trimmed)) {
    return true;
  }

  if (/^[A-Za-z_][A-Za-z0-9_]*\s*=\s*/.test(trimmed)) {
    return true;
  }

  if (trimmed.startsWith("#")) {
    return true;
  }

  const syntaxSignals = ["==", "!=", "<=", ">=", "%", "append(", "range(", "len(", "(", ")", "[", "]", "{", "}"];
  if (syntaxSignals.some((signal) => trimmed.includes(signal))) {
    return true;
  }

  return false;
}

function normalizeNewlines(text) {
  return String(text || "").replace(/\r\n/g, "\n").replace(/\r/g, "\n");
}

function renderInlineCode(text) {
  const value = normalizeNewlines(closeUnbalancedBackticks(text || ""));
  if (!value) {
    return "";
  }

  const chunks = value.split("`");
  return chunks
    .map((chunk, idx) => {
      if (idx % 2 === 1) {
        return `<code class="inline-code">${escapeHtml(chunk)}</code>`;
      }
      return escapeHtml(chunk).replace(/\n/g, "<br />");
    })
    .join("");
}

function closeUnbalancedBackticks(text) {
  const value = String(text || "");
  const ticks = (value.match(/`/g) || []).length;
  if (ticks % 2 === 1) {
    return `${value}\``;
  }
  return value;
}

function attachCardSwipeHandlers() {
  const card = document.getElementById("activeTopicCard");
  if (!card) {
    return;
  }

  const dragState = {
    dragging: false,
    pointerId: null,
    startX: 0,
    dx: 0,
  };

  card.addEventListener("pointerdown", (event) => {
    if (event.button !== 0) {
      return;
    }
    if (isInteractiveNode(event.target)) {
      return;
    }

    dragState.dragging = true;
    dragState.pointerId = event.pointerId;
    dragState.startX = event.clientX;
    dragState.dx = 0;
    card.setPointerCapture(event.pointerId);
    card.classList.add("dragging");
  });

  card.addEventListener("pointermove", (event) => {
    if (!dragState.dragging || event.pointerId !== dragState.pointerId) {
      return;
    }

    dragState.dx = event.clientX - dragState.startX;
    const rotation = dragState.dx / 24;
    card.style.transform = `translateX(${dragState.dx}px) rotate(${rotation}deg)`;
    card.style.opacity = String(Math.max(0.42, 1 - Math.abs(dragState.dx) / 280));
  });

  const onPointerEnd = (event) => {
    if (!dragState.dragging || event.pointerId !== dragState.pointerId) {
      return;
    }

    dragState.dragging = false;
    card.classList.remove("dragging");
    card.releasePointerCapture(event.pointerId);

    const threshold = 130;
    const dx = dragState.dx;
    card.style.transform = "";
    card.style.opacity = "";

    if (dx > threshold) {
      triggerDecision("accepted");
    } else if (dx < -threshold) {
      triggerDecision("rejected");
    }
  };

  card.addEventListener("pointerup", onPointerEnd);
  card.addEventListener("pointercancel", onPointerEnd);
}

function isInteractiveNode(node) {
  return Boolean(node.closest("input,button,label,select,textarea,a,pre,code"));
}

function handleCardInputChange(event) {
  const currentCard = getCurrentCard(getFilteredDeck());
  if (!currentCard) {
    return;
  }

  const draft = ensureDraft(currentCard);
  const input = event.target;
  const role = input.dataset.role;
  const section = input.dataset.section;

  if (role === "default-selection-mode") {
    const mode = input.value === "recommended" ? "recommended" : "none";
    state.preferences.sourceAutoSelectMode = mode;
    if (mode === "recommended") {
      const split = getSourceSplit(currentCard);
      if (!draft.selected.recommended.length) {
        draft.selected.recommended = split.recommended.map((item) => item.id);
      }
    }
    rerenderCurrentCard();
    return;
  }

  if (role === "section-toggle") {
    const checked = Boolean(input.checked);
    draft.sections[section] = checked;

    rerenderCurrentCard();
    return;
  }

  if (role === "item-toggle") {
    const itemId = input.dataset.itemId;
    const key = sectionToSelectionKey(section);
    if (!key) {
      return;
    }

    const existing = draft.selected[key];
    const next = new Set(existing);
    if (input.checked) {
      next.add(itemId);
    } else {
      next.delete(itemId);
    }
    draft.selected[key] = [...next];
    rerenderCurrentCard();
    return;
  }
}

function handleCardClick(event) {
  const infoTrigger = event.target.closest("[data-role='toggle-info']");
  if (infoTrigger) {
    event.preventDefault();
    const infoChip = infoTrigger.closest(".info-chip");
    if (!infoChip) {
      return;
    }
    const shouldOpen = !infoChip.classList.contains("open");
    closeOpenInfoPopovers();
    if (shouldOpen) {
      infoChip.classList.add("open");
      positionInfoPopover(infoChip);
    }
    return;
  }

  if (!event.target.closest(".info-chip")) {
    closeOpenInfoPopovers();
  }

  const trigger = event.target.closest("[data-role='toggle-card-settings']");
  if (!trigger) {
    return;
  }

  const currentCard = getCurrentCard(getFilteredDeck());
  if (!currentCard) {
    return;
  }

  const draft = ensureDraft(currentCard);
  draft.ui.settingsOpen = !Boolean(draft.ui?.settingsOpen);
  rerenderCurrentCard();
}

function handleCardMouseOver(event) {
  const infoChip = event.target.closest(".info-chip");
  if (!infoChip || !refs.cardHost.contains(infoChip)) {
    return;
  }
  positionInfoPopover(infoChip);
}

function positionInfoPopover(infoChip) {
  const popover = infoChip.querySelector(".info-popover");
  if (!popover) {
    return;
  }

  popover.style.setProperty("--popover-shift-x", "0px");
  const rect = popover.getBoundingClientRect();
  const viewportPadding = 8;
  const maxRight = window.innerWidth - viewportPadding;
  let shiftX = 0;

  if (rect.left < viewportPadding) {
    shiftX += viewportPadding - rect.left;
  }
  if (rect.right > maxRight) {
    shiftX -= rect.right - maxRight;
  }

  popover.style.setProperty("--popover-shift-x", `${Math.round(shiftX)}px`);
}

function closeOpenInfoPopovers() {
  refs.cardHost.querySelectorAll(".info-chip.open").forEach((chip) => chip.classList.remove("open"));
}

function rerenderCurrentCard() {
  const currentCard = getCurrentCard(getFilteredDeck());
  if (!currentCard) {
    return;
  }
  const draft = ensureDraft(currentCard);
  refs.cardHost.innerHTML = renderTopicCard(currentCard, draft);
  attachCardSwipeHandlers();
}

function ensureSectionHasSelection(card, draft, section) {
  // No-op: selections are manual by default unless user enables auto-select recommended.
  void card;
  void draft;
  void section;
}

function sectionToSelectionKey(section) {
  const map = {
    aiExamples: "aiExamples",
    keyPoints: "keyPoints",
    recommended: "recommended",
    additional: "additional",
  };
  return map[section] || "";
}

function triggerDecision(status) {
  const currentCard = getCurrentCard(getFilteredDeck());
  if (!currentCard) {
    return;
  }

  const cardElement = document.getElementById("activeTopicCard");
  if (!cardElement) {
    commitDecision(status, currentCard);
    return;
  }

  const className = status === "accepted" ? "swipe-right" : "swipe-left";
  cardElement.classList.add(className);

  window.setTimeout(() => {
    commitDecision(status, currentCard);
  }, 150);
}

function commitDecision(status, card) {
  const previousDecision = state.decisions[card.id] ? deepClone(state.decisions[card.id]) : null;
  const previousOrder = [...state.acceptedOrder];
  state.history.push({
    cardId: card.id,
    previousDecision,
    previousOrder,
  });

  if (status === "accepted") {
    const draft = ensureDraft(card);
    state.decisions[card.id] = {
      status: "accepted",
      selection: cloneDraft(draft),
    };

    if (!state.acceptedOrder.includes(card.id)) {
      state.acceptedOrder.push(card.id);
    }
  } else {
    state.decisions[card.id] = { status: "rejected" };
    state.acceptedOrder = state.acceptedOrder.filter((id) => id !== card.id);
  }

  renderAll();

  const noPending = getPendingCards(getFilteredDeck()).length === 0;
  if (noPending && state.acceptedOrder.length > 0) {
    setView("preview");
  }
}

function undoLastDecision() {
  const entry = state.history.pop();
  if (!entry) {
    return;
  }

  if (entry.previousDecision) {
    state.decisions[entry.cardId] = entry.previousDecision;
  } else {
    delete state.decisions[entry.cardId];
  }

  state.acceptedOrder = entry.previousOrder;
  renderAll();
}

function getEffectiveGridSettings(totalCards) {
  if (!state.layout.autoGrid) {
    return {
      columns: state.layout.gridColumns,
      rows: state.layout.gridRows,
    };
  }

  let columns = 1;
  if (totalCards > 24) {
    columns = 4;
  } else if (totalCards > 12) {
    columns = 3;
  } else if (totalCards > 5) {
    columns = 2;
  }

  if (state.layout.fontSize >= 11.5) {
    columns = Math.max(1, columns - 1);
  }
  if (state.layout.fontSize <= 8.5) {
    columns = Math.min(4, columns + 1);
  }

  let rows = Math.ceil(Math.max(1, totalCards) / (2 * columns));
  rows = clamp(rows, 3, 14);

  if (state.layout.lineHeight <= 1.0 && rows < 14) {
    rows += 1;
  }
  if (state.layout.lineHeight >= 1.35 && rows > 3) {
    rows -= 1;
  }

  return {
    columns,
    rows,
  };
}

function renderPreview() {
  refs.page1Content.innerHTML = "";
  refs.page2Content.innerHTML = "";

  refs.previewOrderList.innerHTML = "";
  state.acceptedOrder.forEach((cardId) => {
    const card = state.cards.find((entry) => entry.id === cardId);
    if (!card) {
      return;
    }
    const li = document.createElement("li");
    li.textContent = humanizeTopic(card.topic);
    refs.previewOrderList.appendChild(li);
  });

  const acceptedCards = state.acceptedOrder
    .map((id) => state.cards.find((card) => card.id === id))
    .filter((card) => card && state.decisions[card.id]?.status === "accepted");

  const grid = getEffectiveGridSettings(acceptedCards.length);

  refs.page1Content.style.setProperty("--grid-cols", String(grid.columns));
  refs.page1Content.style.setProperty("--grid-rows", String(grid.rows));
  refs.page2Content.style.setProperty("--grid-cols", String(grid.columns));
  refs.page2Content.style.setProperty("--grid-rows", String(grid.rows));

  const capacityPerPage = grid.columns * grid.rows;
  const totalCapacity = capacityPerPage * 2;

  if (!acceptedCards.length) {
    refs.page1Content.innerHTML = `<div class="empty-state" style="grid-column:1/-1;grid-row:1/-1;"><p>No accepted topics yet.</p><p>Go to Swipe Mode and add cards first.</p></div>`;
    refs.page2Content.innerHTML = `<div class="empty-state" style="grid-column:1/-1;grid-row:1/-1;"><p>Page 2 is empty.</p></div>`;
    refs.overflowNotice.classList.add("hidden");
    syncGridControls(grid);
    return;
  }

  const page1Cards = acceptedCards.slice(0, capacityPerPage);
  const page2Cards = acceptedCards.slice(capacityPerPage, capacityPerPage * 2);
  const overflowCards = acceptedCards.slice(totalCapacity);

  page1Cards.forEach((card) => {
    const selection = state.decisions[card.id]?.selection;
    if (!selection) {
      return;
    }
    refs.page1Content.appendChild(buildPreviewCard(card, selection));
  });

  page2Cards.forEach((card) => {
    const selection = state.decisions[card.id]?.selection;
    if (!selection) {
      return;
    }
    refs.page2Content.appendChild(buildPreviewCard(card, selection));
  });

  if (!page1Cards.length) {
    refs.page1Content.innerHTML = `<div class="empty-state" style="grid-column:1/-1;grid-row:1/-1;"><p>Page 1 is empty.</p></div>`;
  }

  if (!page2Cards.length) {
    refs.page2Content.innerHTML = `<div class="empty-state" style="grid-column:1/-1;grid-row:1/-1;"><p>Page 2 is empty.</p></div>`;
  }

  if (overflowCards.length) {
    refs.overflowNotice.classList.remove("hidden");
    refs.overflowNotice.textContent = `${overflowCards.length} topic(s) do not fit in 2 A4 pages at current rows/columns. Reduce selected cards or increase grid density.`;
  } else {
    refs.overflowNotice.classList.add("hidden");
  }

  syncGridControls(grid);
}

function syncGridControls(effectiveGrid) {
  refs.autoGridToggle.checked = state.layout.autoGrid;

  refs.gridColumnsRange.disabled = state.layout.autoGrid;
  refs.gridRowsRange.disabled = state.layout.autoGrid;

  refs.gridColumnsRange.value = String(state.layout.gridColumns);
  refs.gridRowsRange.value = String(state.layout.gridRows);

  refs.gridColumnsValue.textContent = state.layout.autoGrid
    ? `${effectiveGrid.columns} (auto)`
    : String(state.layout.gridColumns);
  refs.gridRowsValue.textContent = state.layout.autoGrid
    ? `${effectiveGrid.rows} (auto)`
    : String(state.layout.gridRows);
}

function buildPreviewCard(card, selection) {
  const sectionHtml = [];

  if (selection.sections.aiSummary && card.sections.ai_summary?.content) {
    sectionHtml.push(`<div class="section-title">Summary</div>`);
    sectionHtml.push(`<p>${renderInlineCode(trimWords(card.sections.ai_summary.content, 55))}</p>`);
  }

  if (selection.sections.aiQuestions) {
    const bullets = (card.sections.ai_common_questions?.bullets || []).slice(0, 4);
    if (bullets.length) {
      sectionHtml.push(`<div class="section-title">Common Questions</div>`);
      sectionHtml.push(`<ul>${bullets.map((item) => `<li>${renderInlineCode(trimWords(item, 16))}</li>`).join("")}</ul>`);
    }
  }

  if (selection.sections.keyPoints) {
    const groups = getSelectedKeyPointGroups(card, selection).slice(0, 3);
    if (groups.length) {
      sectionHtml.push(`<div class="section-title">Key Points for Reference</div>`);
      sectionHtml.push(renderPreviewKeyPoints(groups));
    }
  }

  if (selection.sections.aiExamples) {
    const aiExamples = usefulAIExamples(card).filter((item) => selection.selected.aiExamples.includes(item.id));
    if (aiExamples.length) {
      sectionHtml.push(`<div class="section-title">Code Examples</div>`);
      aiExamples.slice(0, 2).forEach((item) => {
        sectionHtml.push(`<p><strong>${escapeHtml(item.kind === "incorrect" ? "Incorrect" : "Correct")}</strong> ${renderInlineCode(trimWords(item.title || "Example", 12))}</p>`);
        sectionHtml.push(`<pre>${escapeHtml(trimLines(item.code || "", 5))}</pre>`);
      });
    }
  }

  if (selection.sections.recommended) {
    const recommended = getSelectedSourceItemsForPreview(card, selection, "recommended").slice(0, 2);
    if (recommended.length) {
      sectionHtml.push(`<div class="section-title">Recommended</div>`);
      recommended.forEach((sourceItem) => {
        sectionHtml.push(renderPreviewSourceItem(sourceItem));
      });
    }
  }

  if (selection.sections.additional) {
    const additional = getSelectedSourceItemsForPreview(card, selection, "additional").slice(0, 1);
    if (additional.length) {
      sectionHtml.push(`<div class="section-title">Additional</div>`);
      additional.forEach((sourceItem) => {
        sectionHtml.push(renderPreviewSourceItem(sourceItem));
      });
    }
  }

  const cardElement = document.createElement("article");
  cardElement.className = "preview-card";
  cardElement.draggable = true;
  cardElement.dataset.cardId = card.id;

  const weeksText = card.weeks.length ? card.weeks.map((week) => `W${week}`).join(", ") : "W?";
  cardElement.innerHTML = `
    <h4>${escapeHtml(humanizeTopic(card.topic))}</h4>
    <div class="tiny-meta">${escapeHtml(weeksText)} • ${card.exam_stats.total_hits} exam question${card.exam_stats.total_hits === 1 ? "" : "s"}</div>
    <div class="preview-body">${sectionHtml.join("")}</div>
  `;

  return cardElement;
}

function getSelectedSourceItemsForPreview(card, selection, sectionKey) {
  const split = getSourceSplit(card);
  const selectedIds = new Set(selection.selected[sectionKey] || []);
  const bucket = sectionKey === "recommended" ? split.recommended : split.additional;
  return bucket.filter((item) => selectedIds.has(item.id));
}

function getSelectedKeyPointGroups(card, selection) {
  const selectedIds = new Set(selection.selected.keyPoints || []);
  return keyPointGroups(card)
    .map((group) => {
      const selectedDetails = group.details.filter((detail) => selectedIds.has(detail.id));
      const pointSelected = selectedIds.has(group.id);
      if (!pointSelected && !selectedDetails.length) {
        return null;
      }
      return {
        ...group,
        pointSelected,
        selectedDetails,
      };
    })
    .filter(Boolean);
}

function renderPreviewKeyPoints(groups) {
  const blocks = groups
    .map((group) => {
      const title = group.pointSelected
        ? `<p class="preview-kp-main">${renderInlineCode(trimWords(group.text, 16))}</p>`
        : `<p class="preview-kp-main"><span class="preview-kp-ref">Ref:</span> ${renderInlineCode(trimWords(group.text, 12))}</p>`;

      const detailHtml = group.selectedDetails.length
        ? `<div class="preview-kp-details">${group.selectedDetails.slice(0, 2).map((detail) => renderPreviewKeyPointDetail(detail)).join("")}</div>`
        : "";

      return `<div class="preview-kp-group">${title}${detailHtml}</div>`;
    })
    .join("");
  return `<div class="preview-kp-list">${blocks}</div>`;
}

function renderPreviewKeyPointDetail(detail) {
  if (detail.table) {
    const headers = detail.table.headers.join(" / ");
    const firstRow = (detail.table.rows[0] || []).join(" / ");
    return `<p class="preview-kp-detail"><strong>${escapeHtml(trimWords(detail.title || "Table", 6))}:</strong> ${renderInlineCode(trimWords(`${headers}: ${firstRow}`, 14))}</p>`;
  }
  if (detail.code) {
    return `<pre>${escapeHtml(trimLines(detail.code, 3))}</pre>`;
  }
  const text = detail.text || detail.title || "Optional detail";
  return `<p class="preview-kp-detail">${renderInlineCode(trimWords(text, 14))}</p>`;
}

function renderPreviewSourceItem(sourceItem) {
  const item = sourceItem.item;

  if (sourceItem.sourceType === "exam") {
    let html = `<p><strong>${renderInlineCode(trimWords(sourceItem.header, 10))}:</strong> ${renderInlineCode(trimWords(item.question || "", 24))}</p>`;
    if (item.correct) {
      html += `<p>Correct: <strong>${escapeHtml(String(item.correct))}</strong></p>`;
    }
    return html;
  }

  if (sourceItem.sourceType === "lecture") {
    let html = "";
    if (item.explanation) {
      html += `<p>${renderInlineCode(trimWords(item.explanation, 22))}</p>`;
    }
    const firstCode = (item.code_examples || [])[0];
    if (firstCode?.code) {
      html += `<pre>${escapeHtml(trimLines(firstCode.code, 5))}</pre>`;
    }
    return html || `<p>${renderInlineCode(trimWords(sourceItem.header, 16))}</p>`;
  }

  return `<pre>${escapeHtml(trimLines(item.source || "", 5))}</pre>`;
}

function applyLayoutVariables() {
  refs.sheetStage.style.setProperty("--sheet-font", state.layout.fontFamily);
  refs.sheetStage.style.setProperty("--sheet-font-size", `${state.layout.fontSize}px`);
  refs.sheetStage.style.setProperty("--sheet-line-height", String(state.layout.lineHeight));
  refs.sheetStage.style.setProperty("--sheet-letter-spacing", `${state.layout.letterSpacing}px`);
  refs.sheetStage.style.setProperty("--sheet-card-gap", `${state.layout.cardGap}px`);
  refs.sheetStage.style.setProperty("--sheet-card-padding", `${state.layout.cardPadding}px`);

  refs.fontFamilySelect.value = state.layout.fontFamily;
  refs.fontSizeRange.value = String(state.layout.fontSize);
  refs.lineHeightRange.value = String(state.layout.lineHeight);
  refs.letterSpacingRange.value = String(state.layout.letterSpacing);
  refs.cardGapRange.value = String(state.layout.cardGap);
  refs.cardPaddingRange.value = String(state.layout.cardPadding);

  refs.fontSizeValue.textContent = String(state.layout.fontSize);
  refs.lineHeightValue.textContent = String(state.layout.lineHeight);
  refs.letterSpacingValue.textContent = String(state.layout.letterSpacing);
  refs.cardGapValue.textContent = String(state.layout.cardGap);
  refs.cardPaddingValue.textContent = String(state.layout.cardPadding);
}

async function exportPng() {
  setView("preview");

  if (typeof window.html2canvas !== "function") {
    alert("PNG export library not loaded. Use Print as fallback.");
    return;
  }

  const pages = getNonEmptyPageElements();
  if (!pages.length) {
    alert("No content to export.");
    return;
  }

  const originalText = refs.exportPngBtn.textContent;
  refs.exportPngBtn.textContent = "Exporting...";
  refs.exportPngBtn.disabled = true;

  try {
    for (let idx = 0; idx < pages.length; idx += 1) {
      const page = pages[idx];
      const canvas = await window.html2canvas(page, {
        scale: 2,
        useCORS: true,
        backgroundColor: "#ffffff",
      });

      const url = canvas.toDataURL("image/png");
      const link = document.createElement("a");
      link.href = url;
      link.download = `python-cheatsheet-page-${idx + 1}.png`;
      link.click();
    }
  } finally {
    refs.exportPngBtn.textContent = originalText;
    refs.exportPngBtn.disabled = false;
  }
}

async function exportPdf() {
  setView("preview");

  if (typeof window.html2canvas !== "function" || !window.jspdf || !window.jspdf.jsPDF) {
    alert("PDF export libraries not loaded. Use Print as fallback.");
    return;
  }

  const pages = getNonEmptyPageElements();
  if (!pages.length) {
    alert("No content to export.");
    return;
  }

  const originalText = refs.exportPdfBtn.textContent;
  refs.exportPdfBtn.textContent = "Exporting...";
  refs.exportPdfBtn.disabled = true;

  try {
    const { jsPDF } = window.jspdf;
    const pdf = new jsPDF({ orientation: "portrait", unit: "mm", format: "a4" });

    for (let idx = 0; idx < pages.length; idx += 1) {
      const page = pages[idx];
      const canvas = await window.html2canvas(page, {
        scale: 2,
        useCORS: true,
        backgroundColor: "#ffffff",
      });
      const imageData = canvas.toDataURL("image/png");

      if (idx > 0) {
        pdf.addPage("a4", "portrait");
      }

      pdf.addImage(imageData, "PNG", 0, 0, 210, 297, undefined, "FAST");
    }

    pdf.save("python-midterm-cheatsheet.pdf");
  } finally {
    refs.exportPdfBtn.textContent = originalText;
    refs.exportPdfBtn.disabled = false;
  }
}

function getNonEmptyPageElements() {
  const pages = [];
  const page1Has = refs.page1Content.querySelector(".preview-card");
  const page2Has = refs.page2Content.querySelector(".preview-card");

  if (page1Has) {
    pages.push(refs.page1Content.parentElement);
  }
  if (page2Has) {
    pages.push(refs.page2Content.parentElement);
  }
  return pages;
}

function formatExamLabel(label) {
  return EXAM_LABELS[label] || label || "Unknown exam";
}

function trimWords(text, maxWords) {
  if (!text) {
    return "";
  }
  const words = text.trim().split(/\s+/);
  if (words.length <= maxWords) {
    return text.trim();
  }
  return `${words.slice(0, maxWords).join(" ")}…`;
}

function trimLines(text, maxLines) {
  if (!text) {
    return "";
  }
  const lines = text.split("\n");
  if (lines.length <= maxLines) {
    return text;
  }
  return `${lines.slice(0, maxLines).join("\n")}\n# ...`;
}

function humanizeTopic(topic) {
  const raw = String(topic || "").trim();
  if (!raw) {
    return "";
  }

  const cleaned = raw.replace(/_/g, " ").replace(/\s+/g, " ").trim();
  if (cleaned !== cleaned.toLowerCase()) {
    return cleaned;
  }

  const smallWords = new Set(["and", "or", "of", "vs", "in", "to", "for", "on", "with"]);
  return cleaned
    .split(" ")
    .map((word, index) => {
      if (index > 0 && smallWords.has(word)) {
        return word;
      }
      return word.charAt(0).toUpperCase() + word.slice(1);
    })
    .join(" ");
}

function looksCodeLike(text) {
  const value = (text || "").trim();
  if (!value) {
    return false;
  }

  if (value.includes("\n")) {
    return true;
  }

  const codeSignals = ["=", "(", ")", "[", "]", "{", "}", ":", "+", "-", "*", "/", "%", "."];
  const codeKeywords = ["print", "for ", "if ", "while ", "def ", "return", "import ", "from ", "lambda", "range", "len", "sorted"];
  const lower = value.toLowerCase();

  return codeSignals.some((signal) => value.includes(signal)) || codeKeywords.some((kw) => lower.startsWith(kw) || lower.includes(` ${kw}`));
}

function isLowValueSnippet(text) {
  const value = (text || "").trim();
  if (!value) {
    return true;
  }

  if (value.includes("\n")) {
    return false;
  }

  const lower = value.toLowerCase();
  if (lower.startsWith("#") || lower.startsWith("##") || lower.startsWith("###")) {
    return true;
  }

  const lowPhrases = [
    "below you will find",
    "the following",
    "function definitions start",
    "you call functions",
    "dictionaries are",
    "global and local names",
  ];

  if (lowPhrases.some((phrase) => lower.includes(phrase)) && !looksCodeLike(value)) {
    return true;
  }

  if (!looksCodeLike(value) && value.split(/\s+/).length <= 8) {
    return true;
  }

  return false;
}

function clamp(value, min, max) {
  return Math.min(max, Math.max(min, value));
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function deepClone(value) {
  return JSON.parse(JSON.stringify(value));
}

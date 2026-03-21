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

function usefulHomeworkSnippets(card) {
  return (card.sections.homework_snippets || []).filter((snippet) => !isLowValueSnippet(snippet.source || ""));
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

function buildHomeworkItems(card) {
  return usefulHomeworkSnippets(card).map((item) => ({
    id: item.id,
    sourceType: "homework",
    header: `Homework • W${item.week || "?"} cell ${item.cell_index || "?"} • ${item.topic || ""}`,
    item,
  }));
}

function getHomeworkSplit(card) {
  const allItems = buildHomeworkItems(card);
  const byId = new Map(allItems.map((item) => [item.id, item]));
  const recommendedIdsRaw = card.sections.homework_recommended_ids || [];
  const recommendedIds = recommendedIdsRaw.filter((id) => byId.has(id));

  const recommended = [];
  recommendedIds.forEach((id) => {
    if (!recommended.some((item) => item.id === id)) {
      recommended.push(byId.get(id));
    }
  });

  if (!recommended.length && allItems.length) {
    const fallbackCount = Math.min(4, Math.max(1, Math.ceil(allItems.length / 2)));
    recommended.push(...allItems.slice(0, fallbackCount));
  }

  const recSet = new Set(recommended.map((item) => item.id));
  const additional = allItems.filter((item) => !recSet.has(item.id));
  return { recommended, additional };
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
  const existing = state.drafts[card.id];
  if (existing) {
    normalizeDraftForCard(existing, card);
    return existing;
  }

  const split = getSourceSplit(card);
  const homeworkSplit = getHomeworkSplit(card);
  const recommendedIds = split.recommended.map((item) => item.id);
  const additionalIds = split.additional.map((item) => item.id);
  const homeworkRecommendedIds = homeworkSplit.recommended.map((item) => item.id);
  const homeworkAdditionalIds = homeworkSplit.additional.map((item) => item.id);
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
      homeworkRecommended: homeworkRecommendedIds.length > 0,
      homeworkAdditional: homeworkAdditionalIds.length > 0,
    },
    selected: {
      aiExamples: [],
      keyPoints: [],
      recommended: autoSelectRecommended ? [...recommendedIds] : [],
      additional: [],
      homeworkRecommended: autoSelectRecommended ? [...homeworkRecommendedIds] : [],
      homeworkAdditional: [],
    },
  };

  return state.drafts[card.id];
}

function normalizeDraftForCard(draft, card) {
  if (!draft.ui || typeof draft.ui !== "object") {
    draft.ui = { settingsOpen: false };
  }
  if (!draft.sections || typeof draft.sections !== "object") {
    draft.sections = {};
  }
  if (!draft.selected || typeof draft.selected !== "object") {
    draft.selected = {};
  }

  const split = getSourceSplit(card);
  const homeworkSplit = getHomeworkSplit(card);
  const aiExampleIds = usefulAIExamples(card).map((item) => item.id);
  const keyPointIds = keyPointSelectableIds(card);

  const legacyHomeworkSection = typeof draft.sections.homework === "boolean" ? draft.sections.homework : null;
  if (legacyHomeworkSection !== null) {
    if (typeof draft.sections.homeworkRecommended !== "boolean") {
      draft.sections.homeworkRecommended = legacyHomeworkSection;
    }
    if (typeof draft.sections.homeworkAdditional !== "boolean") {
      draft.sections.homeworkAdditional = legacyHomeworkSection;
    }
  }

  const legacyHomeworkSelected = Array.isArray(draft.selected.homework) ? draft.selected.homework : null;
  if (legacyHomeworkSelected && (!Array.isArray(draft.selected.homeworkRecommended) || !Array.isArray(draft.selected.homeworkAdditional))) {
    const recIds = new Set(homeworkSplit.recommended.map((item) => item.id));
    draft.selected.homeworkRecommended = legacyHomeworkSelected.filter((id) => recIds.has(id));
    draft.selected.homeworkAdditional = legacyHomeworkSelected.filter((id) => !recIds.has(id));
  }

  const sectionDefaults = {
    aiSummary: Boolean(card.sections.ai_summary?.content),
    aiQuestions: (card.sections.ai_common_questions?.bullets || []).length > 0,
    keyPoints: keyPointIds.length > 0,
    aiExamples: aiExampleIds.length > 0,
    recommended: split.recommended.length > 0,
    additional: split.additional.length > 0,
    homeworkRecommended: homeworkSplit.recommended.length > 0,
    homeworkAdditional: homeworkSplit.additional.length > 0,
  };

  Object.entries(sectionDefaults).forEach(([key, value]) => {
    if (typeof draft.sections[key] !== "boolean") {
      draft.sections[key] = value;
    }
  });

  const selectedKeys = ["aiExamples", "keyPoints", "recommended", "additional", "homeworkRecommended", "homeworkAdditional"];
  selectedKeys.forEach((key) => {
    if (!Array.isArray(draft.selected[key])) {
      draft.selected[key] = [];
    }
  });
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
      homeworkRecommended: [...(draft.selected.homeworkRecommended || [])],
      homeworkAdditional: [...(draft.selected.homeworkAdditional || [])],
    },
  };
}

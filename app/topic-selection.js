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
    .filter((snippet) => Boolean(snippet.explanation || snippet.question || (snippet.code_examples || []).length));
}

function usefulNotebookSnippets(card) {
  return (card.sections.notebook_snippets || []).filter((snippet) => !isLowValueSnippet(snippet.source || ""));
}

function usefulAIExamples(card) {
  return (card.sections.ai_examples || [])
    .filter((item) => (item.code || "").trim().length > 0)
    .map((item) => ({
      ...item,
      subtopic_id: item.subtopic_id || "",
      subtopic_title: item.subtopic_title || "",
    }));
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
        subtopic_id: String(item.subtopic_id || "").trim(),
        subtopic_title: String(item.subtopic_title || "").trim(),
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
      subtopicId: item.subtopic_id || "",
      subtopicTitle: item.subtopic_title || "",
      item,
    });
  });

  usefulLectureSnippets(card).forEach((item) => {
    items.push({
      id: item.id,
      sourceType: "lecture",
      priority: 1,
      header: `Lecture • ${item.topic || "snippet"} • W${item.week || "?"}`,
      subtopicId: item.subtopic_id || "",
      subtopicTitle: item.subtopic_title || "",
      item,
    });
  });

  usefulNotebookSnippets(card).forEach((item) => {
    items.push({
      id: item.id,
      sourceType: "notebook",
      priority: 2,
      header: `Notebook • W${item.week || "?"} cell ${item.cell_index || "?"} • ${item.topic || ""}`,
      subtopicId: item.subtopic_id || "",
      subtopicTitle: item.subtopic_title || "",
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

function getCardSubtopics(card) {
  const subtopics = Array.isArray(card?.subtopics) ? card.subtopics : [];
  return [...subtopics].sort((a, b) => Number(a?.order || 0) - Number(b?.order || 0));
}

function getSubtopicLookup(card) {
  const lookup = new Map();
  getCardSubtopics(card).forEach((subtopic) => {
    lookup.set(String(subtopic.id || ""), subtopic);
  });
  return lookup;
}

function groupItemsBySubtopic(card, items, getSubtopicId, getSubtopicTitle) {
  const lookup = getSubtopicLookup(card);
  const grouped = new Map();

  getCardSubtopics(card).forEach((subtopic) => {
    grouped.set(String(subtopic.id || ""), {
      id: String(subtopic.id || ""),
      title: String(subtopic.title || "Subtopic"),
      summary: String(subtopic.summary || "").trim(),
      items: [],
    });
  });

  items.forEach((item) => {
    const explicitId = String(getSubtopicId(item) || "").trim();
    const explicitTitle = String(getSubtopicTitle(item) || "").trim();
    const fallbackSubtopic = getCardSubtopics(card)[0] || null;
    const resolvedId = explicitId || String(fallbackSubtopic?.id || "misc");

    if (!grouped.has(resolvedId)) {
      grouped.set(resolvedId, {
        id: resolvedId,
        title: explicitTitle || lookup.get(resolvedId)?.title || "Subtopic",
        summary: String(lookup.get(resolvedId)?.summary || "").trim(),
        items: [],
      });
    }

    grouped.get(resolvedId).items.push(item);
  });

  return [...grouped.values()].filter((group) => group.items.length > 0);
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
      recommended: [],
      additional: [],
    },
    overrides: {
      keyPoints: {},
      keyPointDetails: {},
      aiExamples: {},
      sources: {},
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
      aiExamples: [...(draft.selected.aiExamples || [])],
      keyPoints: [...(draft.selected.keyPoints || [])],
      recommended: [...(draft.selected.recommended || [])],
      additional: [...(draft.selected.additional || [])],
    },
    overrides: deepClone(draft.overrides || { keyPoints: {}, keyPointDetails: {}, aiExamples: {}, sources: {} }),
  };
}

function getRenderableSelection(card, draft) {
  if (!draft) {
    return null;
  }

  const normalized = cloneDraft(draft);
  const aiExampleIds = new Set(usefulAIExamples(card).map((item) => item.id));
  const keyPointIds = new Set(keyPointSelectableIds(card));
  const split = getSourceSplit(card);
  const recommendedIds = new Set(split.recommended.map((item) => item.id));
  const additionalIds = new Set(split.additional.map((item) => item.id));

  normalized.selected.aiExamples = normalized.sections.aiExamples
    ? normalized.selected.aiExamples.filter((id) => aiExampleIds.has(id))
    : [];
  normalized.selected.keyPoints = normalized.sections.keyPoints
    ? normalized.selected.keyPoints.filter((id) => keyPointIds.has(id))
    : [];
  normalized.selected.recommended = normalized.sections.recommended
    ? normalized.selected.recommended.filter((id) => recommendedIds.has(id))
    : [];
  normalized.selected.additional = normalized.sections.additional
    ? normalized.selected.additional.filter((id) => additionalIds.has(id))
    : [];

  const totalSelected =
    normalized.selected.aiExamples.length +
    normalized.selected.keyPoints.length +
    normalized.selected.recommended.length +
    normalized.selected.additional.length;

  return totalSelected ? normalized : null;
}

function getSelectionCounts(card, draft = ensureDraft(card)) {
  const selection = getRenderableSelection(card, draft);
  if (!selection) {
    return { total: 0, aiExamples: 0, keyPoints: 0, recommended: 0, additional: 0 };
  }

  return {
    total:
      selection.selected.aiExamples.length +
      selection.selected.keyPoints.length +
      selection.selected.recommended.length +
      selection.selected.additional.length,
    aiExamples: selection.selected.aiExamples.length,
    keyPoints: selection.selected.keyPoints.length,
    recommended: selection.selected.recommended.length,
    additional: selection.selected.additional.length,
  };
}

function hasRenderableSelection(card, draft = ensureDraft(card)) {
  return getSelectionCounts(card, draft).total > 0;
}

function getSelectedPreviewEntries() {
  return state.cards
    .map((card) => {
      const draft = ensureDraft(card);
      const selection = getRenderableSelection(card, draft);
      return selection ? { card, selection } : null;
    })
    .filter(Boolean)
    .sort((a, b) => {
      const hitDelta = (b.card.exam_stats?.total_hits || 0) - (a.card.exam_stats?.total_hits || 0);
      if (hitDelta !== 0) {
        return hitDelta;
      }
      return humanizeTopic(a.card.topic).localeCompare(humanizeTopic(b.card.topic));
    });
}

function getSelectedItemTotals(cards = state.cards) {
  return cards.reduce(
    (acc, card) => {
      const counts = getSelectionCounts(card);
      acc.topics += counts.total > 0 ? 1 : 0;
      acc.items += counts.total;
      return acc;
    },
    { topics: 0, items: 0 }
  );
}

function getWeekSelectionSummary(bundle) {
  return (bundle.cards || []).reduce(
    (acc, card) => {
      const count = getSelectionCounts(card).total;
      acc.topics += count > 0 ? 1 : 0;
      acc.items += count;
      return acc;
    },
    { topics: 0, items: 0 }
  );
}

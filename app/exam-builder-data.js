const EXAM_BUILDER_SECTION_LABELS = {
  must_know: "Must Know",
  exam_patterns: "Exam Patterns",
  useful_backup: "Useful Backup",
};

const EXAM_BUILDER_SECTION_DESCRIPTIONS = {
  must_know: "The fastest, densest references you should reach for first.",
  exam_patterns: "Recurring traps, worked comparisons, and exam-style patterns worth recognizing quickly.",
  useful_backup: "Support material to add when a narrower question still leaves a gap.",
};

function normalizeExamBuilderPayload(payload) {
  const parentTopics = Array.isArray(payload?.parent_topics)
    ? payload.parent_topics.map(normalizeExamParentTopic).filter(Boolean)
    : [];
  const cards = flattenExamBuilderTopics(parentTopics);
  return { parentTopics, cards };
}

function normalizeExamParentTopic(parentTopic) {
  if (!parentTopic || typeof parentTopic !== "object") {
    return null;
  }

  const mainTopics = Array.isArray(parentTopic.main_topics)
    ? parentTopic.main_topics.map((topic) => normalizeExamCard(parentTopic, topic)).filter(Boolean)
    : [];

  return {
    id: String(parentTopic.id || "").trim(),
    title: String(parentTopic.title || "Topic Group").trim(),
    summary: String(parentTopic.summary || "").trim(),
    mainTopics,
  };
}

function flattenExamBuilderTopics(parentTopics) {
  return parentTopics.flatMap((parentTopic) => parentTopic.mainTopics || []);
}

function normalizeExamCard(parentTopic, mainTopic) {
  if (!mainTopic || typeof mainTopic !== "object") {
    return null;
  }

  const mainWeek = Number(mainTopic.main_week || 0);
  const relatedWeeks = Array.isArray(mainTopic.related_weeks)
    ? mainTopic.related_weeks.map((value) => Number(value)).filter((value) => Number.isFinite(value) && value > 0)
    : [];
  const weeks = [...new Set([mainWeek, ...relatedWeeks].filter((value) => Number.isFinite(value) && value > 0))];
  const sections = Array.isArray(mainTopic.sections)
    ? mainTopic.sections.map(normalizeExamSection).filter(Boolean)
    : [];

  const allSnippets = sections.flatMap((section) => section.snippets);
  const allPieces = allSnippets.flatMap((snippet) => snippet.pieces);
  const examHitCount = allSnippets.filter((snippet) => snippet.snippetType === "past_exam_question").length;

  return {
    id: String(mainTopic.id || "").trim(),
    topic: String(mainTopic.title || "Topic").trim(),
    canonical_topic: String(mainTopic.id || "").trim(),
    parent_topic: String(parentTopic.title || "Topic Group").trim(),
    parent_topic_id: String(parentTopic.id || "").trim(),
    summary: String(mainTopic.summary || "").trim(),
    search_text: String(mainTopic.search_text || `${mainTopic.title || ""} ${parentTopic.title || ""}`).trim(),
    weeks,
    related_weeks: relatedWeeks,
    topic_meta: {
      week: mainWeek,
      topic_order: Number(mainTopic.topic_order || 0),
    },
    exam_stats: {
      total_hits: examHitCount,
      coverage_count: allPieces.length,
    },
    sections,
    snippetCount: allSnippets.length,
    pieceCount: allPieces.length,
  };
}

function normalizeExamSection(section) {
  if (!section || typeof section !== "object") {
    return null;
  }

  const snippets = Array.isArray(section.snippets)
    ? section.snippets
        .map(normalizeExamSnippet)
        .filter(Boolean)
        .sort((a, b) => Number(a.order || 0) - Number(b.order || 0))
    : [];

  return {
    key: String(section.key || "").trim(),
    title: String(section.title || EXAM_BUILDER_SECTION_LABELS[section.key] || humanizeTopic(section.key || "Section")).trim(),
    description: String(section.description || EXAM_BUILDER_SECTION_DESCRIPTIONS[String(section.key || "").trim()] || "").trim(),
    initialVisibleCount: Math.max(1, Number(section.initial_visible_count || 0) || 4),
    snippets,
  };
}

function normalizeExamSnippet(snippet) {
  if (!snippet || typeof snippet !== "object") {
    return null;
  }

  const pieces = Array.isArray(snippet.pieces)
    ? snippet.pieces
        .map(normalizeExamPiece)
        .filter(Boolean)
        .sort((a, b) => Number(a.order || 0) - Number(b.order || 0))
    : [];

  return {
    id: String(snippet.id || "").trim(),
    title: String(snippet.title || "Snippet").trim(),
    order: Number(snippet.order || 0),
    snippetType: String(snippet.snippet_type || "general_snippet").trim(),
    parentTopic: String(snippet.parent_topic || "").trim(),
    mainTopic: String(snippet.main_topic || "").trim(),
    mainWeek: Number(snippet.main_week || 0),
    relatedTopics: Array.isArray(snippet.related_topics)
      ? snippet.related_topics.map((value) => String(value || "").trim()).filter(Boolean)
      : [],
    relatedWeeks: Array.isArray(snippet.related_weeks)
      ? snippet.related_weeks.map((value) => Number(value)).filter((value) => Number.isFinite(value) && value > 0)
      : [],
    summary: String(snippet.summary || "").trim(),
    sourceRefs: Array.isArray(snippet.source_refs) ? deepClone(snippet.source_refs) : [],
    pieces,
  };
}

function normalizeExamPiece(piece) {
  if (!piece || typeof piece !== "object" || !piece.id) {
    return null;
  }

  return {
    id: String(piece.id || "").trim(),
    sourcePieceId: String(piece.source_piece_id || "").trim(),
    pieceType: String(piece.piece_type || "explanation").trim(),
    title: String(piece.title || "Piece").trim(),
    order: Number(piece.order || 0),
    content: deepClone(piece.content || {}),
    selectable: piece.selectable !== false,
    sourceRefs: Array.isArray(piece.source_refs) ? deepClone(piece.source_refs) : [],
  };
}

function getExamCardSections(card) {
  return Array.isArray(card?.sections) ? card.sections : [];
}

function getExamSection(card, sectionKey) {
  return getExamCardSections(card).find((section) => section.key === sectionKey) || null;
}

function getExamSnippet(card, snippetId) {
  return getExamCardSections(card).flatMap((section) => section.snippets).find((snippet) => snippet.id === snippetId) || null;
}

function findExamPieceContext(card, pieceId) {
  for (const section of getExamCardSections(card)) {
    for (const snippet of section.snippets) {
      const piece = snippet.pieces.find((entry) => entry.id === pieceId);
      if (piece) {
        return { section, snippet, piece };
      }
    }
  }
  return null;
}

function getAllSelectablePieceIds(card) {
  return getExamCardSections(card)
    .flatMap((section) => section.snippets)
    .flatMap((snippet) => snippet.pieces)
    .filter((piece) => piece.selectable)
    .map((piece) => piece.id);
}

function getSectionSelectablePieceIds(card, sectionKey) {
  const section = getExamSection(card, sectionKey);
  if (!section) {
    return [];
  }
  return section.snippets.flatMap((snippet) => snippet.pieces.filter((piece) => piece.selectable).map((piece) => piece.id));
}

function getSnippetSelectablePieceIds(card, snippetId) {
  const snippet = getExamSnippet(card, snippetId);
  if (!snippet) {
    return [];
  }
  return snippet.pieces.filter((piece) => piece.selectable).map((piece) => piece.id);
}

const VALID_PIECE_PRESENTATION_EMPHASIS = new Set(["trap"]);

function normalizeSnippetBankPayload(payload) {
  const topics = Array.isArray(payload?.topics) ? payload.topics.map(normalizeTopic).filter(Boolean) : [];
  const snippets = topics.flatMap((topic) => topic.subtopics.flatMap((subtopic) => subtopic.snippets));
  return {
    topics,
    snippets,
    availableCoursePhases: [...new Set(snippets.map((snippet) => snippet.coursePhase).filter(Boolean))],
    availableRecurrenceLevels: [...new Set(snippets.map((snippet) => snippet.recurrenceLevel).filter(Boolean))],
  };
}

function normalizeTopic(topic) {
  if (!topic || typeof topic !== "object") {
    return null;
  }

  const topicSlug = String(topic.topic_slug || "").trim();
  const title = String(topic.title || "Topic").trim();
  const description = String(topic.description || "").trim();
  const subtopics = Array.isArray(topic.subtopics)
    ? topic.subtopics
        .map((subtopic) => normalizeSubtopic(topicSlug, title, subtopic))
        .filter(Boolean)
        .sort((a, b) => a.sortOrder - b.sortOrder || a.title.localeCompare(b.title))
    : [];

  return {
    id: topicSlug,
    topicSlug,
    title,
    summary: description,
    description,
    sortOrder: Number(topic.sort_order || 0),
    snippetCount: Number(topic.snippet_count || subtopics.reduce((sum, subtopic) => sum + subtopic.snippets.length, 0)),
    themeId: topicSlug,
    subtopics,
    searchText: [title, description, ...subtopics.map((subtopic) => subtopic.title)].join(" ").toLowerCase(),
  };
}

function normalizeSubtopic(topicSlug, topicTitle, subtopic) {
  if (!subtopic || typeof subtopic !== "object") {
    return null;
  }

  const subtopicSlug = String(subtopic.slug || "").trim();
  const title = String(subtopic.title || "Subtopic").trim();
  const description = String(subtopic.description || "").trim();
  const snippets = Array.isArray(subtopic.snippets)
    ? subtopic.snippets
        .map((snippet) => normalizeSnippet(topicSlug, topicTitle, subtopicSlug, title, snippet))
        .filter(Boolean)
        .sort((a, b) => a.sortOrder - b.sortOrder || a.title.localeCompare(b.title))
    : [];

  return {
    id: subtopicSlug,
    subtopicSlug,
    topicSlug,
    topicTitle,
    title,
    summary: description,
    description,
    sortOrder: Number(subtopic.sort_order || 0),
    snippetCount: Number(subtopic.snippet_count || snippets.length),
    snippets,
    searchText: [topicTitle, title, description, ...snippets.map((snippet) => snippet.title)].join(" ").toLowerCase(),
  };
}

function normalizeSnippet(topicSlug, topicTitle, subtopicSlug, subtopicTitle, snippet) {
  if (!snippet || typeof snippet !== "object") {
    return null;
  }

  const slug = String(snippet.slug || "").trim();
  const pieces = Array.isArray(snippet.pieces)
    ? snippet.pieces
        .map((piece) => normalizePiece(topicSlug, slug, piece))
        .filter(Boolean)
        .sort((a, b) => a.order - b.order || a.title.localeCompare(b.title))
    : [];
  const trapSlugs = Array.isArray(snippet.trap_slugs) ? snippet.trap_slugs.map((value) => String(value || "").trim()).filter(Boolean) : [];
  const trapLabels = Array.isArray(snippet.trap_labels) ? snippet.trap_labels.map((value) => String(value || "").trim()).filter(Boolean) : [];
  const keywords = Array.isArray(snippet.keywords) ? snippet.keywords.map((value) => String(value || "").trim()).filter(Boolean) : [];
  const searchBits = [
    topicTitle,
    subtopicTitle,
    snippet.title,
    snippet.summary,
    snippet.why,
    ...keywords,
    ...trapSlugs,
    ...trapLabels,
    ...pieces.map((piece) => piece.title),
  ];

  return {
    id: slug,
    slug,
    title: String(snippet.title || "Snippet").trim(),
    summary: String(snippet.summary || "").trim(),
    why: String(snippet.why || "").trim(),
    sortOrder: Number(snippet.sort_order || 0),
    defaultPriority: Number(snippet.default_priority || 0),
    difficulty: String(snippet.difficulty || "").trim(),
    coursePhase: String(snippet.course_phase || "").trim(),
    recurrenceLevel: String(snippet.recurrence_level || "").trim(),
    examFamilyCount: Number(snippet.exam_family_count || 0),
    questionRefCount: Number(snippet.question_ref_count || 0),
    pieceCount: Number(snippet.piece_count || pieces.length),
    keywords,
    trapSlugs,
    trapLabels,
    topicSlug,
    topicTitle,
    subtopicSlug,
    subtopicTitle,
    readmePath: String(snippet.readme_path || "").trim(),
    contentDir: String(snippet.content_dir || "").trim(),
    pieces,
    searchText: searchBits.join(" ").toLowerCase(),
  };
}

function normalizePiece(topicSlug, snippetSlug, piece) {
  if (!piece || typeof piece !== "object" || !piece.piece_id) {
    return null;
  }

  const role = String(piece.role || "").trim();
  const trapSlugs = Array.isArray(piece.trap_slugs) ? piece.trap_slugs.map((value) => String(value || "").trim()).filter(Boolean) : [];
  const presentation = normalizePiecePresentation(piece.presentation, role);

  return {
    id: String(piece.piece_id || "").trim(),
    pieceId: String(piece.piece_id || "").trim(),
    pieceSlug: String(piece.piece_slug || "").trim(),
    order: Number(piece.sort_order || 0),
    title: String(piece.title || "Piece").trim(),
    pieceType: String(piece.kind || "paragraph").trim(),
    kind: String(piece.kind || "paragraph").trim(),
    role,
    topicSlug,
    snippetSlug,
    defaultSelected: Boolean(piece.default_selected),
    questionRefCount: Number(piece.question_ref_count || 0),
    bodyMarkdown: String(piece.body_markdown || ""),
    bodyBlocks: normalizeBodyBlocks(piece.body_blocks),
    selectable: true,
    trapSlugs,
    trapLabels: Array.isArray(piece.trap_labels) ? piece.trap_labels.map((value) => String(value || "").trim()).filter(Boolean) : [],
    bodyPath: String(piece.body_path || "").trim(),
    presentation,
  };
}

function normalizePiecePresentation(presentation, role = "") {
  const explicit = presentation && typeof presentation === "object" ? String(presentation.emphasis || "").trim() : "";
  const derived = role === "trap" ? "trap" : "";
  const emphasis = explicit || derived;
  if (!VALID_PIECE_PRESENTATION_EMPHASIS.has(emphasis)) {
    return null;
  }
  const label =
    presentation && typeof presentation === "object" && String(presentation.label || "").trim()
      ? String(presentation.label).trim()
      : humanizeTopic(emphasis);
  return { emphasis, label };
}

function normalizeBodyBlocks(blocks) {
  if (!Array.isArray(blocks)) {
    return [];
  }
  return blocks
    .map((block) => {
      if (!block || typeof block !== "object") {
        return null;
      }
      const type = String(block.type || "").trim();
      if (!type) {
        return null;
      }
      if (type === "paragraph") {
        return { type, text: String(block.text || "").trim() };
      }
      if (type === "code") {
        return {
          type,
          language: String(block.language || "").trim(),
          code: String(block.code || ""),
        };
      }
      if (type === "list") {
        return {
          type,
          ordered: Boolean(block.ordered),
          items: Array.isArray(block.items) ? block.items.map((item) => String(item || "")) : [],
        };
      }
      if (type === "table") {
        return {
          type,
          headers: Array.isArray(block.headers) ? block.headers.map((cell) => String(cell || "")) : [],
          rows: Array.isArray(block.rows)
            ? block.rows.map((row) => (Array.isArray(row) ? row.map((cell) => String(cell || "")) : []))
            : [],
        };
      }
      return null;
    })
    .filter(Boolean);
}

function getTopicThemeId(value) {
  if (!value || typeof value !== "object") {
    return "";
  }
  return String(value.topicSlug || value.topic_slug || value.themeId || value.id || "").trim();
}

function getParentTopicThemeId(value) {
  return getTopicThemeId(value);
}

function getPiecePresentation(piece) {
  if (!piece || typeof piece !== "object" || !piece.presentation) {
    return null;
  }
  const emphasis = String(piece.presentation.emphasis || "").trim();
  if (!VALID_PIECE_PRESENTATION_EMPHASIS.has(emphasis)) {
    return null;
  }
  return {
    emphasis,
    label: String(piece.presentation.label || humanizeTopic(emphasis)).trim() || humanizeTopic(emphasis),
  };
}

function pieceHasPresentationEmphasis(piece, emphasis) {
  return getPiecePresentation(piece)?.emphasis === emphasis;
}

function getSnippetSelectablePieceIds(snippet) {
  return Array.isArray(snippet?.pieces) ? snippet.pieces.filter((piece) => piece.selectable).map((piece) => piece.id) : [];
}

function getSubtopicSelectablePieceIds(subtopic) {
  return Array.isArray(subtopic?.snippets) ? subtopic.snippets.flatMap((snippet) => getSnippetSelectablePieceIds(snippet)) : [];
}

function getTopicSelectablePieceIds(topic) {
  return Array.isArray(topic?.subtopics) ? topic.subtopics.flatMap((subtopic) => getSubtopicSelectablePieceIds(subtopic)) : [];
}

function findSnippetById(snippetId) {
  return state.snippets.find((snippet) => snippet.id === snippetId) || null;
}

function findPieceContext(snippet, pieceId) {
  if (!snippet) {
    return null;
  }
  const piece = (snippet.pieces || []).find((entry) => entry.id === pieceId);
  if (!piece) {
    return null;
  }
  const topic = state.topics.find((entry) => entry.id === snippet.topicSlug) || null;
  const subtopic = topic?.subtopics.find((entry) => entry.id === snippet.subtopicSlug) || null;
  return { topic, subtopic, snippet, piece };
}

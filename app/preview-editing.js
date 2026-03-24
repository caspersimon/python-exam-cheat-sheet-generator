function bindPreviewEditingEvents() {
  if (!refs.previewView) {
    return;
  }
  refs.previewView.addEventListener("click", handlePreviewEditingClick);
}

function handlePreviewEditingClick(event) {
  const editCardTitleBtn = event.target.closest("[data-role='preview-edit-card-title']");
  if (editCardTitleBtn) {
    event.preventDefault();
    void editPreviewCardTitle(editCardTitleBtn.dataset.cardId || "");
    return;
  }

  const toggleLockBtn = event.target.closest("[data-role='preview-toggle-lock']");
  if (toggleLockBtn) {
    event.preventDefault();
    togglePreviewCardLock(toggleLockBtn.dataset.cardId || "");
    return;
  }

  const deleteCardBtn = event.target.closest("[data-role='preview-delete-card']");
  if (deleteCardBtn) {
    event.preventDefault();
    deletePreviewCard(deleteCardBtn.dataset.cardId || "");
    return;
  }

  const deleteItemBtn = event.target.closest("[data-role='preview-delete-item']");
  if (deleteItemBtn) {
    event.preventDefault();
    deletePreviewItem(deleteItemBtn.dataset.sourceCardId || "", deleteItemBtn.dataset.pieceId || "");
    return;
  }

  const editItemBtn = event.target.closest("[data-role='preview-edit-item']");
  if (editItemBtn) {
    event.preventDefault();
    void editPreviewItem(editItemBtn.dataset.sourceCardId || "", editItemBtn.dataset.pieceId || "");
  }
}

function getPreviewEntry(previewId) {
  return state.previewEntries?.[previewId] || null;
}

function getDraftCardContext(cardId) {
  const card = state.cards.find((entry) => entry.id === cardId);
  if (!card) {
    return null;
  }
  const draft = ensureDraft(card);
  return { card, draft };
}

function deletePreviewCard(previewId) {
  if (!previewId) {
    return;
  }
  const entry = getPreviewEntry(previewId);
  if (!entry) {
    return;
  }

  const confirmed = window.confirm(`Remove "${humanizeTopic(entry.card.topic)}" from the cheat sheet preview?`);
  if (!confirmed) {
    return;
  }

  pushPreviewHistorySnapshot(`Remove card "${humanizeTopic(entry.card.topic)}"`);

  entry.cards.forEach((sourceCard) => {
    const draft = ensureDraft(sourceCard);
    draft.selected.pieces = [];
    draft.overrides = { pieces: {} };
  });

  delete state.previewCards[previewId];
  renderAll();
}

function togglePreviewCardLock(previewId) {
  if (!previewId) {
    return;
  }
  const entry = getPreviewEntry(previewId);
  const layout = state.previewCards[previewId];
  if (!entry || !layout) {
    return;
  }

  const nextLocked = !Boolean(layout.locked);
  pushPreviewHistorySnapshot(`${nextLocked ? "Lock" : "Unlock"} card "${humanizeTopic(entry.card.topic)}"`);
  layout.locked = nextLocked;
  renderPreview();
}

async function editPreviewCardTitle(previewId) {
  if (!previewId) {
    return;
  }
  const entry = getPreviewEntry(previewId);
  const layout = state.previewCards[previewId];
  if (!entry || !layout) {
    return;
  }

  const currentTitle = getPreviewCardTitle(entry, layout);
  const values = await requestPreviewEditValues({
    title: "Edit Card Title",
    subtitle: humanizeTopic(entry.card.topic),
    fields: [
      {
        id: "title",
        label: "Card title",
        prompt: "Edit card title:",
        value: currentTitle,
      },
    ],
  });
  if (!values) {
    return;
  }

  const nextTitle = String(values.title || "").trim();
  pushPreviewHistorySnapshot(`Edit card title for "${humanizeTopic(entry.card.topic)}"`);
  const defaultTitle = derivePreviewCardTitle(entry);
  layout.title = nextTitle && nextTitle !== defaultTitle ? nextTitle : "";
  renderPreview();
}

function deletePreviewItem(cardId, pieceId) {
  if (!cardId || !pieceId) {
    return;
  }

  const context = getDraftCardContext(cardId);
  if (!context) {
    return;
  }

  const { card, draft } = context;
  const overrides = ensureSelectionOverrides(draft);
  pushPreviewHistorySnapshot(`Delete piece in "${humanizeTopic(card.topic)}"`);
  draft.selected.pieces = (draft.selected.pieces || []).filter((id) => id !== pieceId);
  delete overrides.pieces[pieceId];
  renderPreview();
}

async function editPreviewItem(cardId, pieceId) {
  if (!cardId || !pieceId) {
    return;
  }
  const context = getDraftCardContext(cardId);
  if (!context) {
    return;
  }

  const { card, draft } = context;
  const match = findExamPieceContext(card, pieceId);
  if (!match) {
    return;
  }

  const current = getPieceOverride(draft, match.piece);
  const values = await requestPreviewEditValues(buildPieceEditRequest(card, current));
  if (!values) {
    return;
  }

  const nextOverride = buildPieceOverrideFromValues(current, values);
  if (!nextOverride) {
    deletePreviewItem(cardId, pieceId);
    return;
  }

  pushPreviewHistorySnapshot(`Edit piece in "${humanizeTopic(card.topic)}"`);
  ensureSelectionOverrides(draft).pieces[pieceId] = nextOverride;
  renderPreview();
}

function buildPieceEditRequest(card, piece) {
  const base = {
    title: `Edit ${humanizePieceType(piece.pieceType)}`,
    subtitle: humanizeTopic(card.topic),
    fields: [
      {
        id: "title",
        label: "Piece title",
        prompt: "Edit piece title:",
        value: piece.title || "",
      },
    ],
  };

  if (piece.pieceType === "code_example") {
    base.fields.push(
      {
        id: "code",
        label: "Code",
        prompt: "Edit code:",
        value: String(piece.content?.code || ""),
        multiline: true,
        rows: 10,
        kind: "code",
      },
      {
        id: "output",
        label: "Output",
        prompt: "Edit output:",
        value: String(piece.content?.output || ""),
        multiline: true,
        rows: 4,
      },
      {
        id: "text",
        label: "Optional note",
        prompt: "Edit note:",
        value: String(piece.content?.text || ""),
        multiline: true,
        rows: 4,
      }
    );
    return base;
  }

  if (piece.pieceType === "past_exam_piece") {
    base.fields.push(
      {
        id: "question",
        label: "Question",
        prompt: "Edit question:",
        value: String(piece.content?.question || ""),
        multiline: true,
        rows: 7,
      },
      {
        id: "code_context",
        label: "Code context",
        prompt: "Edit code context:",
        value: String(piece.content?.code_context || ""),
        multiline: true,
        rows: 8,
        kind: "code",
      },
      {
        id: "options",
        label: "Options",
        prompt: "Edit options as one per line, for example `a: ...`:",
        value: optionsToEditableText(piece.content?.options || {}),
        multiline: true,
        rows: 6,
      },
      {
        id: "correct",
        label: "Correct option",
        prompt: "Edit correct option:",
        value: String(piece.content?.correct || ""),
      },
      {
        id: "explanation",
        label: "Explanation",
        prompt: "Edit explanation:",
        value: String(piece.content?.explanation || ""),
        multiline: true,
        rows: 6,
      }
    );
    return base;
  }

  if (piece.pieceType === "reference_table") {
    base.fields.push(
      {
        id: "table",
        label: "Table",
        prompt: "Edit the table as tab-separated lines. First line is headers.",
        value: tableToEditableText(piece.content || {}),
        multiline: true,
        rows: 8,
      },
      {
        id: "text",
        label: "Optional note",
        prompt: "Edit note:",
        value: String(piece.content?.text || ""),
        multiline: true,
        rows: 3,
      }
    );
    return base;
  }

  base.fields.push({
    id: "text",
    label: "Text",
    prompt: "Edit text:",
    value: String(piece.content?.text || ""),
    multiline: true,
    rows: 6,
  });
  return base;
}

function buildPieceOverrideFromValues(piece, values) {
  const title = String(values.title || "").trim();
  const content = {};

  if (piece.pieceType === "code_example") {
    content.code = String(values.code || "");
    content.output = String(values.output || "").trim();
    content.text = String(values.text || "").trim();
    if (!title && !content.code.trim() && !content.output && !content.text) {
      return null;
    }
    return { title, content };
  }

  if (piece.pieceType === "past_exam_piece") {
    content.question = String(values.question || "").trim();
    content.code_context = String(values.code_context || "");
    content.options = editableTextToOptions(values.options || "");
    content.correct = String(values.correct || "").trim();
    content.explanation = String(values.explanation || "").trim();
    if (!title && !content.question && !content.code_context.trim() && !Object.keys(content.options).length && !content.correct && !content.explanation) {
      return null;
    }
    return { title, content };
  }

  if (piece.pieceType === "reference_table") {
    const parsed = editableTextToTable(values.table || "");
    content.headers = parsed.headers;
    content.rows = parsed.rows;
    content.text = String(values.text || "").trim();
    if (!title && !content.text && !content.headers.length && !content.rows.length) {
      return null;
    }
    return { title, content };
  }

  content.text = String(values.text || "").trim();
  if (!title && !content.text) {
    return null;
  }
  return { title, content };
}

function optionsToEditableText(options) {
  return Object.entries(options || {})
    .map(([key, value]) => `${key}: ${value}`)
    .join("\n");
}

function editableTextToOptions(text) {
  const lines = String(text || "")
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean);
  const options = {};
  lines.forEach((line) => {
    const match = line.match(/^([A-Za-z0-9]+)\s*:\s*(.+)$/);
    if (match) {
      options[match[1].toLowerCase()] = match[2].trim();
    }
  });
  return options;
}

function tableToEditableText(content) {
  const headers = Array.isArray(content.headers) ? content.headers : [];
  const rows = Array.isArray(content.rows) ? content.rows : [];
  return [headers.join("\t"), ...rows.map((row) => row.join("\t"))].filter(Boolean).join("\n");
}

function editableTextToTable(text) {
  const lines = String(text || "")
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean);
  if (!lines.length) {
    return { headers: [], rows: [] };
  }
  const splitRow = (line) =>
    line.includes("\t")
      ? line.split("\t").map((value) => value.trim())
      : line.split("|").map((value) => value.trim()).filter(Boolean);
  const headers = splitRow(lines[0]).filter(Boolean);
  const rows = lines.slice(1).map(splitRow).filter((row) => row.length > 0);
  return { headers, rows };
}

function humanizePieceType(pieceType) {
  if (pieceType === "past_exam_piece") {
    return "past exam snippet";
  }
  if (pieceType === "reference_table") {
    return "reference table";
  }
  if (pieceType === "code_example") {
    return "code example";
  }
  return "explanation";
}

bindPreviewEditingEvents();

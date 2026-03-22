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
    deletePreviewItem(
      deleteItemBtn.dataset.sourceCardId || "",
      deleteItemBtn.dataset.itemType || "",
      deleteItemBtn.dataset.itemId || "",
      deleteItemBtn.dataset.section || ""
    );
    return;
  }

  const editItemBtn = event.target.closest("[data-role='preview-edit-item']");
  if (editItemBtn) {
    event.preventDefault();
    void editPreviewItem(
      editItemBtn.dataset.sourceCardId || "",
      editItemBtn.dataset.itemType || "",
      editItemBtn.dataset.itemId || "",
      editItemBtn.dataset.section || ""
    );
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
    draft.selected.aiQuestions = [];
    draft.selected.aiExamples = [];
    draft.selected.keyPoints = [];
    draft.selected.recommended = [];
    draft.selected.additional = [];
    draft.overrides = {
      aiQuestions: {},
      keyPoints: {},
      keyPointDetails: {},
      aiExamples: {},
      sources: {},
    };
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

function deletePreviewItem(cardId, itemType, itemId, section) {
  if (!cardId || !itemId) {
    return;
  }
  const context = getDraftCardContext(cardId);
  if (!context) {
    return;
  }

  const { card, draft } = context;
  ensureSelectionOverrides(draft);
  pushPreviewHistorySnapshot(`Delete ${humanizeItemType(itemType)} in "${humanizeTopic(card.topic)}"`);

  if (itemType === "keyPoint") {
    draft.selected.keyPoints = (draft.selected.keyPoints || []).filter((id) => id !== itemId && !id.startsWith(`${itemId}-d`));
    delete draft.overrides.keyPoints[itemId];
    Object.keys(draft.overrides.keyPointDetails).forEach((detailId) => {
      if (detailId.startsWith(`${itemId}-d`)) {
        delete draft.overrides.keyPointDetails[detailId];
      }
    });
  } else if (itemType === "aiQuestion") {
    draft.selected.aiQuestions = (draft.selected.aiQuestions || []).filter((id) => id !== itemId);
    delete draft.overrides.aiQuestions[itemId];
  } else if (itemType === "keyPointDetail") {
    draft.selected.keyPoints = (draft.selected.keyPoints || []).filter((id) => id !== itemId);
    delete draft.overrides.keyPointDetails[itemId];
  } else if (itemType === "aiExample") {
    draft.selected.aiExamples = (draft.selected.aiExamples || []).filter((id) => id !== itemId);
    delete draft.overrides.aiExamples[itemId];
  } else if (itemType === "sourceItem") {
    draft.selected.recommended = (draft.selected.recommended || []).filter((id) => id !== itemId);
    draft.selected.additional = (draft.selected.additional || []).filter((id) => id !== itemId);
    delete draft.overrides.sources[itemId];
  }

  renderPreview();
}

async function editPreviewItem(cardId, itemType, itemId, section) {
  if (!cardId || !itemId) {
    return;
  }
  const context = getDraftCardContext(cardId);
  if (!context) {
    return;
  }

  const { card, draft } = context;
  const overrides = ensureSelectionOverrides(draft);

  if (itemType === "aiQuestion") {
    const item = commonQuestionItems(card).find((entry) => entry.id === itemId);
    if (!item) {
      return;
    }
    const current = getPreviewAIQuestionOverride(draft, itemId, item);
    const values = await requestPreviewEditValues({
      title: "Edit Common Exam Question",
      subtitle: humanizeTopic(card.topic),
      fields: [
        {
          id: "summary",
          label: "Question",
          prompt: "Edit question:",
          value: current.summary || "",
          multiline: true,
          rows: 4,
        },
        {
          id: "detail",
          label: "Answer summary",
          prompt: "Edit answer summary:",
          value: current.detail || "",
          multiline: true,
          rows: 6,
        },
        {
          id: "extra",
          label: "Extra exam note",
          prompt: "Edit extra exam note:",
          value: current.extra || "",
          multiline: true,
          rows: 5,
        },
        {
          id: "code",
          label: "Code example",
          prompt: "Edit code example:",
          value: current.code || "",
          multiline: true,
          rows: 9,
          kind: "code",
        },
      ],
    });
    if (!values) {
      return;
    }
    const trimmedSummary = String(values.summary || "").trim();
    const trimmedDetail = String(values.detail || "").trim();
    const trimmedExtra = String(values.extra || "").trim();
    const codeValue = String(values.code || "");
    if (!trimmedSummary && !trimmedDetail && !trimmedExtra && !codeValue.trim()) {
      deletePreviewItem(cardId, itemType, itemId, section);
      return;
    }
    pushPreviewHistorySnapshot(`Edit common exam question in "${humanizeTopic(card.topic)}"`);
    overrides.aiQuestions[itemId] = {
      summary: trimmedSummary,
      detail: trimmedDetail,
      extra: trimmedExtra,
      code: codeValue,
    };
    renderPreview();
    return;
  }

  if (itemType === "keyPoint") {
    const group = keyPointGroups(card).find((entry) => entry.id === itemId);
    if (!group) {
      return;
    }
    const current = getPreviewKeyPointOverride(draft, itemId, group.text);
    const values = await requestPreviewEditValues({
      title: "Edit Key Point",
      subtitle: humanizeTopic(card.topic),
      fields: [
        {
          id: "text",
          label: "Key point text",
          prompt: "Edit key point text:",
          value: current,
          multiline: true,
          rows: 6,
        },
      ],
    });
    if (!values) {
      return;
    }
    const trimmed = String(values.text || "").trim();
    if (!trimmed) {
      deletePreviewItem(cardId, itemType, itemId, section);
      return;
    }
    pushPreviewHistorySnapshot(`Edit key point in "${humanizeTopic(card.topic)}"`);
    overrides.keyPoints[itemId] = trimmed;
    renderPreview();
    return;
  }

  if (itemType === "keyPointDetail") {
    const detail = findKeyPointDetail(card, itemId);
    if (!detail) {
      return;
    }
    const fallback = detail.code || detail.text || detail.title || "";
    const current = getPreviewKeyPointDetailOverride(draft, itemId) || fallback;
    const values = await requestPreviewEditValues({
      title: "Edit Key Point Detail",
      subtitle: humanizeTopic(card.topic),
      fields: [
        {
          id: "text",
          label: "Detail text",
          prompt: "Edit detail text:",
          value: current,
          multiline: true,
          rows: detail.code ? 9 : 7,
          kind: detail.code ? "code" : "text",
        },
      ],
    });
    if (!values) {
      return;
    }
    const trimmed = String(values.text || "").trim();
    pushPreviewHistorySnapshot(`Edit key point detail in "${humanizeTopic(card.topic)}"`);
    if (!trimmed) {
      delete overrides.keyPointDetails[itemId];
    } else {
      overrides.keyPointDetails[itemId] = trimmed;
    }
    renderPreview();
    return;
  }

  if (itemType === "aiExample") {
    const item = usefulAIExamples(card).find((entry) => entry.id === itemId);
    if (!item) {
      return;
    }
    const current = getPreviewAIExampleOverride(draft, itemId, item);
    const values = await requestPreviewEditValues({
      title: "Edit Example",
      subtitle: humanizeTopic(card.topic),
      fields: [
        {
          id: "title",
          label: "Example title",
          prompt: "Edit example title:",
          value: current.title || "",
        },
        {
          id: "code",
          label: "Example code",
          prompt: "Edit example code:",
          value: current.code || "",
          multiline: true,
          rows: 11,
          kind: "code",
        },
        {
          id: "why",
          label: "Explanation",
          prompt: "Edit explanation:",
          value: current.why || "",
          multiline: true,
          rows: 6,
        },
      ],
    });
    if (!values) {
      return;
    }
    pushPreviewHistorySnapshot(`Edit example in "${humanizeTopic(card.topic)}"`);
    overrides.aiExamples[itemId] = {
      title: String(values.title || "").trim(),
      code: String(values.code || ""),
      why: String(values.why || "").trim(),
    };
    renderPreview();
    return;
  }

  if (itemType === "sourceItem") {
    const sourceItem = findSourceItem(card, itemId);
    if (!sourceItem) {
      return;
    }
    const currentOverride = getPreviewSourceOverride(draft, itemId, sourceItem.header);
    const headerDefault = currentOverride?.header || sourceItem.header;
    const bodyDefault = currentOverride?.body || sourceItemToEditableText(sourceItem);
    const values = await requestPreviewEditValues({
      title: "Edit Snippet",
      subtitle: humanizeTopic(card.topic),
      fields: [
        {
          id: "header",
          label: "Snippet title",
          prompt: "Edit snippet title:",
          value: headerDefault,
        },
        {
          id: "body",
          label: "Snippet content",
          prompt: "Edit snippet content:",
          value: bodyDefault,
          multiline: true,
          rows: 12,
          kind: "code",
        },
      ],
    });
    if (!values) {
      return;
    }
    pushPreviewHistorySnapshot(`Edit snippet in "${humanizeTopic(card.topic)}"`);
    overrides.sources[itemId] = {
      header: String(values.header || "").trim(),
      body: String(values.body || ""),
    };
    renderPreview();
  }
}

function findKeyPointDetail(card, detailId) {
  for (const group of keyPointGroups(card)) {
    const detail = group.details.find((entry) => entry.id === detailId);
    if (detail) {
      return detail;
    }
  }
  return null;
}

function findSourceItem(card, itemId) {
  const split = getSourceSplit(card);
  return [...split.recommended, ...split.additional].find((item) => item.id === itemId) || null;
}

function sourceItemToEditableText(sourceItem) {
  const lines = [];
  if (sourceItem.sourceType === "exam") {
    lines.push(sourceItem.item.question || "");
    lines.push(sourceItem.item.code_context || "");
    Object.entries(sourceItem.item.options || {}).forEach(([key, value]) => {
      lines.push(`${String(key).toUpperCase()}: ${value}`);
    });
    if (sourceItem.item.correct) {
      lines.push(`Correct: ${sourceItem.item.correct}`);
    }
    lines.push(sourceItem.item.explanation || "");
  } else if (sourceItem.sourceType === "lecture") {
    lines.push(sourceItem.item.explanation || "");
    lines.push(sourceItem.item.question || "");
    lines.push(sourceItem.item.code_examples?.map((example) => example.code || "").join("\n\n") || "");
  } else {
    lines.push(sourceItem.item.source || "");
    lines.push((sourceItem.item.outputs || []).join("\n"));
  }
  return lines.filter((line) => String(line || "").trim()).join("\n");
}

function humanizeItemType(itemType) {
  if (itemType === "aiQuestion") {
    return "common exam question";
  }
  if (itemType === "keyPoint") {
    return "key point";
  }
  if (itemType === "keyPointDetail") {
    return "key point detail";
  }
  if (itemType === "aiExample") {
    return "example";
  }
  return "snippet";
}

bindPreviewEditingEvents();

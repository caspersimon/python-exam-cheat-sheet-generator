function bindPreviewEditingEvents() {
  if (!refs.previewView) {
    return;
  }
  refs.previewView.addEventListener("click", handlePreviewEditingClick);
}

function handlePreviewEditingClick(event) {
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
      deleteItemBtn.dataset.cardId || "",
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
      editItemBtn.dataset.cardId || "",
      editItemBtn.dataset.itemType || "",
      editItemBtn.dataset.itemId || "",
      editItemBtn.dataset.section || ""
    );
  }
}

function getAcceptedCardContext(cardId) {
  const card = state.cards.find((entry) => entry.id === cardId);
  const decision = state.decisions[cardId];
  if (!card || !decision || decision.status !== "accepted" || !decision.selection) {
    return null;
  }
  return { card, selection: decision.selection };
}

function deletePreviewCard(cardId) {
  if (!cardId) {
    return;
  }
  const context = getAcceptedCardContext(cardId);
  if (!context) {
    return;
  }
  const confirmed = window.confirm(`Remove "${humanizeTopic(context.card.topic)}" from the cheat sheet preview?`);
  if (!confirmed) {
    return;
  }

  const previousDecision = deepClone(state.decisions[cardId]);
  const previousOrder = [...state.acceptedOrder];
  state.history.push({ cardId, previousDecision, previousOrder });
  pushPreviewHistorySnapshot(`Remove card "${humanizeTopic(context.card.topic)}"`);

  state.decisions[cardId] = { status: "rejected" };
  state.acceptedOrder = state.acceptedOrder.filter((id) => id !== cardId);
  delete state.previewCards[cardId];
  renderAll();
}

function togglePreviewCardLock(cardId) {
  if (!cardId) {
    return;
  }
  const context = getAcceptedCardContext(cardId);
  const layout = state.previewCards[cardId];
  if (!context || !layout) {
    return;
  }

  const nextLocked = !Boolean(layout.locked);
  pushPreviewHistorySnapshot(`${nextLocked ? "Lock" : "Unlock"} card "${humanizeTopic(context.card.topic)}"`);
  layout.locked = nextLocked;
  renderPreview();
}

function deletePreviewItem(cardId, itemType, itemId, section) {
  const resolvedCardId = cardId;
  if (!resolvedCardId || !itemId) {
    return;
  }
  const context = getAcceptedCardContext(resolvedCardId);
  if (!context) {
    return;
  }

  const { selection } = context;
  ensureSelectionOverrides(selection);
  pushPreviewHistorySnapshot(`Delete ${humanizeItemType(itemType)} in "${humanizeTopic(context.card.topic)}"`);

  if (itemType === "keyPoint") {
    selection.selected.keyPoints = (selection.selected.keyPoints || []).filter(
      (id) => id !== itemId && !id.startsWith(`${itemId}-d`)
    );
    delete selection.overrides.keyPoints[itemId];
    Object.keys(selection.overrides.keyPointDetails).forEach((detailId) => {
      if (detailId.startsWith(`${itemId}-d`)) {
        delete selection.overrides.keyPointDetails[detailId];
      }
    });
  } else if (itemType === "keyPointDetail") {
    selection.selected.keyPoints = (selection.selected.keyPoints || []).filter((id) => id !== itemId);
    delete selection.overrides.keyPointDetails[itemId];
  } else if (itemType === "aiExample") {
    selection.selected.aiExamples = (selection.selected.aiExamples || []).filter((id) => id !== itemId);
    delete selection.overrides.aiExamples[itemId];
  } else if (itemType === "sourceItem") {
    selection.selected.recommended = (selection.selected.recommended || []).filter((id) => id !== itemId);
    selection.selected.additional = (selection.selected.additional || []).filter((id) => id !== itemId);
    delete selection.overrides.sources[itemId];
  }

  renderPreview();
}

async function editPreviewItem(cardId, itemType, itemId, section) {
  const resolvedCardId = cardId;
  if (!resolvedCardId || !itemId) {
    return;
  }
  const context = getAcceptedCardContext(resolvedCardId);
  if (!context) {
    return;
  }

  const { card, selection } = context;
  const overrides = ensureSelectionOverrides(selection);

  if (itemType === "keyPoint") {
    const group = keyPointGroups(card).find((entry) => entry.id === itemId);
    if (!group) {
      return;
    }
    const current = getPreviewKeyPointOverride(selection, itemId, group.text);
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
      deletePreviewItem(resolvedCardId, itemType, itemId, section);
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
    const current = getPreviewKeyPointDetailOverride(selection, itemId) || fallback;
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
    const current = getPreviewAIExampleOverride(selection, itemId, item);
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
    const currentOverride = getPreviewSourceOverride(selection, itemId, sourceItem.header);
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

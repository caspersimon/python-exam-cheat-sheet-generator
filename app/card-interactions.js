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

  const resetIntroTrigger = event.target.closest("[data-role='reset-splash']");
  if (resetIntroTrigger) {
    event.preventDefault();
    resetSplashIntro();
    return;
  }

  const resetProgressTrigger = event.target.closest("[data-role='reset-progress']");
  if (resetProgressTrigger) {
    event.preventDefault();
    resetAppProgress();
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
  popover.style.setProperty("--popover-shift-y", "0px");

  window.requestAnimationFrame(() => {
    const rect = popover.getBoundingClientRect();
    const viewportPadding = 8;
    const maxRight = window.innerWidth - viewportPadding;
    const maxBottom = window.innerHeight - viewportPadding;
    let shiftX = 0;
    let shiftY = 0;

    if (rect.left < viewportPadding) {
      shiftX += viewportPadding - rect.left;
    }
    if (rect.right > maxRight) {
      shiftX -= rect.right - maxRight;
    }
    if (rect.bottom > maxBottom) {
      shiftY -= rect.bottom - maxBottom;
    }
    if (rect.top + shiftY < viewportPadding) {
      shiftY += viewportPadding - (rect.top + shiftY);
    }

    popover.style.setProperty("--popover-shift-x", `${Math.round(shiftX)}px`);
    popover.style.setProperty("--popover-shift-y", `${Math.round(shiftY)}px`);
  });
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
  schedulePersistState();
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

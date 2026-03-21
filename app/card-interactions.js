function isInteractiveNode(node) {
  return Boolean(node.closest("input,button,label,select,textarea,a,pre,code"));
}

function getCardById(cardId) {
  return state.cards.find((entry) => entry.id === cardId) || null;
}

function handleCardInputChange(event) {
  const input = event.target;
  const role = input.dataset.role;
  const cardId = input.dataset.cardId || "";
  const card = cardId ? getCardById(cardId) : null;

  if (!card) {
    return;
  }

  const draft = ensureDraft(card);
  const section = input.dataset.section || "";

  if (role === "section-toggle") {
    draft.sections[section] = Boolean(input.checked);
    renderAll();
    return;
  }

  if (role === "item-toggle") {
    const itemId = input.dataset.itemId || "";
    const key = sectionToSelectionKey(section);
    if (!key || !itemId) {
      return;
    }

    const next = new Set(draft.selected[key] || []);
    if (input.checked) {
      next.add(itemId);
      draft.sections[section] = true;
    } else {
      next.delete(itemId);
    }
    draft.selected[key] = [...next];
    renderAll();
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

  const openTopicTrigger = event.target.closest("[data-role='open-topic']");
  if (openTopicTrigger) {
    event.preventDefault();
    const cardId = openTopicTrigger.dataset.cardId || "";
    const week = Number(openTopicTrigger.dataset.week || 0);
    setActiveTopic(cardId, week);
    closeTopicSidebar();
    renderAll();
    return;
  }

  const toggleWeekTrigger = event.target.closest("[data-role='toggle-week']");
  if (toggleWeekTrigger) {
    event.preventDefault();
    const week = Number(toggleWeekTrigger.dataset.week || 0);
    if (Number.isFinite(week) && week > 0) {
      toggleWeekExpanded(week);
      renderSwipe();
      schedulePersistState();
    }
    return;
  }

  const closeSidebarTrigger = event.target.closest("[data-role='close-topic-sidebar']");
  if (closeSidebarTrigger) {
    event.preventDefault();
    closeTopicSidebar();
    renderSwipe();
    schedulePersistState();
    return;
  }

  const sectionSelectAllTrigger = event.target.closest("[data-role='select-all-section']");
  if (sectionSelectAllTrigger) {
    event.preventDefault();
    const cardId = sectionSelectAllTrigger.dataset.cardId || "";
    const section = sectionSelectAllTrigger.dataset.section || "";
    selectAllSectionItems(cardId, section);
    return;
  }

  const clearSectionTrigger = event.target.closest("[data-role='clear-section']");
  if (clearSectionTrigger) {
    event.preventDefault();
    const cardId = clearSectionTrigger.dataset.cardId || "";
    const section = clearSectionTrigger.dataset.section || "";
    clearSectionItems(cardId, section);
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
}

function handleCardMouseOver(event) {
  const infoChip = event.target.closest(".info-chip");
  if (!infoChip || !refs.cardHost.contains(infoChip)) {
    return;
  }
  positionInfoPopover(infoChip);
}

function selectAllSectionItems(cardId, section) {
  const card = getCardById(cardId);
  if (!card) {
    return;
  }
  const draft = ensureDraft(card);
  const key = sectionToSelectionKey(section);
  if (!key) {
    return;
  }

  const allIds = getSectionSelectableIds(card, section);
  draft.sections[section] = true;
  draft.selected[key] = [...new Set(allIds)];
  renderAll();
}

function clearSectionItems(cardId, section) {
  const card = getCardById(cardId);
  if (!card) {
    return;
  }
  const draft = ensureDraft(card);
  const key = sectionToSelectionKey(section);
  if (!key) {
    return;
  }

  draft.selected[key] = [];
  if (key === "keyPoints") {
    const overrides = draft.overrides || {};
    overrides.keyPoints = {};
    overrides.keyPointDetails = {};
    draft.overrides = overrides;
  } else if (key === "aiExamples") {
    draft.overrides.aiExamples = {};
  } else {
    draft.overrides.sources = {};
  }
  renderAll();
}

function getSectionSelectableIds(card, section) {
  if (section === "keyPoints") {
    return keyPointSelectableIds(card);
  }
  if (section === "aiExamples") {
    return usefulAIExamples(card).map((item) => item.id);
  }
  if (section === "recommended" || section === "additional") {
    return getSourceSplit(card)[section].map((item) => item.id);
  }
  return [];
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
  refs.selectionShell?.querySelectorAll(".info-chip.open").forEach((chip) => chip.classList.remove("open"));
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

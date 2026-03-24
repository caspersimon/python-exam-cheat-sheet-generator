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
  Object.values(drawerMap).forEach((drawer) => drawer?.classList.add("hidden"));
  refs.drawerBackdrop.classList.add("hidden");
  state.openDrawer = "";
}

function openTopicSidebar() {
  state.navigation.mobileSidebarOpen = true;
  renderSwipe();
}

function closeTopicSidebar() {
  state.navigation.mobileSidebarOpen = false;
  renderSwipe();
}

function setView(viewName) {
  state.view = viewName;
  refs.swipeView.classList.toggle("active", viewName === "swipe");
  refs.previewView.classList.toggle("active", viewName === "preview");
  syncViewButtons();
  closeDrawers();
  if (viewName === "preview") {
    closeTopicSidebar();
  }
  renderPreview();
}

function renderAll() {
  renderSwipe();
  renderPreview();
}

function syncViewButtons() {
  refs.goToSwipeBtn?.classList.toggle("is-active", state.view === "swipe");
  refs.goToPreviewBtn?.classList.toggle("is-active", state.view === "preview");
  refs.swipeHeaderActions?.classList.toggle("hidden", state.view !== "swipe");
  refs.previewHeaderActions?.classList.toggle("hidden", state.view !== "preview");
}

function getFilteredDeck() {
  return state.cards.filter(cardMatchesFilters);
}

function sortTopicCards(cards) {
  return [...cards].sort((a, b) => {
    const orderDelta = Number(a?.topic_meta?.topic_order || 0) - Number(b?.topic_meta?.topic_order || 0);
    if (orderDelta !== 0) {
      return orderDelta;
    }
    return humanizeTopic(a.topic).localeCompare(humanizeTopic(b.topic));
  });
}

function cardMatchesFilters(card) {
  if (state.filters.weeks.size > 0) {
    const cardWeeks = Array.isArray(card.weeks) ? card.weeks : [];
    if (!cardWeeks.some((week) => state.filters.weeks.has(week))) {
      return false;
    }
  }

  const search = state.filters.search;
  if (!search) {
    return true;
  }

  const haystack = [
    card.topic,
    card.parent_topic,
    card.summary,
    card.search_text,
    ...getExamCardSections(card).flatMap((section) => section.snippets.map((snippet) => snippet.title)),
  ]
    .join(" ")
    .toLowerCase();

  return haystack.includes(search);
}

function getFilteredParentBundles() {
  const filteredCards = sortTopicCards(getFilteredDeck());
  const byParent = new Map();

  filteredCards.forEach((card) => {
    if (!byParent.has(card.parent_topic_id)) {
      const source = state.parentTopics.find((parentTopic) => parentTopic.id === card.parent_topic_id);
      byParent.set(card.parent_topic_id, {
        id: card.parent_topic_id,
        title: source?.title || card.parent_topic,
        summary: source?.summary || "",
        cards: [],
      });
    }
    byParent.get(card.parent_topic_id).cards.push(card);
  });

  return state.parentTopics
    .map((parentTopic) => byParent.get(parentTopic.id))
    .filter((parentTopic) => parentTopic && parentTopic.cards.length > 0);
}

function ensureExplorerNavigation(filteredParents = getFilteredParentBundles()) {
  if (!filteredParents.length) {
    state.navigation.activeParentId = "";
    state.navigation.activeTopicId = "";
    return null;
  }

  if (!state.navigation || typeof state.navigation !== "object") {
    state.navigation = buildDefaultNavigationState();
  }

  filteredParents.forEach((parentTopic, index) => {
    if (typeof state.navigation.expandedParents[parentTopic.id] !== "boolean") {
      state.navigation.expandedParents[parentTopic.id] = index === 0;
    }
  });

  const visibleCardIds = new Set(filteredParents.flatMap((parentTopic) => parentTopic.cards.map((card) => card.id)));
  const currentTopicId = String(state.navigation.activeTopicId || "").trim();
  const activeTopicId = visibleCardIds.has(currentTopicId) ? currentTopicId : filteredParents[0].cards[0].id;
  const activeParent =
    filteredParents.find((parentTopic) => parentTopic.cards.some((card) => card.id === activeTopicId)) || filteredParents[0];
  const activeCard = activeParent.cards.find((card) => card.id === activeTopicId) || activeParent.cards[0];

  state.navigation.activeTopicId = activeCard.id;
  state.navigation.activeParentId = activeParent.id;
  state.navigation.expandedParents[activeParent.id] = true;

  return { parentTopic: activeParent, card: activeCard };
}

function setActiveTopic(cardId, parentId) {
  if (!cardId) {
    return;
  }
  state.navigation.activeTopicId = cardId;
  state.navigation.activeParentId = parentId || state.navigation.activeParentId;
  if (parentId) {
    state.navigation.expandedParents[parentId] = true;
  }
  state.navigation.mobileSidebarOpen = false;
  renderSwipe();
  schedulePersistState();
}

function toggleParentExpanded(parentId) {
  if (!parentId) {
    return;
  }
  state.navigation.expandedParents[parentId] = !Boolean(state.navigation.expandedParents[parentId]);
  renderSwipe();
  schedulePersistState();
}

function getParentSelectionSummary(parentTopic) {
  const cards = Array.isArray(parentTopic?.cards) ? parentTopic.cards : [];
  const selectedTopics = cards.filter((card) => getSelectionCounts(card).total > 0).length;
  const selectedItems = cards.reduce((sum, card) => sum + getSelectionCounts(card).total, 0);
  return {
    topics: selectedTopics,
    items: selectedItems,
  };
}

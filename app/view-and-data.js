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

function getFilteredDeck() {
  return state.cards.filter(cardMatchesFilters);
}

function cardMatchesFilters(card) {
  const search = state.filters.search;

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
}

function getCanonicalWeekOrder() {
  if (Array.isArray(state.deckGroups) && state.deckGroups.length > 0) {
    const weeks = state.deckGroups
      .map((group) => Number(group?.week))
      .filter((week, index, all) => Number.isFinite(week) && !all.slice(0, index).includes(week));
    if (weeks.length > 0) {
      return weeks;
    }
  }
  return Array.isArray(CANONICAL_WEEK_ORDER) ? [...CANONICAL_WEEK_ORDER] : [1, 2, 3, 4, 5, 6];
}

function getWeekCardsForWeek(week, cards = getFilteredDeck()) {
  const weekNumber = Number(week);
  return cards.filter((card) => {
    const weeks = Array.isArray(card.weeks) ? card.weeks : [];
    return weeks.includes(weekNumber);
  });
}

function getFilteredWeekBundles() {
  const cardLookup = new Map(state.cards.map((card) => [card.id, card]));
  const deckGroups = Array.isArray(state.deckGroups) && state.deckGroups.length > 0
    ? state.deckGroups
    : getCanonicalWeekOrder().map((week) => ({
        id: `week-${week}`,
        week,
        title: `Week ${week}`,
        topic_refs: getWeekCardsForWeek(week, state.cards).map((card) => ({ card_id: card.id })),
      }));

  return deckGroups
    .map((group) => {
      const refsForGroup = Array.isArray(group?.topic_refs) ? group.topic_refs : [];
      const seen = new Set();
      const cards = [];

      refsForGroup.forEach((ref) => {
        const cardId = String(ref?.card_id || "").trim();
        const card = cardLookup.get(cardId);
        if (!card || seen.has(card.id) || !cardMatchesFilters(card)) {
          return;
        }
        seen.add(card.id);
        cards.push(card);
      });

      return {
        id: String(group?.id || `week-${group?.week}`),
        title: String(group?.title || `Week ${group?.week}`),
        week: Number(group?.week),
        cards,
      };
    })
    .filter((group) => Number.isFinite(group.week));
}

function ensureExplorerNavigation(filteredWeekBundles = getFilteredWeekBundles()) {
  const visibleBundles = filteredWeekBundles.filter((bundle) => Array.isArray(bundle.cards) && bundle.cards.length > 0);
  if (!visibleBundles.length) {
    state.navigation.activeTopicId = "";
    state.navigation.activeWeek = CANONICAL_WEEK_ORDER[0];
    return null;
  }

  if (!state.navigation || typeof state.navigation !== "object") {
    state.navigation = buildDefaultNavigationState();
  }

  const visibleCardIds = new Set(visibleBundles.flatMap((bundle) => bundle.cards.map((card) => card.id)));
  const currentTopicId = String(state.navigation.activeTopicId || "").trim();
  const activeTopicId = visibleCardIds.has(currentTopicId) ? currentTopicId : visibleBundles[0].cards[0].id;
  const activeBundle =
    visibleBundles.find((bundle) => bundle.cards.some((card) => card.id === activeTopicId)) || visibleBundles[0];

  state.navigation.activeTopicId = activeTopicId;
  state.navigation.activeWeek = activeBundle.week;

  if (!state.navigation.expandedWeeks || typeof state.navigation.expandedWeeks !== "object") {
    state.navigation.expandedWeeks = Object.fromEntries(CANONICAL_WEEK_ORDER.map((week) => [String(week), true]));
  }
  if (!Object.values(state.navigation.expandedWeeks).some(Boolean)) {
    state.navigation.expandedWeeks[String(activeBundle.week)] = true;
  }
  if (!state.navigation.expandedWeeks[String(activeBundle.week)]) {
    state.navigation.expandedWeeks[String(activeBundle.week)] = true;
  }

  return {
    bundle: activeBundle,
    card: activeBundle.cards.find((card) => card.id === activeTopicId) || activeBundle.cards[0],
  };
}

function setActiveTopic(cardId, week) {
  if (!cardId) {
    return;
  }
  state.navigation.activeTopicId = cardId;
  if (Number.isFinite(Number(week))) {
    state.navigation.activeWeek = Number(week);
    state.navigation.expandedWeeks[String(week)] = true;
  }
  state.navigation.mobileSidebarOpen = false;
  renderSwipe();
  schedulePersistState();
}

function toggleWeekExpanded(week) {
  const key = String(week);
  state.navigation.expandedWeeks[key] = !Boolean(state.navigation.expandedWeeks[key]);
  renderSwipe();
  schedulePersistState();
}

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

function getCardWeek(card) {
  const explicitWeek = Number(card?.topic_meta?.week);
  if (Number.isFinite(explicitWeek) && explicitWeek > 0) {
    return explicitWeek;
  }
  const fallbackWeek = Number((card?.weeks || [])[0]);
  return Number.isFinite(fallbackWeek) && fallbackWeek > 0 ? fallbackWeek : CANONICAL_WEEK_ORDER[0];
}

function sortTopicCards(cards) {
  return [...cards].sort((a, b) => {
    const orderDelta = Number(a?.topic_meta?.topic_order || 0) - Number(b?.topic_meta?.topic_order || 0);
    if (orderDelta !== 0) {
      return orderDelta;
    }
    const hitDelta = (b.exam_stats?.total_hits || 0) - (a.exam_stats?.total_hits || 0);
    if (hitDelta !== 0) {
      return hitDelta;
    }
    return humanizeTopic(a.topic).localeCompare(humanizeTopic(b.topic));
  });
}

function cardMatchesFilters(card) {
  const search = state.filters.search;
  const week = getCardWeek(card);

  if (state.filters.onlyExam && card.exam_stats.total_hits === 0) {
    return false;
  }

  if (card.exam_stats.total_hits < state.filters.minHits) {
    return false;
  }

  if (state.filters.weeks.size > 0 && !state.filters.weeks.has(week)) {
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
    if (weeks.length) {
      return weeks;
    }
  }
  return Array.isArray(CANONICAL_WEEK_ORDER) ? [...CANONICAL_WEEK_ORDER] : [1, 2, 3, 4, 5, 6];
}

function getWeekCardsForWeek(week, cards = getFilteredDeck()) {
  const weekNumber = Number(week);
  return sortTopicCards(cards.filter((card) => getCardWeek(card) === weekNumber));
}

function getFilteredWeekBundles() {
  const filteredCards = getFilteredDeck();
  const filteredCardById = new Map(filteredCards.map((card) => [card.id, card]));
  const sourceBundles = Array.isArray(state.deckGroups) && state.deckGroups.length
    ? state.deckGroups
    : getCanonicalWeekOrder().map((week) => ({
        id: `week-${week}`,
        week,
        title: `Week ${week}`,
        topic_groups: [
          {
            id: `week-${week}-topics`,
            title: "Topics",
            shortTitle: "Topics",
            is_default: true,
            topic_refs: getWeekCardsForWeek(week, filteredCards).map((card) => ({
              card_id: card.id,
              topic: card.topic,
              exam_hits: card.exam_stats?.total_hits || 0,
              topic_order: card.topic_meta?.topic_order || 0,
            })),
          },
        ],
      }));

  return sourceBundles
    .map((bundle) => {
      const groups = (bundle.topic_groups || [])
        .map((group) => {
          const cards = sortTopicCards(
            (group.topic_refs || [])
              .map((ref) => filteredCardById.get(ref.card_id))
              .filter(Boolean)
          );

          return {
            id: group.id,
            title: group.title,
            shortTitle: group.shortTitle || group.title,
            isDefault: Boolean(group.is_default),
            cards,
          };
        })
        .filter((group) => group.cards.length > 0);

      return {
        id: bundle.id,
        title: bundle.title,
        week: Number(bundle.week),
        groups,
        cards: groups.flatMap((group) => group.cards),
      };
    })
    .filter((bundle) => Number.isFinite(bundle.week) && bundle.cards.length > 0);
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
  const activeGroup =
    activeBundle.groups?.find((group) => group.cards.some((card) => card.id === activeTopicId)) || activeBundle.groups?.[0] || null;

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
    group: activeGroup,
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

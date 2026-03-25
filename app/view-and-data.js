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

function snippetMatchesFilters(snippet) {
  const selectedCoursePhases = state.filters.coursePhases;
  if (selectedCoursePhases.size > 0 && snippet.coursePhase && !selectedCoursePhases.has(snippet.coursePhase)) {
    return false;
  }

  const selectedRecurrenceLevels = state.filters.recurrenceLevels;
  if (selectedRecurrenceLevels.size > 0 && snippet.recurrenceLevel && !selectedRecurrenceLevels.has(snippet.recurrenceLevel)) {
    return false;
  }

  const search = state.filters.search;
  if (!search) {
    return true;
  }

  return snippet.searchText.includes(search);
}

function getFilteredTopics() {
  return state.topics
    .map((topic) => {
      const subtopics = topic.subtopics
        .map((subtopic) => ({
          ...subtopic,
          snippets: subtopic.snippets.filter(snippetMatchesFilters),
        }))
        .filter((subtopic) => subtopic.snippets.length > 0);

      if (!subtopics.length) {
        return null;
      }

      return {
        ...topic,
        subtopics,
      };
    })
    .filter(Boolean)
    .sort((a, b) => a.sortOrder - b.sortOrder || a.title.localeCompare(b.title));
}

function ensureExplorerNavigation(filteredTopics = getFilteredTopics()) {
  if (!filteredTopics.length) {
    state.navigation.activeTopicId = "";
    return null;
  }

  const visibleTopicIds = new Set(filteredTopics.map((topic) => topic.id));
  const activeTopicId = visibleTopicIds.has(state.navigation.activeTopicId) ? state.navigation.activeTopicId : filteredTopics[0].id;
  const activeTopic = filteredTopics.find((topic) => topic.id === activeTopicId) || filteredTopics[0];
  state.navigation.activeTopicId = activeTopic.id;
  return activeTopic;
}

function setActiveTopic(topicId) {
  if (!topicId) {
    return;
  }
  state.navigation.activeTopicId = topicId;
  state.navigation.mobileSidebarOpen = false;
  renderSwipe();
  schedulePersistState();
}

function getTopicSelectionSummary(topic) {
  const snippets = topic.subtopics.flatMap((subtopic) => subtopic.snippets);
  const selectedSnippets = snippets.filter((snippet) => getSelectionCounts(snippet).total > 0).length;
  const selectedPieces = snippets.reduce((sum, snippet) => sum + getSelectionCounts(snippet).total, 0);
  return {
    snippets: selectedSnippets,
    items: selectedPieces,
  };
}

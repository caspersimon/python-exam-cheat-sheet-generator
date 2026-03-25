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

function getPresetById(presetId) {
  return state.presets.find((preset) => preset.id === presetId) || null;
}

function getSelectedPreset() {
  return getPresetById(state.selectedPresetId);
}

function formatCompactNumber(value) {
  const number = Number(value || 0);
  if (!Number.isFinite(number) || number <= 0) {
    return "0";
  }
  return new Intl.NumberFormat(undefined).format(number);
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
  renderPresetSurfaces();
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

function renderPresetSurfaces() {
  if (refs.presetList) {
    refs.presetList.innerHTML = state.presets.length
      ? state.presets.map((preset) => renderPresetCard(preset, { compact: false })).join("")
      : `<div class="empty-state"><p>No presets found in the current database bundle.</p></div>`;
  }

  if (refs.splashPresetList) {
    refs.splashPresetList.innerHTML = state.presets.length
      ? state.presets.map((preset) => renderPresetCard(preset, { compact: true, splash: true })).join("")
      : "";
  }

  if (refs.activePresetName) {
    const selectedPreset = getSelectedPreset();
    refs.activePresetName.textContent = selectedPreset ? selectedPreset.title : "Custom";
  }
}

function renderPresetCard(preset, { compact = false, splash = false } = {}) {
  const isActive = state.selectedPresetId === preset.id;
  const actionLabel = splash ? "Use preset" : isActive ? "Reapply" : "Apply";
  const metaBits = [
    `${formatCompactNumber(preset.snippetCount)} snippets`,
    `${formatCompactNumber(preset.pieceCount)} pieces`,
    `${formatCompactNumber(preset.charCount)} chars`,
  ];
  return `
    <article class="preset-card${compact ? " is-compact" : ""}${isActive ? " is-active" : ""}">
      <div class="preset-card-copy">
        <div class="preset-card-headline">
          <h4>${escapeHtml(preset.title)}</h4>
          ${isActive ? `<span class="snippet-tag preset-tag-active">Current start</span>` : ""}
        </div>
        ${preset.summary ? `<p class="preset-card-summary">${renderInlineCode(preset.summary)}</p>` : ""}
        ${preset.targetUser ? `<p class="preset-card-target"><strong>Best for:</strong> ${renderInlineCode(preset.targetUser)}</p>` : ""}
        <div class="exam-snippet-meta">${metaBits.map((bit) => `<span class="snippet-tag">${escapeHtml(bit)}</span>`).join("")}</div>
        ${compact ? "" : preset.notes ? `<p class="muted">${renderInlineCode(preset.notes)}</p>` : ""}
      </div>
      <div class="preset-card-actions">
        <button type="button" class="solid-btn" data-role="apply-preset" data-preset-id="${escapeHtml(preset.id)}" data-preset-source="${
          splash ? "splash" : "drawer"
        }">${escapeHtml(actionLabel)}</button>
      </div>
    </article>
  `;
}

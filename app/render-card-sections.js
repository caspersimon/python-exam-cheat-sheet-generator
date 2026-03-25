function renderSwipe() {
  const filteredTopics = getFilteredTopics();
  const activeTopic = ensureExplorerNavigation(filteredTopics);
  const selectedTotals = getSelectedItemTotals();

  refs.acceptedCount.textContent = String(selectedTotals.snippets);
  refs.rejectedCount.textContent = String(selectedTotals.items);
  refs.remainingCount.textContent = String(filteredTopics.length);

  refs.progressText.textContent = [
    `${selectedTotals.snippets} snippets staged`,
    `${selectedTotals.items} pieces selected`,
    `${filteredTopics.length} topics visible`,
  ].join(" • ");

  refs.acceptedTopicsList.innerHTML = "";
  getSelectedPreviewEntries()
    .slice(0, 40)
    .forEach((entry) => {
      const li = document.createElement("li");
      li.textContent = `${entry.snippet.title} · ${entry.snippet.subtopicTitle}`;
      refs.acceptedTopicsList.appendChild(li);
    });

  if (!activeTopic) {
    refs.topicSidebar.innerHTML = "";
    refs.cardHost.innerHTML = `<div class="empty-state">
      <p><strong>No topics match the current filters.</strong></p>
      <p>Adjust the course-phase, recurrence, or search filters to keep exploring.</p>
    </div>`;
    refs.selectionShell?.classList.remove("topic-sidebar-open");
    refs.topicSidebarBackdrop?.classList.add("hidden");
    return;
  }

  refs.topicSidebar.innerHTML = renderTopicSidebar(filteredTopics, activeTopic.id);
  refs.cardHost.innerHTML = renderTopicDetail(activeTopic);
  refs.selectionShell?.classList.toggle("topic-sidebar-open", Boolean(state.navigation.mobileSidebarOpen));
  refs.topicSidebarBackdrop?.classList.toggle("hidden", !state.navigation.mobileSidebarOpen);
}

function renderTopicSidebar(topics, activeTopicId) {
  return `
    <div class="topic-sidebar-head">
      <div>
        <h3>Topic Map</h3>
        <p class="muted">Browse by topic, then scan subtopics and hand-picked snippets beneath them.</p>
      </div>
      <button class="ghost-btn icon-btn topic-sidebar-close mobile-only-btn" type="button" data-role="close-topic-sidebar" aria-label="Close topics">
        <span aria-hidden="true">&times;</span>
      </button>
    </div>
    <div class="topic-sidebar-scroll">
      ${topics.map((topic) => renderSidebarTopicButton(topic, activeTopicId)).join("")}
    </div>
  `;
}

function renderSidebarTopicButton(topic, activeTopicId) {
  const summary = getTopicSelectionSummary(topic);
  const isActive = activeTopicId === topic.id;
  return `
    <button
      class="topic-nav-item ${isActive ? "is-active" : ""}"
      type="button"
      data-role="open-topic"
      data-topic-id="${escapeHtml(topic.id)}"
      data-parent-theme="${escapeHtml(getParentTopicThemeId(topic))}"
    >
      <span class="topic-nav-title">${escapeHtml(topic.title)}</span>
      <span class="topic-nav-meta">${escapeHtml(`${topic.subtopics.length} subtopics • ${summary.snippets} selected`)}</span>
    </button>
  `;
}

function renderTopicDetail(topic) {
  const selectedPieces = topic.subtopics
    .flatMap((subtopic) => subtopic.snippets)
    .reduce((sum, snippet) => sum + getSelectionCounts(snippet).total, 0);

  return `
    <article class="topic-detail-card exam-topic-detail" data-card-id="${escapeHtml(topic.id)}" data-parent-theme="${escapeHtml(
      getParentTopicThemeId(topic)
    )}">
      <header class="topic-detail-header">
        <div class="topic-detail-intro">
          <div class="topic-detail-course-context">
            <span class="topic-course-chip topic-course-chip-parent">${escapeHtml(topic.title)}</span>
          </div>
          <p class="topic-detail-kicker">${escapeHtml(
            `${topic.subtopics.length} subtopics · ${topic.snippetCount} snippets · ${selectedPieces} selected pieces`
          )}</p>
          <div class="topic-detail-title-row">
            <h3>${escapeHtml(topic.title)}</h3>
          </div>
          ${topic.description ? `<p class="topic-detail-summary">${renderInlineCode(topic.description)}</p>` : ""}
          ${renderSubtopicOverview(topic.subtopics)}
        </div>
        <aside class="topic-detail-aside">
          <div class="topic-stat-list" aria-label="Topic stats">
            <article class="topic-stat-card">
              <span>Subtopics</span>
              <strong>${escapeHtml(String(topic.subtopics.length))}</strong>
            </article>
            <article class="topic-stat-card">
              <span>Snippets</span>
              <strong>${escapeHtml(String(topic.snippetCount || 0))}</strong>
            </article>
            <article class="topic-stat-card">
              <span>Selected Pieces</span>
              <strong>${escapeHtml(String(selectedPieces))}</strong>
            </article>
          </div>
          <section class="topic-context-panel topic-focus-panel">
            <h4>Selection guidance</h4>
            <p>Keep the densest snippet pieces first, then only add clarifiers that truly earn space on the sheet.</p>
          </section>
        </aside>
      </header>
      ${topic.subtopics.map((subtopic) => renderSubtopicSection(subtopic)).join("")}
      <footer class="topic-detail-footer">
        <button type="button" class="text-link-btn" data-role="reset-splash">Reset intro</button>
        <button type="button" class="text-link-btn danger-link-btn" data-role="reset-progress">Reset progress</button>
      </footer>
    </article>
  `;
}

const CHECK_ICON = `<svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M2.5 7l3.5 3.5L11.5 3" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
const X_ICON = `<svg width="13" height="13" viewBox="0 0 13 13" fill="none" aria-hidden="true"><path d="M2.5 2.5l8 8M10.5 2.5l-8 8" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>`;

function renderSubtopicSection(subtopic) {
  const selectedCount = subtopic.snippets.reduce((sum, snippet) => sum + getSelectionCounts(snippet).total, 0);
  const totalCount = getSubtopicSelectablePieceIds(subtopic).length;
  const allSelected = totalCount > 0 && selectedCount === totalCount;
  const toggleRole = allSelected ? "clear-subtopic" : "select-all-subtopic";
  const toggleTitle = allSelected ? "Clear all" : "Select all";
  const toggleIcon = allSelected ? X_ICON : CHECK_ICON;
  return renderSubtopicRailGroup(
    subtopic,
    `
      <div class="topic-section-header">
        <div class="topic-section-heading">
          <h4>${escapeHtml(subtopic.title)}</h4>
          ${subtopic.description ? `<p class="muted">${renderInlineCode(subtopic.description)}</p>` : ""}
        </div>
        <div class="topic-section-actions">
          <span class="topic-section-count">${escapeHtml(`${selectedCount}/${totalCount}`)}</span>
          <button type="button" class="ghost-btn icon-btn snippet-toggle-btn" data-role="${toggleRole}" data-subtopic-id="${escapeHtml(subtopic.id)}" title="${toggleTitle}" aria-label="${toggleTitle}">${toggleIcon}</button>
        </div>
      </div>
      <div class="topic-rail">
        ${subtopic.snippets.map((snippet) => renderSnippetCard(snippet)).join("")}
      </div>
    `
  );
}

function renderSnippetCard(snippet) {
  const draft = ensureDraft(snippet);
  const selectedCount = getSelectionCounts(snippet, draft).total;
  const totalPieces = getSnippetSelectablePieceIds(snippet).length;
  const allSelected = totalPieces > 0 && selectedCount === totalPieces;
  const toggleRole = allSelected ? "clear-snippet" : "select-all-snippet";
  const toggleTitle = allSelected ? "Clear" : "Select all";
  const toggleIcon = allSelected ? X_ICON : CHECK_ICON;
  const metadataBits = [
    snippet.recurrenceLevel ? humanizeTopic(snippet.recurrenceLevel) : "",
    snippet.coursePhase ? humanizeTopic(snippet.coursePhase) : "",
    snippet.questionRefCount ? `${snippet.questionRefCount} q refs` : "",
  ].filter(Boolean);

  return `
    <article class="rail-card exam-snippet-card" data-snippet-id="${escapeHtml(snippet.id)}" data-parent-theme="${escapeHtml(
      snippet.topicSlug
    )}">
      <div class="exam-snippet-head">
        <div class="exam-snippet-copy">
          ${metadataBits.length ? `<div class="exam-snippet-meta">${metadataBits.map((bit) => `<span class="snippet-tag">${escapeHtml(bit)}</span>`).join("")}</div>` : ""}
          <h5>${renderInlineCode(snippet.title)}</h5>
          ${snippet.summary ? `<p class="muted">${renderInlineCode(snippet.summary)}</p>` : ""}
          ${snippet.why ? `<p class="muted">${renderInlineCode(snippet.why)}</p>` : ""}
          <p class="snippet-piece-count">${escapeHtml(`${selectedCount}/${totalPieces} pieces`)}</p>
        </div>
        <button type="button" class="ghost-btn icon-btn snippet-toggle-btn" data-role="${toggleRole}" data-snippet-id="${escapeHtml(snippet.id)}" title="${toggleTitle}" aria-label="${toggleTitle}">${toggleIcon}</button>
      </div>
      <div class="rail-card-body">
        ${snippet.pieces.map((piece) => renderPieceSelector(snippet, draft, piece)).join("")}
      </div>
    </article>
  `;
}

function renderPieceSelector(snippet, draft, piece) {
  const selectedSet = new Set(draft.selected.pieces || []);
  const checked = selectedSet.has(piece.id);
  const effectivePiece = getPieceOverride(draft, piece);
  const presentation = getPiecePresentation(effectivePiece);
  const emphasis = presentation?.emphasis || "";
  return `
    <div class="detail-toggle-row exam-piece-row${emphasis ? ` is-${escapeHtml(emphasis)}` : ""}"${
      emphasis ? ` data-piece-emphasis="${escapeHtml(emphasis)}"` : ""
    }>
      <label class="item-select">
        <input
          type="checkbox"
          data-role="item-toggle"
          data-snippet-id="${escapeHtml(snippet.id)}"
          data-piece-id="${escapeHtml(piece.id)}"
          ${checked ? "checked" : ""}
        />
        <span class="exam-piece-heading">
          ${renderPiecePresentationBadge(presentation)}
          <strong>${renderInlineCode(effectivePiece.title || piece.title)}</strong>
        </span>
      </label>
      <div class="rail-card-body exam-piece-preview">
        ${renderPieceBody(effectivePiece)}
      </div>
    </div>
  `;
}

function renderPiecePresentationBadge(presentation) {
  if (!presentation?.emphasis) {
    return "";
  }
  return `<span class="piece-emphasis-badge piece-emphasis-badge--${escapeHtml(presentation.emphasis)}">${escapeHtml(
    presentation.label || humanizeTopic(presentation.emphasis)
  )}</span>`;
}

function renderPieceBody(piece) {
  return renderMarkdownBodyBlocks(piece.bodyBlocks || [], piece.bodyMarkdown || "");
}

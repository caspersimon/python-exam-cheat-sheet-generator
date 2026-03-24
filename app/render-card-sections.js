function renderSwipe() {
  const filteredDeck = getFilteredDeck();
  const filteredParents = getFilteredParentBundles();
  const activeContext = ensureExplorerNavigation(filteredParents);
  const selectedTotals = getSelectedItemTotals();

  refs.acceptedCount.textContent = String(selectedTotals.topics);
  refs.rejectedCount.textContent = String(selectedTotals.items);
  refs.remainingCount.textContent = String(filteredDeck.length);

  const visibleExamTopics = filteredDeck.filter((card) => (card.exam_stats?.total_hits || 0) > 0).length;
  const progressBits = [
    `${selectedTotals.topics} topics staged`,
    `${selectedTotals.items} pieces selected`,
    `${filteredDeck.length} topics visible`,
  ];
  if (visibleExamTopics > 0 && visibleExamTopics !== filteredDeck.length) {
    progressBits.push(`${visibleExamTopics} exam-heavy`);
  }
  refs.progressText.textContent = progressBits.join(" • ");

  refs.acceptedTopicsList.innerHTML = "";
  getSelectedPreviewEntries()
    .slice(0, 40)
    .forEach((entry) => {
      const li = document.createElement("li");
      li.textContent = humanizeTopic(entry.card.topic);
      refs.acceptedTopicsList.appendChild(li);
    });

  if (!activeContext) {
    refs.topicSidebar.innerHTML = "";
    refs.cardHost.innerHTML = `<div class="empty-state">
      <p><strong>No topics match the current filters.</strong></p>
      <p>Adjust the week filters or search terms to keep exploring.</p>
    </div>`;
    refs.selectionShell?.classList.remove("topic-sidebar-open");
    refs.topicSidebarBackdrop?.classList.add("hidden");
    return;
  }

  refs.topicSidebar.innerHTML = renderTopicSidebar(filteredParents, activeContext.card.id);
  refs.cardHost.innerHTML = renderTopicDetail(activeContext.card, activeContext.parentTopic);
  refs.selectionShell?.classList.toggle("topic-sidebar-open", Boolean(state.navigation.mobileSidebarOpen));
  refs.topicSidebarBackdrop?.classList.toggle("hidden", !state.navigation.mobileSidebarOpen);
}

function renderTopicSidebar(parentTopics, activeTopicId) {
  return `
    <div class="topic-sidebar-head">
      <div>
        <h3>Exam Map</h3>
        <p class="muted">Browse by topic, keep only what is worth final-sheet space, and let the ordering show what matters most.</p>
      </div>
      <button class="ghost-btn icon-btn topic-sidebar-close mobile-only-btn" type="button" data-role="close-topic-sidebar" aria-label="Close topics">
        <span aria-hidden="true">&times;</span>
      </button>
    </div>
    <div class="topic-sidebar-scroll">
      ${parentTopics.map((parentTopic) => renderParentSidebarSection(parentTopic, activeTopicId)).join("")}
    </div>
  `;
}

function renderParentSidebarSection(parentTopic, activeTopicId) {
  const expanded = Boolean(state.navigation.expandedParents[parentTopic.id]);
  const summary = getParentSelectionSummary(parentTopic);
  const topicCountLabel = `${parentTopic.cards.length} topic${parentTopic.cards.length === 1 ? "" : "s"}`;
  return `
    <section class="topic-week-group" data-parent-id="${escapeHtml(parentTopic.id)}">
      <button
        class="topic-week-toggle"
        type="button"
        data-role="toggle-parent"
        data-parent-id="${escapeHtml(parentTopic.id)}"
        aria-expanded="${expanded ? "true" : "false"}"
      >
        <div class="topic-week-labels">
          <strong>${escapeHtml(parentTopic.title)}</strong>
          <span>${escapeHtml(topicCountLabel)}</span>
        </div>
        <div class="topic-week-meta">
          <span>${summary.topics} selected</span>
          <span class="topic-week-caret" aria-hidden="true">${expanded ? "−" : "+"}</span>
        </div>
      </button>
      <div class="topic-week-list ${expanded ? "" : "hidden"}">
        ${parentTopic.summary ? `<p class="topic-parent-summary muted">${escapeHtml(parentTopic.summary)}</p>` : ""}
        <div class="topic-course-group topic-course-group-default">
          <div class="topic-course-group-list">
            ${parentTopic.cards.map((card) => renderSidebarTopicButton(card, parentTopic.id, activeTopicId)).join("")}
          </div>
        </div>
      </div>
    </section>
  `;
}

function renderSidebarTopicButton(card, parentId, activeTopicId) {
  const counts = getSelectionCounts(card);
  const isActive = activeTopicId === card.id;
  const badges = [];
  if (counts.total > 0) {
    badges.push(`${counts.total} selected`);
  }
  return `
    <button
      class="topic-nav-item ${isActive ? "is-active" : ""}"
      type="button"
      data-role="open-topic"
      data-card-id="${escapeHtml(card.id)}"
      data-parent-id="${escapeHtml(parentId)}"
    >
      <span class="topic-nav-title">${escapeHtml(humanizeTopic(card.topic))}</span>
      ${badges.length ? `<span class="topic-nav-meta">${escapeHtml(badges.join(" • "))}</span>` : ""}
    </button>
  `;
}

function renderTopicDetail(card, parentTopic) {
  const draft = ensureDraft(card);
  const selectedCounts = getSelectionCounts(card, draft);
  const weekLabel = Array.isArray(card.weeks) && card.weeks.length ? card.weeks.map((week) => `W${week}`).join(" · ") : "No week tag";
  const visibleSections = getExamCardSections(card).filter((section) => section.snippets.length > 0);

  return `
    <article class="topic-detail-card exam-topic-detail" data-card-id="${escapeHtml(card.id)}">
      <header class="topic-detail-header">
        <div class="topic-detail-intro">
          <div class="topic-detail-course-context">
            <span class="topic-course-chip">${escapeHtml(parentTopic.title)}</span>
            <span class="topic-course-chip subtle">${escapeHtml(weekLabel)}</span>
          </div>
          <p class="topic-detail-kicker">${escapeHtml(`${card.snippetCount} curated snippets · ${card.pieceCount} selectable pieces`)}</p>
          <div class="topic-detail-title-row">
            <h3>${escapeHtml(humanizeTopic(card.topic))}</h3>
          </div>
          ${card.summary ? `<p class="topic-detail-summary">${renderInlineCode(card.summary)}</p>` : ""}
        </div>
        <aside class="topic-detail-aside">
          <div class="topic-stat-list" aria-label="Topic stats">
            <article class="topic-stat-card">
              <span>Sections</span>
              <strong>${escapeHtml(String(visibleSections.length))}</strong>
            </article>
            <article class="topic-stat-card">
              <span>Total Pieces</span>
              <strong>${escapeHtml(String(card.pieceCount || 0))}</strong>
            </article>
            <article class="topic-stat-card">
              <span>Selected</span>
              <strong>${escapeHtml(String(selectedCounts.total))}</strong>
            </article>
          </div>
          <section class="topic-context-panel topic-focus-panel">
            <h4>Selection guidance</h4>
            <p>Start near the top, keep the densest references first, and use lower sections only when you still need coverage.</p>
          </section>
        </aside>
      </header>
      ${visibleSections.map((section) => renderSectionBlock(card, draft, section)).join("")}
      <footer class="topic-detail-footer">
        <button type="button" class="text-link-btn" data-role="reset-splash">Reset intro</button>
        <button type="button" class="text-link-btn danger-link-btn" data-role="reset-progress">Reset progress</button>
      </footer>
    </article>
  `;
}

function renderSectionBlock(card, draft, section) {
  const selectedCount = getSectionSelectedCount(card, draft, section.key);
  const isExpanded = Boolean(draft.ui.expandedSections?.[section.key]);
  const visibleSnippets = isExpanded ? section.snippets : section.snippets.slice(0, section.initialVisibleCount);
  const hiddenCount = Math.max(0, section.snippets.length - visibleSnippets.length);

  return `
    <section class="topic-section-block" data-section-block="${escapeHtml(section.key)}">
      <div class="topic-section-header">
        <div class="topic-section-heading">
          <h4>${escapeHtml(section.title)}</h4>
          ${section.description ? `<p class="muted">${escapeHtml(section.description)}</p>` : ""}
        </div>
        <div class="topic-section-actions">
          <span class="topic-section-count">${escapeHtml(`${selectedCount}/${getSectionSelectablePieceIds(card, section.key).length} selected`)}</span>
          <button
            type="button"
            class="ghost-btn compact-btn"
            data-role="select-all-section"
            data-card-id="${escapeHtml(card.id)}"
            data-section-key="${escapeHtml(section.key)}"
          >
            Select all
          </button>
          <button
            type="button"
            class="ghost-btn compact-btn"
            data-role="clear-section"
            data-card-id="${escapeHtml(card.id)}"
            data-section-key="${escapeHtml(section.key)}"
          >
            Clear
          </button>
          ${section.snippets.length > section.initialVisibleCount
            ? `
              <button
                type="button"
                class="ghost-btn compact-btn"
                data-role="toggle-section-expanded"
                data-card-id="${escapeHtml(card.id)}"
                data-section-key="${escapeHtml(section.key)}"
              >
                ${isExpanded ? "Show less" : `Show ${hiddenCount} more`}
              </button>
            `
            : ""}
        </div>
      </div>
      <div class="topic-rail">
        ${visibleSnippets.map((snippet) => renderSnippetCard(card, draft, section, snippet)).join("")}
      </div>
    </section>
  `;
}

function renderSnippetCard(card, draft, section, snippet) {
  const selectedCount = getSnippetSelectedCount(card, draft, snippet.id);
  return `
    <article class="rail-card exam-snippet-card" data-snippet-id="${escapeHtml(snippet.id)}">
      <div class="exam-snippet-head">
        <div class="exam-snippet-copy">
          <div class="exam-snippet-meta">
            ${isPastExamSnippet(snippet) ? `<span class="topic-course-chip subtle">Past exam</span>` : ""}
          </div>
          <h5>${escapeHtml(snippet.title)}</h5>
          ${snippet.summary ? `<p class="muted">${renderInlineCode(snippet.summary)}</p>` : ""}
          <p class="muted">${escapeHtml(`${selectedCount}/${getSnippetSelectablePieceIds(card, snippet.id).length} pieces selected`)}</p>
        </div>
        <div class="topic-section-actions">
          <button
            type="button"
            class="ghost-btn compact-btn"
            data-role="select-all-snippet"
            data-card-id="${escapeHtml(card.id)}"
            data-snippet-id="${escapeHtml(snippet.id)}"
          >
            Select all
          </button>
          <button
            type="button"
            class="ghost-btn compact-btn"
            data-role="clear-snippet"
            data-card-id="${escapeHtml(card.id)}"
            data-snippet-id="${escapeHtml(snippet.id)}"
          >
            Clear
          </button>
        </div>
      </div>
      <div class="rail-card-body">
        ${snippet.pieces.map((piece) => renderPieceSelector(card, draft, section, snippet, piece)).join("")}
      </div>
    </article>
  `;
}

function renderPieceSelector(card, draft, section, snippet, piece) {
  const selectedSet = new Set(draft.selected.pieces || []);
  const checked = selectedSet.has(piece.id);
  const effectivePiece = getPieceOverride(draft, piece);
  return `
    <div class="detail-toggle-row exam-piece-row">
      <label class="item-select">
        <input
          type="checkbox"
          data-role="item-toggle"
          data-card-id="${escapeHtml(card.id)}"
          data-piece-id="${escapeHtml(piece.id)}"
          ${checked ? "checked" : ""}
        />
        <strong>${escapeHtml(effectivePiece.title || piece.title)}</strong>
      </label>
      <div class="rail-card-body exam-piece-preview">
        ${renderPieceBody(effectivePiece)}
      </div>
    </div>
  `;
}

function renderPieceBody(piece) {
  const content = piece.content || {};
  if (piece.pieceType === "reference_table") {
    const text = String(content.text || "").trim();
    const table = {
      headers: Array.isArray(content.headers) ? content.headers : [],
      rows: Array.isArray(content.rows) ? content.rows : [],
    };
    return `
      ${text ? `<p>${renderInlineCode(text)}</p>` : ""}
      ${table.headers.length && table.rows.length ? renderMiniTable(table) : ""}
    `;
  }

  if (piece.pieceType === "code_example") {
    return `
      ${content.text ? `<p>${renderInlineCode(content.text)}</p>` : ""}
      ${content.code ? renderCodeBlock(content.code) : ""}
      ${content.output ? `<p><strong>Output:</strong></p>${renderOutputBlock(content.output)}` : ""}
    `;
  }

  if (piece.pieceType === "past_exam_piece") {
    return `
      ${renderQuestionContent(content.question || "", content.code_context || "")}
      ${renderOptions(content.options || {})}
      ${content.correct ? `<p class="answer-chip">Correct: ${escapeHtml(String(content.correct).toUpperCase())}</p>` : ""}
      ${content.explanation ? `<p class="source-summary">${renderInlineCode(content.explanation)}</p>` : ""}
    `;
  }

  const text = String(content.text || "").trim();
  return text ? `<p>${renderInlineCode(text)}</p>` : "";
}

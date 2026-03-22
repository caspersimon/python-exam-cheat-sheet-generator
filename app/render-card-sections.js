function renderSwipe() {
  const filteredDeck = getFilteredDeck();
  const filteredWeekBundles = getFilteredWeekBundles();
  const activeContext = ensureExplorerNavigation(filteredWeekBundles);
  const selectedTotals = getSelectedItemTotals();
  refs.acceptedCount.textContent = String(selectedTotals.topics);
  refs.rejectedCount.textContent = String(selectedTotals.items);
  refs.remainingCount.textContent = String(filteredDeck.length);
  const visibleExamTopics = filteredDeck.filter((card) => (card.exam_stats?.total_hits || 0) > 0).length;
  const progressBits = [
    `${selectedTotals.topics} topics staged`,
    `${selectedTotals.items} items selected`,
    `${filteredDeck.length} topics visible`,
  ];
  if (visibleExamTopics > 0 && visibleExamTopics !== filteredDeck.length) {
    progressBits.push(`${visibleExamTopics} exam-linked`);
  }
  refs.progressText.textContent = progressBits.join(" • ");
  refs.acceptedTopicsList.innerHTML = "";
  getSelectedPreviewEntries().slice(0, 40).forEach((entry) => {
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
  const { bundle, group, card } = activeContext;
  refs.topicSidebar.innerHTML = renderTopicSidebar(filteredWeekBundles, card.id);
  refs.cardHost.innerHTML = renderTopicDetail(card, bundle, group);
  refs.selectionShell?.classList.toggle("topic-sidebar-open", Boolean(state.navigation.mobileSidebarOpen));
  refs.topicSidebarBackdrop?.classList.toggle("hidden", !state.navigation.mobileSidebarOpen);
}

function renderTopicSidebar(bundles, activeTopicId) {
  return `
    <div class="topic-sidebar-head">
      <div>
        <h3>Course Map</h3>
        <p class="muted">Open a week, scan the topic list, and keep only what belongs on the printed sheet.</p>
      </div>
      <button class="ghost-btn icon-btn topic-sidebar-close mobile-only-btn" type="button" data-role="close-topic-sidebar" aria-label="Close topics">
        <span aria-hidden="true">&times;</span>
      </button>
    </div>
    <div class="topic-sidebar-scroll">
      ${bundles
        .map((bundle) => renderWeekSidebarSection(bundle, activeTopicId))
        .join("")}
    </div>
  `;
}
function renderWeekSidebarSection(bundle, activeTopicId) {
  const expanded = Boolean(state.navigation.expandedWeeks[String(bundle.week)]);
  const summary = getWeekSelectionSummary(bundle);
  const topicCountLabel = `${bundle.cards.length} topic${bundle.cards.length === 1 ? "" : "s"}`;
  return `
    <section class="topic-week-group" data-week="${bundle.week}">
      <button
        class="topic-week-toggle"
        type="button"
        data-role="toggle-week"
        data-week="${bundle.week}"
        aria-expanded="${expanded ? "true" : "false"}"
      >
        <div class="topic-week-labels">
          <strong>${escapeHtml(bundle.title)}</strong>
          <span>${topicCountLabel}</span>
        </div>
        <div class="topic-week-meta">
          <span>${summary.topics} selected</span>
          <span class="topic-week-caret" aria-hidden="true">${expanded ? "−" : "+"}</span>
        </div>
      </button>
      <div class="topic-week-list ${expanded ? "" : "hidden"}">
        ${bundle.groups.map((group) => renderSidebarCourseGroup(group, bundle.week, activeTopicId)).join("")}
      </div>
    </section>
  `;
}
function renderSidebarCourseGroup(group, week, activeTopicId) {
  const groupSelection = getWeekSelectionSummary(group);
  const countLabel = `${group.cards.length} card${group.cards.length === 1 ? "" : "s"}`;
  const metaBits = [countLabel];
  if (groupSelection.topics > 0) {
    metaBits.push(`${groupSelection.topics} selected`);
  }
  if (group.isDefault) {
    return `
      <div class="topic-course-group topic-course-group-default" data-course-group="${escapeHtml(group.id)}">
        <div class="topic-course-group-list">
          ${group.cards.map((card) => renderSidebarTopicButton(card, week, activeTopicId)).join("")}
        </div>
      </div>
    `;
  }
  return `
    <div class="topic-course-group" data-course-group="${escapeHtml(group.id)}">
      <div class="topic-course-group-head">
        <div class="topic-course-group-copy">
          <strong>${escapeHtml(group.title)}</strong>
          <span>${escapeHtml(metaBits.join(" • "))}</span>
        </div>
      </div>
      <div class="topic-course-group-list">
        ${group.cards.map((card) => renderSidebarTopicButton(card, week, activeTopicId)).join("")}
      </div>
    </div>
  `;
}
function renderSidebarTopicButton(card, week, activeTopicId) {
  const counts = getSelectionCounts(card);
  const isActive = activeTopicId === card.id;
  const badges = [];
  if (card.exam_stats.total_hits > 0) {
    badges.push(`${card.exam_stats.total_hits} exam`);
  }
  if (counts.total > 0) {
    badges.push(`${counts.total} selected`);
  }
  return `
    <button
      class="topic-nav-item ${isActive ? "is-active" : ""}"
      type="button"
      data-role="open-topic"
      data-card-id="${escapeHtml(card.id)}"
      data-week="${week}"
    >
      <span class="topic-nav-title">${escapeHtml(humanizeTopic(card.topic))}</span>
      <span class="topic-nav-meta">${escapeHtml(badges.join(" • ") || "Open topic")}</span>
    </button>
  `;
}
function renderTopicDetail(card, bundle, group) {
  const draft = ensureDraft(card);
  const split = getSourceSplit(card);
  const keyPoints = keyPointGroups(card);
  const aiExamples = usefulAIExamples(card);
  const subtopics = getCardSubtopics(card);
  const selectedCounts = getSelectionCounts(card, draft);
  const weekLabel = Array.isArray(card.weeks) && card.weeks.length ? card.weeks.map((week) => `W${week}`).join(" · ") : `W${bundle.week}`;
  const commonQuestions = getCommonQuestionItems(card);
  const examHitsLabel = card.exam_stats.total_hits > 0 ? `${card.exam_stats.total_hits} exam hits` : "Course material only";
  const groupTitle = group?.isDefault ? "Lecture-aligned topic" : group?.title || "Lecture-aligned topic";
  const contextPanels = [
    renderSubtopicOverview(subtopics),
  ]
    .filter(Boolean)
    .join("");
  return `
    <article class="topic-detail-card" data-card-id="${escapeHtml(card.id)}">
      <header class="topic-detail-header">
        <div class="topic-detail-intro">
          <div class="topic-detail-course-context">
            <span class="topic-course-chip">${escapeHtml(`Week ${bundle.week}`)}</span>
            <span class="topic-course-chip subtle">${escapeHtml(groupTitle)}</span>
          </div>
          <p class="topic-detail-kicker">${escapeHtml(`Source weeks ${weekLabel} · ${examHitsLabel}`)}</p>
          <div class="topic-detail-title-row">
            <h3>${escapeHtml(humanizeTopic(card.topic))}</h3>
          </div>
          ${card.sections.ai_summary?.content ? `<p class="topic-detail-summary">${renderInlineCode(normalizeTruncatedDisplayText(card.sections.ai_summary.content))}</p>` : ""}
        </div>
        <aside class="topic-detail-aside">
          <div class="topic-stat-list" aria-label="Topic stats">
            <article class="topic-stat-card">
              <span>Exam Hits</span>
              <strong>${escapeHtml(String(card.exam_stats.total_hits || 0))}</strong>
            </article>
            <article class="topic-stat-card">
              <span>Coverage</span>
              <strong>${escapeHtml(String(card.exam_stats.coverage_count || 0))}</strong>
            </article>
            <article class="topic-stat-card">
              <span>Selected</span>
              <strong>${escapeHtml(String(selectedCounts.total))}</strong>
            </article>
          </div>
          <section class="topic-context-panel topic-focus-panel">
            <h4>Selection guidance</h4>
            <p>Favor exam-linked facts first, then keep only the examples and snippets you can still read quickly under pressure.</p>
          </section>
        </aside>
      </header>
      ${contextPanels ? `<div class="topic-detail-context-grid">${contextPanels}</div>` : ""}
      ${renderCommonQuestionRail(card, draft, commonQuestions)}
      ${renderKeyPointRail(card, draft, keyPoints)}
      ${renderExampleRail(card, draft, aiExamples)}
      ${renderSourceRail(card, draft, "recommended", "Recommended Snippets", split.recommended)}
      ${renderSourceRail(card, draft, "additional", "Additional Snippets", split.additional)}
      <footer class="topic-detail-footer">
        <button type="button" class="text-link-btn" data-role="reset-splash">Reset intro</button>
        <button type="button" class="text-link-btn danger-link-btn" data-role="reset-progress">Reset progress</button>
      </footer>
    </article>
  `;
}
function renderSectionHeaderBar(card, draft, sectionKey, title, countText, description = "") {
  const enabled = Boolean(draft.sections[sectionKey]);
  return `
    <div class="topic-section-header">
      <div class="topic-section-heading">
        <h4>${escapeHtml(title)}</h4>
        ${description ? `<p class="muted">${escapeHtml(description)}</p>` : ""}
      </div>
      <div class="topic-section-actions">
        <span class="topic-section-count">${escapeHtml(countText)}</span>
        <label class="topic-section-toggle plain-toggle">
          <input
            type="checkbox"
            data-role="section-toggle"
            data-card-id="${escapeHtml(card.id)}"
            data-section="${escapeHtml(sectionKey)}"
            ${enabled ? "checked" : ""}
          />
          <span>Show in preview</span>
        </label>
        <button
          type="button"
          class="ghost-btn compact-btn"
          data-role="select-all-section"
          data-card-id="${escapeHtml(card.id)}"
          data-section="${escapeHtml(sectionKey)}"
        >
          Select all
        </button>
        <button
          type="button"
          class="ghost-btn compact-btn"
          data-role="clear-section"
          data-card-id="${escapeHtml(card.id)}"
          data-section="${escapeHtml(sectionKey)}"
        >
          Clear
        </button>
      </div>
    </div>
  `;
}
function renderKeyPointRail(card, draft, groups) {
  const selectedSet = new Set(draft.selected.keyPoints || []);
  const selectableIds = new Set(keyPointSelectableIds(card));
  const selectedCount = [...selectedSet].filter((id) => selectableIds.has(id)).length;
  const grouped = groupItemsBySubtopic(card, groups, (item) => item.subtopic_id, (item) => item.subtopic_title);
  const body = groups.length
    ? grouped
        .map((subtopicGroup) => {
          const itemsHtml = subtopicGroup.items
            .map((group) => {
          const pointChecked = selectedSet.has(group.id);
          const detailsHtml = group.details.length
            ? group.details
                .map((detail) => {
                  const checked = selectedSet.has(detail.id);
                  return `
                    <div class="detail-toggle-row">
                      <label class="mini-toggle">
                        <input
                          type="checkbox"
                          data-role="item-toggle"
                          data-card-id="${escapeHtml(card.id)}"
                          data-section="keyPoints"
                          data-item-id="${escapeHtml(detail.id)}"
                          ${checked ? "checked" : ""}
                        />
                        <span>${escapeHtml(detailDisplayTitle(detail))}</span>
                      </label>
                      ${renderDetailPreview(detail)}
                    </div>
                  `;
                })
                .join("")
            : "";
          return `
            <article class="rail-card">
              <label class="item-select">
                <input
                  type="checkbox"
                  data-role="item-toggle"
                  data-card-id="${escapeHtml(card.id)}"
                  data-section="keyPoints"
                  data-item-id="${escapeHtml(group.id)}"
                  ${pointChecked ? "checked" : ""}
                />
                <strong>${renderInlineCode(group.text)}</strong>
              </label>
              <div class="rail-card-body">
                ${detailsHtml ? `<div class="rail-subsection">${detailsHtml}</div>` : ""}
              </div>
            </article>
          `;
            })
            .join("");
          return renderSubtopicRailGroup(subtopicGroup, itemsHtml);
        })
        .join("")
    : renderEmptyRailCopy("No key points are available for this topic.");
  return `
    <section class="topic-section-block ${draft.sections.keyPoints ? "" : "is-dimmed"}" data-section-block="keyPoints">
      ${renderSectionHeaderBar(
        card,
        draft,
        "keyPoints",
        "Key Points",
        `${selectedCount}/${selectableIds.size} selected`,
        "Keep the facts and optional detail blocks that truly earn space on the sheet."
      )}
      <div class="topic-rail">${body}</div>
    </section>
  `;
}
function renderExampleRail(card, draft, items) {
  const selectedCount = items.filter((item) => draft.selected.aiExamples.includes(item.id)).length;
  const grouped = groupItemsBySubtopic(card, items, (item) => item.subtopic_id, (item) => item.subtopic_title);
  const body = items.length
    ? grouped
        .map((subtopicGroup) => {
          const itemsHtml = subtopicGroup.items
            .map((item) => {
          const checked = draft.selected.aiExamples.includes(item.id);
          const kindLabel = item.kind === "incorrect" ? "Incorrect" : "Correct";
          return `
            <article class="rail-card rail-card-code">
              <label class="item-select">
                <input
                  type="checkbox"
                  data-role="item-toggle"
                  data-card-id="${escapeHtml(card.id)}"
                  data-section="aiExamples"
                  data-item-id="${escapeHtml(item.id)}"
                  ${checked ? "checked" : ""}
                />
                <strong>${escapeHtml(kindLabel)} • ${renderInlineCode(item.title || "Code example")}</strong>
              </label>
              <div class="rail-card-body">
                ${renderCodeBlock(item.code || "")}
                ${item.output ? `<p><strong>Output / Result:</strong></p>${renderOutputBlock(item.output || "")}` : ""}
                ${item.why ? `<p class="item-note">${renderInlineCode(item.why)}</p>` : ""}
              </div>
            </article>
          `;
            })
            .join("");
          return renderSubtopicRailGroup(subtopicGroup, itemsHtml);
        })
        .join("")
    : renderEmptyRailCopy("No code examples are available for this topic.");
  return `
    <section class="topic-section-block ${draft.sections.aiExamples ? "" : "is-dimmed"}" data-section-block="aiExamples">
      ${renderSectionHeaderBar(
        card,
        draft,
        "aiExamples",
        "Code Examples",
        `${selectedCount}/${items.length} selected`,
        "Choose the patterns you want to be able to reproduce from memory."
      )}
      <div class="topic-rail">${body}</div>
    </section>
  `;
}

function renderCommonQuestionRail(card, draft, items) {
  const selectedCount = items.filter((item) => (draft.selected.aiQuestions || []).includes(item.id)).length;
  const body = items.length
    ? `<div class="common-question-list">${items
        .map((item) => {
          const checked = (draft.selected.aiQuestions || []).includes(item.id);
          return `
            <article class="common-question-card">
              <label class="item-select">
                <input
                  type="checkbox"
                  data-role="item-toggle"
                  data-card-id="${escapeHtml(card.id)}"
                  data-section="aiQuestions"
                  data-item-id="${escapeHtml(item.id)}"
                  ${checked ? "checked" : ""}
                />
                <strong>${renderInlineCode(item.summary)}</strong>
              </label>
              <div class="common-question-card-body">
                ${item.detail ? `<p>${renderInlineCode(item.detail)}</p>` : ""}
                ${item.table ? renderMiniTable(item.table) : ""}
                ${item.code ? renderCodeBlock(item.code) : ""}
              </div>
            </article>
          `;
        })
        .join("")}</div>`
    : renderEmptyRailCopy("No common exam questions are available for this topic.");

  return `
    <section class="topic-section-block ${draft.sections.aiQuestions ? "" : "is-dimmed"}" data-section-block="aiQuestions">
      ${renderSectionHeaderBar(
        card,
        draft,
        "aiQuestions",
        "Common Exam Questions",
        `${selectedCount}/${items.length} selected`,
        "Keep the answer patterns and traps you want printed directly on the cheat sheet."
      )}
      ${body}
    </section>
  `;
}

function renderSourceRail(card, draft, sectionKey, title, items) {
  const selectedIds = draft.selected[sectionKey] || [];
  const selectedCount = items.filter((item) => selectedIds.includes(item.id)).length;
  const grouped = groupItemsBySubtopic(card, items, (item) => item.subtopicId, (item) => item.subtopicTitle);
  const body = items.length
    ? grouped
        .map((subtopicGroup) => {
          const itemsHtml = subtopicGroup.items
            .map((sourceItem) => {
          const checked = selectedIds.includes(sourceItem.id);
          return `
            <article class="rail-card rail-card-source">
              <label class="item-select">
                <input
                  type="checkbox"
                  data-role="item-toggle"
                  data-card-id="${escapeHtml(card.id)}"
                  data-section="${escapeHtml(sectionKey)}"
                  data-item-id="${escapeHtml(sourceItem.id)}"
                  ${checked ? "checked" : ""}
                />
                <strong>${escapeHtml(sourceItem.header)}</strong>
              </label>
              <div class="rail-card-body">
                ${renderSourceItemBody(sourceItem)}
              </div>
            </article>
          `;
            })
            .join("");
          return renderSubtopicRailGroup(subtopicGroup, itemsHtml);
        })
        .join("")
    : renderEmptyRailCopy("No snippets are available in this section.");
  return `
    <section class="topic-section-block ${draft.sections[sectionKey] ? "" : "is-dimmed"}" data-section-block="${escapeHtml(sectionKey)}">
      ${renderSectionHeaderBar(
        card,
        draft,
        sectionKey,
        title,
        `${selectedCount}/${items.length} selected`,
        sectionKey === "recommended"
          ? "High-value lecture and exam snippets that usually deserve first priority."
          : "Extra supporting snippets for edge cases, comparisons, and reminders."
      )}
      <div class="topic-rail">${body}</div>
    </section>
  `;
}

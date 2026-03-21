function renderSwipe() {
  const filteredDeck = getFilteredDeck();
  const filteredWeekBundles = getFilteredWeekBundles();
  const activeContext = ensureExplorerNavigation(filteredWeekBundles);
  const selectedTotals = getSelectedItemTotals();

  refs.acceptedCount.textContent = String(selectedTotals.topics);
  refs.rejectedCount.textContent = String(selectedTotals.items);
  refs.remainingCount.textContent = String(filteredDeck.length);

  refs.progressText.textContent = `${selectedTotals.topics} topics in preview • ${selectedTotals.items} items selected`;

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

  const { bundle, card } = activeContext;
  refs.topicSidebar.innerHTML = renderTopicSidebar(filteredWeekBundles, card.id);
  refs.cardHost.innerHTML = renderTopicDetail(card, bundle);

  refs.selectionShell?.classList.toggle("topic-sidebar-open", Boolean(state.navigation.mobileSidebarOpen));
  refs.topicSidebarBackdrop?.classList.toggle("hidden", !state.navigation.mobileSidebarOpen);
}

function renderTopicSidebar(bundles, activeTopicId) {
  return `
    <div class="topic-sidebar-head">
      <div>
        <h3>Weeks & Topics</h3>
        <p class="muted">Browse by week and open a topic.</p>
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
        ${bundle.cards.map((card) => renderSidebarTopicButton(card, bundle.week, activeTopicId)).join("")}
      </div>
    </section>
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

function renderTopicDetail(card, bundle) {
  const draft = ensureDraft(card);
  const split = getSourceSplit(card);
  const keyPoints = keyPointGroups(card);
  const aiExamples = usefulAIExamples(card);
  const selectedCounts = getSelectionCounts(card, draft);
  const weekLabel = Array.isArray(card.weeks) && card.weeks.length ? card.weeks.map((week) => `W${week}`).join(" · ") : `W${bundle.week}`;
  const commonQuestions = card.sections.ai_common_questions?.bullets || [];
  const examHitsLabel = card.exam_stats.total_hits > 0 ? `${card.exam_stats.total_hits} exam hits` : "Course material only";
  const selectedLabel = `${selectedCounts.total} selected`;

  return `
    <article class="topic-detail-card" data-card-id="${escapeHtml(card.id)}">
      <header class="topic-detail-header">
        <div class="topic-detail-intro">
          <p class="topic-detail-kicker">${escapeHtml(`Week ${bundle.week} · ${weekLabel} · ${examHitsLabel}`)}</p>
          <div class="topic-detail-title-row">
            <h3>${escapeHtml(humanizeTopic(card.topic))}</h3>
            <div class="topic-detail-summary-stats">
              <span>${escapeHtml(selectedLabel)}</span>
              <span>${escapeHtml(`${card.exam_stats.coverage_count || 0} sources`)}</span>
            </div>
          </div>
          ${card.sections.ai_summary?.content ? `<p class="topic-detail-summary">${renderInlineCode(normalizeTruncatedDisplayText(card.sections.ai_summary.content))}</p>` : ""}
        </div>
      </header>

      ${commonQuestions.length
        ? `
          <section class="topic-context-panel">
            <h4>Common questions</h4>
            <div class="common-question-list">
              ${commonQuestions.map((question) => `<p>${renderInlineCode(question)}</p>`).join("")}
            </div>
          </section>
        `
        : ""}

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

function truncateText(text, maxLength = 240) {
  const value = normalizeNewlines(String(text || "")).replace(/\s+/g, " ").trim();
  if (!value || value.length <= maxLength) {
    return value;
  }
  return `${value.slice(0, maxLength).replace(/\s+\S*$/, "").trim()}...`;
}

function truncateCode(text, maxLines = 8) {
  const lines = normalizeNewlines(String(text || ""))
    .split("\n")
    .map((line) => line.replace(/\s+$/g, ""));
  if (lines.length <= maxLines) {
    return lines.join("\n").trim();
  }
  return `${lines.slice(0, maxLines).join("\n")}\n...`;
}

function detailDisplayTitle(detail) {
  const raw = String(detail?.title || "").trim();
  if (/^optional\b/i.test(raw)) {
    if (detail.table) {
      return "Reference table";
    }
    if (detail.code) {
      return "Code example";
    }
    if (detail.kind === "commands") {
      return "Commands";
    }
    return "Note";
  }
  return raw || "Detail";
}

function renderDetailPreview(detail) {
  const pieces = [];
  if (detail.text) {
    pieces.push(`<p>${renderInlineCode(truncateText(detail.text, 120))}</p>`);
  }
  if (detail.code) {
    pieces.push(`<pre>${escapeHtml(truncateCode(detail.code, 4))}</pre>`);
  }
  if (detail.table) {
    pieces.push(`<p class="detail-table-note">${escapeHtml(`${detail.table.headers.length} columns • ${detail.table.rows.length} rows`)}</p>`);
  }
  if (!pieces.length) {
    return "";
  }
  return `<div class="detail-preview">${pieces.join("")}</div>`;
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

  const body = groups.length
    ? groups
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
        .join("")
    : renderEmptyRailCopy("No key points are available for this topic.");

  return `
    <section class="topic-section-block ${draft.sections.keyPoints ? "" : "is-dimmed"}" data-section-block="keyPoints">
      ${renderSectionHeaderBar(card, draft, "keyPoints", "Key Points", `${selectedCount}/${selectableIds.size} selected`)}
      <div class="topic-rail">${body}</div>
    </section>
  `;
}

function renderExampleRail(card, draft, items) {
  const selectedCount = items.filter((item) => draft.selected.aiExamples.includes(item.id)).length;
  const body = items.length
    ? items
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
                <pre>${escapeHtml(item.code || "")}</pre>
                ${item.why ? `<p class="item-note">${renderInlineCode(item.why)}</p>` : ""}
              </div>
            </article>
          `;
        })
        .join("")
    : renderEmptyRailCopy("No code examples are available for this topic.");

  return `
    <section class="topic-section-block ${draft.sections.aiExamples ? "" : "is-dimmed"}" data-section-block="aiExamples">
      ${renderSectionHeaderBar(card, draft, "aiExamples", "Code Examples", `${selectedCount}/${items.length} selected`)}
      <div class="topic-rail">${body}</div>
    </section>
  `;
}

function renderSourceRail(card, draft, sectionKey, title, items) {
  const selectedIds = draft.selected[sectionKey] || [];
  const selectedCount = items.filter((item) => selectedIds.includes(item.id)).length;
  const body = items.length
    ? items
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
        .join("")
    : renderEmptyRailCopy("No snippets are available in this section.");

  return `
    <section class="topic-section-block ${draft.sections[sectionKey] ? "" : "is-dimmed"}" data-section-block="${escapeHtml(sectionKey)}">
      ${renderSectionHeaderBar(card, draft, sectionKey, title, `${selectedCount}/${items.length} selected`)}
      <div class="topic-rail">${body}</div>
    </section>
  `;
}

function renderEmptyRailCopy(text) {
  return `<div class="rail-empty">${escapeHtml(text)}</div>`;
}

function renderMiniTable(table) {
  const headHtml = table.headers.map((header) => `<th>${renderInlineCode(header)}</th>`).join("");
  const rowsHtml = table.rows
    .map((row) => `<tr>${row.map((cell) => `<td>${renderInlineCode(cell)}</td>`).join("")}</tr>`)
    .join("");
  return `
    <div class="kp-mini-table-wrap">
      <table class="kp-mini-table">
        <thead><tr>${headHtml}</tr></thead>
        <tbody>${rowsHtml}</tbody>
      </table>
    </div>
  `;
}

function renderSourceItemBody(sourceItem) {
  const item = sourceItem.item;
  if (sourceItem.sourceType === "exam") {
    const parsed = splitPromptAndCode(item.question || "");
    const prompt = parsed.prompt || item.question || "";
    const explanation = truncateText(item.explanation || "", 240);
    const codeContext = parsed.code || item.code_context || "";
    return `
      ${prompt ? `<p class="question-text">${renderInlineCode(truncateText(prompt, 220))}</p>` : ""}
      ${codeContext ? `<pre class="question-code">${escapeHtml(truncateCode(codeContext, 8))}</pre>` : ""}
      ${renderOptions(item.options)}
      ${item.correct ? `<p class="answer-chip">Correct: ${escapeHtml(String(item.correct))}</p>` : ""}
      ${explanation ? `<p class="source-summary">${renderInlineCode(explanation)}</p>` : ""}
    `;
  }

  if (sourceItem.sourceType === "lecture") {
    const codeExamples = (item.code_examples || [])
      .slice(0, 2)
      .map(
        (example) => `
          <p><strong>${renderInlineCode(truncateText(example.description || "Code", 72))}</strong></p>
          <pre>${escapeHtml(truncateCode(example.code || "", 6))}</pre>
        `
      )
      .join("");

    const lectureQuestion = item.question
      ? `
        <p class="question-text"><strong>Lecture question:</strong> ${renderInlineCode(truncateText(splitPromptAndCode(item.question).prompt || item.question, 180))}</p>
        ${renderOptions(item.options)}
        ${item.correct ? `<p class="answer-chip">Correct: ${escapeHtml(String(item.correct))}</p>` : ""}
      `
      : "";

    return `
      ${item.explanation ? `<p class="source-summary">${renderInlineCode(truncateText(item.explanation, 260))}</p>` : ""}
      ${lectureQuestion}
      ${codeExamples}
    `;
  }

  const outText = (item.outputs || []).join("\\n");
  return `
    ${item.source ? `<pre>${escapeHtml(truncateCode(item.source, 10))}</pre>` : ""}
    ${outText ? `<p><strong>Output:</strong></p><pre>${escapeHtml(truncateCode(outText, 6))}</pre>` : ""}
  `;
}

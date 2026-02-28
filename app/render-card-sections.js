function renderSwipe() {
  const filteredDeck = getFilteredDeck();
  const pendingCards = getPendingCards(filteredDeck);
  const currentCard = getCurrentCard(filteredDeck);

  const acceptedCount = Object.values(state.decisions).filter((entry) => entry.status === "accepted").length;
  const rejectedCount = Object.values(state.decisions).filter((entry) => entry.status === "rejected").length;

  refs.acceptedCount.textContent = String(acceptedCount);
  refs.rejectedCount.textContent = String(rejectedCount);
  refs.remainingCount.textContent = String(pendingCards.length);

  const decidedInFilter = filteredDeck.filter((card) => state.decisions[card.id]).length;
  refs.progressText.textContent = `${decidedInFilter}/${filteredDeck.length} decided in current filter • ${acceptedCount} accepted`;

  refs.acceptedTopicsList.innerHTML = "";
  state.acceptedOrder.slice(0, 40).forEach((cardId) => {
    const card = state.cards.find((entry) => entry.id === cardId);
    if (!card) {
      return;
    }
    const li = document.createElement("li");
    li.textContent = humanizeTopic(card.topic);
    refs.acceptedTopicsList.appendChild(li);
  });

  if (!currentCard) {
    refs.cardHost.innerHTML = `<div class="empty-state">
      <p><strong>No more cards in this filter.</strong></p>
      <p>Adjust filters or open preview/export.</p>
      <p>Accepted topics: ${acceptedCount}</p>
    </div>`;
    return;
  }

  const draft = ensureDraft(currentCard);
  refs.cardHost.innerHTML = renderTopicCard(currentCard, draft);
  attachCardSwipeHandlers();
}

function renderTopicCard(card, draft) {
  const weeksText = card.weeks.length ? card.weeks.map((week) => `W${week}`).join(" • ") : "Week unknown";
  const examSources = Object.entries(card.exam_stats.by_exam || {})
    .map(([exam, count]) => `${formatExamLabel(exam)} × ${count}`)
    .join(", ");
  const split = getSourceSplit(card);
  const keyPointGroupsForCard = keyPointGroups(card);
  const keyPointItemCount = keyPointGroupsForCard.reduce((count, group) => count + 1 + group.details.length, 0);
  const examSourceInfo = examSources || "No detailed exam-source mapping is available yet.";

  const totalHitsPill = card.exam_stats.total_hits > 0
    ? `<span class="pill hot exam-count-pill">
         <span>${card.exam_stats.total_hits} exam question${card.exam_stats.total_hits === 1 ? "" : "s"}</span>
         ${renderInfoChip("?", "Exam question sources", `Questions sourced from: ${examSourceInfo}`, "help")}
       </span>`
    : `<span class="pill">Not tested in exams</span>`;

  return `
    <article class="topic-card" data-card-id="${escapeHtml(card.id)}" id="activeTopicCard">
      <div class="card-head">
        <div>
          <h3>${escapeHtml(humanizeTopic(card.topic))}</h3>
          <div class="meta-pill-row">
            <span class="pill">${escapeHtml(weeksText)}</span>
            ${totalHitsPill}
          </div>
        </div>
        <div class="meta-column">
          <span>Swipe / arrow keys to decide</span>
          <button class="ghost-btn compact-btn icon-btn" type="button" data-role="toggle-card-settings" aria-expanded="${draft.ui?.settingsOpen ? "true" : "false"}" title="Card settings">
            <span aria-hidden="true">&#9881;</span>
            <span class="visually-hidden">Card settings</span>
          </button>
        </div>
      </div>

      <section class="card-settings-panel ${draft.ui?.settingsOpen ? "" : "hidden"}">
        <p class="muted settings-hint">Choose section visibility and defaults for new cards.</p>
        <label class="field settings-row">
          <span>Default source selection</span>
          <select data-role="default-selection-mode">
            <option value="none" ${state.preferences.sourceAutoSelectMode === "none" ? "selected" : ""}>Manual (select nothing)</option>
            <option value="recommended" ${state.preferences.sourceAutoSelectMode === "recommended" ? "selected" : ""}>Auto-select recommended</option>
          </select>
        </label>
        <div class="section-toggle-grid">
          ${renderSectionToggle("aiSummary", "Summary", 1, draft.sections.aiSummary, true)}
          ${renderSectionToggle("aiQuestions", "Common Questions", (card.sections.ai_common_questions?.bullets || []).length, draft.sections.aiQuestions, true)}
          ${renderSectionToggle("keyPoints", "Key Points for Reference", keyPointItemCount, draft.sections.keyPoints, true)}
          ${renderSectionToggle("aiExamples", "Code Examples", usefulAIExamples(card).length, draft.sections.aiExamples, true)}
          ${renderSectionToggle("recommended", "Recommended for Cheat Sheet", split.recommended.length, draft.sections.recommended)}
          ${renderSectionToggle("additional", "Additional Snippets", split.additional.length, draft.sections.additional)}
        </div>
        <div class="settings-footer">
          <button type="button" class="text-link-btn" data-role="reset-splash">Reset intro</button>
          <button type="button" class="text-link-btn danger-link-btn" data-role="reset-progress">Reset progress</button>
        </div>
      </section>

      ${renderAISummarySection(card, draft)}
      ${renderAIQuestionsSection(card, draft)}
      ${renderKeyPointsSection(card, draft)}
      ${renderAIExamplesSection(card, draft)}
      ${renderSourceSection(card, draft, "recommended", "Recommended for Cheat Sheet", split.recommended)}
      ${renderSourceSection(card, draft, "additional", "Additional Snippets", split.additional)}
    </article>
  `;
}

function renderSectionToggle(section, label, count, checked, isAI = false) {
  void isAI;
  return `
    <label>
      <input type="checkbox" data-role="section-toggle" data-section="${section}" ${checked ? "checked" : ""} />
      <span>${escapeHtml(label)} (${count})</span>
    </label>
  `;
}

function renderInfoChip(iconHtml, label, text, variant = "") {
  const variantClass = variant ? ` ${variant}` : "";
  return `
    <span class="info-chip${variantClass}">
      <button type="button" class="info-icon-btn" data-role="toggle-info" aria-label="${escapeHtml(label)}" title="${escapeHtml(label)}">
        <span aria-hidden="true">${iconHtml}</span>
      </button>
      <span class="info-popover" role="tooltip">${escapeHtml(text)}</span>
    </span>
  `;
}

function renderSparkleInfo(text, label = "AI-generated details") {
  return renderInfoChip("&#10024;", label, text, "sparkle");
}

function renderSectionHeader(title, countText = "", sparkleText = "", sparkleLabel = "AI-generated details") {
  const hasTitle = Boolean(title);
  const countHtml = countText ? `<span class="section-count">${escapeHtml(countText)}</span>` : "";
  return `
    <div class="section-header ${hasTitle ? "" : "section-header-meta-only"}">
      <div class="section-title-row">
        ${hasTitle ? `<strong>${escapeHtml(title)}</strong>` : ""}
        ${sparkleText ? renderSparkleInfo(sparkleText, sparkleLabel) : ""}
      </div>
      ${countHtml}
    </div>
  `;
}

function renderAISummarySection(card, draft) {
  const summary = normalizeTruncatedDisplayText(card.sections.ai_summary?.content || "");
  const hiddenClass = draft.sections.aiSummary ? "" : "hidden";
  return `
    <section class="section-block ${hiddenClass}" data-section-block="aiSummary">
      <div class="summary-meta">
        ${renderSparkleInfo(AI_GENERATION_NOTE, "How this summary was generated")}
      </div>
      <div class="section-items">
        <p class="section-paragraph">${renderInlineCode(summary)}</p>
      </div>
    </section>
  `;
}

function renderAIQuestionsSection(card, draft) {
  const bullets = card.sections.ai_common_questions?.bullets || [];
  const hiddenClass = draft.sections.aiQuestions ? "" : "hidden";

  return `
    <section class="section-block ${hiddenClass}" data-section-block="aiQuestions">
      ${renderSectionHeader("Common Questions", String(bullets.length), AI_GENERATION_NOTE, "How these questions were generated")}
      <div class="section-items">
        <ul class="plain-bullets">
          ${bullets.map((bullet) => `<li>${renderInlineCode(bullet)}</li>`).join("")}
        </ul>
      </div>
    </section>
  `;
}

function renderKeyPointsSection(card, draft) {
  const groups = keyPointGroups(card);
  const hiddenClass = draft.sections.keyPoints ? "" : "hidden";
  const selectedSet = new Set(draft.selected.keyPoints || []);
  const selectableIds = new Set(keyPointSelectableIds(card));
  const selectedCount = [...selectedSet].filter((id) => selectableIds.has(id)).length;
  const totalCount = selectableIds.size;

  const pointHtml = groups.length
    ? groups
        .map((group) => {
          const checked = selectedSet.has(group.id);
          const detailsHtml = group.details.length
            ? `
              <div class="key-point-details">
                ${group.details
                  .map((detail) => {
                    const detailChecked = selectedSet.has(detail.id);
                    const kindLabel = detail.kind.charAt(0).toUpperCase() + detail.kind.slice(1);
                    return `
                      <div class="kp-detail-item">
                        <label class="item-select kp-detail-select">
                          <input
                            type="checkbox"
                            data-role="item-toggle"
                            data-section="keyPoints"
                            data-item-id="${escapeHtml(detail.id)}"
                            ${detailChecked ? "checked" : ""}
                          />
                          <span class="kp-detail-label">
                            <strong>${escapeHtml(detail.title)}</strong>
                            <span class="kp-detail-kind">${escapeHtml(kindLabel)}</span>
                          </span>
                        </label>
                        <div class="kp-detail-body">
                          ${detail.text ? `<p class="item-note">${renderInlineCode(detail.text)}</p>` : ""}
                          ${detail.table ? renderMiniTable(detail.table) : ""}
                          ${detail.code ? `<pre>${escapeHtml(detail.code)}</pre>` : ""}
                        </div>
                      </div>
                    `;
                  })
                  .join("")}
              </div>
            `
            : "";

          return `
            <div class="item-card key-point-group">
              <label class="item-select">
                <input
                  type="checkbox"
                  data-role="item-toggle"
                  data-section="keyPoints"
                  data-item-id="${escapeHtml(group.id)}"
                  ${checked ? "checked" : ""}
                />
                <strong>${renderInlineCode(group.text)}</strong>
              </label>
              ${detailsHtml}
            </div>
          `;
        })
        .join("")
    : `<p class="muted">No key points available.</p>`;

  return `
    <section class="section-block ${hiddenClass}" data-section-block="keyPoints">
      ${renderSectionHeader("Key Points for Reference", `${selectedCount}/${totalCount} selected`, KEY_POINTS_GENERATION_NOTE, "How these key points were generated")}
      <div class="section-items">${pointHtml}</div>
    </section>
  `;
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

function renderAIExamplesSection(card, draft) {
  const items = usefulAIExamples(card);
  const hiddenClass = draft.sections.aiExamples ? "" : "hidden";

  const itemHtml = items.length
    ? items
        .map((item) => {
          const checked = draft.selected.aiExamples.includes(item.id);
          const kindLabel = item.kind === "incorrect" ? "Incorrect" : "Correct";
          return `
            <div class="item-card">
              <label class="item-select">
                <input
                  type="checkbox"
                  data-role="item-toggle"
                  data-section="aiExamples"
                  data-item-id="${escapeHtml(item.id)}"
                  ${checked ? "checked" : ""}
                />
                <strong>${escapeHtml(kindLabel)} • ${renderInlineCode(item.title || "Code example")}</strong>
              </label>
              <pre>${escapeHtml(item.code || "")}</pre>
              <p class="item-note">${renderInlineCode(item.why || "")}</p>
            </div>
          `;
        })
        .join("")
    : `<p class="muted">No code examples available.</p>`;

  return `
    <section class="section-block ${hiddenClass}" data-section-block="aiExamples">
      ${renderSectionHeader("Code Examples", `${draft.selected.aiExamples.length}/${items.length} selected`, AI_GENERATION_NOTE, "How these examples were generated")}
      <div class="section-items">${itemHtml}</div>
    </section>
  `;
}

function renderSourceSection(card, draft, sectionKey, title, items) {
  const hiddenClass = draft.sections[sectionKey] ? "" : "hidden";
  const selectedIds = draft.selected[sectionKey] || [];
  const selectedCount = items.filter((item) => selectedIds.includes(item.id)).length;

  const itemHtml = items.length
    ? items
        .map((sourceItem) => {
          const checked = selectedIds.includes(sourceItem.id);
          return `
            <div class="item-card">
              <label class="item-select">
                <input
                  type="checkbox"
                  data-role="item-toggle"
                  data-section="${sectionKey}"
                  data-item-id="${escapeHtml(sourceItem.id)}"
                  ${checked ? "checked" : ""}
                />
                <strong>${escapeHtml(sourceItem.header)}</strong>
              </label>
              <div class="item-body">
                ${renderSourceItemBody(sourceItem)}
              </div>
            </div>
          `;
        })
        .join("")
    : `<p class="muted">No snippets in this category.</p>`;

  return `
    <section class="section-block ${hiddenClass}" data-section-block="${sectionKey}">
      ${renderSectionHeader(title, `${selectedCount}/${items.length} selected`)}
      <div class="section-items">${itemHtml}</div>
    </section>
  `;
}

function renderSourceItemBody(sourceItem) {
  const item = sourceItem.item;
  if (sourceItem.sourceType === "exam") {
    return `
      ${renderQuestionContent(item.question, item.code_context)}
      ${renderOptions(item.options)}
      ${item.correct ? `<p class="answer-chip">Correct: ${escapeHtml(String(item.correct))}</p>` : ""}
      ${item.explanation ? `<p>${renderInlineCode(item.explanation)}</p>` : ""}
    `;
  }

  if (sourceItem.sourceType === "lecture") {
    const codeExamples = (item.code_examples || [])
      .map(
        (example) => `
          <p><strong>${renderInlineCode(example.description || "Code")}</strong></p>
          <pre>${escapeHtml(example.code || "")}</pre>
        `
      )
      .join("");

    const lectureQ = item.question
      ? `
        ${renderQuestionContent(item.question, "", "Lecture question")}
        ${renderOptions(item.options)}
        ${item.correct ? `<p class="answer-chip">Correct: ${escapeHtml(String(item.correct))}</p>` : ""}
      `
      : "";

    return `
      ${item.explanation ? `<p>${renderInlineCode(item.explanation)}</p>` : ""}
      ${lectureQ}
      ${codeExamples}
    `;
  }

  const outText = (item.outputs || []).join("\\n");
  return `
    <pre>${escapeHtml(item.source || "")}</pre>
    ${outText ? `<p><strong>Output:</strong></p><pre>${escapeHtml(outText)}</pre>` : ""}
  `;
}


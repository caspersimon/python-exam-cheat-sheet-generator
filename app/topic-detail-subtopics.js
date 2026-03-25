function truncateText(text, maxLength = 240) {
  const value = normalizeNewlines(String(text || "")).replace(/\s+/g, " ").trim();
  if (!value || value.length <= maxLength) {
    return value;
  }
  return `${value.slice(0, maxLength).replace(/\s+\S*$/, "").trim()}...`;
}

function renderSubtopicOverview(subtopics) {
  if (!Array.isArray(subtopics) || !subtopics.length) {
    return "";
  }

  return `
    <section class="topic-context-panel subtopic-overview-panel">
      <h4>Subtopic map</h4>
      <div class="subtopic-overview-list">
        ${subtopics
          .map(
            (subtopic) => `
              <article class="subtopic-overview-item">
                <strong>${escapeHtml(subtopic.title)}</strong>
                ${subtopic.summary ? `<p>${renderInlineCode(truncateText(subtopic.summary, 180))}</p>` : ""}
              </article>
            `
          )
          .join("")}
      </div>
    </section>
  `;
}

function renderSubtopicRailGroup(subtopicGroup, innerHtml) {
  return `
    <section class="rail-subtopic-group" data-subtopic-id="${escapeHtml(subtopicGroup.id)}">
      ${innerHtml}
    </section>
  `;
}

function renderEmptyRailCopy(text) {
  return `<div class="rail-empty">${escapeHtml(text)}</div>`;
}

function renderMiniTable(table) {
  const headers = Array.isArray(table?.headers) ? table.headers : [];
  const rows = Array.isArray(table?.rows) ? table.rows : [];
  if (!headers.length && !rows.length) {
    return "";
  }

  const headHtml = headers.map((header) => `<th>${renderInlineCode(header)}</th>`).join("");
  const rowsHtml = rows
    .map((row) => `<tr>${(Array.isArray(row) ? row : []).map((cell) => `<td>${renderInlineRichText(cell, { preserveNewlines: true })}</td>`).join("")}</tr>`)
    .join("");
  return `
    <div class="kp-mini-table-wrap">
      <table class="kp-mini-table">
        ${headers.length ? `<thead><tr>${headHtml}</tr></thead>` : ""}
        <tbody>${rowsHtml}</tbody>
      </table>
    </div>
  `;
}

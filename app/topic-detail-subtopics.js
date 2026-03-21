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

function renderSubtopicOverview(subtopics) {
  if (!subtopics.length) {
    return "";
  }

  return `
    <section class="topic-context-panel subtopic-overview-panel">
      <h4>Subtopics in this topic</h4>
      <div class="subtopic-overview-list">
        ${subtopics
          .map(
            (subtopic) => `
              <article class="subtopic-overview-item">
                <strong>${escapeHtml(subtopic.title)}</strong>
                ${subtopic.summary ? `<p>${renderInlineCode(normalizeTruncatedDisplayText(subtopic.summary))}</p>` : ""}
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
      <div class="rail-subtopic-head">
        <h5>${escapeHtml(subtopicGroup.title)}</h5>
        ${subtopicGroup.summary ? `<p>${renderInlineCode(normalizeTruncatedDisplayText(subtopicGroup.summary))}</p>` : ""}
      </div>
      <div class="rail-subtopic-items">
        ${innerHtml}
      </div>
    </section>
  `;
}

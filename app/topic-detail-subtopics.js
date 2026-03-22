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
    pieces.push(`<p>${renderInlineCode(detail.text)}</p>`);
  }
  if (detail.code) {
    pieces.push(renderCodeBlock(detail.code));
  }
  if (detail.table) {
    pieces.push(renderMiniTable(detail.table));
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
      <h4>Subtopic map</h4>
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

function getCommonQuestionItems(card) {
  const section = card.sections.ai_common_questions || {};
  const explicitItems = Array.isArray(section.items) ? section.items : [];
  if (explicitItems.length) {
    return explicitItems.map((item, idx) => normalizeCommonQuestionItem(item, idx)).filter(Boolean);
  }

  return (section.bullets || []).map((bullet, idx) => normalizeCommonQuestionBullet(bullet, idx)).filter(Boolean);
}

function normalizeCommonQuestionItem(item, idx = 0) {
  if (!item || typeof item !== "object") {
    return null;
  }

  const summary = sanitizeDisplayText(item.summary || item.question || "").trim();
  const detail = sanitizeDisplayText(item.detail || item.answer || "").trim();
  const extra = sanitizeDisplayText(item.extra || item.additional_info || item.why || "").trim();
  const code = normalizeNewlines(item.code || "").trim();
  const table = normalizeMiniTable(item.table);

  if (!summary && !detail && !extra && !code && !table) {
    return null;
  }

  return {
    id: String(item.id || `aiq-${idx + 1}`),
    summary,
    detail,
    extra,
    code,
    table,
  };
}

function normalizeCommonQuestionBullet(rawBullet, idx = 0) {
  const bullet = sanitizeDisplayText(rawBullet || "").trim();
  if (!bullet) {
    return null;
  }

  const parsed = splitPromptAndCode(bullet);
  const prompt = parsed.prompt.trim();
  const code = parsed.code.trim();

  if (/^what is the output of the following code\??$/i.test(prompt) && code) {
    return {
      id: `aiq-${idx + 1}`,
      summary: "What is the output of this code?",
      detail: "Trace the names, values, and operators before you run it.",
      extra: "",
      code,
    };
  }

  const fixMatch = prompt.match(/^(.*?)(?:\s+[—-]\s+|\s+)Fix:\s*(.+)$/i);
  if (fixMatch) {
    return {
      id: `aiq-${idx + 1}`,
      summary: fixMatch[1].trim(),
      detail: fixMatch[2].trim(),
      extra: code ? "Test the fixed version by stepping through the code and expected output." : "",
      code,
    };
  }

  const dashParts = prompt.split(/\s+[—-]\s+/);
  if (dashParts.length >= 2) {
    return {
      id: `aiq-${idx + 1}`,
      summary: dashParts[0].trim(),
      detail: dashParts.slice(1).join(" - ").trim(),
      extra: "",
      code,
    };
  }

  return {
    id: `aiq-${idx + 1}`,
    summary: prompt,
    detail: "",
    extra: "",
    code,
  };
}

function renderCommonQuestionItem(item) {
  const detailParts = [item.detail, item.extra].filter(Boolean);
  return `
    <details class="common-question-item">
      <summary>${renderInlineCode(item.summary)}</summary>
      <div class="common-question-body">
        ${detailParts.map((part) => `<p>${renderInlineCode(part)}</p>`).join("")}
        ${item.table ? renderMiniTable(item.table) : ""}
        ${item.code ? renderCodeBlock(item.code, "question-code") : ""}
      </div>
    </details>
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
    const codeContext = parsed.code || item.code_context || "";
    return `
      ${prompt ? `<p class="question-text">${renderInlineCode(prompt)}</p>` : ""}
      ${codeContext ? renderCodeBlock(normalizeNewlines(codeContext || "").trim(), "question-code") : ""}
      ${renderOptions(item.options)}
      ${item.correct ? `<p class="answer-chip">Correct: ${escapeHtml(String(item.correct))}</p>` : ""}
      ${item.explanation ? `<p class="source-summary">${renderInlineCode(item.explanation)}</p>` : ""}
    `;
  }
  if (sourceItem.sourceType === "lecture") {
    const codeExamples = (item.code_examples || [])
      .map(
        (example) => `
          <p><strong>${renderInlineCode(example.description || "Code")}</strong></p>
          ${renderCodeBlock(normalizeNewlines(example.code || "").trim())}
        `
      )
      .join("");
    const lectureQuestion = item.question
      ? `
        <p class="question-text"><strong>Lecture question:</strong> ${renderInlineCode(splitPromptAndCode(item.question).prompt || item.question)}</p>
        ${renderOptions(item.options)}
        ${item.correct ? `<p class="answer-chip">Correct: ${escapeHtml(String(item.correct))}</p>` : ""}
      `
      : "";
    return `
      ${item.explanation ? `<p class="source-summary">${renderInlineCode(item.explanation)}</p>` : ""}
      ${lectureQuestion}
      ${codeExamples}
    `;
  }
  const outText = (item.outputs || []).join("\n");
  return `
    ${item.source ? renderCodeBlock(normalizeNewlines(item.source || "").trim()) : ""}
    ${outText ? `<p><strong>Output:</strong></p>${renderOutputBlock(normalizeNewlines(outText).trim())}` : ""}
  `;
}

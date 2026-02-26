function renderOptions(options = {}) {
  const entries = Object.entries(options);
  if (!entries.length) {
    return "";
  }

  const sorted = entries.sort(([a], [b]) => a.localeCompare(b));
  return `
    <ul class="option-list">
      ${sorted
        .map(
          ([key, value]) => `
            <li class="option-item">
              <strong>${escapeHtml(String(key).toUpperCase())}:</strong>
              ${renderOptionValue(value)}
            </li>
          `
        )
        .join("")}
    </ul>
  `;
}

function renderOptionValue(value) {
  const text = normalizeNewlines(String(value ?? "")).trim();
  if (!text) {
    return '<span class="option-text">-</span>';
  }

  if (text.includes("\n") || isCodeBlockLikely(text)) {
    return `<pre class="option-code">${escapeHtml(text)}</pre>`;
  }

  return `<span class="option-text">${renderInlineCode(text)}</span>`;
}

function renderQuestionContent(question, codeContext = "", label = "") {
  const parsed = splitPromptAndCode(question);
  const parts = [];

  if (parsed.prompt) {
    const labelPrefix = label ? `<strong>${escapeHtml(label)}:</strong> ` : "";
    parts.push(`<p class="question-text">${labelPrefix}${renderInlineCode(parsed.prompt)}</p>`);
  }

  const codeBlocks = [];
  if (parsed.code) {
    codeBlocks.push(parsed.code);
  }

  const contextText = normalizeNewlines(codeContext || "").trim();
  if (contextText && !codeBlocks.some((existing) => existing.trim() === contextText)) {
    codeBlocks.push(contextText);
  }

  codeBlocks.forEach((block) => {
    parts.push(`<pre class="question-code">${escapeHtml(block)}</pre>`);
  });

  if (!parts.length) {
    const fallback = normalizeNewlines(question || "").trim();
    if (fallback) {
      parts.push(`<p class="question-text">${renderInlineCode(fallback)}</p>`);
    }
  }

  return parts.join("");
}

function splitPromptAndCode(rawQuestion) {
  const text = normalizeNewlines(rawQuestion || "").trim();
  if (!text) {
    return { prompt: "", code: "" };
  }

  const chunks = text.split(/\n{2,}/);
  if (chunks.length >= 2) {
    const prompt = chunks[0].trim();
    const tail = chunks.slice(1).join("\n\n").trim();
    if (isCodeBlockLikely(tail)) {
      return { prompt, code: tail };
    }
  }

  const lines = text.split("\n");
  if (lines.length > 1) {
    const codeStart = lines.findIndex((line) => isCodeLineLikely(line));
    if (codeStart > 0) {
      const prompt = lines.slice(0, codeStart).join("\n").trim();
      const code = lines.slice(codeStart).join("\n").trim();
      if (isCodeBlockLikely(code)) {
        return { prompt, code };
      }
    }
  }

  return { prompt: text, code: "" };
}

function isCodeBlockLikely(block) {
  const lines = normalizeNewlines(block || "")
    .split("\n")
    .map((line) => line.trimEnd())
    .filter((line) => line.trim().length > 0);

  if (!lines.length) {
    return false;
  }

  const codeLineCount = lines.filter((line) => isCodeLineLikely(line)).length;
  return codeLineCount >= Math.max(2, Math.ceil(lines.length * 0.45));
}

function isCodeLineLikely(line) {
  const raw = String(line || "");
  const trimmed = raw.trim();
  if (!trimmed) {
    return false;
  }

  if (/^\s{2,}\S/.test(raw)) {
    return true;
  }

  if (/^(for|while|if|elif|else|def|class|return|print|from|import|with|try|except|finally)\b/.test(trimmed)) {
    return true;
  }

  if (/^[A-Za-z_][A-Za-z0-9_]*\s*=\s*/.test(trimmed)) {
    return true;
  }

  if (trimmed.startsWith("#")) {
    return true;
  }

  const syntaxSignals = ["==", "!=", "<=", ">=", "%", "append(", "range(", "len(", "(", ")", "[", "]", "{", "}"];
  if (syntaxSignals.some((signal) => trimmed.includes(signal))) {
    return true;
  }

  return false;
}

function normalizeNewlines(text) {
  return String(text || "").replace(/\r\n/g, "\n").replace(/\r/g, "\n");
}

function renderInlineCode(text) {
  const value = normalizeNewlines(closeUnbalancedBackticks(text || ""));
  if (!value) {
    return "";
  }

  const chunks = value.split("`");
  return chunks
    .map((chunk, idx) => {
      if (idx % 2 === 1) {
        return `<code class="inline-code">${escapeHtml(chunk)}</code>`;
      }
      return escapeHtml(chunk).replace(/\n/g, "<br />");
    })
    .join("");
}

function closeUnbalancedBackticks(text) {
  const value = String(text || "");
  const ticks = (value.match(/`/g) || []).length;
  if (ticks % 2 === 1) {
    return `${value}\``;
  }
  return value;
}

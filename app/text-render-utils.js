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

function sanitizeDisplayText(text) {
  return decodeHtmlEntities(
    normalizeNewlines(String(text || ""))
      .replace(/<br\s*\/?>/gi, "\n")
      .replace(/<\/(ul|ol|p)>/gi, "\n")
      .replace(/<(ul|ol|p)>/gi, "")
      .replace(/<li>/gi, "- ")
      .replace(/<\/li>/gi, "\n")
      .replace(/<\/?(strong|b|em|i|code)>/gi, "")
  );
}

function decodeHtmlEntities(text) {
  return String(text || "")
    .replace(/&nbsp;/gi, " ")
    .replace(/&amp;/gi, "&")
    .replace(/&lt;/gi, "<")
    .replace(/&gt;/gi, ">")
    .replace(/&quot;/gi, '"')
    .replace(/&#39;/gi, "'");
}

function autoBacktickInlineCode(text) {
  const value = String(text || "");
  if (!value) {
    return "";
  }

  const tokenPattern =
    /(\b(?:print|len|range|type|id|set|list|dict|tuple|str|int|float|bool|iter|next|map|filter|sorted|enumerate|zip|None|True|False)\b(?=[\s,.:;)\]])|\b[A-Za-z_][A-Za-z0-9_]*\([^()\n]{0,40}\)|\b[A-Za-z_][A-Za-z0-9_]*\.[A-Za-z_][A-Za-z0-9_]*\b|==|!=|<=|>=|\/\/|\*\*|%|\^)/g;

  return value
    .split("`")
    .map((chunk, idx) => {
      if (idx % 2 === 1) {
        return chunk;
      }
      return chunk.replace(tokenPattern, (match, _group, offset, source) => {
        const before = source[offset - 1] || "";
        const after = source[offset + match.length] || "";
        if (before === "`" || after === "`") {
          return match;
        }
        if (/[A-Za-z0-9_]/.test(before) || /[A-Za-z0-9_]/.test(after)) {
          return match;
        }
        return `\`${match}\``;
      });
    })
    .join("`");
}

function renderInlineCode(text) {
  const value = closeUnbalancedBackticks(
    normalizeMalformedInlineCode(autoBacktickInlineCode(sanitizeDisplayText(text || "")))
  );
  if (!value) {
    return "";
  }

  const chunks = value.split("`");
  return chunks
    .map((chunk, idx) => {
      if (idx % 2 === 1) {
        return `<code class="inline-code">${escapeHtml(chunk)}</code>`;
      }
      return escapeHtml(chunk).replace(/\n+/g, " ");
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

function normalizeMalformedInlineCode(text) {
  return String(text || "")
    .replace(/`e\.g`/g, "e.g")
    .replace(/`\/`/g, "/")
    .replace(/`None`(?=\s+of the above)/g, "None")
    .replace(/`from`(?=\s+(?:the value|right to left|the others|the following))/g, "from");
}

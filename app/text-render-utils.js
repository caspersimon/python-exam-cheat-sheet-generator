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
    return renderCodeBlock(text, "option-code");
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
    parts.push(renderCodeBlock(block, "question-code"));
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
  const value = closeUnbalancedBackticks(normalizeMalformedInlineCode(sanitizeDisplayText(text || "")));
  if (!value) {
    return "";
  }

  const chunks = value.split("`");
  return chunks
    .map((chunk, idx) => {
      if (idx % 2 === 1) {
        return `<code class="inline-code">${escapeHtml(chunk)}</code>`;
      }
      return renderInlineMarkdownDecorations(chunk).replace(/\n+/g, " ");
    })
    .join("");
}

function decodeDisplayEscapes(text) {
  return normalizeNewlines(String(text || ""))
    .replace(/\\n/g, "\n")
    .replace(/\\t/g, "\t");
}

function renderInlineRichText(text, { preserveNewlines = false, decodeEscapes = preserveNewlines } = {}) {
  const rawValue = String(text || "");
  const value = decodeEscapes ? decodeDisplayEscapes(rawValue) : normalizeNewlines(rawValue);
  const lines = normalizeNewlines(value).split("\n");
  return lines.map((line) => renderInlineCode(line)).join("<br>");
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

function renderInlineMarkdownDecorations(text) {
  const escaped = escapeHtml(String(text || ""));
  return escaped.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
}

function splitMarkdownTableRow(line) {
  const value = String(line || "").trim().replace(/^\|/, "").replace(/\|$/, "");
  return value.split("|").map((cell) => cell.trim());
}

function isMarkdownTableSeparator(line) {
  const cells = splitMarkdownTableRow(line);
  return cells.length > 0 && cells.every((cell) => /^:?-{3,}:?$/.test(cell || ""));
}

function compileMarkdownBodyBlocks(markdown) {
  const text = normalizeNewlines(String(markdown || "")).replace(/\n+$/g, "");
  if (!text.trim()) {
    return [];
  }

  const lines = text.split("\n");
  const blocks = [];
  let index = 0;

  while (index < lines.length) {
    const line = lines[index];
    const stripped = line.trim();
    if (!stripped) {
      index += 1;
      continue;
    }

    if (stripped.startsWith("```")) {
      const language = stripped.slice(3).trim();
      const codeLines = [];
      index += 1;
      while (index < lines.length && !lines[index].trim().startsWith("```")) {
        codeLines.push(lines[index]);
        index += 1;
      }
      if (index < lines.length) {
        index += 1;
      }
      blocks.push({ type: "code", language, code: codeLines.join("\n").replace(/\s+$/g, "") });
      continue;
    }

    if (index + 1 < lines.length && stripped.includes("|") && lines[index + 1].includes("|") && isMarkdownTableSeparator(lines[index + 1])) {
      const headers = splitMarkdownTableRow(lines[index]);
      const rows = [];
      index += 2;
      while (index < lines.length && lines[index].trim() && lines[index].includes("|")) {
        rows.push(splitMarkdownTableRow(lines[index]));
        index += 1;
      }
      blocks.push({ type: "table", headers, rows });
      continue;
    }

    const unordered = line.match(/^\s*[-*+]\s+(.*)$/);
    const ordered = line.match(/^\s*\d+[.)]\s+(.*)$/);
    if (unordered || ordered) {
      const isOrdered = Boolean(ordered);
      const items = [unordered ? unordered[1].trim() : ordered[1].trim()];
      index += 1;
      while (index < lines.length) {
        const candidate = lines[index];
        if (!candidate.trim()) {
          break;
        }
        const nextUnordered = candidate.match(/^\s*[-*+]\s+(.*)$/);
        const nextOrdered = candidate.match(/^\s*\d+[.)]\s+(.*)$/);
        if (isOrdered && nextOrdered) {
          items.push(nextOrdered[1].trim());
          index += 1;
          continue;
        }
        if (!isOrdered && nextUnordered) {
          items.push(nextUnordered[1].trim());
          index += 1;
          continue;
        }
        if (/^\s{2,}\S/.test(candidate)) {
          items[items.length - 1] = `${items[items.length - 1]}\n${candidate.trim()}`;
          index += 1;
          continue;
        }
        break;
      }
      blocks.push({ type: "list", ordered: isOrdered, items });
      continue;
    }

    const paragraphLines = [stripped.replace(/^>\s?/, "")];
    index += 1;
    while (index < lines.length) {
      const candidate = lines[index];
      const candidateStripped = candidate.trim();
      if (!candidateStripped) {
        break;
      }
      if (candidateStripped.startsWith("```")) {
        break;
      }
      if (index + 1 < lines.length && candidateStripped.includes("|") && lines[index + 1].includes("|") && isMarkdownTableSeparator(lines[index + 1])) {
        break;
      }
      if (/^\s*[-*+]\s+/.test(candidate) || /^\s*\d+[.)]\s+/.test(candidate)) {
        break;
      }
      paragraphLines.push(candidateStripped.replace(/^>\s?/, ""));
      index += 1;
    }
    blocks.push({ type: "paragraph", text: paragraphLines.join("\n").trim() });
  }

  return blocks.filter(Boolean);
}

function renderMarkdownBodyBlocks(blocks, fallbackMarkdown = "") {
  const safeBlocks = Array.isArray(blocks) && blocks.length ? blocks : compileMarkdownBodyBlocks(fallbackMarkdown);
  if (!safeBlocks.length) {
    const fallback = String(fallbackMarkdown || "").trim();
    return fallback ? `<p>${renderInlineRichText(fallback, { preserveNewlines: true })}</p>` : "";
  }

  return safeBlocks
    .map((block) => {
      if (!block || typeof block !== "object") {
        return "";
      }
      if (block.type === "paragraph") {
        return block.text ? `<p>${renderInlineRichText(block.text, { preserveNewlines: true })}</p>` : "";
      }
      if (block.type === "code") {
        return renderCodeBlock(block.code || "", block.language ? `lang-${block.language}` : "");
      }
      if (block.type === "list") {
        const tag = block.ordered ? "ol" : "ul";
        const items = Array.isArray(block.items) ? block.items : [];
        return `<${tag} class="markdown-list">${items
          .map((item) => `<li>${renderInlineRichText(item, { preserveNewlines: true })}</li>`)
          .join("")}</${tag}>`;
      }
      if (block.type === "table") {
        return renderMiniTable({
          headers: Array.isArray(block.headers) ? block.headers : [],
          rows: Array.isArray(block.rows) ? block.rows : [],
        });
      }
      return "";
    })
    .join("");
}

const PYTHON_KEYWORDS = new Set([
  "and",
  "as",
  "assert",
  "break",
  "class",
  "continue",
  "def",
  "del",
  "elif",
  "else",
  "except",
  "False",
  "finally",
  "for",
  "from",
  "global",
  "if",
  "import",
  "in",
  "is",
  "lambda",
  "None",
  "nonlocal",
  "not",
  "or",
  "pass",
  "raise",
  "return",
  "True",
  "try",
  "while",
  "with",
  "yield",
]);

const PYTHON_BUILTINS = new Set([
  "abs",
  "all",
  "any",
  "bool",
  "dict",
  "enumerate",
  "filter",
  "float",
  "input",
  "int",
  "len",
  "list",
  "map",
  "max",
  "min",
  "next",
  "print",
  "range",
  "round",
  "set",
  "sorted",
  "str",
  "sum",
  "tuple",
  "type",
  "zip",
]);

function wrapCodeToken(className, value) {
  return `<span class="${className}">${escapeHtml(value)}</span>`;
}

function looksLikePythonBlock(text) {
  const value = normalizeNewlines(String(text || "")).trim();
  if (!value) {
    return false;
  }
  if (typeof isCodeBlockLikely === "function" && isCodeBlockLikely(value)) {
    return true;
  }
  return /(def |class |for |while |if |elif |else:|return\b|print\(|import\b|from\b|lambda\b|\.loc\[|\.iloc\[)/.test(value);
}

function highlightPythonCode(text) {
  const source = normalizeNewlines(String(text || ""));
  let output = "";
  let index = 0;
  let expectNamedToken = "";

  while (index < source.length) {
    const rest = source.slice(index);

    const stringMatch = rest.match(
      /^(?:[rRuUbBfF]{0,2})(?:"""[\s\S]*?(?:"""|$)|'''[\s\S]*?(?:'''|$)|"(?:\\.|[^"\\\n])*"?|'(?:\\.|[^'\\\n])*'?)/
    );
    if (stringMatch) {
      output += wrapCodeToken("tok-string", stringMatch[0]);
      index += stringMatch[0].length;
      continue;
    }

    if (source[index] === "#") {
      const newlineIndex = source.indexOf("\n", index);
      const end = newlineIndex === -1 ? source.length : newlineIndex;
      output += wrapCodeToken("tok-comment", source.slice(index, end));
      index = end;
      continue;
    }

    const identifierMatch = rest.match(/^[A-Za-z_][A-Za-z0-9_]*/);
    if (identifierMatch) {
      const identifier = identifierMatch[0];
      if (expectNamedToken === "def") {
        output += wrapCodeToken("tok-function", identifier);
        expectNamedToken = "";
      } else if (expectNamedToken === "class") {
        output += wrapCodeToken("tok-class", identifier);
        expectNamedToken = "";
      } else if (PYTHON_KEYWORDS.has(identifier)) {
        output += wrapCodeToken("tok-keyword", identifier);
        expectNamedToken = identifier === "def" || identifier === "class" ? identifier : "";
      } else if (PYTHON_BUILTINS.has(identifier)) {
        output += wrapCodeToken("tok-builtin", identifier);
      } else if (identifier === "self" || identifier === "cls") {
        output += wrapCodeToken("tok-self", identifier);
      } else {
        output += escapeHtml(identifier);
      }
      index += identifier.length;
      continue;
    }

    const numberMatch = rest.match(/^\d+(?:\.\d+)?/);
    if (numberMatch) {
      output += wrapCodeToken("tok-number", numberMatch[0]);
      index += numberMatch[0].length;
      continue;
    }

    const operatorMatch = rest.match(/^(?:==|!=|<=|>=|:=|->|\*\*|\/\/|[-+*/%=<>[\]{}().,:])/);
    if (operatorMatch) {
      output += wrapCodeToken("tok-operator", operatorMatch[0]);
      index += operatorMatch[0].length;
      continue;
    }

    output += escapeHtml(source[index]);
    index += 1;
  }

  return output;
}

function renderCodeBlock(text, className = "") {
  const value = normalizeNewlines(String(text || "")).replace(/\s+$/g, "").trimEnd();
  if (!value.trim()) {
    return "";
  }

  const classes = ["code-block", "python-code", className].filter(Boolean).join(" ");
  const content = looksLikePythonBlock(value) ? highlightPythonCode(value) : escapeHtml(value);
  return `<pre class="${classes}"><code>${content}</code></pre>`;
}

function renderOutputBlock(text, className = "") {
  const value = normalizeNewlines(String(text || "")).replace(/\s+$/g, "").trimEnd();
  if (!value.trim()) {
    return "";
  }
  const classes = ["output-block", className].filter(Boolean).join(" ");
  return `<pre class="${classes}"><code>${escapeHtml(value)}</code></pre>`;
}

function renderAutoBlock(text, className = "") {
  return looksLikePythonBlock(text) ? renderCodeBlock(text, className) : renderOutputBlock(text, className);
}

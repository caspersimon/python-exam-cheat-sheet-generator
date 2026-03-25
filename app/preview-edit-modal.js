const previewEditModalState = {
  root: null,
  card: null,
  title: null,
  subtitle: null,
  form: null,
  fields: null,
  cancelBtn: null,
  saveBtn: null,
  resolve: null,
  active: false,
  eventsBound: false,
  markdownEditors: [],
  resizeObserver: null,
  resizeRaf: 0,
};

function schedulePreviewMarkdownResize() {
  if (previewEditModalState.resizeRaf) {
    return;
  }
  previewEditModalState.resizeRaf = window.requestAnimationFrame(() => {
    previewEditModalState.resizeRaf = 0;
    resizePreviewMarkdownEditorsToFit();
  });
}

function resizePreviewMarkdownEditorsToFit() {
  if (!Array.isArray(previewEditModalState.markdownEditors) || !previewEditModalState.markdownEditors.length) {
    return;
  }

  previewEditModalState.markdownEditors.forEach((entry) => {
    if (!entry?.editor || typeof entry.editor.setHeight !== "function") {
      return;
    }
    const wrapperHeight = entry.wrapperEl?.clientHeight || 0;
    const labelHeight = entry.labelEl?.offsetHeight || 0;
    const availableHeight = Math.max(300, wrapperHeight - labelHeight - 20);
    entry.editor.setHeight(`${Math.round(availableHeight)}px`);
  });
}

function handlePreviewMarkdownWindowResize() {
  schedulePreviewMarkdownResize();
}

function stopPreviewMarkdownResizeTracking() {
  if (previewEditModalState.resizeObserver) {
    previewEditModalState.resizeObserver.disconnect();
    previewEditModalState.resizeObserver = null;
  }
  window.removeEventListener("resize", handlePreviewMarkdownWindowResize);
  if (previewEditModalState.resizeRaf) {
    window.cancelAnimationFrame(previewEditModalState.resizeRaf);
    previewEditModalState.resizeRaf = 0;
  }
}

function startPreviewMarkdownResizeTracking() {
  stopPreviewMarkdownResizeTracking();
  if (!previewEditModalState.card || !Array.isArray(previewEditModalState.markdownEditors) || !previewEditModalState.markdownEditors.length) {
    return;
  }

  if (typeof ResizeObserver === "function") {
    previewEditModalState.resizeObserver = new ResizeObserver(() => {
      schedulePreviewMarkdownResize();
    });
    previewEditModalState.resizeObserver.observe(previewEditModalState.card);
  }
  window.addEventListener("resize", handlePreviewMarkdownWindowResize);
  schedulePreviewMarkdownResize();
}

function destroyPreviewMarkdownEditors() {
  if (!Array.isArray(previewEditModalState.markdownEditors)) {
    previewEditModalState.markdownEditors = [];
    return;
  }
  previewEditModalState.markdownEditors.forEach((entry) => {
    if (entry?.editor && typeof entry.editor.destroy === "function") {
      try {
        entry.editor.destroy();
      } catch (_error) {
        // Toast UI can throw if the host node was already detached.
      }
    }
  });
  previewEditModalState.markdownEditors = [];
}

function syncPreviewMarkdownEditors() {
  if (!Array.isArray(previewEditModalState.markdownEditors) || !previewEditModalState.markdownEditors.length) {
    return;
  }
  previewEditModalState.markdownEditors.forEach((entry) => {
    if (!entry?.inputEl || !entry.editor || typeof entry.editor.getMarkdown !== "function") {
      return;
    }
    entry.inputEl.value = normalizeNewlines(String(entry.editor.getMarkdown() || ""));
  });
}

function mountPreviewMarkdownEditor(wrapper, field, inputEl) {
  if (!window.toastui?.Editor || !field?.multiline || field.kind !== "markdown") {
    return null;
  }

  const editorHost = document.createElement("div");
  editorHost.className = "preview-edit-markdown-editor";
  wrapper.appendChild(editorHost);
  inputEl.classList.add("preview-edit-markdown-source");
  inputEl.spellcheck = false;

  try {
    const rows = Math.max(8, Number(field.rows) || 12);
    const height = Math.max(320, Math.min(780, rows * 28));
    const editor = new window.toastui.Editor({
      el: editorHost,
      height: `${height}px`,
      initialValue: normalizeNewlines(String(field.value || "")),
      initialEditType: "wysiwyg",
      previewStyle: "vertical",
      hideModeSwitch: false,
      usageStatistics: false,
      autofocus: false,
    });
    previewEditModalState.markdownEditors.push({
      fieldId: field.id,
      inputEl,
      editor,
      wrapperEl: wrapper,
      labelEl: wrapper.querySelector("span"),
    });
    return editor;
  } catch (_error) {
    inputEl.classList.remove("preview-edit-markdown-source");
    editorHost.remove();
    return null;
  }
}

function shouldUseNativePromptEditing() {
  if (window.__useNativePromptEditing === true) {
    return true;
  }
  if (window.__useNativePromptEditing === false) {
    return false;
  }
  return Boolean(window.navigator?.webdriver);
}

function ensurePreviewEditModal() {
  if (previewEditModalState.root) {
    return previewEditModalState;
  }

  const root = document.getElementById("previewEditModal");
  const card = root?.querySelector(".preview-edit-modal-card") || null;
  const title = document.getElementById("previewEditModalTitle");
  const subtitle = document.getElementById("previewEditModalSubtitle");
  const form = document.getElementById("previewEditModalForm");
  const fields = document.getElementById("previewEditModalFields");
  const cancelBtn = document.getElementById("previewEditModalCancelBtn");
  const saveBtn = document.getElementById("previewEditModalSaveBtn");

  if (!root || !title || !subtitle || !form || !fields || !cancelBtn || !saveBtn) {
    return null;
  }

  previewEditModalState.root = root;
  previewEditModalState.card = card;
  previewEditModalState.title = title;
  previewEditModalState.subtitle = subtitle;
  previewEditModalState.form = form;
  previewEditModalState.fields = fields;
  previewEditModalState.cancelBtn = cancelBtn;
  previewEditModalState.saveBtn = saveBtn;

  if (!previewEditModalState.eventsBound) {
    previewEditModalState.eventsBound = true;

    cancelBtn.addEventListener("click", () => closePreviewEditModal(null));
    root.addEventListener("click", (event) => {
      if (event.target === root) {
        closePreviewEditModal(null);
      }
    });

    form.addEventListener("submit", (event) => {
      event.preventDefault();
      syncPreviewMarkdownEditors();
      const values = {};
      fields.querySelectorAll("[data-preview-edit-input='true']").forEach((inputEl) => {
        values[inputEl.dataset.fieldId || ""] = inputEl.value;
      });
      closePreviewEditModal(values);
    });

    document.addEventListener("keydown", (event) => {
      if (!previewEditModalState.active) {
        return;
      }
      if (event.key === "Escape") {
        event.preventDefault();
        closePreviewEditModal(null);
        return;
      }
      if ((event.metaKey || event.ctrlKey) && event.key === "Enter") {
        event.preventDefault();
        previewEditModalState.form?.requestSubmit();
      }
    });
  }

  return previewEditModalState;
}

function closePreviewEditModal(payload) {
  if (!previewEditModalState.active) {
    return;
  }
  previewEditModalState.active = false;
  stopPreviewMarkdownResizeTracking();
  destroyPreviewMarkdownEditors();
  previewEditModalState.root?.classList.add("hidden");
  document.body.classList.remove("preview-edit-modal-open");
  const resolver = previewEditModalState.resolve;
  previewEditModalState.resolve = null;
  resolver?.(payload);
}

function openPreviewEditModal(config) {
  const modal = ensurePreviewEditModal();
  if (!modal) {
    return Promise.resolve(null);
  }

  modal.title.textContent = config.title || "Edit content";
  modal.subtitle.textContent = config.subtitle || "";
  modal.subtitle.classList.toggle("hidden", !config.subtitle);
  modal.saveBtn.textContent = config.saveLabel || "Save";
  stopPreviewMarkdownResizeTracking();
  destroyPreviewMarkdownEditors();
  modal.fields.innerHTML = "";

  let firstInput = null;
  config.fields.forEach((field, index) => {
    const wrapper = document.createElement("label");
    wrapper.className = "preview-edit-field";
    if (field.kind) {
      wrapper.dataset.fieldKind = String(field.kind);
    }

    const label = document.createElement("span");
    label.textContent = field.label || field.id;
    wrapper.appendChild(label);

    const inputEl = field.multiline ? document.createElement("textarea") : document.createElement("input");
    if (!field.multiline) {
      inputEl.type = "text";
    } else {
      inputEl.rows = Math.max(3, Number(field.rows) || 6);
    }
    if (field.placeholder) {
      inputEl.placeholder = field.placeholder;
    }
    if (field.kind === "code") {
      inputEl.spellcheck = false;
    }
    inputEl.dataset.previewEditInput = "true";
    inputEl.dataset.fieldId = field.id;
    inputEl.value = String(field.value || "");
    wrapper.appendChild(inputEl);

    const markdownEditor = mountPreviewMarkdownEditor(wrapper, field, inputEl);
    modal.fields.appendChild(wrapper);

    if (index === 0) {
      if (markdownEditor && typeof markdownEditor.focus === "function") {
        firstInput = {
          focus: () => markdownEditor.focus(),
        };
      } else {
        firstInput = inputEl;
      }
    }
  });

  modal.root.classList.remove("hidden");
  document.body.classList.add("preview-edit-modal-open");

  return new Promise((resolve) => {
    if (modal.resolve) {
      modal.resolve(null);
    }
    modal.resolve = resolve;
    modal.active = true;
    window.requestAnimationFrame(() => {
      startPreviewMarkdownResizeTracking();
      firstInput?.focus();
      firstInput?.select?.();
    });
  });
}

async function requestPreviewEditValues(config) {
  if (!config || !Array.isArray(config.fields) || !config.fields.length) {
    return null;
  }
  if (shouldUseNativePromptEditing()) {
    const values = {};
    for (const field of config.fields) {
      const promptLabel = field.prompt || `Edit ${field.label || field.id}:`;
      const next = window.prompt(promptLabel, String(field.value || ""));
      if (next === null) {
        return null;
      }
      values[field.id] = next;
    }
    return values;
  }
  return openPreviewEditModal(config);
}

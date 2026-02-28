const previewEditModalState = {
  root: null,
  title: null,
  subtitle: null,
  form: null,
  fields: null,
  cancelBtn: null,
  saveBtn: null,
  resolve: null,
  active: false,
  eventsBound: false,
};

function shouldUseNativePromptEditing() {
  return Boolean(window.__useNativePromptEditing) || Boolean(window.navigator?.webdriver);
}

function ensurePreviewEditModal() {
  if (previewEditModalState.root) {
    return previewEditModalState;
  }

  const root = document.getElementById("previewEditModal");
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
    modal.fields.appendChild(wrapper);

    if (index === 0) {
      firstInput = inputEl;
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

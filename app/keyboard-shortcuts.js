function isEditableKeyTarget(target) {
  if (!(target instanceof Element)) {
    return false;
  }
  return Boolean(target.closest("input, textarea, select, [contenteditable='true']"));
}

function isPreviewEditModalOpen() {
  return document.body.classList.contains("preview-edit-modal-open");
}

function bindGlobalKeyboardShortcuts() {
  document.addEventListener("keydown", (event) => {
    if (isSplashVisible()) {
      if (event.key === "Escape") {
        event.preventDefault();
        dismissSplash();
      }
      return;
    }

    if (event.key === "Escape") {
      closeOpenInfoPopovers();
      closeDrawers();
      return;
    }

    if ((event.metaKey || event.ctrlKey) && !event.shiftKey && !event.altKey && event.key.toLowerCase() === "z") {
      if (isEditableKeyTarget(event.target) || isPreviewEditModalOpen()) {
        return;
      }
      event.preventDefault();
      undoLastPreviewChange();
      return;
    }

    if ((event.metaKey || event.ctrlKey) && !event.shiftKey && !event.altKey && event.key.toLowerCase() === "p") {
      if (state.view !== "preview" || isEditableKeyTarget(event.target) || isPreviewEditModalOpen()) {
        return;
      }
      event.preventDefault();
      openPrintView();
    }
  });
}

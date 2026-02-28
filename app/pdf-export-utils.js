function isPdfExportReady() {
  return typeof window.html2canvas === "function" && !!window.jspdf && !!window.jspdf.jsPDF;
}

async function buildPdfDocumentFromPages(pages) {
  const { jsPDF } = window.jspdf;
  const pdf = new jsPDF({ orientation: "portrait", unit: "mm", format: "a4" });
  const renderOptions = getExportRenderOptions();

  for (let idx = 0; idx < pages.length; idx += 1) {
    const page = pages[idx];
    const canvas = await window.html2canvas(page, renderOptions);
    const imageData = canvas.toDataURL("image/png");
    if (idx > 0) {
      pdf.addPage("a4", "portrait");
    }
    pdf.addImage(imageData, "PNG", 0, 0, 210, 297, undefined, "FAST");
  }
  return pdf;
}

async function exportPdf() {
  setView("preview");

  if (!isPdfExportReady()) {
    alert("PDF export libraries not loaded. Use browser Print as fallback.");
    return;
  }

  const pages = getNonEmptyPageElements();
  if (!pages.length) {
    alert("No content to export.");
    return;
  }

  const originalText = refs.exportPdfBtn.textContent;
  refs.exportPdfBtn.textContent = "Exporting...";
  refs.exportPdfBtn.disabled = true;

  try {
    const pdf = await buildPdfDocumentFromPages(pages);
    pdf.save("python-midterm-cheatsheet.pdf");
    showSupportPrompt();
  } finally {
    refs.exportPdfBtn.textContent = originalText;
    refs.exportPdfBtn.disabled = false;
  }
}

async function printGeneratedPdf() {
  setView("preview");

  if (!isPdfExportReady()) {
    alert("PDF export libraries not loaded. Use browser Print as fallback.");
    return;
  }

  const pages = getNonEmptyPageElements();
  if (!pages.length) {
    alert("No content to print.");
    return;
  }

  const originalText = refs.printBtn.textContent;
  refs.printBtn.textContent = "Preparing PDF...";
  refs.printBtn.disabled = true;

  let frame = null;
  let url = "";
  try {
    const pdf = await buildPdfDocumentFromPages(pages);
    url = URL.createObjectURL(pdf.output("blob"));
    frame = document.createElement("iframe");
    frame.style.position = "fixed";
    frame.style.width = "0";
    frame.style.height = "0";
    frame.style.opacity = "0";
    frame.style.pointerEvents = "none";
    document.body.appendChild(frame);

    await new Promise((resolve, reject) => {
      frame.onload = resolve;
      frame.onerror = reject;
      frame.src = url;
    });

    frame.contentWindow?.focus();
    frame.contentWindow?.print();
    window.setTimeout(() => {
      showSupportPrompt();
    }, 600);
  } catch (error) {
    alert(`Could not generate printable PDF: ${error?.message || "unknown error"}`);
  } finally {
    refs.printBtn.textContent = originalText;
    refs.printBtn.disabled = false;
    window.setTimeout(() => {
      if (frame?.parentNode) {
        frame.parentNode.removeChild(frame);
      }
      if (url) {
        URL.revokeObjectURL(url);
      }
    }, 3000);
  }
}

function showSupportPrompt() {
  const message = "Found this useful? Consider supporting the project on Buy Me a Coffee.";
  const confirmed = window.confirm(`${message}\n\nOpen support page now?`);
  if (!confirmed) {
    return;
  }
  window.open("https://buymeacoffee.com/caspersimon", "_blank", "noopener,noreferrer");
}

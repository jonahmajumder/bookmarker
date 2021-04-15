// ---------- PAGE CONTROL ----------

function getPageNum() {
    return PDFViewerApplication.page - 1;
}

function setPageNum(pagenum) {
    PDFViewerApplication.page = pagenum + 1;
    return;
}

function numPages() {
    return PDFViewerApplication.pagesCount;
}

function goToNextPage() {
    app.page = Math.min(app.page + 1, app.pagesCount);
    return;
}

function goToPreviousPage() {
    app.page = Math.max(app.page - 1, 1);
    return;
}

// ---------- SIDEBAR CONTROL ----------

function getSidebarState() {
    return PDFViewerApplication.pdfSidebar.isOpen;
}

function toggleSidebarState() {
    PDFViewerApplication.pdfSidebar.toggle();
    return;
}

function setSidebarState(newstate) {
    if (newstate) {
        PDFViewerApplication.pdfSidebar.open();
    }
    else {
        PDFViewerApplication.pdfSidebar.close();
    }
    return;
}

function showSidebar() {
    setSidebarState(true);
    return;
}

function hideSidebar() {
    setSidebarState(false);
    return;
}

function resetSidebar() {
    PDFViewerApplication.pdfSidebar.reset();
    return;
}

// ---------- ZOOM CONTROL ----------

function resetZoom() {
    PDFViewerApplication.zoomReset();
    return;
}

function setZoomFactor(factor) {
    PDFViewerApplication.pdfViewer.currentScaleValue = factor;
    return;
}

function getZoomFactor(factor) {
    return PDFViewerApplication.pdfViewer.currentScaleValue;
}

function getPageDimensions() {
    var viewer = PDFViewerApplication.pdfViewer.viewer;
    return [viewer.clientWidth, viewer.clientHeight]
}

// ---------- MISC ----------

function getCurrentFileUri() {
    return PDFViewerApplication.url;
}

function hideFileOpener() {
    PDFViewerApplication.appConfig.toolbar.openFile.setAttribute("hidden", "true");
    return;
}

function openFind() {
    PDFViewerApplication.findBar.open();
    PDFViewerApplication.findBar.findField.focus();
    return;
}

// ---------- EXECUTE ON LOAD ----------

function onRender() {
    resetSidebar();
    hideSidebar();
    hideFileOpener();
    resetZoom();
    return;
}

function loadFile(fileuri) {
    PDFViewerApplication.open(fileuri).then(onRender);
    return;
}


// this runs as script (i.e. on file execution)

PDFViewerApplication.pdfViewer.eventBus.on("pagerendered", onRender);
PDFViewerApplication.pdfViewer.eventBus.on("pagesloaded", function() {setPageNum(0);});

// document.onkeydown = function (e) {
//         return false;
// }
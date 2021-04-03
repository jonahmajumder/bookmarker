
function getPageNum() {
    return PDFViewerApplication.page - 1;
}

function setPageNum(pagenum) {
    PDFViewerApplication.page = pagenum + 1;
    return;
}

function getSidebarState() {
    var cl = document.getElementById("sidebarToggle").getAttribute("class");
    return cl.split(" ").some(c => c == "toggled");
}

function setSidebarState(newstate) {
    var state = getSidebarState();
    if (newstate != state) {
        document.getElementById("sidebarToggle").click();
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

function getCurrentFileUri() {
    return PDFViewerApplication.url;
}

function resetZoom() {
    PDFViewerApplication.zoomReset();
    return;
}

// this runs as script (i.e. on file execution)

document.onkeydown = function (e) {
        return false;
}
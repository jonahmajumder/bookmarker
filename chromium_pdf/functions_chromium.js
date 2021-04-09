function getPageNum() {
    return window.viewer.viewport_.getMostVisiblePage();
}

function setPageNum(pagenum) {
    window.viewer.viewport_.goToPage(pagenum);
    return;
}

function goToPreviousPage() {
    window.viewer.viewport_.goToPreviousPage();
    return;
}

function goToNextPage() {
    window.viewer.viewport_.goToNextPage();
    return;
}

function getCurrentFileUri() {
    return window.viewer.plugin_.src;
}

function fitToPage() {
    window.viewer.viewport_.fitToPage();
    return;
}

function fitToHeight() {
    window.viewer.viewport_.fitToHeight();
    return;
}

function fitToWidth() {
    window.viewer.viewport_.fitToWidth();
    return;
}

function getZoom() {
    return window.viewer.viewport_.getZoom();
}

function setZoom(factor) {
    window.viewer.viewport_.setZoom(factor);
    return
}

// this runs as script (i.e. on file execution)

document.onkeydown = function (e) {
        return false;
}
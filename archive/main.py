# main.py

import sys
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QMenu, QFileDialog
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings, QWebEngineScript

from pathlib import Path
from urllib.parse import urlparse, unquote

from rebookmark import parseBookmarksToModel, BookmarkItem, writeModelToFile

with open('functions.js', 'r') as f:
    jsSource = f.read()

def asURI(localpath):
    p = Path(localpath)
    assert p.exists()
    return p.absolute().as_uri()

def fromURI(fileuri):
    fullpath = unquote(urlparse(fileuri).path)
    return fullpath

class PDFApp(QMainWindow):

    VIEWER = 'pdfjs/web/viewer.html'

    def __init__(self):
        QtWidgets.QDialog.__init__(self)

        self.ui = uic.loadUi('main.ui')

        self.setupTreeView()
        self.addWebViewer()

        self.connectMenuActions()

        if len(sys.argv) > 1:
            p = Path(sys.argv[1])
            if p.exists() and p.suffix == '.pdf':
                self.loadPdf('sample_toc.pdf')

        self.ui.setWindowTitle('PDF App')

        self.ui.show()
        self.ui.raise_()

    def setupTreeView(self):
        self.ui.treeView.setHeaderHidden(True)
        self.ui.treeView.setDragDropMode(self.ui.treeView.InternalMove)
        self.ui.treeView.setAlternatingRowColors(True)

        self.treeContextMenu = QMenu(self)
        self.treeContextMenu.addAction('Rename')
        self.treeContextMenu.addAction('Delete')
        self.treeContextMenu.addAction('Add')

        self.ui.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.treeView.customContextMenuRequested.connect(self.treeItemRightClick)

        self.ui.treeView.doubleClicked.connect(self.treeItemDoubleClick)

    def treeItemDoubleClick(self, index):
        pg = index.model().itemFromIndex(index).data(Qt.UserRole)
        self.setPageNum(pg)

    def treeItemRightClick(self, point):
        index = self.ui.treeView.indexAt(point)
        if index is not None:
            action = self.treeContextMenu.exec_(self.ui.treeView.viewport().mapToGlobal(point))
            self.parseAction(action, index)

    def parseAction(self, action, index):
        if action is not None:
            if action.text() == 'Rename' and index is not None:
                self.renameBookmark(index)
            elif action.text() == 'Delete' and index is not None:
                self.deleteBookmark(index)
            elif action.text() == 'Add':
                self.getPageNum(self.addBookmark)

    def renameBookmark(self, index):
        item = index.model().itemFromIndex(index)
        item.setEditable(True)
        self.ui.treeView.edit(index)
        item.setEditable(False)

    def deleteBookmark(self, index):
        model = index.model()
        item = model.itemFromIndex(index)
        model.removeRow(item.row())

    def addBookmark(self, currentpage):
        newBookmark = BookmarkItem('New Bookmark', currentpage)
        self.ui.treeView.model().appendRow(newBookmark)

        self.renameBookmark(newBookmark.index())

    def addWebViewer(self):
        sp = QSizePolicy()
        sp.setHorizontalPolicy(QSizePolicy.Expanding)
        sp.setVerticalPolicy(QSizePolicy.Expanding)
        sp.setHorizontalStretch(3)

        self.browser = QWebEngineView()
        self.browser.setSizePolicy(sp)

        self.browser.loadFinished.connect(self.onPdfLoad)

        self.ui.hLayout.addWidget(self.browser)

    def connectMenuActions(self):
        self.ui.actionOpen.triggered.connect(self.selectOpenFile)
        self.ui.actionSaveAs.triggered.connect(self.selectSaveAsFile)
        self.ui.actionQuit.triggered.connect(lambda: QApplication.instance().quit())

    def selectOpenFile(self):
        chosenFile, _ = QFileDialog.getOpenFileName(self, 'Open File', '~', 'PDF files (*.pdf)')
        if len(chosenFile) > 0:
            self.loadPdf(chosenFile)

    def selectSaveAsFile(self):
        chosenFile, _ = QFileDialog.getSaveFileName(self, 'Save New PDF', '', 'PDF files (*.pdf)')
        if len(chosenFile) > 0:
            self.saveAsPdf(chosenFile)

    def getCurrentFile(self, callback):
        convertToPath = lambda uri: callback(fromURI(uri))
        self.browser.page().runJavaScript('getCurrentFileUri()', convertToPath)

    def loadPdf(self, pdffile):
        self.loadPdfView(pdffile)
        self.loadPdfBookmarks(pdffile)

    def loadPdfView(self, pdffile):
        pdfURI = asURI(pdffile)
        viewerURI = asURI(self.VIEWER)
        self.browser.load(QUrl.fromUserInput('{0}?file={1}'.format(viewerURI, pdfURI)))

    def onPdfLoad(self, loadSuccessful):
        assert loadSuccessful

        self.browser.page().runJavaScript(jsSource)
        self.browser.page().runJavaScript("setSidebarState(false);")
        self.ui.treeView.setEnabled(True)

    def loadPdfBookmarks(self, pdffile):
        model = parseBookmarksToModel(pdffile)
        self.ui.treeView.setModel(model)
        self.ui.treeView.setEnabled(False)

    def saveAsPdf(self, newfile):
        model = self.ui.treeView.model()

        self.getCurrentFile(lambda file: writeModelToFile(model, file, newfile))

    def getPageNum(self, callback):
        ret = self.browser.page().runJavaScript('getPageNum()', callback)

    def setPageNum(self, pagenum):
        # self.getPageNum(print)
        self.browser.page().runJavaScript('setPageNum({})'.format(pagenum))

app = QApplication(sys.argv)
window = PDFApp()

if __name__ == '__main__':
    sys.exit(app.exec_())
# main.py

import sys
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QMenu, QFileDialog, QMessageBox
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings, QWebEngineScript

from pathlib import Path
from urllib.parse import urlparse, unquote

from viewer import PDFView
from bookmarks import BookmarkModel, BookmarkItem
from locations import ResourceFile, DOCUMENTS

DEBUG = True
DEBUG_PORT = 5000

print(getattr(sys, '_MEIPASS', False))

class PDFApp(QMainWindow):

    def __init__(self):
        QtWidgets.QDialog.__init__(self)

        self.ui = uic.loadUi(ResourceFile('main.ui'))
        self.ui.setWindowTitle('PDF Bookmarker')

        self.setupTreeView()
        self.addWebViewer()

        self.connectMenuActions()

        toLoad = None
        if len(sys.argv) > 1:
            p = Path(sys.argv[1])
            if p.exists() and p.suffix == '.pdf':
                toLoad = str(p)

        if toLoad is not None:
            self.loadPdf(toLoad)
        else:
            self.selectOpenFile()

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

        self.ui.treeView.clicked.connect(self.treeItemClick)
        self.ui.treeView.doubleClicked.connect(self.treeItemDoubleClick)

    def treeItemClick(self, index):
        pg = index.model().itemFromIndex(index).data(Qt.UserRole)
        self.browser.setPageNum(pg)

    def treeItemDoubleClick(self, index):
        self.renameBookmark(index)

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
                self.addBookmark()

    def renameBookmark(self, index):
        item = index.model().itemFromIndex(index)
        item.setEditable(True)
        self.ui.treeView.edit(index)
        item.setEditable(False)

    def deleteBookmark(self, index):
        model = index.model()
        item = model.itemFromIndex(index)
        model.removeRow(item.row())

    def deleteAllBookmarks(self):
        if QMessageBox.critical(self.ui, 'Confirm', 'Are you sure you want to delete all bookmarks?',
            QMessageBox.Cancel | QMessageBox.Ok, QMessageBox.Ok) == QMessageBox.Ok:
            model = self.ui.treeView.model()
            model.removeRows(0, model.rowCount())

    def addBookmark(self):
        currentpage = self.browser.getPageNum()
        newBookmark = BookmarkItem('New Bookmark', currentpage)
        self.ui.treeView.model().appendRow(newBookmark)

        self.renameBookmark(newBookmark.index())

    def addWebViewer(self):
        self.browser = PDFView()
        self.ui.documentLayout.addWidget(self.browser)

        self.ui.splitter.setStretchFactor(0,2)
        self.ui.splitter.setStretchFactor(1,3)

        self.splitterState = self.ui.splitter.saveState()

    def connectMenuActions(self):
        self.ui.actionOpen.triggered.connect(self.selectOpenFile)
        self.ui.actionSave.triggered.connect(self.selectSaveFile)
        self.ui.actionSaveAs.triggered.connect(self.selectSaveAsFile)
        self.ui.actionQuit.triggered.connect(lambda: QApplication.instance().quit())

        self.ui.actionFind.triggered.connect(self.findInPdf)
        self.ui.actionShowOutline.setChecked(True)
        self.ui.actionShowOutline.toggled.connect(self.toggleOutline)

        self.ui.actionNewBookmark.triggered.connect(self.addBookmark)
        self.ui.actionClearBookmarks.triggered.connect(self.deleteAllBookmarks)
        self.ui.actionImportBookmarks.triggered.connect(self.selectImportFile)
        self.ui.actionExportBookmarks.triggered.connect(self.selectExportFile)

        self.enableMenus(False)

    def enableMenus(self, state):
        self.ui.actionSave.setEnabled(state)
        self.ui.actionSaveAs.setEnabled(state)
        self.ui.actionNewBookmark.setEnabled(state)
        self.ui.actionClearBookmarks.setEnabled(state)
        self.ui.actionImportBookmarks.setEnabled(state)
        self.ui.actionExportBookmarks.setEnabled(state)
        self.ui.actionFind.setEnabled(state)
        self.ui.actionShowOutline.setEnabled(state)

    def findInPdf(self):
        self.browser.openFind()

    def toggleOutline(self, checkState):
        if checkState and self.ui.splitter.sizes()[0] == 0:
            self.ui.splitter.restoreState(self.splitterState)
        elif not checkState and self.ui.splitter.sizes()[0] != 0:
            self.splitterState = self.ui.splitter.saveState()
            self.ui.splitter.moveSplitter(0, 1)

    def selectOpenFile(self):
        chosenFile, _ = QFileDialog.getOpenFileName(self, 'Open File', DOCUMENTS, 'PDF files (*.pdf)')
        if len(chosenFile) > 0:
            self.loadPdf(chosenFile)

    def selectSaveAsFile(self):
        filedir = self.browser.getCurrentDir()
        chosenFile, _ = QFileDialog.getSaveFileName(self, 'Save New PDF', filedir, 'PDF files (*.pdf)')
        if len(chosenFile) > 0:
            self.savePdf(chosenFile)

    def selectSaveFile(self):
        file = self.browser.getCurrentFile()
        self.savePdf(file)
        self.browser.reload()

    def selectImportFile(self):
        filedir = self.browser.getCurrentDir()
        chosenFile, _ = QFileDialog.getSaveFileName(self, 'Import Bookmarks', filedir, 'JSON files (*.json)')
        if len(chosenFile) > 0:
            self.importBookmarks(chosenFile)

    def selectExportFile(self):
        filedir = self.browser.getCurrentDir()
        chosenFile, _ = QFileDialog.getSaveFileName(self, 'Export Bookmarks', filedir, 'JSON files (*.json)')
        if len(chosenFile) > 0:
            self.exportBookmarks(chosenFile)

    def loadPdf(self, pdffile):
        self.ui.setWindowTitle(Path(pdffile).name)
        self.browser.loadPdf(pdffile)
        model = BookmarkModel(pdffile)
        self.ui.treeView.setModel(model)

        self.enableMenus(True)

    def savePdf(self, newfile):
        model = self.ui.treeView.model()
        file = self.browser.getCurrentFile()
        model.writeToPdfFile(file, newfile)

    def importBookmarks(self, file):
        pass

    def exportBookmarks(self, file):
        model = self.ui.treeView.model()
        model.exportJsonBookmarks(file)

if DEBUG:
    sys.argv.append('--remote-debugging-port={}'.format(DEBUG_PORT))

app = QApplication(sys.argv)
gui = PDFApp()

if __name__ == '__main__':
    sys.exit(app.exec_())
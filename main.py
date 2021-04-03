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

class PDFApp(QMainWindow):

    def __init__(self):
        QtWidgets.QDialog.__init__(self)

        self.ui = uic.loadUi('main.ui')
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
        sp = QSizePolicy()
        sp.setHorizontalPolicy(QSizePolicy.Expanding)
        sp.setVerticalPolicy(QSizePolicy.Expanding)
        sp.setHorizontalStretch(3)

        self.browser = PDFView()
        self.browser.setSizePolicy(sp)

        self.ui.hLayout.addWidget(self.browser)

    def connectMenuActions(self):
        self.ui.actionOpen.triggered.connect(self.selectOpenFile)
        self.ui.actionSave.triggered.connect(self.selectSaveFile)
        self.ui.actionSaveAs.triggered.connect(self.selectSaveAsFile)
        self.ui.actionQuit.triggered.connect(lambda: QApplication.instance().quit())

        self.ui.actionNewBookmark.triggered.connect(self.addBookmark)
        self.ui.actionClearBookmarks.triggered.connect(self.deleteAllBookmarks)

    def selectOpenFile(self):
        chosenFile, _ = QFileDialog.getOpenFileName(self, 'Open File', '~', 'PDF files (*.pdf)')
        if len(chosenFile) > 0:
            self.loadPdf(chosenFile)

    def selectSaveAsFile(self):
        chosenFile, _ = QFileDialog.getSaveFileName(self, 'Save New PDF', '', 'PDF files (*.pdf)')
        if len(chosenFile) > 0:
            self.savePdf(chosenFile)

    def selectSaveFile(self):
        file = self.browser.getCurrentFile()
        self.savePdf(file)
        self.browser.reload()

    def loadPdf(self, pdffile):
        self.ui.setWindowTitle(Path(pdffile).name)
        self.browser.loadPdf(pdffile)
        model = BookmarkModel(pdffile)
        self.ui.treeView.setModel(model)

    def savePdf(self, newfile):
        model = self.ui.treeView.model()
        file = self.browser.getCurrentFile()
        model.writeToFile(file, newfile)

app = QApplication(sys.argv)
gui = PDFApp()

if __name__ == '__main__':
    sys.exit(app.exec_())
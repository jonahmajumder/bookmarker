# main.py

import sys
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QSizePolicy, QMenu, QMenuBar, QFileDialog, QMessageBox, qApp
from PyQt5.QtCore import QUrl, Qt, QEvent, QChildEvent
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings, QWebEngineScript

from pathlib import Path
from urllib.parse import urlparse, unquote

from viewer import PDFView
from bookmarks import BookmarkModel, BookmarkItem
from locations import ResourceFile, DOCUMENTS
from qevents import EventObj

class PDFAppWindow(QWidget):

    def __init__(self, toLoad=None, **kwargs):
        QtWidgets.QDialog.__init__(self)

        self.ui = uic.loadUi(ResourceFile('mainwidget.ui'))
        self.ui.setWindowTitle('PDF Bookmarker')

        self.setupTreeView()
        self.addWebViewer()

        self.connectMenuActions()

        self.open = True

        if self.isValidPdf(toLoad):
            self.loadPdf(toLoad)
            self.ui.show()
            self.ui.raise_()
        else:
            chosen = self.selectOpenFile()
            if not chosen:
                self.closeFcn()
            else:
                self.ui.show()
                self.ui.raise_()

    @staticmethod
    def isValidPdf(file):
        if file is None:
            return False

        p = Path(file)
        if p.exists() and p.suffix == '.pdf':
            return True
        else:
            return False

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
        self.ui.actionClose.triggered.connect(self.closeFcn)
        self.ui.actionQuit.triggered.connect(sys.exit)

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

    def closeFcn(self):
        self.close()
        self.open = False
        if self in QApplication.instance().windows:
            QApplication.instance().windows.remove(self)

    def event(self, event):
        print('(Window event) {}'.format(EventObj(event)))
        # if isinstance(event, QChildEvent):
        #     print(event.child())

        return super(PDFAppWindow, self).event(event)

    def selectOpenFile(self, newWindow=True):
        chosenFile, _ = QFileDialog.getOpenFileName(self, 'Open File', DOCUMENTS, 'PDF files (*.pdf)')
        if len(chosenFile) > 0:
            if self.browser.isFileLoaded():
                QApplication.instance().newWindow(chosenFile)
            else:
                self.loadPdf(chosenFile)
            return True
        else:
            return False

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

class HandlerApp(QApplication):
    """
    docstring for HandlerApp
    """
    DEBUG_PORT = 5000
    LOCATION = DOCUMENTS

    def __init__(self, *args, **kwargs):
        toLoad = args[0][1] if len(args[0]) > 1 else None

        if kwargs.pop('web_debug', False):
            args[0].append('--remote-debugging-port={}'.format(self.DEBUG_PORT))
        super(HandlerApp, self).__init__(*args, **kwargs)

        self.createMenu()

        self.windows = []
        # if not self.anyWindows():
        #     self.newWindow(toLoad)

        # if not self.anyWindows():
        #     sys.exit()

    def createMenu(self):
        self.menuBar = QMenuBar()
        self.fileMenu = self.menuBar.addMenu('File')
        self.fileMenu.addAction('Open', self.selectOpenFile, 'Ctrl+O')

    def selectOpenFile(self):
        chosenFile, _ = QFileDialog.getOpenFileName(None, 'Open File', self.LOCATION, 'PDF files (*.pdf)')
        if len(chosenFile) > 0:
            self.newWindow(chosenFile)

    def event(self, event):
        # print('(Application event) {}'.format(EventObj(event))
        if event.type() == QEvent.FileOpen:
            self.newWindow(event.file())
        
        return super(HandlerApp, self).event(event)

    def newWindow(self, toLoad=None):
        w = PDFAppWindow(toLoad)
        if w.open:
            self.windows.append(w)

    def anyWindows(self):
        return len(self.windows) > 0

app = HandlerApp(sys.argv, web_debug=False)

if __name__ == '__main__':
    # gui = PDFAppWindow(sys.argv[1])
    sys.exit(app.exec_())
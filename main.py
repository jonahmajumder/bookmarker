# main.py

import sys
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow,
    QVBoxLayout, QTreeView, QLabel, QSplitter,
    QSizePolicy, QMenu, QMenuBar, QStyle,
    QFileDialog, QMessageBox, qApp
)
from PyQt5.QtCore import QUrl, Qt, QEvent, QSize, QMargins
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings, QWebEngineScript

from pathlib import Path
from urllib.parse import urlparse, unquote

from viewer import PDFView
from bookmarks import BookmarkModel, BookmarkItem
from locations import ResourceFile, DOCUMENTS
from events import EventObj

class PDFAppWindow(QWidget):

    def __init__(self, toLoad, **kwargs):
        super(PDFAppWindow, self).__init__()

        self.setWindowTitle('PDF Bookmarker')

        self.setupUi()

        if self.isValidPdf(toLoad):
            self.loadPdf(toLoad)
            self.configureSize()
            self.show()
            self.raise_()
        else:
            raise Exception('Invalid PDF file!')

        # print(QApplication.instance().anyWindows())

    @staticmethod
    def isValidPdf(file):
        if file is None:
            return False

        p = Path(file)
        if p.exists() and p.suffix == '.pdf':
            return True
        else:
            return False

    def setupUi(self):
        self.outlineLayout = QVBoxLayout()
        self.outlineLabel = QLabel('Document Outline')
        self.outlineLabel.setAlignment(Qt.AlignCenter)
        self.treeView = QTreeView()
        self.treeView.setHeaderHidden(True)
        self.treeView.setDragDropMode(self.treeView.InternalMove)
        self.treeView.setAlternatingRowColors(True)

        self.treeContextMenu = QMenu(self)
        self.treeContextMenu.addAction('Rename')
        self.treeContextMenu.addAction('Delete')
        self.treeContextMenu.addAction('Add')

        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.treeItemRightClick)
        self.treeView.clicked.connect(self.treeItemClick)
        self.treeView.doubleClicked.connect(self.renameBookmark)

        self.outlineLayout.addWidget(self.outlineLabel)
        self.outlineLayout.addWidget(self.treeView)

        self.documentLayout = QVBoxLayout()
        self.browser = PDFView()
        self.documentLayout.addWidget(self.browser)

        self.splitter = QSplitter()
        self.leftWidget = QWidget()
        self.leftWidget.setLayout(self.outlineLayout)
        self.splitter.addWidget(self.leftWidget)
        self.rightWidget = QWidget()
        self.rightWidget.setLayout(self.documentLayout)
        self.splitter.addWidget(self.rightWidget)
        self.splitter.setStretchFactor(0,2)
        self.splitter.setStretchFactor(1,3)
        w = self.geometry().width()
        self.splitterState = self.splitter.saveState()

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(QMargins(5,5,5,5))
        self.mainLayout.addWidget(self.splitter)
        self.setLayout(self.mainLayout)

    def configureSize(self):

        pdfdims = self.treeView.model().dimensions
        fulldims = QSize(round(pdfdims[0])*3//2, round(pdfdims[1]))
        available = QApplication.desktop().availableGeometry()
        fulldims.scale(available.size(), Qt.KeepAspectRatio)

        self.setGeometry(
            QStyle.alignedRect(
                Qt.LeftToRight,
                Qt.AlignCenter,
                fulldims,
                available # rectangle to center to
            )
        )

        w = fulldims.width()
        self.splitter.setSizes([w//3+20, w*2//3])

    def treeItemClick(self, index):
        pg = index.model().itemFromIndex(index).data(Qt.UserRole)
        self.browser.setPageNum(pg)

    def treeItemRightClick(self, point):
        index = self.treeView.indexAt(point)
        if index is not None:
            action = self.treeContextMenu.exec_(self.treeView.viewport().mapToGlobal(point))
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
        self.treeView.edit(index)
        item.setEditable(False)

    def deleteBookmark(self, index):
        model = index.model()
        item = model.itemFromIndex(index)
        model.removeRow(item.row())

    def deleteAllBookmarks(self):
        if QMessageBox.critical(self, 'Confirm', 'Are you sure you want to delete all bookmarks?',
            QMessageBox.Cancel | QMessageBox.Ok, QMessageBox.Ok) == QMessageBox.Ok:
            model = self.treeView.model()
            model.removeRows(0, model.rowCount())

    def addBookmark(self):
        currentpage = self.browser.getPageNum()
        newBookmark = BookmarkItem('New Bookmark', currentpage)
        self.treeView.model().appendRow(newBookmark)

        self.renameBookmark(newBookmark.index())

    def findInPdf(self):
        self.browser.openFind()

    def toggleOutline(self, checkState):
        if checkState and self.splitter.sizes()[0] == 0:
            self.splitter.restoreState(self.splitterState)
        elif not checkState and self.splitter.sizes()[0] != 0:
            self.splitterState = self.splitter.saveState()
            self.splitter.moveSplitter(0, 1)

    def closeFcn(self):
        QApplication.instance().currentWindow = None
        QApplication.instance().enableMenus(False)
        if self in QApplication.instance().windowList:
            QApplication.instance().windowList.remove(self)

        self.deleteLater()

    def event(self, event):
        # ev = EventObj(event)
        # print('(Window event) {}'.format(ev))
        if event.type() == QEvent.Close:
            self.closeFcn()
        elif event.type() == QEvent.WindowActivate:
            QApplication.instance().currentWindow = self
            QApplication.instance().enableMenus(True)

        return super(PDFAppWindow, self).event(event)

    def selectOpenFile(self):
        QApplication.instance().selectOpenFile()

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
        chosenFile, _ = QFileDialog.getOpenFileName(self, 'Import Bookmarks', filedir, 'JSON files (*.json)')
        if len(chosenFile) > 0:
            self.importBookmarks(chosenFile)

    def selectExportFile(self):
        filedir = self.browser.getCurrentDir()
        chosenFile, _ = QFileDialog.getSaveFileName(self, 'Export Bookmarks', filedir, 'JSON files (*.json)')
        if len(chosenFile) > 0:
            self.exportBookmarks(chosenFile)

    def loadPdf(self, pdffile):
        self.setWindowTitle(Path(pdffile).name)
        self.browser.loadPdf(pdffile)
        model = BookmarkModel(pdffile)
        self.treeView.setModel(model)

    def savePdf(self, newfile):
        model = self.treeView.model()
        file = self.browser.getCurrentFile()
        model.writeToPdfFile(file, newfile)

    def importBookmarks(self, file):
        model = self.treeView.model()
        model.initFromJson(file)

    def exportBookmarks(self, file):
        model = self.treeView.model()
        model.exportJsonBookmarks(file)

class HandlerApp(QApplication):
    """
    docstring for HandlerApp
    """
    DEBUG_PORT = 5000
    LOCATION = DOCUMENTS
    LoadedEvent = QEvent.User + 1

    def __init__(self, *args, **kwargs):
        sysargs = args[0]
        toLoad = sysargs[1] if len(sysargs) > 1 else None

        if kwargs.pop('web_debug', False):
            args[0].append('--remote-debugging-port={}'.format(self.DEBUG_PORT))
        super(HandlerApp, self).__init__(*args, **kwargs)

        self.setQuitOnLastWindowClosed(False)
        self.lastWindowClosed.connect(lambda: 'last window closed!')

        self.windowList = []
        self.currentWindow = None

        self.createMenus()

        if PDFAppWindow.isValidPdf(toLoad):
            self.newWindow(toLoad)

        self.processEvents()

        # send event that will fire after 
        self.postEvent(self, QEvent(self.LoadedEvent), Qt.LowEventPriority)

        # if not self.anyWindows():
        #     chosen = self.selectOpenFile()
            # if not chosen:
            #     sys.exit()

    def createMenus(self):
        self.menuBar = QMenuBar()

        self.menuFile = self.menuBar.addMenu('File')
        self.actionOpen = self.menuFile.addAction('Open...', self.selectOpenFile, 'Ctrl+O')
        self.actionOpen.setToolTip('Open New PDF')
        self.actionSave = self.menuFile.addAction('Save', self.selectSaveFile, 'Ctrl+S')
        self.actionSave.setToolTip('Save (Overwrite) PDF with Bookmarks')
        self.actionSaveAs = self.menuFile.addAction('Save As...', self.selectSaveAsFile, 'Ctrl+Shift+S')
        self.actionSaveAs.setToolTip('Save (New) PDF with Bookmarks')
        self.actionClose = self.menuFile.addAction('Close Window', self.closeFcn, 'Ctrl+W')
        self.actionClose.setToolTip('Close Current PDF')
        self.menuFile.addSeparator()
        self.actionQuit = self.menuFile.addAction('Quit', sys.exit, 'Ctrl+Alt+Q')
        self.actionQuit.setToolTip('Quit Application (Close All Windows)')

        self.menuEdit = self.menuBar.addMenu('Edit')
        self.actionFind = self.menuEdit.addAction('Find...', self.findInPdf, 'Ctrl+F')
        self.actionFind.setToolTip('Find in PDF')

        self.menuView = self.menuBar.addMenu('View')
        self.actionShowOutline = self.menuView.addAction('Show Outline')
        self.actionShowOutline.toggled.connect(self.toggleOutline)
        self.actionShowOutline.setShortcut('Ctrl+Shift+O')
        self.actionShowOutline.setCheckable(True)
        self.actionShowOutline.setChecked(True)
        self.actionShowOutline.setToolTip('Show/Hide Outline Sidebar')
        self.menuView.addSeparator()

        self.menuBookmark = self.menuBar.addMenu('Bookmarks')
        self.actionNewBookmark = self.menuBookmark.addAction('New Bookmark', self.addBookmark, 'Ctrl+B') # fcn
        self.actionNewBookmark.setToolTip('Bookmark Current Page')
        self.actionClearBookmarks = self.menuBookmark.addAction('Clear Bookmarks', self.deleteAllBookmarks, 'Ctrl+Shift+D') # fcn
        self.actionClearBookmarks.setToolTip('Remove All Bookmarks')
        self.menuBookmark.addSeparator()
        self.actionImportBookmarks = self.menuBookmark.addAction('Import Bookmarks', self.selectImportFile, 'Ctrl+I') # fcn
        self.actionImportBookmarks.setToolTip('Import Bookmarks from File')
        self.actionExportBookmarks = self.menuBookmark.addAction('Export Bookmarks', self.selectExportFile, 'Ctrl+E') # fcn
        self.actionExportBookmarks.setToolTip('Export Bookmarks to File')

        self.enableMenus(False)

    def enableMenus(self, state):
        self.actionSave.setEnabled(state)
        self.actionSaveAs.setEnabled(state)
        self.actionClose.setEnabled(state)
        self.actionNewBookmark.setEnabled(state)
        self.actionClearBookmarks.setEnabled(state)
        self.actionImportBookmarks.setEnabled(state)
        self.actionExportBookmarks.setEnabled(state)
        self.actionFind.setEnabled(state)
        self.actionShowOutline.setEnabled(state)

    def selectOpenFile(self):
        chosenFile, _ = QFileDialog.getOpenFileName(None, 'Open File', self.LOCATION, 'PDF files (*.pdf)')
        if len(chosenFile) > 0:
            self.newWindow(chosenFile)
            return True
        else:
            return False

    def selectSaveFile(self):
        if self.currentWindow is not None:
            self.currentWindow.selectSaveFile()

    def selectSaveAsFile(self):
        if self.currentWindow is not None:
            self.currentWindow.selectSaveAsFile()

    def closeFcn(self):
        if self.currentWindow is not None:
            self.currentWindow.closeFcn()

    def findInPdf(self):
        if self.currentWindow is not None:
            self.currentWindow.findInPdf()

    def toggleOutline(self, checkState):
        if self.currentWindow is not None:
            self.currentWindow.toggleOutline(checkState)

    def addBookmark(self):
        if self.currentWindow is not None:
            self.currentWindow.addBookmark()

    def deleteAllBookmarks(self):
        if self.currentWindow is not None:
            self.currentWindow.deleteAllBookmarks()

    def selectImportFile(self):
        if self.currentWindow is not None:
            self.currentWindow.selectImportFile()

    def selectExportFile(self):
        if self.currentWindow is not None:
            self.currentWindow.selectExportFile()

    def event(self, event):
        # print('(Application event) {}'.format(EventObj(event)))
        if event.type() == QEvent.FileOpen:
            if PDFAppWindow.isValidPdf(event.file()):
                self.newWindow(event.file())
        elif event.type() == self.LoadedEvent:
            # print('Loaded Event - {} windows'.format(len(self.windows())))
            if not self.anyWindows():
                print('Loaded Event received with no windows, opening new window.')
                chosen = self.selectOpenFile()
        
        return super(HandlerApp, self).event(event)

    def newWindow(self, file):
        self.windowList.append(PDFAppWindow(file))

    def windows(self):
        return [w for w in self.topLevelWidgets() if isinstance(w, PDFAppWindow)]

    def anyWindows(self):
        return len(self.windows()) > 0

app = HandlerApp(sys.argv, web_debug=False)

if __name__ == '__main__':
    # gui = PDFAppWindow(sys.argv[1])
    sys.exit(app.exec_())
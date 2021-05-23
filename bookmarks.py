from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import Destination
from PyPDF2.utils import PdfReadError

from PyQt5.Qt import QStandardItemModel, QStandardItem, Qt

import os
import json
from tempfile import NamedTemporaryFile

class BookmarkItem(QStandardItem):
    def __init__(self, title='', page=None):
        super().__init__()

        self.setEditable(False)
        self.setText(title)
        self.setPage(page)

    def page(self):
        return self.data(Qt.UserRole)

    def setPage(self, page):
        self.setData(page, Qt.UserRole)

    def toDict(self):
        return {'text': self.text(), 'page': self.page(), 'children': []}

    @staticmethod
    def fromDict(itemDict):
        return BookmarkItem(itemDict['text'], itemDict['page'])


class BookmarkModel(QStandardItemModel):
    """
    subclass of QStandardItemModel to represent bookmark tree
    """
    def __init__(self, pdffile):
        super().__init__()

        self.reader = None
        self.writer = None

        self.initFromPdfFile(pdffile)

    def clear(self):
        self.removeRows(0, self.rowCount())

    def addBookmarkNodeFromDest(self, item, parent=None, lastBookmark=None):
        if isinstance(item, Destination):
            bookmark = BookmarkItem(item.title, self.reader.getDestinationPageNumber(item))
            parent.appendRow(bookmark)
            return bookmark
        elif isinstance(item, list):
            parent = lastBookmark
            lastBookmark = None
            for m in item:
                lastBookmark = self.addBookmarkNodeFromDest(m, parent, lastBookmark)
        
    def initFromPdfFile(self, filename):
        self.clear()

        infile = open(filename, 'rb')
        self.reader = PdfFileReader(infile, strict=False)

        box = self.reader.getPage(0).mediaBox
        self.dimensions = [box[2] - box[0], box[3] - box[1]]

        try:
            self.addBookmarkNodeFromDest(self.reader.outlines, parent=self, lastBookmark=self.invisibleRootItem())
        except PdfReadError:
            pass

        self.reader = None
        infile.close()

    def writeBookmarks(self, parentNode, parentBookmark=None):
        for row in range(parentNode.rowCount()):
            item = parentNode.child(row)
            dest = self.writer.addBookmark(item.text(), item.page(), parentBookmark)
            if item.hasChildren():
                self.writeBookmarks(item, dest)

    def writeToPdfFile(self, oldfilename, newfilename):
        oldfile = open(oldfilename, 'rb')
        reader = PdfFileReader(oldfile, strict=False)
        self.writer = PdfFileWriter()
        self.writer.appendPagesFromReader(reader)
        self.writeBookmarks(self.invisibleRootItem())

        # make new file as temp file regardless, then copy it to relevant file
        # advantage -- works for both "save as" and "save"
        with NamedTemporaryFile(delete=False) as temp:
            with open(temp.name, 'wb') as newfile:
                self.writer.write(newfile)
            oldfile.close()
            self.writer = None
            os.replace(temp.name, os.path.abspath(newfilename))

    def bookmarkDictionary(self, parentNode):
        dictList = []
        for row in range(parentNode.rowCount()):
            item = parentNode.child(row)
            itemDict = item.toDict()
            itemDict['children'] = self.bookmarkDictionary(item) if item.hasChildren() else []
            dictList.append(itemDict)
        return dictList

    def fullDictionary(self):
        return self.bookmarkDictionary(self.invisibleRootItem())

    def exportJsonBookmarks(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.fullDictionary(), f, indent=2)

    def initFromJson(self, filename, clear=True):
        if clear:
            self.clear()

        with open(filename, 'r') as f:
            d = json.load(f)

        if isinstance(d, dict):
            self.addBookmarkNodeFromDict(d, self.invisibleRootItem())
        elif isinstance(d, list):
            [self.addBookmarkNodeFromDict(dd, self.invisibleRootItem()) for dd in d]       

    def addBookmarkNodeFromDict(self, itemDict, parent):
        node = BookmarkItem.fromDict(itemDict)
        parent.appendRow(node)
        for ch in itemDict['children']:
            self.addBookmarkNodeFromDict(ch, node)








from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import Destination

from PyQt5.Qt import QStandardItemModel, QStandardItem, Qt

import os
from tempfile import NamedTemporaryFile

class BookmarkItem(QStandardItem):
    def __init__(self, title='', page=None):
        super().__init__()

        self.setEditable(False)
        self.setText(title)
        self.setData(page, Qt.UserRole)


class BookmarkModel(QStandardItemModel):
    """
    subclass of QStandardItemModel to represent bookmark tree
    """
    def __init__(self, pdffile):
        super().__init__()

        self.reader = None
        self.writer = None

        self.initFromFile(pdffile)

    def clear(self):
        self.removeRows(0, self.rowCount())

    def addBookmark(self, item, parent=None, lastBookmark=None):
        if isinstance(item, Destination):
            bookmark = BookmarkItem(item.title, self.reader.getDestinationPageNumber(item))
            parent.appendRow(bookmark)
            return bookmark
        elif isinstance(item, list):
            parent = lastBookmark
            lastBookmark = None
            for m in item:
                lastBookmark = self.addBookmark(m, parent, lastBookmark)
        
    def initFromFile(self, filename):
        self.clear()

        infile = open(filename, 'rb')
        self.reader = PdfFileReader(infile, strict=False)

        # print(reader.outlines)

        self.addBookmark(self.reader.outlines, parent=self, lastBookmark=self.invisibleRootItem())

        self.reader = None
        infile.close()

    def writeBookmarks(self, parentNode=None, parentBookmark=None):
        for row in range(parentNode.rowCount()):
            item = parentNode.child(row)
            dest = self.writer.addBookmark(item.text(), item.data(Qt.UserRole), parentBookmark)
            if item.hasChildren():
                self.writeBookmarks(item, dest)

    def writeToFile(self, oldfilename, newfilename):
        oldfile = open(oldfilename, 'rb')
        reader = PdfFileReader(oldfile, strict=False)
        self.writer = PdfFileWriter()
        self.writer.appendPagesFromReader(reader)
        self.writeBookmarks(parentNode=self.invisibleRootItem())

        # make new file as temp file regardless, then copy it to relevant file
        # advantage -- works for both "save as" and "save"
        with NamedTemporaryFile(delete=False) as temp:
            with open(temp.name, 'wb') as newfile:
                self.writer.write(newfile)
            oldfile.close()
            self.writer = None
            os.replace(temp.name, os.path.abspath(newfilename))


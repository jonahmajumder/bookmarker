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

def make_bookmark_nested(item, reader, model, parent=None, lastBookmark=None):
    if isinstance(item, Destination):
        bookmark = BookmarkItem(item.title, reader.getDestinationPageNumber(item))
        parent.appendRow(bookmark)
        return bookmark
    elif isinstance(item, list):
        parent = lastBookmark
        lastBookmark = None
        for m in item:
            lastBookmark = make_bookmark_nested(m, reader, model, parent, lastBookmark)

def parseBookmarksToModel(filename):
    infile = open(filename, 'rb')
    reader = PdfFileReader(infile, strict=False)

    treeModel = QStandardItemModel()
    rootNode = treeModel.invisibleRootItem()

    # print(reader.outlines)

    make_bookmark_nested(reader.outlines, reader, treeModel, lastBookmark=rootNode)

    infile.close()

    return treeModel

def write_bookmarks_nested(newpdfobj, parentNode=None, parentBookmark=None):
    for row in range(parentNode.rowCount()):
        item = parentNode.child(row)
        dest = newpdfobj.addBookmark(item.text(), item.data(Qt.UserRole), parentBookmark)

        if item.hasChildren():
            write_bookmarks_nested(newpdfobj, item, dest)

def writeModelToFile(model, oldfilename, newfilename):
    oldfile = open(oldfilename, 'rb')
    reader = PdfFileReader(oldfile, strict=False)
    writer = PdfFileWriter()
    writer.appendPagesFromReader(reader)
    write_bookmarks_nested(writer, parentNode=model.invisibleRootItem())

    # make new file as temp file regardless, then copy it to relevant file
    # advantage -- works for both "save as" and "save"
    with NamedTemporaryFile(delete=False) as temp:
        with open(temp.name, 'wb') as newfile:
            writer.write(newfile)
        oldfile.close()
        os.replace(temp.name, os.path.abspath(newfilename))


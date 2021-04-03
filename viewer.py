# viewer.py
import sys
import re
import json
import types
from urllib.parse import urlparse, unquote

from pathlib import Path
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings, QWebEngineScript

class PDFView(QWebEngineView):
    """
    subclass of QWebEngineView designed to display PDFs
    """
    jsfnRE = re.compile(
        r'function\s*(?P<name>[A-z0-9]+)?\s*\((?P<args>(?:[^)(]+|\((?:[^)(]+|\([^)(]*\))*\)))*\)\s*\{(?P<body>(?:[^}{]+|\{(?:[^}{]+|\{[^}{]*\})*\})*)\}',
        re.DOTALL
    )
    jsSourceFiles = [
        'functions.js'
    ]
    viewerHtmlPath = 'pdfjs/web/viewer.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.loadFinished.connect(self.onLoad)

        if len(args) > 1:
            self.loadPdf(args[1])

    @staticmethod
    def asUri(localpath):
        p = Path(localpath)
        # assert p.exists()
        return p.absolute().as_uri()

    @staticmethod
    def fromUri(fileuri):
        fullpath = unquote(urlparse(fileuri).path)
        return fullpath

    # ---------- INSTANCE METHODS ----------

    def onLoad(self, success):
        if success:
            for filename in self.jsSourceFiles:
                with open(filename, 'r') as f:
                    jsSource = f.read()

                self.page().runJavaScript(jsSource)
                self.loadJsFunctions(jsSource)

            self.getPageNum() # force wait until js functions working
            self.hideSidebar()
            self.resetZoom()

    def loadPdf(self, pdffile):
        self.load(QUrl.fromUserInput(
            '{0}?file={1}'.format(self.asUri(self.viewerHtmlPath), self.asUri(pdffile))
        ))

    def getCurrentFile(self):
        return self.fromUri(self.getCurrentFileUri())

    # ---------- JS PAGE INTERACTION INSTANCE METHODS ----------

    def callJsFunction(self, jsFn, *args):
        callString = jsFn.constructCallString(*args)
        jsFn.resetResponse()
        self.page().runJavaScript(callString, jsFn.captureResponse)

        while not jsFn.responseCaptured:
            QApplication.processEvents()

        return jsFn.response

    def makeJsMethod(self, jsFn):
        return lambda self, *args: self.callJsFunction(jsFn, *args)

    def loadJsFunctions(self, jsSource):
        self.jsFns = [JsFn(m) for m in self.jsfnRE.finditer(jsSource) if m['name']] # list of named functions

        for j in self.jsFns:
            setattr(self, j.name, types.MethodType(self.makeJsMethod(j), self))

class JsFn(object):
    """
    represents a callable javascript function
    """
    def __init__(self, reMatch):
        super().__init__()

        self.name = reMatch['name']
        self.args = [a.strip() for a in reMatch['args'].split(',')] if reMatch['args'] else []
        self.body = reMatch['body'].strip()

    def constructCallString(self, *callArgs):
        if len(callArgs) != len(self.args):
            raise Exception('Expected {0} arguments, but got {1}!'.format(len(self.args), len(callArgs)))
        else:
            argstring = ', '.join([json.dumps(a) for a in callArgs])
            return '{0}({1})'.format(self.name, argstring)

    def resetResponse(self):
        self.responseCaptured = False
        self.response = None

    def captureResponse(self, response):
        self.responseCaptured = True
        self.response = response

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QMainWindow()
    p = PDFView()
    w.setCentralWidget(p)
    p.loadPdf('sample_toc.pdf')
    w.show()
    sys.exit(app.exec_())   

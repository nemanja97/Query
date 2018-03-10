from PySide.QtCore import QUrl
from PySide.QtWebKit import QWebView


class DocumentView(QWebView):

    def __init__(self, path):
        super(DocumentView, self).__init__()
        self.setWindowTitle(path)
        self.load(QUrl.fromLocalFile(path))

    def loadFile(self, path):
        self.load(QUrl.fromLocalFile(path))
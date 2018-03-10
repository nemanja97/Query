from PySide.QtGui import QApplication

def openDocumentAction():
    QApplication.instance().webview.loadFile(QApplication.instance().doclist.currentItem().path)

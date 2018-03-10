import sys

from PySide.QtCore import Qt
from PySide.QtGui import QApplication, QPixmap, QSplashScreen

from dialog.directory_dialog import DirectoryDialog
from indexer.indexer import Indexer
from gui.mainwindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dir = DirectoryDialog()
    if dir.exec_() and dir.result() != "" and dir.result() != None:
        app.indexer = Indexer(dir.result())
        splash_pix = QPixmap('res/SplashScreen.png')
        splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
        splash.setMask(splash_pix.mask())
        splash.show()
        app.processEvents()
        app.indexer.load_data()
        app.doclist = None
        app.webview = None
        app.currentWord = None
        app.mainWindow = MainWindow()
        splash.finish(app.mainWindow)
        app.mainWindow.show()
        sys.exit(app.exec_())
    else:
        app.quit()

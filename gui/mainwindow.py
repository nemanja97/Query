import os

from PySide.QtCore import Qt

from PySide.QtGui import QMainWindow, QLabel, QDockWidget, QApplication, QListWidget, QIcon

from actions.open_document_action import openDocumentAction
from gui.search_toolbar import SearchBar
from view.document_view import DocumentView


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Query")
        self.setWindowIcon(QIcon("res/SplashScreen.png"))
        self.initCentral()
        self.initStatusBar()
        self.initToolbar()
        self.initList()
        self.showMaximized()
        self.leftDock.hide()

    def initCentral(self):
        QApplication.instance().webview = DocumentView(os.getcwd() + "\\res\\ProjectGreeter.html")
        self.setCentralWidget(QApplication.instance().webview)

    def initToolbar(self):
        self.addToolBar(Qt.TopToolBarArea, SearchBar(self))

    def initStatusBar(self):
        self.statusBar().addWidget(QLabel(QApplication.instance().indexer.root))

    def initList(self):
        self.leftDock = QDockWidget()
        self.leftDock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        QApplication.instance().doclist = QListWidget()
        QApplication.instance().doclist.itemDoubleClicked.connect(openDocumentAction)
        self.leftDock.setWidget(QApplication.instance().doclist)
        self.leftDock.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.leftDock)

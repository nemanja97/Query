import os

from PySide.QtGui import QToolBar, QLineEdit, QPushButton, QLabel, QApplication, QCompleter, QStringListModel
from PySide.QtWebKit import QWebPage

from model.document import Document
from parsers.logic_parser import parseResult


class SearchBar(QToolBar):

    def __init__(self, parent):
        super(SearchBar, self).__init__(parent)
        self.parent = parent
        self.setMovable(False)
        self.setStyleSheet('QToolBar{spacing:5px;}')
        self.addWidget(QLabel("                                                                                         "))
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search...")
        self.completer = QCompleter()
        self.search.setCompleter(self.completer)
        self.indexer = QApplication.instance().indexer
        self.search.selectionChanged.connect(self.changeSelection)
        self.search.textChanged.connect(self.setCompleterModel)
        self.addWidget(self.search)
        searchbtn = QPushButton("Search")
        searchbtn.clicked.connect(self.searchDocuments)
        highlighttn = QPushButton("Highlight text")
        highlighttn.clicked.connect(self.highlightText)
        self.addWidget(searchbtn)
        self.addWidget(highlighttn)
        self.addWidget(QLabel("                                                                                         "))

    def changeSelection(self):
        selekcija = self.search.selectedText()
        if selekcija != "":
            self.selectedText = selekcija

    def setCompleterModel(self):
        result = self.search.text()
        if len(result) == 1:
            wordobjects = self.indexer.data['WORDS'].start_with_prefix(result)
            words = []
            for wordobj in wordobjects:
                words.append(wordobj.word)
            model = QStringListModel()
            model.setStringList(words)
            self.completer.setModel(model)

    def clearResults(self):
        QApplication.instance().doclist.clear()

    def highlightText(self):
        QApplication.instance().webview.findText("", QWebPage.HighlightAllOccurrences)
        QApplication.instance().webview.findText(self.selectedText, QWebPage.HighlightAllOccurrences)

    def searchDocuments(self):
        QApplication.instance().doclist.show()
        result = self.search.text()
        QApplication.instance().currentWord = result
        self.clearResults()
        documents = []
        if result == "":
            for filepath in self.indexer.data['FILES']:
                QApplication.instance().doclist.addItem(Document(filepath, os.path.basename(filepath)))
                self.parent.leftDock.show()
        else:
            try:
                documentSet = parseResult(result)
                for filepath in documentSet:
                    documents.append(Document(filepath, os.path.basename(filepath), result))
                documents.sort(key=lambda x: x.rank, reverse=True)
                for doc in documents:
                    QApplication.instance().doclist.addItem(doc)
                self.parent.leftDock.show()
            except ValueError:
                pass
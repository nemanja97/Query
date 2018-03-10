import re
from PySide.QtGui import QIcon, QListWidgetItem, QApplication

REGEX = r'(?:\b[a-zA-Z1-9-!\-@#$|%*\[\];\'\\,./+]+\b)|(?:\^AND)|(?:\^OR)|(?:\^NOT)'

class Document(QListWidgetItem):

    def __init__(self, path, name, search_param = None):
        super(Document, self).__init__(QIcon("res/classTypeHtml.png"), name)
        self.path = path
        self.rank = self.calculateRank(search_param)

    def getProperSearch(self, search_param):
        tokens = re.findall(REGEX, search_param)
        properSearch = ["" for x in xrange(len(tokens))]
        counter = 0
        for token in tokens:
            if token.encode("ascii") != "^NOT" and token.encode("ascii") != "^AND" and token.encode("ascii") != "^OR":
                properSearch[counter] += token.encode("ascii") + " "
            else:
                counter += 1
        finalizedSearch = []
        for search in properSearch:
            if search != "":
                finalizedSearch.append(search.strip())
        return finalizedSearch

    def calculateRank(self, search_param):
        if search_param is not None:
            rank = 0
            with open(self.path, 'r') as document:
                content = document.read()
                document.close()
            for search in self.getProperSearch(search_param):
                rank += 7 * len(re.findall(search, content))
            indexer = QApplication.instance().indexer
            for doc in indexer.data['LINKS'][self.path].getIncomingEdges():
                rank += 5
                with open(doc, 'r') as document:
                    content = document.read()
                    document.close()
                rank += 3 * len(re.findall(search, content))
            return rank
        else:
            return 0

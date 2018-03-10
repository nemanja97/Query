from PySide.QtGui import QApplication, QMessageBox, QMainWindow

from logic_stack import Stack, StackError
import re

REGEX = r'(?:\b[a-zA-Z1-9-!\-@#$|%*\[\];\'\\,./+]+\b)|(?:\^AND)|(?:\^OR)|(?:\^NOT)'

def findSets(tokens):

    operatorPriority = {
        '^NOT': 3,
        '^AND': 2,
        '^OR': 1,
        '$BASE' : 0,
    }

    logicFunctions = {
        '^AND' : lambda x, y : set(x).intersection(set(y)),
        '^OR' : lambda x, y : set(x).union(set(y)),
        '^NOT' : lambda x, y : set(x).difference(set(y))
    }

    operatorStack = Stack()
    docStack = Stack()
    indexer = QApplication.instance().indexer

    def doOperation():
        operation = operatorStack.pop()
        try:
            setB = docStack.pop()
            if not isinstance(setB, set):
                setB = setB.documentSet
            setA = docStack.pop()
            if not isinstance(setA, set):
                setA = setA.documentSet
            docStack.push(logicFunctions[operation](setA, setB))
        except StackError:
            QMessageBox.information(QMainWindow(), "No items found", "There was an error parsing your request",
                                        QMessageBox.Ok)

    def repeatOperation(operator):
        try:
            if operator == "^NOT" and operatorStack.top() == "^NOT":
                pass
            else:
                while len(docStack) > 1 and len(operatorStack) and operatorPriority[operatorStack.top()] >= operatorPriority[operator]:
                        doOperation()
        except StackError:
            pass


    if len(tokens) == 1 and tokens[0] not in logicFunctions:
        if indexer.data['WORDS'].has_word(tokens[0].encode('ascii')):
            return QApplication.instance().indexer.data['WORDS'].getData(tokens[0]).documentSet
        else:
            QMessageBox.information(QMainWindow(), "Word not found",
                                    "The word " + tokens[0].encode('ascii') + " is not in any documents. Did you mean " + indexer.data['WORDS'].getSimilar(tokens[0].encode('ascii')) + "?",
                                    QMessageBox.Ok)
            raise ValueError

    phraseCounter = 0
    phrase = ""
    for token in tokens:
        if token not in logicFunctions:
            if indexer.data['WORDS'].has_word(token.encode('ascii')):
                docStack.push(QApplication.instance().indexer.data['WORDS'].getData(token).documentSet)
                phraseCounter += 1
                phrase += token.encode('ascii') + " "
            else:
                QMessageBox.information(QMainWindow(), "Word not found", "The word " + token.encode('ascii') + " is not in any documents. Did you mean " + indexer.data['WORDS'].getSimilar(token.encode('ascii')) + "?",
                                        QMessageBox.Ok)
                raise ValueError
        else:
            if phraseCounter > 1:
                while phraseCounter > 0:
                    setB = docStack.pop()
                    if not isinstance(setB, set):
                        setB = setB.documentSet
                    setA = docStack.pop()
                    if not isinstance(setA, set):
                        setA = setA.documentSet
                    docStack.push(logicFunctions["^AND"](setA, setB))
                    properSet = set()
                    for doc in docStack.pop():
                        with open(doc, 'r') as document:
                            content = document.read()
                            document.close()
                        if bool(re.search(phrase.strip(), content)):
                            properSet.add(doc)
                    docStack.push(properSet)
                    phraseCounter -= 2
            phrase = ""
            phraseCounter = 0
            if token == "^NOT":
                docStack.push(indexer.data['FILES'])
            if not operatorStack.isEmpty():
                repeatOperation(token)
            operatorStack.push(token)
    if phraseCounter > 1:
        while phraseCounter > 0:
            setB = docStack.pop()
            if not isinstance(setB, set):
                setB = setB.documentSet
            setA = docStack.pop()
            if not isinstance(setA, set):
                setA = setA.documentSet
            docStack.push(logicFunctions["^AND"](setA, setB))
            properSet = set()
            for doc in docStack.pop():
                with open(doc, 'r') as document:
                    content = document.read()
                    document.close()
                if bool(re.search(phrase.strip(), content)):
                    properSet.add(doc)
            docStack.push(properSet)
            phraseCounter -= 2
    repeatOperation('$BASE')
    if len(docStack) == 1:
        return docStack.pop()
    else:
        QMessageBox.information(QMainWindow(), "No items found", "There was an error parsing your request",
                                QMessageBox.Ok)
        raise ValueError


def parseResult(result):
    tokens = re.findall(REGEX, result)
    return findSets(tokens)

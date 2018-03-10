from PySide.QtGui import QDialog, QApplication, QFormLayout, QPushButton, QLineEdit, QDialogButtonBox, QLabel, \
    QFileDialog, QIcon


class DirectoryDialog(QDialog):

    def __init__(self):
        super(DirectoryDialog, self).__init__()

        self.setWindowTitle("Query")
        rect = QApplication.desktop().screenGeometry()
        height = rect.height()
        width = rect.width()
        self.setGeometry(width / 3, height / 3, width / 3, height / 8)

        formLayout = QFormLayout()

        self.dir = QLineEdit()
        self.dir.setReadOnly(True)
        formLayout.addRow(QLabel("Select a folder"), self.dir)
        browseBtn = QPushButton("Browse")
        browseBtn.clicked.connect(self.browseAction)

        formLayout.addWidget(browseBtn)

        btnOk = QPushButton("Ok")
        btnOk.clicked.connect(self.okAction)

        btnCancel = QPushButton("Cancel")
        btnCancel.clicked.connect(self.reject)

        group = QDialogButtonBox()
        group.addButton(btnOk, QDialogButtonBox.AcceptRole)
        group.addButton(btnCancel, QDialogButtonBox.RejectRole)
        formLayout.addRow(group)

        self.setLayout(formLayout)
        self.setWindowIcon(QIcon("res/SplashScreen.png"))
        self.__result = None

    def browseAction(self):
        name = QFileDialog.getExistingDirectory(None, "Select directory")
        self.dir.setReadOnly(False)
        self.dir.setText(name)
        self.dir.setReadOnly(True)

    def okAction(self):
        self.__result = self.dir.text()
        self.accept()

    def result(self):
        return self.__result

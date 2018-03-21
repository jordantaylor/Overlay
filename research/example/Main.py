from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

import sys

from ui_Main import Ui_Main

class Main(QMainWindow, Ui_Main):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)

        self.OpenTiffBtn.clicked.connect(self.OpenWindow1)
        self.OpenPrevBtn.clicked.connect(self.OpenWindow2)
        self.OpenTestBtn.clicked.connect(self.OpenWindow3)
        self.OpenTestBtn2.clicked.connect(self.OpenWindow0)
        self.OpenTestBtn3.clicked.connect(self.OpenWindow0)
        self.setWindowTitle("USNG Overlay - Main")

    def OpenWindow0(self):
        self.setWindowTitle("USNG Overlay - Main")
        self.QtStack.setCurrentIndex(0)

    def OpenWindow1(self):
        self.setWindowTitle("USNG Overlay - <Filename.tif>")
        self.QtStack.setCurrentIndex(1)

    def OpenWindow2(self):
        self.setWindowTitle("USNG Overlay - Open Prev File")
        self.QtStack.setCurrentIndex(2)

    def OpenWindow3(self):
        self.setWindowTitle("USNG Overlay - Map Widget Testing")
        self.QtStack.setCurrentIndex(3)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    showMain = Main()
    sys.exit(app.exec_())
from PyQt5 import QtCore, QtGui, QtWidgets

import sys

class Ui_Main(QtWidgets.QWidget):
    def setupUi(self, Main):
        Main.setObjectName("Main")
        Main.resize(800, 480)

        self.QtStack = QtWidgets.QStackedLayout()

        self.stack1 = QtWidgets.QWidget()
        self.stack2 = QtWidgets.QWidget()
        self.stack3 = QtWidgets.QWidget()

        self.Window1UI()
        self.Window2UI()
        self.Window3UI()

        self.QtStack.addWidget(self.stack1)
        self.QtStack.addWidget(self.stack2)
        self.QtStack.addWidget(self.stack3)

    def Window1UI(self):
        self.stack1.resize(800, 480)

        #OpenTiffBtn#
        self.OpenTiffBtn = QtWidgets.QPushButton(self.stack1)
        self.OpenTiffBtn.setText("Open a TIFF file")
        self.OpenTiffBtn.setGeometry(QtCore.QRect(325, 140, 150, 30))

        #OpenPrevBtn#
        self.OpenPrevBtn = QtWidgets.QPushButton(self.stack1)
        self.OpenPrevBtn.setText("Open from Previous Files")
        self.OpenPrevBtn.setGeometry(QtCore.QRect(325, 190, 150, 30))

        #OpenTestBtn#
        self.OpenTestBtn = QtWidgets.QPushButton(self.stack1)
        self.OpenTestBtn.setText("[TESTING] Open DMS02.tif")
        self.OpenTestBtn.setGeometry(QtCore.QRect(325,240,150,30))

    def Window2UI(self):
        self.stack2.resize(800, 480)
        self.stack2.setStyleSheet("background: red")

        self.OpenTestBtn2 = QtWidgets.QPushButton(self.stack2)
        self.OpenTestBtn2.setText("Open Prev File Window")
        self.OpenTestBtn2.setGeometry(QtCore.QRect(325,240,150,30))

    def Window3UI(self):
        self.stack3.resize(800, 480)
        self.stack3.setStyleSheet("background: blue")

        self.OpenTestBtn3 = QtWidgets.QPushButton(self.stack3)
        self.OpenTestBtn3.setText("Open DMS02.tif for Testing")
        self.OpenTestBtn3.setGeometry(QtCore.QRect(325,240,150,30))
from PyQt5 import QtCore, QtGui, QtWidgets


class widgetB(QtWidgets.QWidget):

    procDoneSignal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(widgetB, self).__init__(parent)

        self.lineEdit = QtWidgets.QLineEdit(self)
        self.btnSendToA = QtWidgets.QPushButton("Send Message to A", self)
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.lineEdit)
        self.layout.addWidget(self.btnSendToA)

        self.btnSendToA.clicked.connect(self.on_btnToA_clicked)

    @QtCore.pyqtSlot()
    def on_btnToA_clicked(self):
        self.procDoneSignal.emit(self.lineEdit.text())

    @QtCore.pyqtSlot(str)
    def on_procStartSignal(self, message):
        self.lineEdit.setText("From A: " + message)

        self.raise_()


class widgetA(QtWidgets.QWidget):
    procStartSignal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(widgetA, self).__init__(parent)

        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setText("Hello!")

        self.btnSendToB = QtWidgets.QPushButton("Send Message to B", self)
        self.btnSendToB.clicked.connect(self.on_btnToB_clicked)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.lineEdit)
        self.layout.addWidget(self.btnSendToB)

    @QtCore.pyqtSlot()
    def on_btnToB_clicked(self):
        self.procStartSignal.emit(self.lineEdit.text())

    @QtCore.pyqtSlot(str)
    def on_widgetB_procDoneSignal(self, message):
        self.lineEdit.setText("From B: " + message)

        self.raise_()


class mainwindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(mainwindow, self).__init__(parent)

        self.button = QtWidgets.QPushButton("Click Me", self)
        self.button.clicked.connect(self.on_clickme_btn_clicked)

        self.setCentralWidget(self.button)

        self.widgetA = widgetA()
        self.widgetB = widgetB()

        self.widgetA.procStartSignal.connect(self.widgetB.on_procStartSignal)
        self.widgetB.procDoneSignal.connect(self.widgetA.on_widgetB_procDoneSignal)

    @QtCore.pyqtSlot()
    def on_clickme_btn_clicked(self):
        self.widgetA.show()
        self.widgetB.show()

        self.widgetA.raise_()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    main = mainwindow()
    main.show()
    sys.exit(app.exec_())
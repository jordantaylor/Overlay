from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import sys

from ui_Main import Ui_Main

class Main(QMainWindow, Ui_Main):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)

        self.OpenTiffBtn.clicked.connect(self.loadFile)
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

    def setImagePath(self, str):
        self.imagePath = str

    def loadFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, 'Choose a file', '', 'Tagged Image Files (*.tif);;Tagged Image Files (*.tiff)', options=options)
        if fileName:
            self.setImagePath(fileName)
        self.showImage()

    def ZoomInBtnPress(self):
        self.view.scale(1.5, 1.5)

    def ZoomOutBtnPress(self):
        self.view.scale(0.7, 0.7)

    def FitToScreenBtnPress(self):
        self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

    def showImage(self):
        self.pixmap = QPixmap(self.imagePath)

        self.scene = QGraphicsScene()
        self.scene.addPixmap(self.pixmap)

        self.view = QGraphicsView()
        self.view.setScene(self.scene)
        self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

        self.view.setRenderHints(QPainter.Antialiasing|QPainter.SmoothPixmapTransform)
        self.view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.view.setDragMode(QGraphicsView.ScrollHandDrag)

        ZoomInBtn = QPushButton('+', self.view)
        ZoomInBtn.setGeometry(40, 40, 40, 40)
        ZoomInBtn.setStyleSheet("background-color: white")
        ZoomInBtn.clicked.connect(self.ZoomInBtnPress)

        ZoomOutBtn = QPushButton('-', self.view)
        ZoomOutBtn.setGeometry(40, 90, 40, 40)
        ZoomOutBtn.setStyleSheet("background-color: white")
        ZoomOutBtn.clicked.connect(self.ZoomOutBtnPress)

        FitToScreenBtn = QPushButton('[]', self.view)
        FitToScreenBtn.setGeometry(40, 140, 40, 40)
        FitToScreenBtn.setStyleSheet("background-color: white")
        FitToScreenBtn.clicked.connect(self.FitToScreenBtnPress)

        self.view.show()

        def wheelEvent(self,event):        
            adj = (event.delta()/120) * 0.1
            self.scale(1+adj,1+adj)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    showMain = Main()
    sys.exit(app.exec_())
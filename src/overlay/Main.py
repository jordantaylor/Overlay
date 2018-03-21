import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QRect

from StackWidget import StackWidget

class Overlay(QMainWindow):
	def __init__(self):
		super().__init__()
		
		self.initUI()
		
		
	def initUI(self):
		self.setGeometry(135, 200, 800, 600)
		self.setWindowTitle('USNG Overlay - Main')
		self.setWindowIcon(QIcon('..\\..\\assets\\gimp_pepper.png')) 

		self.createMenuBar()

		wid = StackWidget()
		self.setCentralWidget(wid)
		layout = QVBoxLayout()
		wid.setLayout(layout)

		self.center()
		self.show()

	def createMenuBar(self):
		# Create a file menu for opening new file, exporting to image, & other file ops
		menubar = self.menuBar()
		fileMenu = menubar.addMenu('File')
		viewMenu = menubar.addMenu('View')
		
		# Create the file actions and add them
		openAct = QAction('Open TIFF Image', self)
		exportPngAct = QAction('Export Overlay to PNG', self)
		saveWayptsAct = QAction('Save Waypoints to File', self)
		exitAct = QAction('Exit Program', self)
		fileMenu.addAction(openAct)
		fileMenu.addAction(exportPngAct)
		fileMenu.addAction(saveWayptsAct)
		fileMenu.addAction(exitAct)

		# Create a view menu for show/hide waypoint list popup, & other view ops
		zoomInAct = QAction('Zoom in', self)
		zoomOutAct = QAction('Zoom out', self)
		toggleWayptsAct = QAction('Toggle Waypoint List', self)
		viewMenu.addAction(zoomInAct)
		viewMenu.addAction(zoomOutAct)
		viewMenu.addAction(toggleWayptsAct)

	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())    
		
if __name__ == '__main__':
	
	app = QApplication(sys.argv)
	ex = Overlay()
	sys.exit(app.exec_())
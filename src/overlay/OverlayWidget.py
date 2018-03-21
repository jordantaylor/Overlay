from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QGridLayout, QSizePolicy
from PyQt5.QtCore import *#QRect, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QIcon, QImage
from QtImageViewer import QtImageViewer

class OverlayWidget(QWidget):
	########################################################################
	# For the overlay page. Needs to contain:
	# 1. QtImageViewer Widget
	# 2. menubar with buttons to:
	#	a) open a new tif file
	#	b) export tif as png image
	#	c) display list of placed waypoints in a popup or docked widget
	# 3.
	#
	# Highest priority for meeting customer needs
	#
	########################################################################
	changeWidgetSignal = pyqtSignal(int)
	def __init__(self):
		super().__init__()
		self.initUI()
	def initUI(self):
		self.waypts = QPushButton("TODO: WAYPOINTS",self)
		self.waypts.setSizePolicy( QSizePolicy.Preferred, QSizePolicy.Expanding )

		self.start_btn = QPushButton("<-- Back [temporary]",self)
		self.load_btn = QPushButton("To Loadpage [temporary]",self)
		self.start_btn.clicked.connect(self.on_start_clicked)
		self.load_btn.clicked.connect(self.on_load_clicked)

		self.viewer = QtImageViewer()
		self.viewer.aspectRatioMode = Qt.KeepAspectRatio
		self.viewer.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
		self.viewer.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
		self.viewer.canZoom = True
		self.viewer.canPan = True
		# self.viewer.leftMouseButtonPressed.connect(self.handleLeftClick)

		self.navlayout = QHBoxLayout()
		self.navlayout.addWidget(self.start_btn)
		self.navlayout.addWidget(self.load_btn)

		self.subgridlayout = QGridLayout()
		self.subgridlayout.addWidget(self.viewer,0,0,10,10)

		self.mainlayout = QHBoxLayout()
		self.mainlayout.addWidget(self.waypts, 1)
		self.mainlayout.addLayout(self.subgridlayout, 3)

		self.whyyyy = QVBoxLayout()
		self.whyyyy.addLayout(self.navlayout)
		self.whyyyy.addLayout(self.mainlayout)
		self.setLayout(self.whyyyy)

	# May not be needed, but here if we want to add it
	def initToolbar(self):
		exitAct = QAction(QIcon('gimp_pepper.png'), 'Exit', self)
		exitAct.triggered.connect(self.close)
		toolbar = self.addToolBar('Exit')
		toolbar.addAction(exitAct)

	# Custom slot for handling mouse clicks in our viewer.
	# Just prints the (row, column) matrix index of the 
	# image pixel that was clicked on.
	# def handleLeftClick(x, y):
	# 	row = int(y)
	# 	column = int(x)
	# 	print("Pixel (row="+str(row)+", column="+str(column)+")")

	@pyqtSlot()
	def on_start_clicked(self):
		self.changeWidgetSignal.emit(0)

	@pyqtSlot()
	def on_load_clicked(self):
		self.changeWidgetSignal.emit(2)

	@pyqtSlot(str)
	def on_load_signal(self,filename):
		self.viewer.setImage(QImage(filename))
		#self.viewer.getpoints(filename)
		#for key in points.keys():
		#	print(key,points[key])
		self.changeWidgetSignal.emit(1)
	########################################################################
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QIcon

class OverlayWidget(QWidget):
	########################################################################
	# For the overlay page. Needs to contain:
	# 1. QtImageViewer Widget
	# 2. Toolbar with buttons to:
	#	a) open a new tif file
	#	b) export tif as png image
	#	c) display list of placed waypoints in a popup or docked widget
	# 3.
	#
	# Highest priority for meeting customer needs
	#
	########################################################################
	def __init__(self):
		super().__init__()
		self.initUI()
	def initUI(self):
		layout = QVBoxLayout()
		layout.addWidget(QLabel("OverlayWidget"))
		self.setLayout(layout)
		#self.initToolbar()
	def initToolbar(self):
		exitAct = QAction(QIcon('gimp_pepper.png'), 'Exit', self)
		exitAct.triggered.connect(self.close)
		toolbar = self.addToolBar('Exit')
		toolbar.addAction(exitAct)
	########################################################################
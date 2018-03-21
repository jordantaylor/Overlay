from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QApplication
from PyQt5.QtCore import QRect

class MainWidget(QWidget):
	########################################################################
	# Widget seen on program startup giving options to open, load, and 
	# any buttons to aid in testing during development
	#
	# Second highest priority
	#
	########################################################################
	def __init__(self):
		super().__init__()
		self.initUI()
	def initUI(self):
		# self.layout = QLayout()
		#self.layout.addWidget(QLabel("MainWidget"))
		title = QLabel("Main Widget")
		title.setGeometry(QRect(325,90,150,30))
		self.initBtns()
		# self.setLayout(self.layout)
	
	def initBtns(self):
		# OpenTiffBtn#
		OpenTiffBtn = QPushButton('Open a TIFF file',self)
		# self.layout.addWidget(OpenTiffBtn)
		OpenTiffBtn.setGeometry(QRect(325,140,150,30))

		# OpenPrevBtn#
		OpenPrevBtn = QPushButton("Open from Previous Files",self)
		# self.layout.addWidget(OpenPrevBtn)
		OpenPrevBtn.setGeometry(QRect(325,190,150,30))

		# OpenTestBtn#
		OpenTestBtn = QPushButton("[TESTING] Open DMS02.tif",self)
		# self.layout.addWidget(OpenTestBtn)
		OpenTestBtn.setGeometry(QRect(325,240,150,30))

		# QuitBtn#
		QuitBtn = QPushButton("Exit",self)
		# self.layout.addWidget(QuitBtn)
		QuitBtn.setGeometry(QRect(325,290,150,30))
		QuitBtn.clicked.connect(QApplication.instance().quit)
	########################################################################
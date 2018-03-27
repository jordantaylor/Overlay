from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QApplication, QFileDialog
from PyQt5.QtCore import QRect, pyqtSlot, pyqtSignal

class MainWidget(QWidget):
	########################################################################
	# Widget seen on program startup giving options to open, load, and 
	# any buttons to aid in testing during development
	#
	# Second highest priority
	#
	########################################################################
	changeWidgetSignal = pyqtSignal(int)
	selectTifSignal = pyqtSignal(str)
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
		OpenTiffBtn.clicked.connect(self.on_opentif_clicked)

		# OpenPrevBtn#
		OpenPrevBtn = QPushButton("Open from Previous Files",self)
		# self.layout.addWidget(OpenPrevBtn)
		OpenPrevBtn.setGeometry(QRect(325,190,150,30))
		OpenPrevBtn.clicked.connect(self.on_prevfiles_clicked)

		# OpenTestBtn#
		OpenTestBtn = QPushButton("[TESTING] Open DMS02.tif",self)
		# self.layout.addWidget(OpenTestBtn)
		OpenTestBtn.setGeometry(QRect(325,240,150,30))

		# QuitBtn#
		QuitBtn = QPushButton("Exit",self)
		# self.layout.addWidget(QuitBtn)
		QuitBtn.setGeometry(QRect(325,290,150,30))
		QuitBtn.clicked.connect(QApplication.instance().quit)

	@pyqtSlot()
	def on_opentif_clicked(self):
		# when main tiff button clicked, first get a filename then 
		fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","TIFF Files (*.tif)")
		#fileName, dummy = QFileDialog.getOpenFileName(None, "Open image file...")
		self.selectTifSignal.emit(fileName)
		#self.changeWidgetSignal.emit(1)
	@pyqtSlot()
	def on_prevfiles_clicked(self):
		self.changeWidgetSignal.emit(2)
	########################################################################
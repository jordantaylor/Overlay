from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

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
		self.layout = QVBoxLayout()
		self.layout.setAlignment(Qt.AlignCenter|Qt.AlignCenter)
		self.initBtns()
		self.setLayout(self.layout)
	
	def initBtns(self):
		# OpenTiffBtn#
		OpenTiffBtn = QPushButton('Open a TIFF file',self)
		OpenTiffBtn.setFixedSize(QSize(225, 100))
		OpenTiffBtn.clicked.connect(self.on_opentif_clicked)
		self.layout.addWidget(OpenTiffBtn)

		# OpenPrevBtn#
		OpenPrevBtn = QPushButton("Previous Files",self)
		OpenPrevBtn.setFixedSize(QSize(225, 100))
		OpenPrevBtn.clicked.connect(self.on_prevfiles_clicked)
		self.layout.addWidget(OpenPrevBtn)

		# QuitBtn#
		QuitBtn = QPushButton("Exit",self)
		QuitBtn.setFixedSize(QSize(225, 100))
		QuitBtn.clicked.connect(QApplication.instance().quit)
		self.layout.addWidget(QuitBtn)

	@pyqtSlot()
	def on_opentif_clicked(self):
		# when main tiff button clicked, first get a filename then
		fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","TIFF Files (*.tif)")
		self.selectTifSignal.emit(fileName)
		
	@pyqtSlot()
	def on_prevfiles_clicked(self):
		self.changeWidgetSignal.emit(2)
	########################################################################
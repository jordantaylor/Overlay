from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy
from PyQt5.QtCore import QRect, pyqtSlot, pyqtSignal


class PrevFilesWidget(QWidget):
	########################################################################
	# Widget seen when user selects load from previous file, in the end this
	# should show TIFFs that have saved waypoints associated with them.
	# - need to handle if original file is missing -> error OR move original
	#   but we can't copy it because of size.
	#
	# Of lowest priority in meeting the customer's primary needs.
	#
	########################################################################
	changeWidgetSignal = pyqtSignal(int)
	chosenSaveFileSignal = pyqtSignal(str)
	def __init__(self):
		super().__init__()
		self.initUI()
	def initUI(self):
		#layout = QGridLayout()
		#layout.addWidget(QLabel("PrevFilesWidget"))
		self.l = QLabel("PrevFilesWidget")
		self.btn = QPushButton("<-- Back",self)
		#self.btn.setGeometry(QRect(50,50,150,30))

		self.btn2 = QPushButton("TODO: SAVED WAYPOINTS",self)
		self.btn2.setSizePolicy( QSizePolicy.Preferred, QSizePolicy.Expanding )

		self.qbly = QVBoxLayout()
		self.qbly.addWidget(self.btn,1)
		self.qbly.addWidget(self.btn2,14)
		self.btn.clicked.connect(self.on_back_clicked)
		self.setLayout(self.qbly)

	@pyqtSlot()
	def on_back_clicked(self):
		self.changeWidgetSignal.emit(0)

	# When user picks a savefile, its path/save filename will be set as a local and passed with this to the overlay.
	@pyqtSlot()
	def on_savefile_chosen(self):
		self.changeWidgetSignal.emit(self.saveChoice)
	########################################################################
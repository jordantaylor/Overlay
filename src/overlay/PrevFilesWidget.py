from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QGridLayout
from PyQt5.QtCore import QRect, pyqtSlot, pyqtSignal
from pprint import pprint
import os


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
	selectTifSignal = pyqtSignal(str)
	def __init__(self):
		super().__init__()
		self.initUI()
	def initUI(self):
		self.l = QLabel("PrevFilesWidget")
		self.btn = QPushButton("<-- Back",self)

		self.qbly = QVBoxLayout()
		self.qbly.addWidget(self.btn,1)
		self.btn.clicked.connect(self.on_back_clicked)
		#self.setLayout(self.qbly)

		self.itemvlist = QVBoxLayout()
		self.tiflist = {}

		dirlist = os.listdir("../../saves")
		for item in dirlist: 
			if item[0] != '.':
				if item[len(item)-4:len(item)] == ".tif":
					itemhlist = QHBoxLayout()
					itembtn = QPushButton(item[0:len(item)-4],self)
					itembtn.clicked.connect(lambda *, item=item: self.item_button_clicked("../../saves/"+item))
					itemhlist.addWidget(itembtn)
					self.tiflist[item] = itembtn
					self.itemvlist.addLayout(itemhlist)
		self.setLayout(self.itemvlist)
		

	@pyqtSlot(str)
	def item_button_clicked(self,itemName):
		self.selectTifSignal.emit(itemName) 
		
	@pyqtSlot()
	def on_back_clicked(self):
		self.changeWidgetSignal.emit(0)

	# When user picks a savefile, its path/save filename will be set as a local and passed with this to the overlay.
	@pyqtSlot()
	def on_savefile_chosen(self):
		self.changeWidgetSignal.emit(self.saveChoice)
	########################################################################

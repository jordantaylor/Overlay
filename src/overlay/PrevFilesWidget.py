from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QGridLayout
from PyQt5.QtCore import QRect, pyqtSlot, pyqtSignal
from QtImageViewer import QtImageViewer
from pprint import pprint
import os

# This widget is responsible for rendering the page where waypoints can be loaded from save files.
class PrevFilesWidget(QWidget):
	changeWidgetSignal = pyqtSignal(int)
	chosenSaveFileSignal = pyqtSignal(str)
	selectTifSignal = pyqtSignal(str,str)
	def __init__(self):
		super().__init__()
		self.savespath = '../../saves'
		self.initUI()

	def initUI(self):
		self.l = QLabel("PrevFilesWidget")
		self.btn = QPushButton("<-- Back",self)

		self.qbly = QVBoxLayout()
		self.qbly.addWidget(self.btn,1)
		self.btn.clicked.connect(self.on_back_clicked)

		self.itemvlist = QVBoxLayout()
		self.tiflist = {}

		dirlist = os.listdir( self.savespath )
		for item in dirlist:
			if item[0] != '.':
				if item[len(item)-4:len(item)] == ".txt":
					itemhlist = QHBoxLayout()
					itembtn = QPushButton(item[0:len(item)-4],self)
					fline = open(self.savespath + "/" + item).readline().rstrip()
					itembtn.clicked.connect(lambda *, item=item: self.item_button_clicked(fline))
					itemhlist.addWidget(itembtn)
					self.tiflist[item] = itembtn
					self.itemvlist.addLayout(itemhlist)
			item = None
		self.setLayout(self.itemvlist)

	#
	def getLocations(self):
		coords = []
		namedFile = ""
		dirlist = os.listdir( self.savespath )
		for item in dirlist:
			if item[0] != '.':
				if item[len(item)-4:len(item)] == ".txt":
					namedFile = self.savespath + "/" + item
					lines = [line.rstrip('\n') for line in open(namedFile)]
					fline = lines[0]
					for i in range(1, len(lines)):
						temp_string = lines[i]
						loc = temp_string.find(',')
						x = temp_string[:loc]
						y = temp_string[loc+1:]
						coords.append([item[:len(item)-4], x , y])
		return coords

	@pyqtSlot(str)
	def item_button_clicked(self,itemName):
		self.selectTifSignal.emit(itemName)

	# When the back button is clicked, go back to the MainWidget
	@pyqtSlot()
	def on_back_clicked(self):
		self.changeWidgetSignal.emit(0)

	# When user picks a savefile, its path/save filename will be set as a local and passed with this to the overlay.
	@pyqtSlot()
	def on_savefile_chosen(self):
		self.selectTifSignal.emit(self.saveChoice, "prevfiles")

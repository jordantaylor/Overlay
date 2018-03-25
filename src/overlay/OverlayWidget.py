import sys
from functools import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
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
	########################################################################

	changeWidgetSignal = pyqtSignal(int)

	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):

		################################################################
		#
		# The following code if for the waypoint panel
		#
		################################################################

		# 'waypts' is the panel itself, it is a QWidget
		self.waypts = QWidget()
		self.waypts.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

		# 'waypts_layout' allows us to add waypoints to 'waypts'
		# 'waypts_layout' is a QVBoxLayout so the waypoints are shown vertically
		self.waypts_layout = QVBoxLayout()
		self.waypts_layout.setAlignment(Qt.AlignCenter)
		self.waypts.setLayout(self.waypts_layout)

		# each waypoint will be a QWidget
		self.waypoint_widgets = []

		for x in range(0, 26):
			# each waypoint's QWidget 'waypts_widget' is created
			self.waypts_widget = QWidget()
			self.waypts_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

			# 'waypts_widget_label' will display the waypoint's key, a letter between 'A' and 'Z'
			self.waypts_widget_label = QLabel()
			self.waypts_widget_label.setText(chr(ord('A') + x))

			# 'waypoint_delete_btn' will display the waypoint's delete button
			self.waypoint_delete_btn = QPushButton("X")
			self.waypoint_delete_btn.setFixedSize(QSize(45, 45))
			self.waypoint_delete_btn.clicked.connect(partial(self.del_hide_waypoint, chr(ord('A') + x)))

			# 'waypts_widget_layout' allows us to add a label and button to 'waypts_widget'
            # 'waypts_widget_layout' is a QHBoxLayout so the label and buttons are shown horizontally
			self.waypts_widget_layout = QHBoxLayout()
			self.waypts_widget_layout.addWidget(self.waypts_widget_label)
			self.waypts_widget_layout.addWidget(self.waypoint_delete_btn)
			self.waypts_widget.setLayout(self.waypts_widget_layout)

			# each waypoint's QWidget 'waypts_widget' is added to 'waypoint_widgets'
			self.waypoint_widgets.append(self.waypts_widget)

		################################################################

		self.start_btn = QPushButton("<-- Back [temporary]",self)
		self.load_btn = QPushButton("To Loadpage [temporary]",self)
		self.start_btn.clicked.connect(self.on_start_clicked)
		self.load_btn.clicked.connect(self.on_load_clicked)

		self.viewer = QtImageViewer()
		self.make_connection(self.viewer)

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

		# the following code is for the loading_screen
		# the loading_screen is displayed while the .tif is being loaded
		self.loading_screen = QWidget()
		self.loading_screen.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
		self.loading_screen.setWindowTitle("              Loading...")
		self.loading_screen.resize(200, 200)
		self.loading_layout = QVBoxLayout()
		self.loading_screen.setLayout(self.loading_layout)

		self.loading_screen.show()

		self.viewer.set_image(filename)

		self.loading_screen.close()

		self.changeWidgetSignal.emit(1)

	# 'make_connection' connects this class to the 'viewer'
	def make_connection(self, viewer_object):
		viewer_object.add_delete_waypoint_signal.connect(self.add_delete_waypoint_widget)

	# 'del_hide_waypoint' deletes the waypoint from 'waypts'
	def del_hide_waypoint(self, _key):
		index = ord(_key) - ord('A')
		self.waypts_layout.removeWidget(self.waypoint_widgets[index])
		self.waypoint_widgets[index].hide()
		self.viewer.delete_waypoint(_key)

	# 'add_show_waypoint' adds the waypoint from 'waypts'
	def add_show_waypoint(self, _key):
		index = ord(_key) - ord('A')
		self.waypoint_widgets[index].show()
		self.waypts_layout.addWidget(self.waypoint_widgets[index])

	# this slot is called when a signal is passed from the QtImageViewer class
	@pyqtSlot(int, str)
	def add_delete_waypoint_widget(self, flag, _key):
		if flag is 1:
			self.add_show_waypoint(_key)
		else:
			self.del_hide_waypoint(_key)

	########################################################################
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from StackWidget import StackWidget
from SaveWaypoints import buildEntry

class Overlay(QMainWindow):
	def __init__(self):
		super().__init__()
		
		self.initUI()
		
#### Initialization Functions ###########################################################

	def initUI(self):
		#self.setGeometry(135, 200, 800, 600)
		self.setWindowTitle('USNG Overlay - Start')

		# TODO make platform independent
		self.setWindowIcon(QIcon('..\\..\\assets\\gimp_pepper.png')) 

		self.wid = StackWidget()
		self.setCentralWidget(self.wid)

		# Button signals
		self.wid.page1.changeWidgetSignal.connect(self.switchWidget)
		self.wid.page2.changeWidgetSignal.connect(self.switchWidget)
		self.wid.page3.changeWidgetSignal.connect(self.switchWidget)
		self.wid.page1.selectTifSignal.connect(self.wid.page2.on_load_signal)
		# Slot to receive tif loading error and handle it
		self.wid.page2.load_error_signal.connect(self.handleFileError)

		# self.initErrorWindow()
		self.createMenuBar()
		self.menubar.hide()
		self.showMaximized()

	# def initErrorWindow(self):
	# 	self.error_screen = QWidget()
	# 	self.error_screen.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
	# 	self.error_screen.frameGeometry().moveCenter(QDesktopWidget().availableGeometry().center())
	# 	self.error_screen.setWindowTitle("Error")
	# 	self.error_screen.resize(200, 50)
	# 	self.error_layout = QVBoxLayout()
	# 	self.error_layout.addWidget( QLabel("") )
	# 	self.error_screen.setLayout(self.loading_layout)

	def createMenuBar(self):
		# Create a file menu for opening new file, exporting to image, & other file ops
		self.menubar = self.menuBar()
		fileMenu = self.menubar.addMenu('File')
		viewMenu = self.menubar.addMenu('View')
		
		# Create the file actions and add them
		openAct = QAction('Open TIFF Image', self)
		openAct.triggered.connect(self.wid.page1.on_opentif_clicked)
		loadAct = QAction('Load Saved TIFF File', self)
		loadAct.triggered.connect(self.wid.page1.on_prevfiles_clicked)
		exportPngAct = QAction('Export Overlay to PNG [TODO]', self)
		saveWayptsAct = QAction('Save Waypoints to File [TODO]', self)
                saveWayptsAct.triggered.connect(buildEntry())
		exitAct = QAction('Exit Program', self)
		exitAct.triggered.connect(QApplication.instance().quit)
		fileMenu.addAction(openAct)
		fileMenu.addAction(loadAct)
		fileMenu.addAction(exportPngAct)
		fileMenu.addAction(saveWayptsAct)
		fileMenu.addAction(exitAct)

		# Create a view menu for show/hide waypoint list popup, & other view ops
		toggleWayptsAct = QAction('Toggle Waypoint List', self)
		toggleWayptsAct.triggered.connect(self.wid.page2.hide_sidebar)
		viewMenu.addAction(toggleWayptsAct)

		toggle100mGrid = QAction('Toggle 100 meter Grid Lines', self)
		toggle100mGrid.triggered.connect(self.wid.page2.hide_100m_grid)
		viewMenu.addAction(toggle100mGrid)

#### Helper Functions ###################################################################

	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

#### Slots ##############################################################################

	@pyqtSlot(int)
	def switchWidget(self,widgetID):
		if widgetID == 0:
			self.setWindowTitle("USNG Overlay - Start")
			self.menubar.hide()
		elif widgetID == 1:
			self.setWindowTitle("USNG Overlay - Main")
			self.menubar.show()
		else:
			self.setWindowTitle("USNG Overlay - Load Saved Waypoints")
			self.menubar.hide()
		self.wid.setCurrentIndex(widgetID)

	@pyqtSlot(str)
	def handleFileError(self,errmsg):
		# Set the error message in the error window and show it
		QMessageBox.warning(self, "Error", errmsg, QMessageBox.Ok)

		# On clicking ok, switch back to main widget
		self.setWindowTitle("USNG Overlay - Start")
		self.wid.setCurrentIndex(0)

#########################################################################################
		
if __name__ == '__main__':
	
	app = QApplication(sys.argv)
	ex = Overlay()
	sys.exit(app.exec_())

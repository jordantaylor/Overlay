from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


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
	def __init__(self):
		super().__init__()
		self.initUI()
	def initUI(self):
		layout = QVBoxLayout()
		layout.addWidget(QLabel("PrevFilesWidget"))
		self.setLayout(layout)
	########################################################################
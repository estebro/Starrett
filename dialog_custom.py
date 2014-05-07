"""
    dialog_custom.py
    Gathers user-desired settings for the creation
    of a new ball in the simulation.

"""

import sys
from PySide.QtCore import *
from PySide.QtGui import *

class CustomDialog(QDialog):

	def __init__(self, parent=None):
		super(CustomDialog,self).__init__(parent)
		self.setParent(None,Qt.WindowSystemMenuHint | Qt.WindowTitleHint)	# remove '?' button
		self.setWindowTitle('Shoot Custom Ball')
		self.setFixedSize(290,150)

		# label names		
		names = ['Pos (X)','Pos (Y)','Vel (X)',
				 'Vel (Y)','Mass','Radius']

		self.labels = []
		self.text_boxes = []

		# creating dialog's labels and textboxes
		for i in range(0,6):
			self.labels.append(QLabel(names[i]))
			self.text_boxes.append(QLineEdit())
		
		# creating buttons and button group
		ok_btn = QPushButton('OK')
		cancel_btn = QPushButton('Cancel')
		
		# connect buttons to listeners
		ok_btn.clicked.connect(self.accept)
		cancel_btn.clicked.connect(self.reject)

		self.btn_box = QDialogButtonBox()
		self.btn_box.addButton(ok_btn,QDialogButtonBox.AcceptRole)
		self.btn_box.addButton(cancel_btn,QDialogButtonBox.RejectRole)

		# creating vertical/horizontal layouts
		vertical = QVBoxLayout()		
		horizontal = QHBoxLayout()

		for i in range(0,6):
			# new row every two label/textbox combo
			if (i%2 == 0 and i!=0):
				vertical.addLayout(horizontal)	# add row
				horizontal = QHBoxLayout()		# new row
			
			horizontal.addWidget(self.labels[i])		# add label
			horizontal.addWidget(self.text_boxes[i])	# add textbox
		
		vertical.addLayout(horizontal)		# add last row

		# creating the button row
		buttons = QHBoxLayout()
		buttons.addStretch(1)
		buttons.addWidget(ok_btn)
		buttons.addWidget(cancel_btn)

		vertical.addLayout(buttons)
		self.setLayout(vertical)

	"""
		function called when the user accepts the dialog's
		inputs by hitting 'OK'
	"""
	def accept(self):

		# retrieve results
		self.results = []
		for i in range(0,6):
			self.results.append(self.text_boxes[i].text())

		self.done(QDialog.Accepted)		# allow dialog to close

if __name__ == '__main__':
	
	# create the Qt Application
	app = QApplication(sys.argv)

	# create and show the form
	dialog = CustomDialog()
	dialog.show()

	# run the main Qt loop
	sys.exit(app.exec_())
from functools import partial

from PyQt5.QtWidgets import (QDialog, QLabel, QGridLayout, QPushButton,
	QCheckBox, QDialogButtonBox, QSpacerItem, QSizePolicy)
from PyQt5.Qt import Qt

class dialog(QDialog):
	def __init__(self, parent):
		super().__init__(parent)
		parent.statusbar.showMessage('Preferences Opened')

		self.setGeometry(250, 250, 250, 250)
		lblDialog = QLabel('label on Dialog')

		# center the label and increase the font size
		lblDialog.setAlignment(Qt.AlignCenter)
		#parent.setFontSize(self.lblDialog, 15)
		gridLayout = QGridLayout()
		gridLayout.addWidget(lblDialog,0 ,0 )
		gridLayout.addWidget(QLabel('Save'),1 ,0 )
		gridLayout.addWidget(QCheckBox('Save Window Size & Position'),2 ,0 )
		verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding) 
		#gridLayout.addWidget(verticalSpacer, 2, 0)
		#pb = QPushButton('Exit')
		buttonBox = QDialogButtonBox()
		buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Apply)
		gridLayout.addWidget(buttonBox)
		cancelBtn = buttonBox.button(QDialogButtonBox.Cancel)
		cancelBtn.clicked.connect(self.reject)

		applyBtn = buttonBox.button(QDialogButtonBox.Apply)
		applyBtn.clicked.connect(partial(self.apply, parent))

		#self.gridLayout.addWidget(pb)
		#pb.clicked.connect(self.close)

		self.setLayout(gridLayout)

	def apply(self, parent):
		parent.statusbar.showMessage('Preferences Saved')
		self.close()

	def _okBtn(self):
		print('ok')


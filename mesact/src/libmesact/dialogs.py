import os

from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel
from PyQt5.QtWidgets import QMessageBox, QCheckBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
'''
QMessageBox::Ok	0x00000400	An "OK" button defined with the AcceptRole.
QMessageBox::Open	0x00002000	An "Open" button defined with the AcceptRole.
QMessageBox::Save	0x00000800	A "Save" button defined with the AcceptRole.
QMessageBox::Cancel	0x00400000	A "Cancel" button defined with the RejectRole.
QMessageBox::Close	0x00200000	A "Close" button defined with the RejectRole.
QMessageBox::Discard	0x00800000	A "Discard" or "Don't Save" button, depending on the platform, defined with the DestructiveRole.
QMessageBox::Apply	0x02000000	An "Apply" button defined with the ApplyRole.
QMessageBox::Reset	0x04000000	A "Reset" button defined with the ResetRole.
QMessageBox::RestoreDefaults	0x08000000	A "Restore Defaults" button defined with the ResetRole.
QMessageBox::Help	0x01000000	A "Help" button defined with the HelpRole.
QMessageBox::SaveAll	0x00001000	A "Save All" button defined with the AcceptRole.
QMessageBox::Yes	0x00004000	A "Yes" button defined with the YesRole.
QMessageBox::YesToAll	0x00008000	A "Yes to All" button defined with the YesRole.
QMessageBox::No	0x00010000	A "No" button defined with the NoRole.
QMessageBox::NoToAll	0x00020000	A "No to All" button defined with the NoRole.
QMessageBox::Abort	0x00040000	An "Abort" button defined with the RejectRole.
QMessageBox::Retry	0x00080000	A "Retry" button defined with the AcceptRole.
QMessageBox::Ignore	0x00100000	An "Ignore" button defined with the AcceptRole.
'''

def msg_open_abort_cancel(msg, title):
	msgBox = QMessageBox()
	msgBox.setIcon(QMessageBox.Warning)
	msgBox.setWindowTitle(title)
	msgBox.setText(msg)
	msgBox.setStandardButtons(QMessageBox.Open | QMessageBox.Abort | QMessageBox.Cancel)
	returnValue = msgBox.exec()
	if returnValue == QMessageBox.Open:
		return 'Open'
	elif returnValue == QMessageBox.Abort:
		return 'Abort'
	else:
		return False

def msg_open_cancel(msg, title):
	msgBox = QMessageBox()
	msgBox.setIcon(QMessageBox.Warning)
	msgBox.setWindowTitle(title)
	msgBox.setText(msg)
	msgBox.setStandardButtons(QMessageBox.Open | QMessageBox.Cancel)
	returnValue = msgBox.exec()
	if returnValue == QMessageBox.Open:
		return 'Open'
	else:
		return False

def errorMsgCancelOk(text, title):
	msgBox = QMessageBox()
	msgBox.setIcon(QMessageBox.Warning)
	msgBox.setWindowTitle(title)
	msgBox.setText(text)
	msgBox.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
	returnValue = msgBox.exec()
	if returnValue == QMessageBox.Ok:
		return True
	else:
		return False

def errorMsgOk(text, title=None):
	msgBox = QMessageBox()
	msgBox.setIcon(QMessageBox.Warning)
	msgBox.setWindowTitle(title)
	msgBox.setText(text)
	msgBox.setStandardButtons(QMessageBox.Ok)
	returnValue = msgBox.exec()
	if returnValue == QMessageBox.Ok:
		return True
	else:
		return False

def questionMsg(text, title=None): # unused function
	msgBox = QMessageBox()
	msgBox.setIcon(QMessageBox.Question)
	msgBox.setWindowTitle(title)
	msgBox.setText(text)
	msgBox.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
	returnValue = msgBox.exec()
	if returnValue == QMessageBox.Ok:
		return True
	else:
		return False

def errorMsgYesNo(text, title=None):
	msgBox = QMessageBox()
	msgBox.setIcon(QMessageBox.Warning)
	msgBox.setWindowTitle(title)
	msgBox.setText(text)
	msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
	returnValue = msgBox.exec()
	if returnValue == QMessageBox.Yes:
		return True
	else:
		return False

def msgYesNoCheck(title, body_text, chkbx_text):
	chkBox = QCheckBox()
	chkBox.setText(chkbx_text)
	msgBox = QMessageBox()
	msgBox.setCheckBox(chkBox)
	msgBox.setIcon(QMessageBox.Warning)
	msgBox.setWindowTitle(title)
	msgBox.setText(body_text)
	msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
	returnValue = msgBox.exec()
	answer = True if returnValue == QMessageBox.Yes else False
	return answer, chkBox.isChecked()

def infoMsgOk(text, title=None):
	msgBox = QMessageBox()
	msgBox.setIcon(QMessageBox.Information)
	msgBox.setWindowTitle(title)
	msgBox.setText(text)
	msgBox.setStandardButtons(QMessageBox.Ok)
	returnValue = msgBox.exec()
	if returnValue == QMessageBox.Ok:
		return True
	else:
		return False


def aboutDialog(parent):
	dialogBox = QDialog()
	dialogBox.setMinimumSize(300, 300)
	dialogBox.setWindowTitle('About')

	layout = QVBoxLayout(dialogBox)


	titleLabel =  QLabel()
	titleLabel.setText('Mesa Configuration Tool')
	titleLabel.setAlignment(Qt.AlignCenter)
	layout.addWidget(titleLabel)

	imageLabel = QLabel()
	imageLabel.setAlignment(Qt.AlignCenter)

	image_path = os.path.join(parent.lib_path, 'mesact.jpg')
	pixmap = QPixmap(image_path)
	pixmap = pixmap.scaled(256, 256, Qt.KeepAspectRatio)
	imageLabel.setPixmap(pixmap)
	layout.addWidget(imageLabel)

	authorLabel =  QLabel()
	authorLabel.setText('Author: John Thornton')
	authorLabel.setAlignment(Qt.AlignCenter)
	layout.addWidget(authorLabel)

	versionLabel =  QLabel()
	versionLabel.setText(f'Version: {parent.version}')
	versionLabel.setAlignment(Qt.AlignCenter)
	layout.addWidget(versionLabel)

	aboutLabel =  QLabel()
	aboutLabel.setText('Mesa CT Creates LinuxCNC\nconfigurations for Mesa Boards')
	aboutLabel.setAlignment(Qt.AlignCenter)
	layout.addWidget(aboutLabel)


	websiteLabel =  QLabel()
	websiteLabel.setText("<a href='https://gnipsel.com/'>Authors Website</a>")
	websiteLabel.setAlignment(Qt.AlignCenter)
	websiteLabel.setOpenExternalLinks(True)
	layout.addWidget(websiteLabel)

	repoLabel =  QLabel()
	repoLabel.setText("<a href='https://github.com/jethornton/mesact'>Code Website</a>")
	repoLabel.setAlignment(Qt.AlignCenter)
	repoLabel.setOpenExternalLinks(True)
	layout.addWidget(repoLabel)


	copyrightLabel =  QLabel()
	copyrightLabel.setText('Copyright © 1953-2023 John Thornton')
	copyrightLabel.setAlignment(Qt.AlignCenter)
	layout.addWidget(copyrightLabel)


	layout.addStretch()

	buttonBox = QDialogButtonBox()
	buttonBox.setStandardButtons(QDialogButtonBox.Ok)
	buttonBox.setCenterButtons(True)
	#buttonBox.addButton("Credits", QDialogButtonBox.ActionRole)
	buttonBox.accepted.connect(dialogBox.close)
	layout.addWidget(buttonBox)

	dialogBox.exec()


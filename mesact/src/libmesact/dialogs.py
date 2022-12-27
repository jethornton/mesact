#!/usr/bin/env python3

from PyQt5.QtWidgets import QMessageBox

def errorMsgOk(text, title=None):
	#print(type(text))
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


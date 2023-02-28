#!/usr/bin/env python3

import os

from PyQt5.QtWidgets import QApplication, QFileDialog, QDialog

app = QApplication([])

if os.path.isdir(os.path.expanduser('~/linuxcnc/configs')):
	configsDir = os.path.expanduser('~/linuxcnc/configs')
else:
	configsDir = os.path.expanduser('~/')

options = QFileDialog.Options()
options |= QFileDialog.DontUseNativeDialog
options |= QFileDialog.DontUseCustomDirectoryIcons

dialog = QFileDialog(caption="Select Configuration INI File")
dialog.setOptions(options)
dialog.setDirectory(configsDir)
#dialog.caption("Select Configuration INI File")

if dialog.exec_() == QDialog.Accepted:
	path = dialog.selectedFiles()[0]
	print(type(path))
else:
	print('Canceled')

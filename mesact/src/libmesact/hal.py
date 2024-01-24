import os

from PyQt5.Qt import Qt

def custom_hal(parent, state):
	#CheckState Unchecked Checked
	if state == Qt.CheckState.Checked:
		parent.hal_tw.setTabVisible(1, True)
		txt = '# Put HAL commands in this file that you want to run before the GUI loads\n'
		if parent.custom_hal_pte.blockCount() == 1: # empty QPlainTextEdit
			parent.custom_hal_pte.setPlainText(txt)
	else:
		parent.hal_tw.setTabVisible(1, False)

def postgui_hal(parent, state):
	if state == Qt.CheckState.Checked:
		parent.hal_tw.setTabVisible(2, True)
		txt = '# Put HAL commands in this file that you want to run after the GUI loads\n'
		if parent.postgui_hal_pte.blockCount() == 1: # empty QPlainTextEdit
			parent.postgui_hal_pte.setPlainText(txt)
	else:
		parent.hal_tw.setTabVisible(2, False)

def shutdown_hal(parent, state):
	if state == Qt.CheckState.Checked:
		parent.hal_tw.setTabVisible(3, True)
		txt = '# Put HAL commands in this file that you want to run at Shutdown\n'
		if parent.shutdown_hal_pte.blockCount() == 1: # empty QPlainTextEdit
			parent.shutdown_hal_pte.setPlainText(txt)
	else:
		parent.hal_tw.setTabVisible(3, False)

def open_hal(parent, directory):
	custom_hal = os.path.join(directory, 'custom.hal')
	if os.path.isfile(custom_hal):
		with open(custom_hal,'r') as f:
			parent.custom_hal_pte.setPlainText(f.read())
	postgui_hal = os.path.join(directory, 'postgui.hal')
	if os.path.isfile(postgui_hal):
		with open(postgui_hal,'r') as f:
			parent.postgui_hal_pte.setPlainText(f.read())
	shutdown_hal = os.path.join(directory, 'shutdown.hal')
	if os.path.isfile(shutdown_hal):
		with open(shutdown_hal,'r') as f:
			parent.shutdown_hal_pte.setPlainText(f.read())





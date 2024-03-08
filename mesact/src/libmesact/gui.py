
from PyQt5.Qt import Qt

def gui_changed(parent):
	if parent.guiCB.currentData():
		if parent.guiCB.currentData() == 'flexgui':
			parent.flex_gui_gb.setEnabled(True)
		else:
			parent.flex_gui_gb.setEnabled(False)
			parent.keyboard_qss_cb.setChecked(False)
			parent.touch_qss_cb.setChecked(False)
			parent.flex_gui_le.setText('')
			parent.custom_qss_le.setText('')
			parent.flex_size_cb.setCurrentIndex(0)
	else:
		parent.flex_gui_gb.setEnabled(False)

def qss_changed(parent, state):
	if state == Qt.CheckState.Checked:
		if parent.sender().objectName() == 'keyboard_qss_cb':
			parent.touch_qss_cb.setChecked(False)
		elif parent.sender().objectName() == 'touch_qss_cb':
			parent.keyboard_qss_cb.setChecked(False)






from PyQt5.QtWidgets import QLineEdit, QComboBox, QDoubleSpinBox

from libmesact import preferences

def new(parent):
	children = parent.findChildren(QLineEdit)
	for child in children:
		child.clear()

	children = parent.findChildren(QComboBox)
	for child in children:
		if child.currentIndex() > 0:
			child.setCurrentIndex(0)

	children = parent.findChildren(QDoubleSpinBox)
	for child in children:
		child.setValue(0)

def open(parent):
	pass

def open_recent(parent):
	pass

def save(parent):
	pass

def save_as(parent):
	pass

def update(parent):
	parent.recent_menu.clear()
	for row, filename in enumerate(get_recent_files(), 1):
		recent_action = self.recent_menu.addAction('&{}. {}'.format(
			row, filename))
		recent_action.setData(filename)

def get_recent_files(parent):
	recent = self.settings.get('recent files')
	if not recent:
		# just for testing purposes
		recent = parent.settings['recent files'] = ['filename 4', 'filename1', 'filename2', 'filename3']
	return recent

def edit_preferences(parent):
	dialog = preferences.dialog(parent)
	dialog.exec()

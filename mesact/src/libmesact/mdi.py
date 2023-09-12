from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit

def get_mdi_commands_count(parent):
	# Workaround for QGridLayout.rowCount() that returns 1 for empty grid
	grid_layout: QGridLayout = parent.mdiCommandsListGL
	rows = 0
	grid_layout.rowCount()
	for i in range(grid_layout.count()):
		row, _, span, _ = grid_layout.getItemPosition(i)
		rows = max(1, row + span)
	return rows

def add_mdi_command_row(parent):
	grid_layout: QGridLayout = parent.mdiCommandsListGL
	row = get_mdi_commands_count(parent)
	__add_mdi_command_row(grid_layout, row)

def set_mdi_command(parent, command_number, value):
	row_count = get_mdi_commands_count(parent)
	i = row_count
	while i <= command_number:
		add_mdi_command_row(parent)
		i += 1
	text_box: QLineEdit = parent.findChild(QLineEdit, __get_mdi_command_control_name(command_number))
	text_box.setText(value)

def get_mdi_command(parent, command_number):
	rows_count = get_mdi_commands_count(parent)
	if rows_count == 0 or command_number >= rows_count:
		return ""
	text_box: QLineEdit = parent.findChild(QLineEdit, __get_mdi_command_control_name(command_number))
	return text_box.text().strip()

def cleanup_mdi_commands(parent):
	grid_layout: QGridLayout = parent.mdiCommandsListGL
	for i in reversed(range(grid_layout.count())):
		widget = grid_layout.itemAt(i).widget()
		grid_layout.removeWidget(widget)
		widget.setParent(None)
	for i in range(8):
		__add_mdi_command_row(grid_layout, i)

def __get_mdi_command_control_name(command_number):
	return f'mdiCmdLE_{command_number}'

def __add_mdi_command_row(grid_layout, row):
	label = QLabel(f'MDI Command {row}')
	grid_layout.addWidget(label, row, 0)
	text_box = QLineEdit()
	text_box.setObjectName(__get_mdi_command_control_name(row))
	grid_layout.addWidget(text_box, row, 1)

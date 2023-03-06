def ssCardChanged(parent):
	sscards = {
	'Select':'No Card Selected',
	'7i64':'24 Outputs, 24 Inputs',
	'7i69':'48 Digital I/O Bits',
	'7i70':'48 Inputs',
	'7i71':'48 Sourcing Outputs',
	'7i72':'48 Sinking Outputs',
	'7i73':'Pendant Card',
	'7i84':'32 Inputs 16 Outputs',
	'7i87':'8 Analog Inputs'
	}

	sspage = {
	'Select':0,
	'7i64':1,
	'7i69':2,
	'7i70':3,
	'7i71':4,
	'7i72':5,
	'7i73':6,
	'7i84':7,
	'7i87':8
	}
	parent.ss_info.setText(sscards[parent.ssCardCB.currentText()])
	parent.ss_pages.setCurrentIndex(sspage[parent.ssCardCB.currentText()])


def ss7i73Changed(parent):
	if parent.ss7i73lcdCB.currentData() == 'w7d': # no LCD
		parent.ss7i73w7Lbl.setText('W7 Down')
		lcd = False
	elif parent.ss7i73lcdCB.currentData() == 'w7u': # LCD
		parent.ss7i73w7Lbl.setText('W7 Up')
		lcd = True
	if parent.ss7i73_keypadCB.currentData()[0] == 'w5d':
		if parent.ss7i73_keypadCB.currentData()[1] == 'w6d': # no keypad
			parent.ss7i73w5Lbl.setText('W5 Down')
			parent.ss7i73w6Lbl.setText('W6 Down')
			keypad = False
		elif parent.ss7i73_keypadCB.currentData()[1] == 'w6u': # 4x8 keypad
			parent.ss7i73w5Lbl.setText('W5 Down')
			parent.ss7i73w6Lbl.setText('W6 Up')
			keypad = True
			keys = '4x8'
	elif parent.ss7i73_keypadCB.currentData()[0] == 'w5u': # 8x8 keypad
			parent.ss7i73w5Lbl.setText('W5 Up')
			parent.ss7i73w6Lbl.setText('W6 Down')
			keypad = True
			keys = '8x8'

	# No LCD No Keypad
	if not lcd and not keypad:
		for i in range(8):
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Output {i+10}')
			button = getattr(parent, f'ss7i73key_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)
		for i in range(8,16):
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Input {i+8}')
			button = getattr(parent, f'ss7i73key_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(inputs, menu)
			button.setMenu(menu)
		for i in range(8):
			getattr(parent, 'ss7i73lcd_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Output {i+2}')
			button = getattr(parent, f'ss7i73lcd_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)
		for i in range(8,12):
			getattr(parent, 'ss7i73lcd_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Output {i+10}')
			button = getattr(parent, f'ss7i73lcd_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)

	# LCD No Keypad
	if lcd and not keypad:
		for i in range(8):
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Output {i+6}')
			button = getattr(parent, f'ss7i73key_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)
		for i in range(8,16):
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Input {i+8}')
			button = getattr(parent, f'ss7i73key_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(inputs, menu)
			button.setMenu(menu)
		for i in range(4):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Output {i+2}')
			button = getattr(parent, f'ss7i73lcd_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)
		for i in range(4,12):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'LCD {i}')
			getattr(parent, 'ss7i73lcd_' + str(i)).setEnabled(False)

	# LCD 4x8 Keypad
	if lcd and keypad and keys == '4x8':
		for i in range(4):
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Output {i+6}')
			button = getattr(parent, f'ss7i73key_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)
		for i in range(4,16):
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Key {i}')
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(False)
		for i in range(5):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Output {i+2}')
			button = getattr(parent, f'ss7i73lcd_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)
		for i in range(4,12):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'LCD {i}')
			getattr(parent, 'ss7i73lcd_' + str(i)).setEnabled(False)

	# LCD 8x8 Keypad
	if lcd and keypad and keys == '8x8':
		for i in range(16):
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Key {i}')
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(False)
		for i in range(5):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Output {i+2}')
			button = getattr(parent, f'ss7i73lcd_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)
		for i in range(4,12):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'LCD {i}')
			getattr(parent, 'ss7i73lcd_' + str(i)).setEnabled(False)

	# No LCD 4x8 Keypad
	if not lcd and keypad and keys == '4x8':
		for i in range(4):
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Output {i+10}')
			button = getattr(parent, f'ss7i73key_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)

		for i in range(4,16):
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Key {i}')
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(False)
		for i in range(8):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Output {i+2}')
			button = getattr(parent, f'ss7i73lcd_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)
		for i in range(8,12):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Output {i+6}')
			button = getattr(parent, f'ss7i73lcd_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)

	# No LCD 8x8 Keypad
	if not lcd and keypad and keys == '8x8':
		for i in range(16):
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Key {i}')
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(False)
		for i in range(12):
			getattr(parent, 'ss7i73lcd_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Output {i+2}')
			button = getattr(parent, f'ss7i73lcd_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)


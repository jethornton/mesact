import os

from libmesact import downloads

def load(parent):
	# firmware combobox
	parent.firmwareCB.clear()
	parent.firmwareDescPTE.clear()
	board = parent.boardCB.currentData()
	path = os.path.join(parent.firmware_path, board)
	if os.path.exists(path):
		firmware = ['.bit', '.bin']
		extensions = list(set(os.path.splitext(file)[-1] for file in os.listdir(path)))
		if any(x in firmware for x in extensions):
			files = sorted([entry.path for entry in os.scandir(path) if entry.is_file()])
			parent.firmwareCB.addItem('Select', False)
			for file in files:
				if os.path.splitext(file)[1] in firmware:
					parent.firmwareCB.addItem(os.path.basename(file), file)
			parent.firmwarePTE.clear()
			parent.firmwarePTE.appendPlainText(f'Firmware for {parent.boardCB.currentText()} Loaded')
		else:
			noFirmware(parent, board)
	else:
		noFirmware(parent, board)

def noFirmware(parent, board):
	#  if someone selects a board can you check for the firmware and ask in a dialog to DL?
	parent.firmwareTW.setCurrentIndex(1)
	msg = (f'No Firmware found for the {board}\n'
	'Downloads > Firmware from the menu if you have an Internet connection\n'
	'The firmware will be to downloaded and installed\n'
	f'in {os.path.expanduser("~")}/.local/lib/libmesact/{board}.\n\n'
	'If you do not have an Internet connection\nfrom another computer download from \n'
	f'https://github.com/jethornton/mesact_firmware/releases/download/1.0.0/{board}.tar.xz\n'
	f'Extract the firmware to {os.path.expanduser("~")}/.local/lib/libmesact/{board}')
	parent.firmwarePTE.setPlainText(msg)
	#		check_state = settings.value(SETTINGS_TRAY, False, type=bool)
	#print(parent.settings.value('test', False, type=bool))
	#print(parent.settings.value('no_nag_firmware', None, type=bool))
	#print(True if parent.settings.value('no_nag_firmware') == "true" else False)
	# msgYesNoCheck(self, title=None, body_text, chkbx_text="Don't show this message again"):

	if parent.settings.value('NAGS/firmware', None, type=bool):
		msg = (f'No Firmware was found for the {board}.\n'
		'Do you want to download the firmware now?')
		response, no_nag = parent.msgYesNoCheck('Firmware', msg, "Don't Check for Firmware Again!")
		if response:
			downloads.downloadFirmware(parent)
		if no_nag:
			parent.settings.setValue('NAGS/firmware', False)
			parent.no_check_firmware_cb.setChecked(False)
		else:
			parent.settings.setValue('NAGS/firmware', True)
			parent.no_check_firmware_cb.setChecked(True)

def firmwareChanged(parent):
	if parent.firmwareCB.currentData():
		parent.firmware_lb.setText(parent.firmwareCB.currentText())
		parent.firmwareTW.setCurrentIndex(1)
		board = parent.boardCB.currentData()
		if '-' in board:
			board = board.replace("-", "_")

		path = os.path.splitext(parent.firmwareCB.currentData())[0]

		pinfile = os.path.join(path + '.pin')
		if os.path.exists(pinfile):
			stepgens = 0
			pwmgens = 0
			encoders = 0

			# get smart serial channels for each connector
			p1 = False
			p2 = False
			parent.p2_channels = []
			parent.p1_channels = []
			with open(pinfile, 'r') as file:
				for line in file:
					if 'of StepGen in configuration' in line:
						stepgens = int(''.join(filter(str.isdigit, line)))
					if 'of PWM in configuration' in line:
						pwmgens = int(''.join(filter(str.isdigit, line)))
					if 'of QCount in configuration' in line:
						encoders = int(''.join(filter(str.isdigit, line)))
					if 'P1' in line:
						p1 = True
						p2 = False
					if 'P2' in line:
						p1 = False
						p2 = True
					if p1:
						if 'TXData' in line:
							for word in line.split():
								if word.startswith('TXData'):
									parent.p1_channels.append(word[-1])
					if p2:
						if 'TXData' in line:
							for word in line.split():
								if word.startswith('TXData'):
									parent.p2_channels.append(word[-1])

			parent.p1_channels.sort()
			parent.p2_channels.sort()
			parent.p2_channels_lb.setText(', '.join(parent.p2_channels))
			parent.p1_channels_lb.setText(', '.join(parent.p1_channels))

			parent.stepgens_cb.clear()
			parent.pwmgens_cb.clear()
			parent.encoders_cb.clear()

			for i in reversed(range(stepgens + 1)):
				parent.stepgens_cb.addItem(str(i), i)
			for i in reversed(range(pwmgens + 1)):
				parent.pwmgens_cb.addItem(str(i), i)
			for i in reversed(range(encoders + 1)):
				parent.encoders_cb.addItem(str(i), i)

			with open(pinfile, 'r') as file:
				data = file.read()
			parent.firmwarePTE.clear()
			parent.firmwarePTE.setPlainText(data)

		descfile = os.path.join(path + '.txt')
		if os.path.exists(descfile):
			with open(descfile, 'r') as file:
				data = file.read()
			parent.firmwareDescPTE.clear()
			parent.firmwareDescPTE.setPlainText(data)
		else:
			parent.firmwareDescPTE.clear()
			parent.firmwareDescPTE.setPlainText(f'No description file found\n')


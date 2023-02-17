import os

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
	msg = (f'No Firmware found for {board}\n'
	'Downloads > Firmware from the menu if you have an Internet connection\n'
	'The firmware will be to downloaded and installed\n'
	f'in {os.path.expanduser("~")}/.local/lib/libmesact/{board}.\n\n'
	'If you do not have an Internet connection\nfrom another computer download from \n'
	f'https://github.com/jethornton/mesact_firmware/releases/download/1.0.0/{board}.tar.xz\n'
	f'Extract the firmware to {os.path.expanduser("~")}/.local/lib/libmesact/{board}')
	parent.firmwarePTE.setPlainText(msg)

def firmwareChanged(parent):
	if parent.firmwareCB.currentData():
		board = parent.boardCB.currentData()
		if '-' in board:
			board = board.replace("-", "_")

		path = os.path.splitext(parent.firmwareCB.currentData())[0]

		pinfile = os.path.join(path + '.pin')
		if os.path.exists(pinfile):
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
			parent.firmwareDescPTE.setPlainText(f'No description file found\n'
				'for {parent.firmwareCB.currentText()}')


	'''

		if parent.boardCB.currentData() in parent.mainBoards:
			daughters = getattr(firmware, f'd{board}')(parent)
			if parent.firmwareCB.currentText() in daughters:
				cards = daughters[parent.firmwareCB.currentText()]
				parent.daughterCB_0.clear()
				if cards[0]:
					parent.daughterCB_0.addItem('Select', False)
					parent.daughterCB_0.addItem(cards[0], cards[0])
				parent.daughterCB_1.clear()
				if cards[1]:
					parent.daughterCB_1.addItem('Select', False)
					parent.daughterCB_1.addItem(cards[1], cards[1])
			else:
				parent.daughterCB_0.clear()
				parent.daughterCB_1.clear()

		# might combine these
		elif  parent.boardCB.currentData() in parent.allInOneBoards:
			daughters = getattr(firmware, f'd{board}')(parent)
			if daughters:
				if parent.firmwareCB.currentText() in daughters:
					cards = daughters[parent.firmwareCB.currentText()]
					parent.daughterCB_0.clear()
					if cards[0]:
						parent.daughterCB_0.addItem('Select', False)
						parent.daughterCB_0.addItem(cards[0], cards[0])
					parent.daughterCB_1.clear()
					if cards[1]:
						parent.daughterCB_1.addItem('Select', False)
						parent.daughterCB_1.addItem(cards[1], cards[1])
				else:
					parent.daughterCB_0.clear()
					parent.daughterCB_1.clear()

			if "7i92t" in pinfile:
				gpio = []
				with open(pinfile, 'r') as f:
					for line in f:
						if 'IOPort' in line:
							lst = line.split()
							if lst[1].isnumeric():
								gpio.append(lst)
				for i in range(34):
					try:
						getattr(parent, f'gpioPinLB_{i}').setText(gpio[i][0])
						getattr(parent, f'gpioSecLB_{i}').setText(gpio[i][3])
						if gpio[i][3] != 'None':
							getattr(parent, f'gpioChanLB_{i}').setText(gpio[i][4])
							getattr(parent, f'gpioFunctionLB_{i}').setText(gpio[i][5])
							getattr(parent, f'gpioDirLB_{i}').setText(gpio[i][6])
					except Exception as e:
						parent.p1LB.setText('Error Loading Pins')
						parent.p2LB.setText('Error Loading Pins')
						print(e)

		else:
			parent.machinePTE.clear()
			parent.machinePTE.setPlainText(f'No pin file found for {parent.firmwareCB.currentText()}')

		options = getattr(firmware, f'o{board}')(parent)
		# options stepgens, pwmgens, qcount
		if options:
			if parent.firmwareCB.currentText() in options:
				parent.stepgensCB.clear()
				if options[parent.firmwareCB.currentText()][0]:
					for i in range(options[parent.firmwareCB.currentText()][0], -1, -1):
						parent.stepgensCB.addItem(f'{i}', f'{i}')
				parent.pwmgensCB.clear()
				if options[parent.firmwareCB.currentText()][1]:
					for i in range(options[parent.firmwareCB.currentText()][1], -1, -1):
						parent.pwmgensCB.addItem(f'{i}', f'{i}')
				parent.encodersCB.clear()
				if options[parent.firmwareCB.currentText()][2]:
					for i in range(options[parent.firmwareCB.currentText()][2], -1, -1):
						parent.encodersCB.addItem(f'{i}', f'{i}')
	else:
		parent.machinePTE.clear()
		parent.daughterCB_0.clear()
		parent.daughterCB_1.clear()
	'''



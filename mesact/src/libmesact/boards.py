from libmesact import firmware

def boardChanged(parent):
	# daughter cards
	db25 = [
	['Select', None],
	['7i76', '7i76'],
	['7i77', '7i77'],
	['7i78', '7i78'],
	['7i85', '7i85'],
	['7i85S', '7i85s']
	]
	idc50 = [
	['Select', None],
	['7i33TA', '7i33ta'],
	['7i37TA', '7i37ta'],
	['7i47', '7i47'],
	['7i47S', '7i47s']
	]

	if parent.boardCB.currentData():
		board = parent.boardCB.currentData()
		parent.board_0 = parent.boardCB.currentData()
		name = parent.boardCB.currentText()
		if parent.mesaflash:
			parent.verify_board_pb.setEnabled(True)
		# set all tabs visible then hide as needed
		for i in range(10):
			parent.c0_JointTW.setTabVisible(i, True)
		firmware.load(parent)
		tabs = parent.c0_JointTW.count()
		parent.daughterCB_0.clear()
		parent.daughterCB_1.clear()
		parent.daughterLB_0.clear()
		parent.daughterLB_1.clear()
		parent.ipAddressCB.setEnabled(False)
		parent.mainTW.setTabVisible(3, True)
		parent.mainTW.setTabText(3, name)
		for i in range(3): # show output tabs
			for j in range(6):
				getattr(parent, f'c{i}_settings_{j}').setTabVisible(2, True)
				getattr(parent, f'c{i}_settings_{j}').setTabVisible(3, True)
				getattr(parent, f'c{i}_settings_{j}').setTabVisible(4, True)
		for i in range(1, 7):
			parent.spindleTypeCB.model().item(i).setEnabled(False)
		parent.firmware_options_lb.setText('No Firmware Selected!')
		# Configure Options
		parent.stepgens_cb.clear()
		parent.stepgens_cb.addItem('n/a', 0)
		parent.pwmgens_cb.clear()
		parent.pwmgens_cb.addItem('n/a', 0)
		parent.encoders_cb.clear()
		parent.encoders_cb.addItem('n/a', 0)
		parent.port_0_channels_lb.clear()
		parent.port_1_channels_lb.clear()

		if board == '5i24': # PCI IDC50
			parent.hal_name = '5i24'
			parent.boardType = 'pci'
			parent.c0_JointTW.setTabText(0, name)
			for i in range(1, tabs + 1):
				parent.c0_JointTW.setTabVisible(i, False)
			parent.daughterLB_0.setText('P2')
			parent.daughterLB_1.setText('P3')
			parent.mainTW.setTabText(4, 'P2')
			parent.mainTW.setTabText(5, 'P3')
			for item in idc50:
				parent.daughterCB_0.addItem(item[0], item[1])
				parent.daughterCB_1.addItem(item[0], item[1])

		elif board == '5i25': # PCI DB25F IDC26
			# port 0 is P3 port 1 is P2
			parent.hal_name = '5i25'
			parent.boardType = 'pci'
			parent.c0_JointTW.setTabText(0, name)
			for i in range(1, tabs + 1):
				parent.c0_JointTW.setTabVisible(i, False)
			parent.daughterLB_0.setText('P2')
			parent.daughterLB_1.setText('P3')
			parent.ss_port_0_lb.setText('P2')
			parent.ss_port_1_lb.setText('P3')
			#parent.mainTW.setTabText(4, 'P2')
			#parent.mainTW.setTabText(5, 'P3')
			for item in db25:
				parent.daughterCB_0.addItem(item[0], item[1])
				parent.daughterCB_1.addItem(item[0], item[1])

		elif board == '7i76e': # ETH 5 Axis Step/Direction
			parent.hal_name = '7i76e'
			# 5 step/dir 32 inputs 16 outputs 1 spindle 1 encoder
			parent.boardType = 'eth'
			parent.c0_JointTW.setTabText(0, name)
			parent.c0_JointTW.setTabVisible(6, False)
			parent.ipAddressCB.setEnabled(True)
			parent.daughterLB_0.setText('P1')
			parent.daughterLB_1.setText('P2')
			parent.mainTW.setTabText(4, 'P1')
			parent.mainTW.setTabText(5, 'P2')
			info = ('Connector 5v Power\n'
			'W7 Up for P1\n'
			'W12 Up for P2\n'
			'\nIP Address\nW2 Down W3 Up for 10.10.10.10\n'
			'\nDefault Firmware 7i76e_7i76x1D.bit\n'
			)
			parent.hal_name_info_pte.setPlainText(info)

			for item in db25:
				parent.daughterCB_0.addItem(item[0], item[1])
				parent.daughterCB_1.addItem(item[0], item[1])
			for j in range(32):
				getattr(parent, f'c0_input_{j}').setEnabled(True)
				getattr(parent, f'c0_input_invert_{j}').setEnabled(True)
				getattr(parent, f'c0_input_debounce_{j}').setEnabled(False)
			for i in range(6): # hide analog and encoder tabs
				getattr(parent, f'c0_settings_{i}').setTabVisible(3, False)
				getattr(parent, f'c0_settings_{i}').setTabVisible(4, False)

		elif board == '7i80db-16': # ETH DB25F
			parent.hal_name = '7i80db-16'
			parent.boardType = 'eth'
			parent.c0_JointTW.setTabText(0, name)
			for i in range(1, tabs + 1):
				parent.c0_JointTW.setTabVisible(i, False)
			parent.ipAddressCB.setEnabled(True)
			parent.daughterLB_0.setText('J2')
			parent.daughterLB_1.setText('J3')
			parent.mainTW.setTabText(4, 'J2')
			parent.mainTW.setTabText(5, 'J3')
			for item in db25:
				parent.daughterCB_0.addItem(item[0], item[1])
				parent.daughterCB_1.addItem(item[0], item[1])

		elif board == '7i80db-25': # ETH DB25F
			parent.hal_name = '7i80db-25'
			parent.boardType = 'eth'
			parent.c0_JointTW.setTabText(0, name)
			for i in range(1, tabs + 1):
				parent.c0_JointTW.setTabVisible(i, False)
			parent.ipAddressCB.setEnabled(True)
			parent.daughterLB_0.setText('J2')
			parent.daughterLB_1.setText('J3')
			parent.mainTW.setTabText(4, 'J2')
			parent.mainTW.setTabText(5, 'J3')
			for item in db25:
				parent.daughterCB_0.addItem(item[0], item[1])
				parent.daughterCB_1.addItem(item[0], item[1])

		elif board == '7i80hd-16': # ETH IDC50
			parent.hal_name = '7i80hd-16'
			parent.boardType = 'eth'
			parent.c0_JointTW.setTabText(0, name)
			for i in range(1, tabs + 1):
				parent.c0_JointTW.setTabVisible(i, False)
			parent.ipAddressCB.setEnabled(True)
			parent.daughterLB_0.setText('P1')
			parent.daughterLB_1.setText('P2')
			parent.mainTW.setTabText(4, 'P1')
			parent.mainTW.setTabText(5, 'P2')
			for item in idc50:
				parent.daughterCB_0.addItem(item[0], item[1])
				parent.daughterCB_1.addItem(item[0], item[1])

		elif board == '7i80hd-25': # ETH IDC50
			parent.hal_name = '7i80hd-25'
			parent.boardType = 'eth'
			parent.c0_JointTW.setTabText(0, name)
			for i in range(1, tabs + 1):
				parent.c0_JointTW.setTabVisible(i, False)
			parent.ipAddressCB.setEnabled(True)
			parent.daughterLB_0.setText('P1')
			parent.daughterLB_1.setText('P2')
			parent.mainTW.setTabText(4, 'P1')
			parent.mainTW.setTabText(5, 'P2')
			for item in idc50:
				parent.daughterCB_0.addItem(item[0], item[1])
				parent.daughterCB_1.addItem(item[0], item[1])

		elif board == '7i80hd-ts': # ETH IDC50
			parent.hal_name = '7i80hd-ts'
			parent.boardType = 'eth'
			parent.c0_JointTW.setTabText(0, name)
			for i in range(1, tabs + 1):
				parent.c0_JointTW.setTabVisible(i, False)
			parent.ipAddressCB.setEnabled(True)
			parent.daughterLB_0.setText('P1')
			parent.daughterLB_1.setText('P2')
			parent.mainTW.setTabText(4, 'P1')
			parent.mainTW.setTabText(5, 'P2')
			for item in idc50:
				parent.daughterCB_0.addItem(item[0], item[1])
				parent.daughterCB_1.addItem(item[0], item[1])

		elif board == '7i92': # ETH DB25F IDC26
			parent.hal_name = '7i92'
			parent.boardType = 'eth'
			parent.c0_JointTW.setTabText(0, name)
			for i in range(1, tabs + 1):
				parent.c0_JointTW.setTabVisible(i, False)
			parent.ipAddressCB.setEnabled(True)
			parent.daughterLB_0.setText('P1')
			parent.daughterLB_1.setText('P2')
			parent.mainTW.setTabText(4, 'P1')
			parent.mainTW.setTabText(5, 'P2')
			for item in db25:
				parent.daughterCB_0.addItem(item[0], item[1])
				parent.daughterCB_1.addItem(item[0], item[1])

		elif board == '7i92t': # ETH DB25F IDC26
			parent.hal_name = '7i92'
			parent.boardType = 'eth'
			parent.c0_JointTW.setTabText(0, name)
			info = ('Connector 5v Power\n'
			'W3 Up for P1\n'
			'W4 Up for P2\n'
			'\nIP Address Settings\n'
			'W5 Down W6 Up for 10.10.10.10\n'
			'Power off before moving jumpers\n'
			'\nDefault firmware 7i92t_g540d.bin'
			)
			parent.hal_name_info_pte.setPlainText(info)
			for i in range(1, tabs + 1):
				parent.c0_JointTW.setTabVisible(i, False)
			parent.ipAddressCB.setEnabled(True)
			parent.daughterLB_0.setText('P1')
			parent.daughterLB_1.setText('P2')
			for item in db25:
				parent.daughterCB_0.addItem(item[0], item[1])
				parent.daughterCB_1.addItem(item[0], item[1])

		elif board == '7i93': # ETH IDC50
			parent.hal_name = '7i93'
			parent.boardType = 'eth'
			parent.c0_JointTW.setTabText(0, name)
			for i in range(1, tabs + 1):
				parent.c0_JointTW.setTabVisible(i, False)
			parent.ipAddressCB.setEnabled(True)
			parent.daughterLB_0.setText('P1')
			parent.daughterLB_1.setText('P2')
			parent.mainTW.setTabText(4, 'P1')
			parent.mainTW.setTabText(5, 'P2')
			for item in idc50:
				parent.daughterCB_0.addItem(item[0], item[1])
				parent.daughterCB_1.addItem(item[0], item[1])

		elif board == '7i95': # ETH 6 Axis Step/Direction
			parent.hal_name = '7i95'
			parent.boardType = 'eth'
			parent.c0_JointTW.setTabText(0, name)
			parent.ipAddressCB.setEnabled(True)
			parent.daughterLB_0.setText('P1')
			parent.mainTW.setTabText(4, 'P1')
			for item in db25:
				parent.daughterCB_0.addItem(item[0], item[1])
			for i in range(6): # hide analog and encoder tabs
				getattr(parent, f'c0_settings_{i}').setTabVisible(3, False)
				getattr(parent, f'c0_settings_{i}').setTabVisible(4, False)

		elif board == '7i95t': # ETH 6 Axis Step/Direction
			parent.hal_name = '7i95'
			parent.boardType = 'eth'
			parent.c0_JointTW.setTabText(0, name)
			parent.ipAddressCB.setEnabled(True)
			parent.daughterLB_0.setText('P1')
			parent.mainTW.setTabText(4, 'P1')
			info = ('The 7i95T requires LinuxCNC version 2.10 to run\n'
			'\nTo Flash the 7i95T Mesaflash version 3.4.7\nor newer must be installed\n'
			'\nIP Address Jumpers\nW15 Down W16 Up for 10.10.10.10\n'
			'\nDefault firmware 7i95t_d.bin'
			)
			parent.hal_name_info_pte.setPlainText(info)
			for item in db25:
				parent.daughterCB_0.addItem(item[0], item[1])
			for i in range(6): # hide analog tabs
				getattr(parent, f'c0_settings_{i}').setTabVisible(3, False)

			if parent.mesaflash:
				if parent.mesaflash_version < (3, 4, 7):
					parent.firmwareGB.setEnabled(False)
					parent.checkBoardPB.setEnabled(False)
					parent.read_hmid_gb.setEnabled(False)
					parent.firmware_info_pte.setPlainText('The 7i95T requires Mesaflash 3.4.7 or newer')

		elif board == '7i96': # ETH 5 Axis Step/Direction
			parent.hal_name = '7i96'
			parent.boardType = 'eth'
			parent.c0_JointTW.setTabText(0, name)
			parent.c0_JointTW.setTabVisible(6, False)
			parent.ipAddressCB.setEnabled(True)
			parent.daughterLB_0.setText('P1')
			parent.mainTW.setTabText(4, 'P1')
			info = ('Connector 5v Power\n'
			'W8 Up for P1\n'
			'\nIP Address\nW5 Down W6 Up for 10.10.10.10\n'
			'\nDefault Firmware 7i96d.bit\n'
			)
			parent.hal_name_info_pte.setPlainText(info)
			for item in db25:
				parent.daughterCB_0.addItem(item[0], item[1])
			for i in range(6): # hide analog and encoder tabs
				getattr(parent, f'c0_settings_{i}').setTabVisible(3, False)
				getattr(parent, f'c0_settings_{i}').setTabVisible(4, False)

		elif board == '7i96s': # ETH 5 Axis Step/Direction
			parent.hal_name = '7i96s'
			parent.boardType = 'eth'
			# 5 step/dir 11 inputs 6 outputs 1 spindle 1 encoder
			parent.c0_JointTW.setTabText(0, name)
			parent.c0_JointTW.setTabVisible(6, False)
			parent.ipAddressCB.setEnabled(True)
			parent.daughterLB_0.setText('P1')
			parent.mainTW.setTabText(4, 'P1')
			info = ('Connector 5v Power\n'
			'W6 Up for P1\n'
			'\nIP Address\nW4 Down W5 Up for 10.10.10.10\n'
			'\nDefault Firmware 7i96s_d.bit\n'
			)
			parent.hal_name_info_pte.setPlainText(info)
			for item in db25:
				parent.daughterCB_0.addItem(item[0], item[1])
			for j in range(11):
				getattr(parent, f'c0_input_{j}').setEnabled(True)
				getattr(parent, f'c0_input_invert_{j}').setEnabled(True)
				getattr(parent, f'c0_input_debounce_{j}').setEnabled(True)
			for j in range(11,32):
				getattr(parent, f'c0_input_{j}').setEnabled(False)
				getattr(parent, f'c0_input_invert_{j}').setEnabled(False)
				getattr(parent, f'c0_input_debounce_{j}').setEnabled(False)
			for j in range(6,16):
				getattr(parent, f'c0_output_{j}').setEnabled(False)
				getattr(parent, f'c0_output_invert_{j}').setEnabled(False)
			for i in range(6): # hide analog and encoder tabs
				getattr(parent, f'c0_settings_{i}').setTabVisible(3, False)
				getattr(parent, f'c0_settings_{i}').setTabVisible(4, False)
			parent.pwmFrequencySB.setValue(15000)
			parent.spindleGB.setEnabled(True)
			parent.spindleTypeCB.model().item(1).setEnabled(True)
			for i in range(2, 7):
				parent.spindleTypeCB.model().item(i).setEnabled(False)

		elif board == '7i97': # ETH 6 Axis Analog
			parent.hal_name = '7i97'
			parent.boardType = 'eth'
			parent.c0_JointTW.setTabText(0, name)
			parent.ipAddressCB.setEnabled(True)
			parent.daughterLB_0.setText('P1')
			parent.mainTW.setTabText(4, 'P1')
			for item in db25:
				parent.daughterCB_0.addItem(item[0], item[1])
			for i in range(6): # hide stepper tab
				getattr(parent, f'c0_settings_{i}').setTabVisible(2, False)

		elif board == '7i97t': # ETH 6 Axis Analog
			parent.hal_name = '7i97'
			parent.boardType = 'eth'
			parent.c0_JointTW.setTabText(0, name)
			parent.ipAddressCB.setEnabled(True)
			parent.daughterLB_0.setText('P1')
			parent.mainTW.setTabText(4, 'P1')
			for item in db25:
				parent.daughterCB_0.addItem(item[0], item[1])
			for i in range(6): # hide stepper tab
				getattr(parent, f'c0_settings_{i}').setTabVisible(2, False)

		elif board == '7i98': # ETH IDC26
			parent.hal_name = '7i98'
			parent.boardType = 'eth'
			parent.c0_JointTW.setTabText(0, name)
			for i in range(1, tabs + 1):
				parent.c0_JointTW.setTabVisible(i, False)
			parent.ipAddressCB.setEnabled(True)
			parent.daughterLB_0.setText('P1')
			parent.daughterLB_1.setText('P2')
			parent.mainTW.setTabText(4, 'P1')
			parent.mainTW.setTabText(5, 'P2')
			for item in db25:
				parent.daughterCB_0.addItem(item[0], item[1])
				parent.daughterCB_1.addItem(item[0], item[1])

	else: # no board is selected
		parent.hal_name = ''
		parent.boardType = False
		parent.c0_JointTW.setTabText(0, 'Board')
		parent.mainTW.setTabVisible(3, False)
		parent.daughterCB_0.clear()
		parent.daughterCB_1.clear()
		parent.spindleGB.setEnabled(False)
		# if no board is selected turn off mesaflash tools
		parent.firmwareGB.setEnabled(False)
		parent.verify_board_pb.setEnabled(False)
		parent.read_hmid_gb.setEnabled(False)
		parent.firmware_info_pte.clear()
		parent.firmwareCB.clear()


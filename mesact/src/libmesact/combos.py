import shutil

def build(parent):
	# Machine Tab
	boards = [
	['Select', False],
	['5i24/6i24', '5i24'],
	['5i25/6i25', '5i25'],
	['7i76e', '7i76e'],
	['7i80DB-16', '7i80db16'],
	['7i80DB-25', '7i80db25'],
	['7i80HD-16', '7i80hd16'],
	['7i80HD-25', '7i80hd25'],
	['7i80HD-TS', '7i80hdts'],
	['7i92', '7i92'],
	['7i92T', '7i92t'],
	['7i93', '7i93'],
	['7i95', '7i95'],
	['7i96', '7i96'],
	['7i96S', '7i96s'],
	['7i97', '7i97'],
	['7i98', '7i98'],
	]

	for item in boards:
		parent.boardCB.addItem(item[0], item[1])

	ipAddress = [
	['Select', False],
	['10.10.10.10', '10.10.10.10'],
	['192.168.1.121', '192.168.1.121']
	]

	for item in ipAddress:
		parent.ipAddressCB.addItem(item[0], item[1])
	parent.ipAddressCB.setEditable(True)

	# Firmware Tab

	db25_daughters = [
	['Select', False],
	['7i74', '7i74'],
	['7i76', '7i76'],
	['7i77', '7i77'],
	['7i78', '7i78'],
	['7i85', '7i85'],
	['7i85s', '7i85s'],
	['7i88', '7i88'],
	['7i89', '7i89']
	]

	for i in range(1, 3):
		for item in db25_daughters:
			getattr(parent, f'hmid_terminals_{i}').addItem(item[0], item[1])

	# Settings Tab
	gui = [
		['Select', False],
		['Axis', 'axis'],
		['Gmoccapy', 'gmoccapy'],
		['Tklinuxcnc', 'tklinuxcnc'],
		['Touchy', 'touchy']
		]

	for item in gui:
		parent.guiCB.addItem(item[0], item[1])

	linearUnits = [
		['Select', False],
		['Inch', 'inch'],
		['Millimeter', 'mm']
		]

	for item in linearUnits:
		parent.linearUnitsCB.addItem(item[0], item[1])

	positionOffset = [
		['Select', False],
		['Relative', 'RELATIVE'],
		['Machine', 'MACHINE']
		]

	for item in positionOffset:
		parent.positionOffsetCB.addItem(item[0], item[1])

	positionFeedback = [
		['Select', False],
		['Commanded', 'COMMANDED'],
		['Actual', 'ACTUAL']
		]

	for item in positionFeedback:
		parent.positionFeedbackCB.addItem(item[0], item[1])

	editors = {'Gedit':'gedit', 'Geany':'geany', 'Pyroom':'pyroom',
		'Pluma':'pluma', 'Scite':'scite', 'Kwrite':'kwrite',
		'Kate':'kate', 'Mousepad':'mousepad', 'Jedit':'jedit',
		'XED':'xed'}
	installed = False
	for key, value in editors.items():
		if shutil.which(value) is not None:
			if not installed:
				parent.editorCB.addItem('Select', False)
				installed = True
			parent.editorCB.addItem(key, value)
	if not installed:
		parent.editorCB.addItem('None', False)
		parent.machinePTE.appendPlainText('No Editors were found!')

	# Joint Tabs

	axes = [
		['Select', False],
		['X', 'X'],
		['Y', 'Y'],
		['Z', 'Z'],
		['A', 'A'],
		['B', 'B'],
		['C', 'C'],
		['U', 'U'],
		['V', 'V'],
		['W', 'W']
		]

	for i in range(4):
		for j in range(6):
			for item in axes:
				getattr(parent, f'c{i}_axis_{j}').addItem(item[0], item[1])

	drives = [
		['Custom', False],
		['Gecko 201', ['500', '4000', '20000', '1000']],
		['Gecko 202', ['500', '4500', '20000', '1000']],
		['Gecko 203v', ['1000', '2000', '200', '200']],
		['Gecko 210', ['500', '4000', '20000', '1000']],
		['Gecko 212', ['500', '4000', '20000', '1000']],
		['Gecko 320', ['3500', '500', '200', '200']],
		['Gecko 540', ['1000', '2000', '200', '200']],
		['TB6600', ['5000', '5000', '20000', '20000']],
		['L297', ['500', '4000', '4000', '1000']],
		['PMDX 150', ['1000', '2000', '1000', '1000']],
		['Sherline', ['22000', '22000', '100000', '100000']],
		['Xylotex BS-3', ['2000', '1000', '200', '200']],
		['Parker 750', ['1000', '1000', '1000', '200000']],
		['JVL SMD41/42', ['500', '500', '2500', '2500']],
		['Hobbycnc', ['2000', '2000', '2000', '2000']],
		['Keling 4030', ['5000', '5000', '20000', '20000']]
		]

	for i in range(4):
		for j in range(6):
			for item in drives:
				getattr(parent, f'c{i}_drive_{j}').addItem(item[0], item[1])

	# Spindle Tab

	# SS Card Tab
	ssCards = [
		['Select', False],
		['7i64', '7i64'],
		['7i69', '7i69'],
		['7i70', '7i70'],
		['7i71', '7i71'],
		['7i72', '7i72'],
		['7i73', '7i73'],
		['7i84', '7i84'],
		['7i87', '7i87']
		]

	for item in ssCards:
		parent.ssCardCB.addItem(item[0], item[1])

	# 7i73 Combo Boxes
	parent.ss7i73_keypadCB.addItem('None', ['w5d', 'w6d'])
	parent.ss7i73_keypadCB.addItem('4x8', ['w5d', 'w6u'])
	parent.ss7i73_keypadCB.addItem('8x8', ['w5u', 'w6d'])

	parent.ss7i73lcdCB.addItem('None', 'w7d')
	parent.ss7i73lcdCB.addItem('Enabled', 'w7u')

	cpuSpeed = [
		['MHz', 1000000],
		['GHz', 1000000000]
		]

	for item in cpuSpeed:
		parent.nt_cpu_units_cb.addItem(item[0], item[1])
	for item in cpuSpeed:
		parent.st_cpu_units_cb.addItem(item[0], item[1])




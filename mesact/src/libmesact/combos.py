

def build(parent):
	linearUnits = [
		['Select', False],
		['Inch', 'inch'],
		['Millimeter', 'mm']
		]

	for item in linearUnits:
		parent.linearUnitsCB.addItem(item[0], item[1])

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

	for i in range(6):
		for item in axes:
			getattr(parent, f'c0_axis_{i}').addItem(item[0], item[1])
			#getattr(parent, f'c1_axis_{i}').addItem(item[0], item[1])





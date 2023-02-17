from libmesact import firmware

def boardChanged(parent):
	db25 = [
	['Select', False],
	['7i76', '7i76'],
	['7i77', '7i77'],
	['7i78', '7i78'],
	]
	idc50 = [
	['Select', False],
	['7i33TA', '7i33ta'],
	['7i37TA', '7i37ta'],
	['7i47', '7i47'],
	['7i47S', '7i47s'],
	['7i49', '7i49'],
	]


	if parent.boardCB.currentData():
		board = parent.boardCB.currentData()
		name = parent.boardCB.currentText()
		# set all tabs visible then hide as needed
		# parent.c0_JointTW.show()
		for i in range(10):
			parent.c0_JointTW.setTabVisible(i, True)
		firmware.load(parent)
		tabs = parent.c0_JointTW.count()
		parent.daughterCB_0.clear()
		parent.daughterCB_1.clear()
		parent.daughterCB_2.clear()
		parent.daughterLB_0.clear()
		parent.daughterLB_1.clear()
		parent.daughterLB_2.clear()
		parent.ipAddressCB.setEnabled(False)
		parent.mainTW.setTabVisible(2, True)
		parent.mainTW.setTabText(2, name)

		if board == '5i24':
			parent.c0_JointTW.setTabText(0, name)
			for i in range(1, tabs + 1):
				parent.c0_JointTW.setTabVisible(i, False)
			parent.daughterLB_0.setText('P2')
			parent.daughterLB_1.setText('P3')
			parent.daughterLB_2.setText('P4')
			parent.mainTW.setTabText(3, 'P2')
			parent.mainTW.setTabText(4, 'P3')
			parent.mainTW.setTabText(5, 'P4')
			for item in idc50:
				parent.daughterCB_0.addItem(item[0], item[1])
				parent.daughterCB_1.addItem(item[0], item[1])
				parent.daughterCB_2.addItem(item[0], item[1])
		elif board == '5i25':
			parent.c0_JointTW.setTabText(0, name)
			for i in range(1, tabs + 1):
				parent.c0_JointTW.setTabVisible(i, False)
			parent.daughterLB_0.setText('P2')
			parent.daughterLB_1.setText('P3')
			parent.mainTW.setTabText(3, 'P2')
			parent.mainTW.setTabText(4, 'P3')
			for item in db25:
				parent.daughterCB_0.addItem(item[0], item[1])
				parent.daughterCB_1.addItem(item[0], item[1])
		elif board == '7i76e':
			parent.c0_JointTW.setTabText(0, name)
			parent.c0_JointTW.setTabVisible(5, False)
			parent.ipAddressCB.setEnabled(True)
			parent.daughterLB_0.setText('P1')
			parent.daughterLB_1.setText('P2')
			parent.mainTW.setTabText(3, 'P1')
			parent.mainTW.setTabText(4, 'P2')
			for item in db25:
				parent.daughterCB_0.addItem(item[0], item[1])
				parent.daughterCB_1.addItem(item[0], item[1])
		elif board == '7i80db16':
			parent.c0_JointTW.setTabText(0, name)
			for i in range(1, tabs + 1):
				parent.c0_JointTW.setTabVisible(i, False)
			parent.ipAddressCB.setEnabled(True)
			parent.daughterLB_0.setText('J2')
			parent.daughterLB_1.setText('J3')
			parent.daughterLB_2.setText('J4')
			parent.mainTW.setTabText(3, 'J2')
			parent.mainTW.setTabText(4, 'J3')
			parent.mainTW.setTabText(5, 'J4')
			for item in idc50:
				parent.daughterCB_0.addItem(item[0], item[1])
				parent.daughterCB_1.addItem(item[0], item[1])
				parent.daughterCB_2.addItem(item[0], item[1])
		elif board == '7i80db25':
			parent.c0_JointTW.setTabText(0, name)
			for i in range(1, tabs + 1):
				parent.c0_JointTW.setTabVisible(i, False)
			parent.ipAddressCB.setEnabled(True)
			parent.daughterLB_0.setText('J2')
			parent.daughterLB_1.setText('J3')
			parent.daughterLB_2.setText('J4')
			parent.mainTW.setTabText(3, 'J2')
			parent.mainTW.setTabText(4, 'J3')
			parent.mainTW.setTabText(5, 'J4')
			for item in idc50:
				parent.daughterCB_0.addItem(item[0], item[1])
				parent.daughterCB_1.addItem(item[0], item[1])
				parent.daughterCB_2.addItem(item[0], item[1])
		elif board == '7i80hd16':
			parent.c0_JointTW.setTabText(0, name)
			for i in range(1, tabs + 1):
				parent.c0_JointTW.setTabVisible(i, False)
			parent.ipAddressCB.setEnabled(True)
			parent.daughterLB_0.setText('P1')
			parent.daughterLB_1.setText('P2')
			parent.daughterLB_2.setText('P3')
			parent.mainTW.setTabText(3, 'P1')
			parent.mainTW.setTabText(4, 'P2')
			parent.mainTW.setTabText(5, 'P3')
			for item in idc50:
				parent.daughterCB_0.addItem(item[0], item[1])
				parent.daughterCB_1.addItem(item[0], item[1])
				parent.daughterCB_2.addItem(item[0], item[1])
		elif board == '7i80hd25':
			parent.c0_JointTW.setTabText(0, name)
			for i in range(1, tabs + 1):
				parent.c0_JointTW.setTabVisible(i, False)
			parent.ipAddressCB.setEnabled(True)
			parent.daughterLB_0.setText('P1')
			parent.daughterLB_1.setText('P2')
			parent.daughterLB_2.setText('P3')
			parent.mainTW.setTabText(3, 'P1')
			parent.mainTW.setTabText(4, 'P2')
			parent.mainTW.setTabText(5, 'P3')
			for item in idc50:
				parent.daughterCB_0.addItem(item[0], item[1])
				parent.daughterCB_1.addItem(item[0], item[1])
				parent.daughterCB_2.addItem(item[0], item[1])
		elif board == '7i80hdts':
			parent.c0_JointTW.setTabText(0, name)
			for i in range(1, tabs + 1):
				parent.c0_JointTW.setTabVisible(i, False)
			parent.ipAddressCB.setEnabled(True)
			parent.daughterLB_0.setText('P1')
			parent.daughterLB_1.setText('P2')
			parent.daughterLB_2.setText('P3')
			parent.mainTW.setTabText(3, 'P1')
			parent.mainTW.setTabText(4, 'P2')
			parent.mainTW.setTabText(5, 'P3')
			for item in idc50:
				parent.daughterCB_0.addItem(item[0], item[1])
				parent.daughterCB_1.addItem(item[0], item[1])
				parent.daughterCB_2.addItem(item[0], item[1])
		elif board == '7i92':
			parent.c0_JointTW.setTabText(0, name)
			for i in range(1, tabs + 1):
				parent.c0_JointTW.setTabVisible(i, False)
			parent.ipAddressCB.setEnabled(True)
			parent.daughterLB_0.setText('P1')
			parent.daughterLB_1.setText('P2')
			parent.mainTW.setTabText(3, 'P1')
			parent.mainTW.setTabText(4, 'P2')
			for item in db25:
				parent.daughterCB_0.addItem(item[0], item[1])
				parent.daughterCB_1.addItem(item[0], item[1])
		elif board == '7i92t':
			parent.c0_JointTW.setTabText(0, name)
			for i in range(1, tabs + 1):
				parent.c0_JointTW.setTabVisible(i, False)
			parent.ipAddressCB.setEnabled(True)
			parent.daughterLB_0.setText('P1')
			parent.daughterLB_1.setText('P2')
			parent.mainTW.setTabText(3, 'P1')
			parent.mainTW.setTabText(4, 'P2')
			for item in db25:
				parent.daughterCB_0.addItem(item[0], item[1])
				parent.daughterCB_1.addItem(item[0], item[1])
		elif board == '7i93':
			parent.c0_JointTW.setTabText(0, name)
			for i in range(1, tabs + 1):
				parent.c0_JointTW.setTabVisible(i, False)
			parent.ipAddressCB.setEnabled(True)
			parent.daughterLB_0.setText('P1')
			parent.daughterLB_1.setText('P2')
			parent.mainTW.setTabText(3, 'P1')
			parent.mainTW.setTabText(4, 'P2')
			for item in idc50:
				parent.daughterCB_0.addItem(item[0], item[1])
				parent.daughterCB_1.addItem(item[0], item[1])
		elif board == '7i95':
			parent.c0_JointTW.setTabText(0, name)
			parent.ipAddressCB.setEnabled(True)
			parent.daughterLB_0.setText('P1')
			parent.mainTW.setTabText(3, 'P1')
			for item in db25:
				parent.daughterCB_0.addItem(item[0], item[1])
		elif board == '7i96':
			parent.c0_JointTW.setTabText(0, name)
			parent.c0_JointTW.setTabVisible(6, False)
			parent.ipAddressCB.setEnabled(True)
			parent.daughterLB_0.setText('P1')
			parent.mainTW.setTabText(3, 'P1')
			for item in db25:
				parent.daughterCB_0.addItem(item[0], item[1])
		elif board == '7i96s':
			parent.c0_JointTW.setTabText(0, name)
			parent.c0_JointTW.setTabVisible(6, False)
			parent.ipAddressCB.setEnabled(True)
			parent.daughterLB_0.setText('P1')
			parent.mainTW.setTabText(3, 'P1')
			for item in db25:
				parent.daughterCB_0.addItem(item[0], item[1])
		elif board == '7i97':
			parent.c0_JointTW.setTabText(0, name)
			parent.ipAddressCB.setEnabled(True)
			parent.daughterLB_0.setText('P1')
			parent.mainTW.setTabText(3, 'P1')
			for item in db25:
				parent.daughterCB_0.addItem(item[0], item[1])
		elif board == '7i98':
			parent.c0_JointTW.setTabText(0, name)
			for i in range(1, tabs + 1):
				parent.c0_JointTW.setTabVisible(i, False)
			parent.ipAddressCB.setEnabled(True)
			parent.daughterLB_0.setText('P1')
			parent.daughterLB_1.setText('P2')
			parent.daughterLB_2.setText('P3')
			parent.mainTW.setTabText(3, 'P1')
			parent.mainTW.setTabText(4, 'P2')
			parent.mainTW.setTabText(5, 'P3')
			for item in db25:
				parent.daughterCB_0.addItem(item[0], item[1])
				parent.daughterCB_1.addItem(item[0], item[1])
				parent.daughterCB_2.addItem(item[0], item[1])

	else:
		parent.c0_JointTW.setTabText(0, 'Board')
		parent.mainTW.setTabVisible(2, False)
		parent.daughterCB_0.clear()
		parent.daughterCB_1.clear()
		parent.daughterCB_2.clear()


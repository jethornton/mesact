import os

from PyQt5.QtWidgets import QWidget

def boardChanged(parent):
	boardTab = parent.mainTW.indexOf(parent.mainTW.findChild(QWidget, 'boardTab'))
	if parent.boardCB.currentData():
		parent.mainTW.setTabText(boardTab, parent.boardCB.currentText())
		board = parent.boardCB.currentData()
		loadFirmware(parent)
		#print(f'Board {parent.boardCB.currentData()}')
		eth = ['7i76e', '7i80db16', '7i80db25', '7i80hd16', '7i80hd25', '7i92',
			'7i92t', '7i93', '7i95', '7i96', '7i96s', '7i97', '7i98']
		pci = ['5i25']
		if board in eth:
			parent.ipAddressCB.setEnabled(True)
		else:
			parent.ipAddressCB.setEnabled(False)
		func = {'5i24':board5i24, '5i25':board5i25, '7i76e':board7i76e,
		'7i80db16':board7i80db16, '7i80db25':board7i80db25,
		'7i80hd16':board7i80hd16,'7i80hd25':board7i80hd25, '7i92':board7i92,
		'7i92t':board7i92t ,'7i93':board7i93 ,'7i95':board7i95 ,'7i96':board7i96,
		'7i96s':board7i96s ,'7i97':board7i97 ,'7i98':board7i98}
		func[board](parent, board)


	else:
		clearFirmware(parent)
		parent.ipAddressCB.setEnabled(False)
		parent.mainTW.setTabText(boardTab, 'Board')

def loadFirmware(parent): # firmware combobox
	path = os.path.join(parent.firmware_path, parent.boardCB.currentData())
	files = sorted([entry.path for entry in os.scandir(path) if entry.is_file()])
	extensions = ['.bit', '.bin']
	if any(x.endswith(tuple(extensions)) for x in files): # firmware files present
		parent.firmwareCB.clear()
		parent.firmwareCB.addItem('Select', False)
		for file in files:
			if os.path.splitext(file)[1] in extensions:
				parent.firmwareCB.addItem(os.path.basename(file), file)
	parent.firmwareLB.setText('No Firmware Selected')

def clearFirmware(parent):
	parent.firmwareCB.clear()

def board5i24(parent, board):
	print(board)

def board5i25(parent, board):
	print(board)

def board7i76e(parent, board):
	print(board)

def board7i80db16(parent, board):
	print(board)

def board7i80db25(parent, board):
	print(board)

def board7i80hd16(parent, board):
	print(board)

def board7i80hd25(parent, board):
	print(board)

def board7i92(parent, board):
	print(board)

def board7i92t(parent, board):
	print(board)

def board7i93(parent, board):
	print(board)

def board7i95(parent, board):
	print(board)

def board7i96(parent, board):
	print(board)

def board7i96s(parent, board):
	print(board)

def board7i97(parent, board):
	print(board)

def board(parent, board):
	print(board)

def board7i98(parent, board):
	print(board)






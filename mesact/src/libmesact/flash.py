import subprocess
from subprocess import Popen, PIPE

from PyQt5.QtWidgets import QInputDialog, QLineEdit, QDialogButtonBox

ETH = ['7i76e', '7i80db-16', '7i80db-25', '7i80hd-16', '7i80hd-25', '7i92',
	'7i92t', '7i93', '7i95', '7i96', '7i96s', '7i97', '7i98']
PCI = ['5i24', '5i25']

def check_emc():
	if "0x48414c32" in subprocess.getoutput('ipcs'):
		return True
	else:
		return False

def check_ip(parent):
	if not parent.ipAddressCB.currentData():
		parent.errorMsgOk('An IP address must be selected', 'Error!')
		return False
	return True

def getPassword(parent):
	dialog = 'You need root privileges\nfor this operation.\nEnter your Password:'
	password, okPressed = QInputDialog.getText(parent, 'Password Required', dialog, QLineEdit.Password, "")
	if okPressed and password != '':
		return password

def getResults(parent, prompt, result, viewport, task=None):
	if result == 0:
		output = prompt[0]
		outcome = 'Success'
	else:
		output = prompt[1]
		outcome = 'Failed'
	getattr(parent, viewport).clear()
	getattr(parent, viewport).setPlainText(f'{task} returned: {outcome}\n')
	getattr(parent, viewport).appendPlainText(f'{output}\n')

def checkCard(parent):
	board = parent.boardCB.currentData()
	if not board:
		parent.errorMsgOk(f'A board must be selected', 'Error')
		return
	prompt = None
	if check_emc():
		parent.errorMsgOk(f'LinuxCNC must NOT be running\n to read the {parent.board}', 'Error')
		return

	if board in ETH:
		if check_ip(parent):
			ipAddress = parent.ipAddressCB.currentText()
			p = Popen(['mesaflash', '--device', board, '--addr', ipAddress],
				stdin=PIPE, stderr=PIPE, stdout=PIPE, universal_newlines=True)
			prompt = p.communicate()
		else:
			return

	elif board in PCI:
		if not parent.password:
			password = getPassword(parent)
			parent.password = password
		if parent.password != None:
			p = Popen(['sudo', '-S', 'mesaflash', '--device', board],
				stdin=PIPE, stderr=PIPE, stdout=PIPE, universal_newlines=True)
			prompt = p.communicate(parent.password + '\n')
	if prompt:
		getResults(parent, prompt, p.returncode, 'verifyPTE', 'Check IP')






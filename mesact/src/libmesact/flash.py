import subprocess
from subprocess import Popen, PIPE

from PyQt5.QtWidgets import QInputDialog, QLineEdit, QDialogButtonBox

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
	parent.firmwareTW.setCurrentIndex(1)

def checkCard(parent):
	board = parent.boardCB.currentData()
	if not board:
		parent.errorMsgOk(f'A board must be selected', 'Error')
		return
	prompt = None
	if check_emc():
		parent.errorMsgOk(f'LinuxCNC must NOT be running\n to read the {board}', 'Error')
		return

	if parent.boardType == 'eth':
		if check_ip(parent):
			ipAddress = parent.ipAddressCB.currentText()
			p = Popen(['mesaflash', '--device', board, '--addr', ipAddress],
				stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
			prompt = p.communicate()
		else:
			return

	elif parent.boardType == 'pci':
		if not parent.password:
			password = getPassword(parent)
			parent.password = password
		if parent.password != None:
			p = Popen(['sudo', '-S', 'mesaflash', '--device', board],
				stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
			prompt = p.communicate(parent.password + '\n')
	if prompt:
		getResults(parent, prompt, p.returncode, 'verifyPTE', 'Check IP')

def readhmid(parent):
	#  mesaflash --device 7i92t --addr 10.10.10.10 --readhmid --dbname1 7i76 --dbname2 7i85s > 7i92_7i76_7i85sd.txt
	prompt = None
	board = parent.boardCB.currentData()
	if check_emc():
		parent.errorMsgOk(f'LinuxCNC must NOT be running\n to read the {parent.board}', 'Error')
		return
	if parent.boardType == 'eth':
		if check_ip(parent):
			ipAddress = parent.ipAddressCB.currentText()
			cmd = ['mesaflash', '--device', board, '--addr', ipAddress, '--readhmid']
			if parent.hmid_terminals_1:
				cmd.append('--dbname1')
				cmd.append(parent.hmid_terminals_1.currentData())
			if parent.hmid_terminals_2:
				cmd.append('--dbname2')
				cmd.append(parent.hmid_terminals_2.currentData())
			p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
			prompt = p.communicate()
		else:
			return

	elif parent.boardType == 'pci':
		if not parent.password:
			password = getPassword(parent)
			parent.password = password
		if parent.password != None:
			p = Popen(['sudo', '-S', 'mesaflash', '--device', board, '--readhmid'],
				stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
			prompt = p.communicate(parent.password + '\n')

	if prompt:
		getResults(parent, prompt, p.returncode, 'firmwarePTE', 'Read HMID')

def readpd(parent):
	prompt = None
	board = parent.boardCB.currentData()
	if check_emc():
		parent.errorMsgOk(f'LinuxCNC must NOT be running\n to read the {parent.board}', 'Error')
		return
	if parent.boardType == 'eth':
		if check_ip(parent):
			ipAddress = parent.ipAddressCB.currentText()
			p = Popen(['mesaflash', '--device', parent.board, '--addr', ipAddress, '--print-pd'],
				stdin=PIPE, stderr=PIPE, stdout=PIPE, universal_newlines=True)
			prompt = p.communicate()
		else:
			return

	elif parent.boardType == 'pci':
		if not parent.password:
			password = getPassword(parent)
			parent.password = password
		if parent.password != None:
			p = Popen(['sudo', '-S', 'mesaflash', '--device', parent.board, '--print-pd'],
				stdin=PIPE, stderr=PIPE, stdout=PIPE, universal_newlines=True)
			prompt = p.communicate(parent.password + '\n')
	if prompt:
		getResults(parent, prompt, p.returncode, 'firmwarePTE', 'Read Pin Descriptions')





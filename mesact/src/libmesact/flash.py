import os, subprocess
from subprocess import Popen, PIPE

from PyQt5.QtWidgets import QApplication, QInputDialog, QLineEdit, qApp
from PyQt5.QtWidgets import QDialogButtonBox

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
	cmd = []
	prompt = None
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
			cmd = ['mesaflash', '--device', board, '--addr', ipAddress]
			#print(f'command: {cmd}')
			p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
			prompt = p.communicate()
		else:
			return

	elif parent.boardType == 'pci':
		if not parent.password:
			password = getPassword(parent)
			parent.password = password
		if parent.password != None:
			cmd = ['sudo', '-S', 'mesaflash', '--device', board]
			#print(f'command: {cmd}')
			p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
			prompt = p.communicate(parent.password + '\n')
	if prompt:
		getResults(parent, prompt, p.returncode, 'verifyPTE', 'Check IP')

def readhmid(parent):
	#  mesaflash --device 7i92t --addr 10.10.10.10 --readhmid --dbname1 7i76 --dbname2 7i85s > 7i92_7i76_7i85sd.txt
	board = parent.boardCB.currentData()
	cmd = []
	prompt = None
	if check_emc():
		parent.errorMsgOk(f'LinuxCNC must NOT be running\n to read the {parent.board}', 'Error')
		return
	if parent.boardType == 'eth':
		if check_ip(parent):
			ipAddress = parent.ipAddressCB.currentText()
			cmd = ['mesaflash', '--device', board, '--addr', ipAddress, '--readhmid']
			if parent.hmid_terminals_1.currentData():
				cmd.append('--dbname1')
				cmd.append(parent.hmid_terminals_1.currentData())
			if parent.hmid_terminals_2.currentData():
				cmd.append('--dbname2')
				cmd.append(parent.hmid_terminals_2.currentData())
			#print(f'command: {cmd}')
			p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
			prompt = p.communicate()
		else:
			return

	elif parent.boardType == 'pci':
		if not parent.password:
			password = getPassword(parent)
			parent.password = password
		if parent.password != None:
			cmd = ['sudo', '-S', 'mesaflash', '--device', board, '--readhmid']
			#print(f'command: {cmd}')
			p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
			prompt = p.communicate(parent.password + '\n')

	if prompt:
		getResults(parent, prompt, p.returncode, 'firmwarePTE', 'Read HMID')

def readpd(parent):
	board = parent.boardCB.currentData()
	cmd = []
	prompt = None
	if check_emc():
		parent.errorMsgOk(f'LinuxCNC must NOT be running\n to read the {parent.board}', 'Error')
		return
	if parent.boardType == 'eth':
		if check_ip(parent):
			ipAddress = parent.ipAddressCB.currentText()
			cmd = ['mesaflash', '--device', board, '--addr', ipAddress, '--print-pd']
			#print(f'command: {cmd}')
			p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
			prompt = p.communicate()
		else:
			return

	elif parent.boardType == 'pci':
		if not parent.password:
			password = getPassword(parent)
			parent.password = password
		if parent.password != None:
			cmd = ['sudo', '-S', 'mesaflash', '--device', parent.board, '--print-pd']
			#print(f'command: {cmd}')
			p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
			prompt = p.communicate(parent.password + '\n')
	if prompt:
		getResults(parent, prompt, p.returncode, 'firmwarePTE', 'Read Pin Descriptions')

def flashCard(parent):
	board = parent.boardCB.currentData()
	cmd = []
	prompt = None
	if check_emc():
		parent.errorMsgOk(f'LinuxCNC must NOT be running\n to flash the {parent.board}', 'Error')
		return
	if parent.firmwareCB.currentData():
		firmware = os.path.basename(parent.firmwareCB.currentData())
		parent.firmwarePTE.clear()
		parent.firmwarePTE.setPlainText(f'Flashing: {firmware} to {parent.board}')
		qApp.processEvents()
		firmware = os.path.join(parent.lib_path, parent.firmwareCB.currentData())
		if parent.boardType == 'eth':
			if check_ip(parent):
				ipAddress = parent.ipAddressCB.currentText()
				cmd = ['mesaflash', '--device', board, '--addr', ipAddress, '--write', firmware]
				#print(f'command: {cmd}')
				p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
				prompt = p.communicate()
			else:
				return

		elif parent.boardType == 'pci':
			if not parent.password:
				password = getPassword(parent)
				parent.password = password
			if parent.password != None:
				cmd = ['sudo', '-S', 'mesaflash', '--device', parent.board, '--write', firmware]
				#print(f'command: {cmd}')
				p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
				prompt = p.communicate(parent.password + '\n')

		if prompt:
			getResults(parent, prompt, p.returncode, 'firmwarePTE', 'Flash')

	else:
		parent.errorMsgOk('A firmware must be selected', 'Error!')
		return

def reloadCard(parent):
	board = parent.boardCB.currentData()
	cmd = []
	prompt = None
	if check_emc():
		parent.errorMsgOk(f'LinuxCNC must NOT be running\n to reload the {board}', 'Error')
		return
	if parent.boardType == 'eth':
		if check_ip(parent):
			ipAddress = parent.ipAddressCB.currentText()
			cmd = ['mesaflash', '--device', board, '--addr', ipAddress, '--reload']
			#print(f'command: {cmd}')
			p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
			prompt = p.communicate()
		else:
			return

	elif parent.boardType == 'pci':
		if not parent.password:
			password = getPassword(parent)
			parent.password = password
		if parent.password != None:
			cmd = ['sudo', '-S', 'mesaflash', '--device', parent.board, '--reload']
			#print(f'command: {cmd}')
			p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
			prompt = p.communicate(parent.password + '\n')

	if prompt:
		getResults(parent, prompt, p.returncode, 'firmwarePTE', 'Reload Firmware')
		parent.firmwarePTE.appendPlainText('Wait 30 seconds before Verifying the Firmware')

def verifyFirmware(parent):
	board = parent.boardCB.currentData()
	cmd = []
	prompt = None
	if check_emc():
		parent.errorMsgOk(f'LinuxCNC must NOT be running\n to verify the {board}', 'Error')
		return
	if parent.firmwareCB.currentData():
		firmware = os.path.join(parent.lib_path, parent.firmwareCB.currentData())
		if parent.boardType == 'eth':
			if check_ip(parent):
				ipAddress = parent.ipAddressCB.currentText()
				cmd = ['mesaflash', '--device', board, '--addr', ipAddress, '--verify', firmware]
				#print(f'command: {cmd}')
				p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
				prompt = p.communicate()
			else:
				return

		elif parent.boardType == 'pci':
			if not parent.password:
				password = getPassword(parent)
				parent.password = password
			if parent.password != None:
				cmd = ['sudo', '-S', 'mesaflash', '--device', board, '--verify', firmware]
				#print(f'command: {cmd}')
				p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
				prompt = p.communicate(parent.password + '\n')

		if prompt:
			getResults(parent, prompt, p.returncode, 'firmwarePTE', 'Verify Firmware')
	else:
		parent.errorMsgOk('A firmware must be selected', 'Error!')
		return

def copyOutput(parent):
	qclip = QApplication.clipboard()
	qclip.setText(parent.firmwarePTE.toPlainText())
	parent.statusbar.showMessage('Output copied to clipboard')



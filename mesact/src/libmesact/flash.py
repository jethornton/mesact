import os, subprocess
from subprocess import Popen, PIPE

from PyQt5.QtWidgets import QApplication, QInputDialog, QLineEdit, qApp
from PyQt5.QtWidgets import QDialogButtonBox

from libmesact import dialogs

def check_emc():
	if "0x48414c32" in subprocess.getoutput('ipcs'):
		return True
	else:
		return False

def firmware_changed(parent):
	if parent.firmwareCB.currentData():
		parent.flashPB.setEnabled(True)
	else:
		parent.flashPB.setEnabled(False)

def check_ip(parent):
	if not parent.ipAddressCB.currentData():
		dialogs.errorMsgOk('An IP address must be selected', 'Error!')
		parent.mainTW.setCurrentIndex(0)
		parent.ipAddressCB.setFocus()
		return False
	return True

def getPassword(parent):
	dialog = 'You need root privileges\nfor this operation.\nEnter your Password:'
	password, okPressed = QInputDialog.getText(parent, 'Password Required', dialog, QLineEdit.Password, "")
	if okPressed and password != '':
		return password

def getResults(parent, prompt, result, viewport, task=None):
	output = prompt[0].lstrip()
	if result == 0:
		outcome = 'Success'
	else:
		outcome = 'Failed'
	getattr(parent, viewport).clear()
	getattr(parent, viewport).appendPlainText(f'{task}')
	getattr(parent, viewport).appendPlainText(f'Returned: {outcome}')
	getattr(parent, viewport).appendPlainText(f'{output}\n')

def find_ip_board(parent):
	addresses = ['10.10.10.10', '192.168.1.121']
	for address in addresses:
		cmd = ['ping', '-c', '1', address]
		output = subprocess.run(cmd, capture_output=True, text=True)
		if output.returncode == 0:
			cmd = ['mesaflash', '--device', 'ether', '--addr', address]
			output = subprocess.run(cmd, capture_output=True, text=True)
			if output.returncode == 0:
				parent.verifyPTE.clear()
				msg = (f'Find IP Board Results:{output.stdout}')
				parent.verifyPTE.setPlainText(msg)
				return

	# print(f'Return Code: {output.returncode}')
	# print(f'Std Output: {output.stdout}')
	# print(f'Std Error: {output.stderr}')

def verify_ip_board(parent): # make me toss up the error message and return False
	if check_ip(parent):
		address = parent.ipAddressCB.currentText()
		if os.system(f'ping -c 1 {address}') != 0:
			msg = (f'No Board found at {address}')
			dialogs.errorMsgOk(msg, 'Error')
			return
		cmd = ['mesaflash', '--device', 'ether', '--addr', address]
		p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
		prompt = p.communicate()
		selected_board = parent.boardCB.currentText().upper()
		if prompt[0].split()[0] == 'ETH':
			connected_board = prompt[0].split()[2]
		else:
			msg = (f'Device found at {address}\nis not a Mesa Board')
			dialogs.errorMsgOk(msg, 'Error')
			return
		if selected_board == connected_board:
			return True
		else:
			msg = (f'The selected {selected_board} board\n'
			f'does not match the\nconnected {connected_board} board')
			dialogs.errorMsgOk(msg, 'Error')
			return False

def connected_ip_board(parent):
	address = parent.ipAddressCB.currentText()
	cmd = ['mesaflash', '--device', 'ether', '--addr', address]
	p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
	prompt = p.communicate()
	board = parent.boardCB.currentText().upper()
	print(prompt[0].split()[2])


def checkCard(parent):
	board = parent.boardCB.currentData()
	cmd = []
	prompt = None
	if not board:
		dialogs.errorMsgOk('A board must be selected', 'Error')
		return
	prompt = None
	if check_emc():
		dialogs.errorMsgOk(f'LinuxCNC must NOT be running\n to read the {board}', 'Error')
		return

	if parent.boardType == 'eth':
		if verify_ip_board(parent):
			ipAddress = parent.ipAddressCB.currentText()
			cmd = ['mesaflash', '--device', board, '--addr', ipAddress]
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
			p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
			prompt = p.communicate(parent.password + '\n')
	if prompt:
		getResults(parent, prompt, p.returncode, 'verifyPTE', 'Verify Board')

def readhmid(parent):
	board = parent.boardCB.currentData()
	cmd = []
	prompt = None
	if check_emc():
		dialogs.errorMsgOk(f'LinuxCNC must NOT be running\n to read the {parent.board}', 'Error')
		return
	if parent.boardType == 'eth':
		if verify_ip_board(parent):
			ipAddress = parent.ipAddressCB.currentText()
			cmd = ['mesaflash', '--device', board, '--addr', ipAddress, '--readhmid']
			if parent.hmid_terminals_1.currentData():
				cmd.append('--dbname1')
				cmd.append(parent.hmid_terminals_1.currentData())
			if parent.hmid_terminals_2.currentData():
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
			cmd = ['sudo', '-S', 'mesaflash', '--device', board, '--readhmid']
			p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
			prompt = p.communicate(parent.password + '\n')

	if prompt:
		parent.firmwareTW.setCurrentIndex(1)
		parent.firmwarePTE.clear()
		parent.firmwarePTE.setPlainText('Reading HMID')
		getResults(parent, prompt, p.returncode, 'firmwarePTE', 'Read HMID')

def readpd(parent):
	parent.firmwareTW.setCurrentIndex(1)
	parent.firmwarePTE.clear()
	parent.firmwarePTE.setPlainText('Reading PD')
	board = parent.boardCB.currentData()
	cmd = []
	prompt = None
	if check_emc():
		dialogs.errorMsgOk(f'LinuxCNC must NOT be running\n to read the {parent.board}', 'Error')
		return
	if parent.boardType == 'eth':
		if verify_ip_board(parent):
			ipAddress = parent.ipAddressCB.currentText()
			cmd = ['mesaflash', '--device', board, '--addr', ipAddress, '--print-pd']
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
			p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
			prompt = p.communicate(parent.password + '\n')
	if prompt:
		getResults(parent, prompt, p.returncode, 'firmwarePTE', 'Read Pin Descriptions')

def flashCard(parent):
	board = parent.boardCB.currentData()
	cmd = []
	prompt = None
	if check_emc():
		dialogs.errorMsgOk(f'LinuxCNC must NOT be running\n to flash the {parent.board}', 'Error')
		return
	if parent.firmwareCB.currentData():
		firmware = os.path.basename(parent.firmwareCB.currentData())
		firmware = os.path.join(parent.lib_path, parent.firmwareCB.currentData())
		if parent.boardType == 'eth':
			if verify_ip_board(parent):
				parent.firmware_info_pte.clear()
				parent.firmware_info_pte.setPlainText(f'Flashing: {parent.firmwareCB.currentText()} to {board}')
				qApp.processEvents()
				ipAddress = parent.ipAddressCB.currentText()
				cmd = ['mesaflash', '--device', board, '--addr', ipAddress, '--write', firmware]
				p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
				prompt = p.communicate()
			else:
				return

		elif parent.boardType == 'pci':
			if not parent.password:
				password = getPassword(parent)
				parent.password = password
			if parent.password != None:
				parent.firmware_info_pte.clear()
				parent.firmware_info_pte.setPlainText(f'Flashing: {parent.firmwareCB.currentText()} to {board}')
				qApp.processEvents()
				cmd = ['sudo', '-S', 'mesaflash', '--device', parent.board, '--write', firmware]
				p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
				prompt = p.communicate(parent.password + '\n')

		if prompt:
			getResults(parent, prompt, p.returncode, 'results_pte', 'Flash')
			parent.firmwareTW.setCurrentIndex(2)

	else:
		dialogs.errorMsgOk('A firmware must be selected', 'Error!')
		return

def reloadCard(parent):
	board = parent.boardCB.currentData()
	cmd = []
	prompt = None
	if check_emc():
		dialogs.errorMsgOk(f'LinuxCNC must NOT be running\n to reload the {board}', 'Error')
		return
	if parent.boardType == 'eth':
		if verify_ip_board(parent):
			parent.firmware_info_pte.clear()
			parent.firmware_info_pte.setPlainText('Reloading')
			qApp.processEvents()
			ipAddress = parent.ipAddressCB.currentText()
			cmd = ['mesaflash', '--device', board, '--addr', ipAddress, '--reload']
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
			p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
			prompt = p.communicate(parent.password + '\n')

	if prompt:
		getResults(parent, prompt, p.returncode, 'firmware_info_pte', 'Reload Firmware')
		parent.firmware_info_pte.appendPlainText('Wait 30 seconds before Verifying')

def verifyFirmware(parent):
	parent.firmware_info_pte.clear()
	board = parent.boardCB.currentData()
	cmd = []
	prompt = None
	if check_emc():
		dialogs.errorMsgOk(f'LinuxCNC must NOT be running\n to verify the {board}', 'Error')
		return
	if parent.firmwareCB.currentData():
		firmware = os.path.join(parent.lib_path, parent.firmwareCB.currentData())
		if parent.boardType == 'eth':
			if verify_ip_board(parent):
				parent.firmware_info_pte.setPlainText(f'Verifying {parent.firmwareCB.currentText()} on {board}')
				qApp.processEvents()
				ipAddress = parent.ipAddressCB.currentText()
				cmd = ['mesaflash', '--device', board, '--addr', ipAddress, '--verify', firmware]
				p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
				prompt = p.communicate()
			else:
				return

		elif parent.boardType == 'pci':
			if not parent.password:
				password = getPassword(parent)
				parent.password = password
			if parent.password != None:
				parent.firmware_info_pte.setPlainText(f'Verifying {parent.firmwareCB.currentText()} on {board}')
				qApp.processEvents()
				cmd = ['sudo', '-S', 'mesaflash', '--device', board, '--verify', firmware]
				p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
				prompt = p.communicate(parent.password + '\n')

		if prompt:
			getResults(parent, prompt, p.returncode, 'results_pte', 'Verify Firmware')
			parent.firmwareTW.setCurrentIndex(2)
	else:
		dialogs.errorMsgOk('A firmware must be selected', 'Error!')
		return

def copyOutput(parent):
	qclip = QApplication.clipboard()
	qclip.setText(parent.firmwarePTE.toPlainText())
	parent.statusbar.showMessage('Output copied to clipboard')



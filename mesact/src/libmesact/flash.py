import os, subprocess
from subprocess import Popen, PIPE

from PyQt5.QtWidgets import QApplication, QInputDialog, QLineEdit, qApp
from PyQt5.QtWidgets import QDialogButtonBox

from libmesact import dialogs
from libmesact import utilities

'''
subprocess.check_output Run command with arguments and return its output

subprocess.run Run the command described by args. Wait for command to complete,
then return a CompletedProcess instance.

class subprocess.CompletedProcess
	The return value from run(), representing a process that has finished.
	args
		The arguments used to launch the process. This may be a list or a string.
	returncode
		Exit status of the child process. Typically, an exit status of 0 indicates that it ran successfully.
		A negative value -N indicates that the child was terminated by signal N (POSIX only).
	stdout
		Captured stdout from the child process. A bytes sequence, or a string if run() was called with an encoding, errors, or text=True. None if stdout was not captured.
		If you ran the process with stderr=subprocess.STDOUT, stdout and stderr will be combined in this attribute, and stderr will be None.
	stderr
		Captured stderr from the child process. A bytes sequence, or a string if run() was called with an encoding, errors, or text=True. None if stderr was not captured.
	check_returncode()
		If returncode is non-zero, raise a CalledProcessError.

50 pin firmware
<pcw-home> sv=servo st=stepper rm=resolvermod im=index-mask ss=smart-serial
ssi=ssi biss-biss fa=fanux-abs pkt=packet-uart sdi=step/dir-index
pl=plasma = encoder-input has 3 'A' inputs 
'''

def firmware_changed(parent):
	if parent.firmwareCB.currentData():
		parent.flashPB.setEnabled(True)
	else:
		parent.flashPB.setEnabled(False)

def check_ip(parent):
	if not parent.address_cb.currentData():
		dialogs.errorMsgOk('An IP address must be selected', 'Error!')
		parent.mainTW.setCurrentIndex(0)
		parent.address_cb.setFocus()
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
	if utilities.check_emc():
		dialogs.errorMsgOk(f'LinuxCNC must NOT be running\n to search for a board', 'Error')
		return
	addresses = ['10.10.10.10', '192.168.1.121']
	parent.verifyPTE.setPlainText('Looking for IP boards')
	qApp.processEvents()
	for address in addresses:
		parent.verifyPTE.appendPlainText(f'Checking {address}')
		qApp.processEvents()
		cmd = ['ping', '-c', '1', address]
		output = subprocess.run(cmd, capture_output=True, text=True)
		if output.returncode == 0:
			cmd = ['mesaflash', '--device', 'ether', '--addr', address]
			output = subprocess.run(cmd, capture_output=True, text=True)
			parent.verifyPTE.clear()
			msg = (f'Find IP Board Results:{output.stdout}')
			parent.verifyPTE.setPlainText(msg)
			break
		elif output.returncode != 0:
			parent.verifyPTE.appendPlainText(f'No Board found at {address}')

def verify_ip_board(parent): # make me toss up the error message and return False
	board_name = parent.boardCB.currentText()
	if utilities.check_emc():
		dialogs.errorMsgOk(f'LinuxCNC must NOT be running\n to read the {board_name}', 'Error')
		return
	if check_ip(parent):
		address = parent.address_cb.currentText()
		cmd = ['ping', '-c', '1', address]
		output = subprocess.run(cmd, capture_output=True, text=True)
		if output.returncode != 0:
			msg = (f'No Board found at {address}')
			dialogs.errorMsgOk(msg, 'Error')
			return
		cmd = ['mesaflash', '--device', 'ether', '--addr', address]
		output = subprocess.run(cmd, capture_output=True, text=True)
		selected_board = parent.boardCB.currentText().upper()
		if output.stdout.split()[0] == 'ETH':
			connected_board = output.stdout.split()[2]
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

def verify_board(parent): # needs to use Popen for password
	board_name = parent.boardCB.currentText()
	cmd = []
	prompt = None
	if not board_name:
		dialogs.errorMsgOk('A board must be selected', 'Error')
		return
	prompt = None
	if utilities.check_emc():
		dialogs.errorMsgOk(f'LinuxCNC must NOT be running\n to read the {board_name}', 'Error')
		return

	if parent.boardType == 'eth':
		if verify_ip_board(parent):
			ipAddress = parent.address_cb.currentText()
			cmd = ['mesaflash', '--device', parent.mesaflash_name, '--addr', ipAddress]
			p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
			prompt = p.communicate()
		else:
			return

	elif parent.boardType == 'spi':
		msg = ('The Verify Board Function\n'
		'has not been programed yet for SPI\n'
		'JT might need your help\n'
		'getting this done')
		dialogs.msg_ok(msg, 'title')

	elif parent.boardType == 'pci':
		if not parent.password:
			password = getPassword(parent)
			parent.password = password
		if parent.password != None:
			cmd = ['sudo', '-S', 'mesaflash', '--device', parent.mesaflash_name]
			p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
			prompt = p.communicate(parent.password + '\n')
	if prompt:
		getResults(parent, prompt, p.returncode, 'verifyPTE', 'Verify Board')

def read_hmid(parent):
	board_name = parent.boardCB.currentText()
	cmd = []
	prompt = None
	if utilities.check_emc():
		dialogs.errorMsgOk(f'LinuxCNC must NOT be running\n to read the {board_name}', 'Error')
		return
	if parent.boardType == 'eth':
		if verify_ip_board(parent):
			ipAddress = parent.address_cb.currentText()
			cmd = ['mesaflash', '--device', parent.mesaflash_name, '--addr', ipAddress, '--readhmid']
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

	elif parent.boardType == 'spi':
		# sudo mesaflash --device 7i81 --spi --addr /dev/spidev0.0 --readhmid
		if not parent.password:
			password = getPassword(parent)
			parent.password = password
		if parent.password != None:
			spi_address = parent.address_cb.currentText()
			cmd = ['sudo', '-S', 'mesaflash', '--device', parent.mesaflash_name, '--spi', '--addr', spi_address, '--readhmid']
			p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
			prompt = p.communicate(parent.password + '\n')

	elif parent.boardType == 'pci':
		if not parent.password:
			password = getPassword(parent)
			parent.password = password
		if parent.password != None:
			cmd = ['sudo', '-S', 'mesaflash', '--device', parent.mesaflash_name, '--readhmid']
			p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
			prompt = p.communicate(parent.password + '\n')

	if prompt:
		parent.firmwareTW.setCurrentIndex(1)
		parent.firmwarePTE.clear()
		parent.firmwarePTE.setPlainText('Reading HMID')
		getResults(parent, prompt, p.returncode, 'firmwarePTE', 'Read HMID')
		parent.create_pin_pb.setEnabled(True)

def read_pd(parent):
	parent.firmwareTW.setCurrentIndex(1)
	parent.firmwarePTE.clear()
	parent.firmwarePTE.setPlainText('Reading PD')
	board_name = parent.boardCB.currentText()
	cmd = []
	prompt = None
	if utilities.check_emc():
		dialogs.errorMsgOk(f'LinuxCNC must NOT be running\n to read the {board_name}', 'Error')
		return
	if parent.boardType == 'eth':
		if verify_ip_board(parent):
			ipAddress = parent.address_cb.currentText()
			cmd = ['mesaflash', '--device', parent.mesaflash_name, '--addr', ipAddress, '--print-pd']
			p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
			prompt = p.communicate()
		else:
			return

	elif parent.boardType == 'spi':
		# sudo mesaflash --device 7i81 --spi --addr /dev/spidev0.0 --print-pd
		if not parent.password:
			password = getPassword(parent)
			parent.password = password
		if parent.password != None:
			spi_address = parent.address_cb.currentText()
			cmd = ['sudo', '-S', 'mesaflash', '--device', parent.mesaflash_name, '--spi', '--addr', spi_address, '--print-pd']
			p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
			prompt = p.communicate(parent.password + '\n')

	elif parent.boardType == 'pci':
		if not parent.password:
			password = getPassword(parent)
			parent.password = password
		if parent.password != None:
			cmd = ['sudo', '-S', 'mesaflash', '--device', parent.mesaflash_name, '--print-pd']
			p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
			prompt = p.communicate(parent.password + '\n')

	if prompt:
		getResults(parent, prompt, p.returncode, 'firmwarePTE', 'Read Pin Descriptions')

def flash_board(parent):
	board_name = parent.boardCB.currentText()
	cmd = []
	prompt = None
	if utilities.check_emc():
		dialogs.errorMsgOk(f'LinuxCNC must NOT be running\n to flash the {board_name}', 'Error')
		return
	if parent.firmwareCB.currentData():
		#firmware = os.path.basename(parent.firmwareCB.currentData())
		firmware = os.path.join(parent.lib_path, parent.firmwareCB.currentData())
		if parent.boardType == 'eth':
			if verify_ip_board(parent):
				parent.firmware_info_pte.clear()
				parent.firmware_info_pte.setPlainText(f'Flashing: {parent.firmwareCB.currentText()} to {board_name}')
				qApp.processEvents()
				ipAddress = parent.address_cb.currentText()
				cmd = ['mesaflash', '--device', parent.mesaflash_name, '--addr', ipAddress, '--write', firmware]
				p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
				prompt = p.communicate()
			else:
				return

		elif parent.boardType == 'spi':
			if not parent.password:
				password = getPassword(parent)
				parent.password = password
			if parent.password != None:
				spi_address = parent.address_cb.currentText()
				cmd = ['sudo', '-S', 'mesaflash', '--device', parent.mesaflash_name, '--spi', '--addr', spi_address, '--write', firmware]
				p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
				prompt = p.communicate(parent.password + '\n')

		elif parent.boardType == 'pci':
			if not parent.password:
				password = getPassword(parent)
				parent.password = password
			if parent.password != None:
				parent.firmware_info_pte.clear()
				parent.firmware_info_pte.setPlainText(f'Flashing: {parent.firmwareCB.currentText()} to {board_name}')
				qApp.processEvents()
				cmd = ['sudo', '-S', 'mesaflash', '--device', parent.mesaflash_name, '--write', firmware]
				p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
				prompt = p.communicate(parent.password + '\n')

		if prompt:
			getResults(parent, prompt, p.returncode, 'results_pte', 'Flash')
			parent.firmwareTW.setCurrentIndex(2)
			parent.flashed = True

	else:
		dialogs.errorMsgOk('A firmware must be selected', 'Error!')
		return

def reload_board(parent):
	board_name = parent.boardCB.currentText()
	cmd = []
	prompt = None
	if utilities.check_emc():
		dialogs.errorMsgOk(f'LinuxCNC must NOT be running\n to reload the {board_name}', 'Error')
		return
	if parent.boardType == 'eth':
		if verify_ip_board(parent):
			parent.firmware_info_pte.clear()
			parent.firmware_info_pte.setPlainText('Reloading')
			qApp.processEvents()
			ipAddress = parent.address_cb.currentText()
			cmd = ['mesaflash', '--device', parent.mesaflash_name, '--addr', ipAddress, '--reload']
			p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
			prompt = p.communicate()
		else:
			return

	elif parent.boardType == 'spi':
		if not parent.password:
			password = getPassword(parent)
			parent.password = password
		if parent.password != None:
			spi_address = parent.address_cb.currentText()
			cmd = ['sudo', '-S', 'mesaflash', '--device', parent.mesaflash_name, '--spi', '--addr', spi_address, '--reload']
			p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
			prompt = p.communicate(parent.password + '\n')

	elif parent.boardType == 'pci':
		if not parent.password:
			password = getPassword(parent)
			parent.password = password
		if parent.password != None:
			cmd = ['sudo', '-S', 'mesaflash', '--device', parent.mesaflash_name, '--reload']
			p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
			prompt = p.communicate(parent.password + '\n')

	if prompt:
		getResults(parent, prompt, p.returncode, 'firmware_info_pte', 'Reload Firmware')
		parent.firmware_info_pte.appendPlainText('Wait 30 seconds before Verifying')
		parent.flashed = False

def verify_firmware(parent):
	parent.firmware_info_pte.clear()
	board_name = parent.boardCB.currentText()
	cmd = []
	prompt = None
	if utilities.check_emc():
		dialogs.errorMsgOk(f'LinuxCNC must NOT be running\n to verify the {board_name}', 'Error')
		return
	if parent.firmwareCB.currentData():
		if parent.flashed:
			msg = (f'The {board_name} needs to be reloaded\n'
				'before verifying the firmware.\n')
			dialogs.dialogs.msg_ok(msg, 'Error')
			return
		firmware = os.path.join(parent.lib_path, parent.firmwareCB.currentData())
		if parent.boardType == 'eth':
			if verify_ip_board(parent):
				parent.firmware_info_pte.setPlainText(f'Verifying {parent.firmwareCB.currentText()} on {board_name}')
				qApp.processEvents()
				ipAddress = parent.address_cb.currentText()
				cmd = ['mesaflash', '--device', parent.mesaflash_name, '--addr', ipAddress, '--verify', firmware]
				p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
				prompt = p.communicate()
			else:
				return

		elif parent.boardType == 'spi':
			if not parent.password:
				password = getPassword(parent)
				parent.password = password
			if parent.password != None:
				spi_address = parent.address_cb.currentText()
				cmd = ['sudo', '-S', 'mesaflash', '--device', parent.mesaflash_name, '--spi', '--addr', spi_address, '--verify']
				p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
				prompt = p.communicate(parent.password + '\n')

		elif parent.boardType == 'pci':
			if not parent.password:
				password = getPassword(parent)
				parent.password = password
			if parent.password != None:
				parent.firmware_info_pte.setPlainText(f'Verifying {parent.firmwareCB.currentText()} on {board_name}')
				qApp.processEvents()
				cmd = ['sudo', '-S', 'mesaflash', '--device', parent.mesaflash_name, '--verify', firmware]
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



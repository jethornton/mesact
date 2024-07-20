import os, subprocess
import urllib.request
from datetime import datetime

from PyQt5.QtWidgets import QApplication, QInputDialog, QLineEdit, QComboBox
from PyQt5.QtWidgets import QDoubleSpinBox, QCheckBox

from libmesact import dialogs

def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False

def is_int(n):
	try:
		int(n)
		return True
	except ValueError:
		return False

def check_emc():
	cp = subprocess.run(['pgrep', '-l', 'linuxcnc'], text=True, capture_output=True)
	if 'linuxcnc' in cp.stdout:
		return True
	else:
		return False

def download(parent, down_url, save_loc):
	def Handle_Progress(blocknum, blocksize, totalsize):
		## calculate the progress
		readed_data = blocknum * blocksize
		if totalsize > 0:
			download_percentage = readed_data * 100 / totalsize
			parent.progressBar.setValue(int(download_percentage))
			QApplication.processEvents()
	urllib.request.urlretrieve(down_url, save_loc, Handle_Progress)
	parent.progressBar.setValue(100)
	parent.timer.start(1000)

def getPassword(parent):
	dialog = 'You need root privileges\nfor this operation.\nEnter your Password:'
	password, okPressed = QInputDialog.getText(parent, 'Password Required', dialog, QLineEdit.Password, "")
	if okPressed and password != '':
		return password

def unitsChanged(parent):
	if not parent.linearUnitsCB.currentData():
		for i in range(3):
			getattr(parent, f'unitsLB_{i}').setText('Select Units\nSettings Tab')
		parent.units_second = 'N/A'
		parent.units_second2 = 'N/A'
		parent.units_minute = 'N/A'
	if parent.linearUnitsCB.currentData() == 'mm':
		parent.units_second = 'mm/s'
		parent.units_second2 = 'mm/s^2'
		parent.units_minute = 'mm/m'
	elif parent.linearUnitsCB.currentData() == 'inch':
		parent.units_second = 'in/s'
		parent.units_second2 = 'i/s^2'
		parent.units_minute = 'in/m'

	for i in range(3): # cards
		for j in range(6): # drives
			getattr(parent, f'c{i}_max_vel_suffix_{j}').setText(parent.units_second)
			getattr(parent, f'c{i}_max_vel_min_suffix_{j}').setText(parent.units_minute)

	# c0_max_vel_suffix_0
	parent.c0_max_vel_min_suffix_0.setText(parent.units_minute)
	for i in range(6):
		for j in range(3): # <-- change when more cards are added
			getattr(parent, f'c{j}_max_vel_{i}').setPlaceholderText(parent.units_second)
			getattr(parent, f'c{j}_max_accel_{i}').setPlaceholderText(parent.units_second2)
	for i in range(3):
		getattr(parent, f'unitsLB_{i}').setText(f'Vel & Acc\n{parent.units_second}')
	parent.max_lin_vel_lb.setText(f'{parent.units_second}')
	#parent.trajMaxLinVelDSB.setSuffix(f' {parent.units_second}')
	parent.min_lin_jog_lb.setText(f'{parent.units_second}')
	parent.default_lin_jog_lb.setText(f'{parent.units_second}')
	parent.max_lin_jog_lb.setText(f'{parent.units_second}')
	#parent.minLinJogVelDSB.setSuffix(f' {parent.units_second}')
	#parent.defLinJogVelDSB.setSuffix(f' {parent.units_second}')
	#parent.maxLinJogVelDSB.setSuffix(f' {parent.units_second}')
	parent.minLinearVelLB.setText(f'{parent.minLinJogVelDSB.value() * 60:.1f} {parent.units_minute}')
	parent.defLinearVelLB.setText(f'{parent.defLinJogVelDSB.value() * 60:.1f} {parent.units_minute}')
	parent.maxLinearVelLB.setText(f'{parent.maxLinJogVelDSB.value() * 60:.1f} {parent.units_minute}')
	if set('ABC')&set(parent.coordinatesLB.text()): # angular axis
		parent.minAngularVelLB.setText(f'{parent.minAngJogVelDSB.value() * 60:.1f} deg/min')
		parent.defAngularVelLB.setText(f'{parent.defAngJogVelDSB.value() * 60:.1f} deg/min')
		parent.maxAngularVelLB.setText(f'{parent.maxAngJogVelDSB.value() * 60:.1f} deg/min')

	maxVelChanged(parent)

def maxVelChanged(parent):
	if parent.trajMaxLinVelDSB.value() > 0:
		val = parent.trajMaxLinVelDSB.value()
		if parent.linearUnitsCB.currentData() == 'mm':
			parent.mlvPerMinLB.setText(F'{val * 60:.1f} mm/min')
		if parent.linearUnitsCB.currentData() == 'inch':
			parent.mlvPerMinLB.setText(F'{val * 60:.1f} in/min')
	else:
		parent.mlvPerMinLB.setText('')

def backupFiles(parent, configPath=None):
	if not configPath:
		configPath = parent.configPath
	if not os.path.exists(configPath):
		parent.info_pte.setPlainText('Nothing to Back Up')
		return
	backupDir = os.path.join(configPath, 'backups')
	if not os.path.exists(backupDir):
		os.mkdir(backupDir)
	p1 = subprocess.Popen(['find',configPath,'-maxdepth','1','-type','f','-print'], stdout=subprocess.PIPE)
	backupFile = os.path.join(backupDir, f'{datetime.now():%m-%d-%y-%H-%M-%S}')
	p2 = subprocess.Popen(['zip','-j',backupFile,'-@'], stdin=p1.stdout, stdout=subprocess.PIPE)
	p1.stdout.close()
	parent.info_pte.appendPlainText('Backing up Confguration')
	output = p2.communicate()[0]
	parent.info_pte.appendPlainText(output.decode())

def cleanDir(parent, configPath):
	with os.scandir(configPath) as i:
		for entry in i:
			if entry.is_file():
				os.remove(os.path.join(configPath, entry.name)) 

def file_delete(parent, file_path):
	if os.path.isfile(file_path):
		os.remove(file_path)

def axisDisplayChanged(parent, radioButton):
	for button in parent.axisButtonGroup.buttons():
		if button is not radioButton:
			button.setChecked(False)

def copyValues(parent):
	entries = ['_scale_',
	'_min_limit_',
	'_max_limit_',
	'_max_vel_',
	'_max_accel_',
	'_p_',
	'_i_',
	'_d_',
	'_ff0_',
	'_ff0_',
	'_ff1_',
	'_ff2_',
	'_deadband_',
	'_bias_',
	'_maxOutput_',
	'_maxError_',
	'_min_ferror_',
	'_max_ferror_',
	'_home_',
	'_homeOffset_',
	'_homeSearchVel_',
	'_homeLatchVel_',
	'_homeFinalVelocity_'
	]

	button = parent.sender().objectName()
	card = button[:2]
	joint = button[-1]
	next_joint = int(joint) + 1
	next_tab = int(joint) + 2
	for item in entries:
		getattr(parent, f'{card}{item}{int(joint) + 1}').setText(getattr(parent, f'{card}{item}{joint}').text())

	step_driver = getattr(parent, f'{card}_drive_{joint}').currentText()
	index = getattr(parent, f'{card}_drive_{next_joint}').findText(step_driver)
	getattr(parent, f'{card}_drive_{next_joint}').setCurrentIndex(index)
	getattr(parent, f'{card}_axis_{next_joint}').setFocus()
	getattr(parent, f'{card}_JointTW').setCurrentIndex(next_tab)

def new_config(parent):
	for child in parent.findChildren(QLineEdit):
		if child.text():
			msg = ('Erase all entries and start new?')
			result = dialogs.errorMsgYesNo(msg, 'Data found')
			if result:
				break
			elif not result:
				return
	for child in parent.findChildren(QLineEdit):
		child.clear()
	for child in parent.findChildren(QComboBox):
		child.setCurrentIndex(0)
	for child in parent.findChildren(QDoubleSpinBox):
		child.setValue(0)
	for child in parent.findChildren(QCheckBox):
		child.setChecked(False)
	parent.servoPeriodSB.setValue(1000000)
	parent.introGraphicLE.setText('emc2.gif')
	parent.mainTW.setCurrentIndex(0)

def inputChanged(parent): # test to see if not checked then enable both
	card, item, function, number = parent.sender().objectName().split('_')
	state =  parent.sender().checkState()
	debounce = ['7i96s', '7i97']
	if state == 0: # only 7i96s and 7i97 have debounce
		if parent.boardCB.currentData() in debounce:
			getattr(parent, f'{card}_input_debounce_{number}').setEnabled(True)
		getattr(parent, f'{card}_input_invert_{number}').setEnabled(True)
	if function == 'invert' and state == 2:
		getattr(parent, f'{card}_input_debounce_{number}').setEnabled(False)
	elif function == 'debounce' and state == 2:
		getattr(parent, f'{card}_input_invert_{number}').setEnabled(False)

def changed(parent): # if anything is changed add *
	parent.status_lb.setText('Changed')
	parent.actionBuild.setText('Build Config *')

def calc_angular_scale(parent):
	if len(parent.lin_steps_rev_le.text()) > 0: # required entry
		if is_number(parent.lin_steps_rev_le.text()):
			steps_rev = int(float(parent.lin_steps_rev_le.text())) if parent.lin_steps_rev_le.text() != '' else False
		else:
			msg = (f'{parent.lin_steps_rev_le.text()} is not a valid number\n'
			f'for {parent.lin_steps_rev_le.property("name")}')
			dialogs.errorMsgOk(msg, 'Error')
			return
	else:
		msg = (f'{parent.lin_steps_rev_le.property("name")} must be not be blank')
		dialogs.errorMsgOk(msg, 'Error')
		return

	if len(parent.angular_rotations_le.text()) > 0: # required entry
		if is_number(parent.angular_rotations_le.text()):
			gear_ratio = float(parent.angular_rotations_le.text()) if parent.angular_rotations_le.text() != '' else False
			print(gear_ratio)
		else:
			msg = (f'{parent.angular_rotations_le.text()} is not a valid number\n'
			f'for {parent.angular_rotations_le.property("name")}')
			dialogs.errorMsgOk(msg, 'Error')
			return
	else:
		msg = (f'{parent.angular_rotations_le.property("name")} must be not be blank')
		dialogs.errorMsgOk(msg, 'Error')
		return

	if len(parent.angular_microsteps_le.text()) > 0:
		if is_number(parent.angular_microsteps_le.text()):
			micro_steps = int(float(parent.angular_microsteps_le.text()))
		else:
			msg = (f'{parent.angular_microsteps_le.text()} is not a valid number\n'
			f'for {parent.angular_microsteps_le.property("name")}')
			dialogs.errorMsgOk(msg, 'Error')
			return
	else:
		micro_steps = False

	if micro_steps:
		steps_rev = steps_rev * micro_steps

	parent.angular_scale_le.setText(f'{(steps_rev * gear_ratio) / 360:.2f}')

def calc_scale(parent):
	# scale = steps/rev * microsteps * (leadscrew teeth / motor teeth) * leadscrew revs/ unit
	if len(parent.lin_steps_rev_le.text()) > 0: # required entry
		if is_number(parent.lin_steps_rev_le.text()):
			steps_rev = int(float(parent.lin_steps_rev_le.text())) if parent.lin_steps_rev_le.text() != '' else False
		else:
			msg = (f'{parent.lin_steps_rev_le.text()} is not a valid number\n'
			f'for {parent.lin_steps_rev_le.property("name")}')
			dialogs.errorMsgOk(msg, 'Error')
			return
	else:
		msg = (f'{parent.lin_steps_rev_le.property("name")} must be not be blank')
		dialogs.errorMsgOk(msg, 'Error')
		return

	if len(parent.lin_leadscrew_pitch_le.text()) > 0: # required entry
		if is_number(parent.lin_leadscrew_pitch_le.text()):
			leadscrew_pitch = float(parent.lin_leadscrew_pitch_le.text())
		else:
			msg = (f'{parent.lin_leadscrew_pitch_le.text()} is not a valid number\n'
			f'for {parent.lin_leadscrew_pitch_le.property("name")}')
			dialogs.errorMsgOk(msg, 'Error')
			return
	else:
		msg = (f'{parent.lin_leadscrew_pitch_le.property("name")} must be not be blank')
		dialogs.errorMsgOk(msg, 'Error')
		return

	if len(parent.lin_microsteps_le.text()) > 0:
		if is_number(parent.lin_microsteps_le.text()):
			micro_steps = int(float(parent.lin_microsteps_le.text()))
		else:
			msg = (f'{parent.lin_microsteps_le.text()} is not a valid number\n'
			f'for {parent.lin_microsteps_le.property("name")}')
			dialogs.errorMsgOk(msg, 'Error')
			return
	else:
		micro_steps = False

	if len(parent.lin_stepper_teeth_le.text()) > 0:
		if is_number(parent.lin_stepper_teeth_le.text()):
			stepper_teeth = int(float(parent.lin_stepper_teeth_le.text()))
		else:
			msg = (f'{parent.lin_stepper_teeth_le.text()} is not a valid number\n'
			f'for {parent.lin_stepper_teeth_le.property("name")}')
			dialogs.errorMsgOk(msg, 'Error')
			return
	else:
		stepper_teeth = False

	if len(parent.lin_leadscrew_teeth_le.text()) > 0:
		if is_number(parent.lin_leadscrew_teeth_le.text()):
			leadscrew_teeth = int(float(parent.lin_leadscrew_teeth_le.text()))
		else:
			msg = (f'{parent.lin_leadscrew_teeth_le.text()} is not a valid number\n'
			f'for {parent.lin_leadscrew_teeth_le.property("name")}')
			dialogs.errorMsgOk(msg, 'Error')
			return
	else:
		leadscrew_teeth = False

	if micro_steps: # get steps per rev
		steps_rev = steps_rev * micro_steps

	if leadscrew_teeth and stepper_teeth:
		parent.lin_scale_le.setText(f'{round(steps_rev * (leadscrew_teeth/stepper_teeth) * leadscrew_pitch, 4):g}')
	else:
		parent.lin_scale_le.setText(f'{round(steps_rev * leadscrew_pitch, 4):g}')



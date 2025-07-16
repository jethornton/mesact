
from PyQt5.QtWidgets import QWidget

from libmesact import mdi
from libmesact import dialogs
from libmesact import utilities

def checkit(parent):
	configErrors = []
	tabError = False
	nextHeader = 0
	validNumber = 'is not a valid number in the form 0.0 or 0'

	# check the Machine Tab for errors
	if not parent.configNameLE.text():
		tabError = True
		configErrors.append('\tA configuration name must be entered')
	if not parent.boardCB.currentData():
		tabError = True
		configErrors.append('\tA Board must be selected')
	if parent.boardType == 'eth' and not parent.ipAddressCB.currentData():
		tabError = True
		configErrors.append('\tAn IP address must be selected, 10.10.10.10 is recommended')

	if tabError:
		configErrors.insert(nextHeader, 'Machine Tab:')
		nextHeader = len(configErrors)
		tabError = False
	# end of Machine Tab

	# check the Firmware Tab for errors

	if tabError:
		configErrors.insert(nextHeader, 'Firmware Tab:')
		nextHeader = len(configErrors)
		tabError = False
	# end of Firmware Tab

	# check the Settings Tab for errors
	if parent.guiCB.currentText() == 'Select': # allow custom gui
		tabError = True
		configErrors.append('\tA GUI must be selected')
	elif parent.guiCB.currentText() == 'Gmoccapy': # Warn user about issues
		if parent.emc_version > (2, 9, 2):
			msg = ('Gmoccapy has removed auto G43\n'
			'since version 2.10.0 due to programming issues.\n'
			f"You're running LinxuCNC version {parent.emc_version}\n"
			'To retain this function see the Gmoccapy section of the forum\n'
			'https://forum.linuxcnc.org/gmoccapy/55011-lcnc-2-10-ask-for-automatic-g43-in-pncconf#318781')
			dialogs.errorMsgOk(msg, 'Warning')

	if not parent.linearUnitsCB.currentData():
		tabError = True
		configErrors.append('\tLinear Units must be selected')
	if not parent.positionOffsetCB.currentData():
		tabError = True
		configErrors.append('\tA Position Offset must be selected')
	if not parent.positionFeedbackCB.currentData():
		tabError = True
		configErrors.append('\tA Position Feedback must be selected')
	if parent.maxFeedOverrideSB.value() == 0.0:
		tabError = True
		configErrors.append('\tThe Max Feed Override must be greater than zero, 1.2 is suggested')
	if set('XYZUVW') & set(parent.coordinatesLB.text()):
		if parent.defLinJogVelDSB.value() == 0.0:
			tabError = True
			configErrors.append('\tDefault Linear Jog Velocity must be greater than zero')
		if parent.maxLinJogVelDSB.value() == 0.0:
			tabError = True
			configErrors.append('\tMaximum Linear Jog Velocity must be greater than zero')
	if set('ABC') & set(parent.coordinatesLB.text()):
		if parent.defAngJogVelDSB.value() == 0.0:
			tabError = True
			configErrors.append('\tDefault Angular Jog Velocity must be greater than zero')
		if parent.maxAngJogVelDSB.value() == 0.0:
			tabError = True
			configErrors.append('\tMaximum Angular Jog Velocity must be greater than zero')
	foamAxes = ['XYUV', 'XYZA', 'XYUZ']
	if parent.foamRB.isChecked():
		if parent.coordinatesLB.text() not in foamAxes:
			tabError = True
			configErrors.append('\tFoam axes must be one of XYUV, XYZA or XYUZ')

	if tabError:
		configErrors.insert(nextHeader, 'Settings Tab:')
		nextHeader = len(configErrors)
		tabError = False
	# end of Settings Tab


	# check for no Axis
	board = None
	axis_boards = ['7i76', '7i76e', '7i76eu', '7i77', '7i78', '7i85', '7i85s', '7i95',
	'7i95t', '7i96', '7i96s', '7i97', '7i97t']

	# find the card index by tab name
	#card_index_0 = parent.mainTW.indexOf(parent.mainTW.findChild(QWidget, 'card_0'))
	#card_index_1 = parent.mainTW.indexOf(parent.mainTW.findChild(QWidget, 'card_1'))
	#card_index_2 = parent.mainTW.indexOf(parent.mainTW.findChild(QWidget, 'card_2'))

	card_indexes = {}
	for i in range(3):
		card_indexes[f'card_index_{i}'] = parent.mainTW.indexOf(parent.mainTW.findChild(QWidget, f'card_{i}'))

	# FIXME this does not give the correct tab name
	if parent.boardCB.currentData() in axis_boards:
		board = parent.boardCB.currentData()
		tab = parent.mainTW.tabText(card_indexes['card_index_0'])

	elif parent.daughterCB_0.currentData() in axis_boards:
		board = parent.daughterCB_0.currentData()
		tab = parent.mainTW.tabText(card_indexes['card_index_1'])

	elif parent.daughterCB_1.currentData() in axis_boards:
		board = parent.daughterCB_1.currentData()
		tab = parent.mainTW.tabText(card_indexes['card_index_2'])

	if len(parent.coordinatesLB.text()) == 0 and board is not None:
		tabError = True
		configErrors.append('\tAt least one Axis must be configured')

	else: # check for home sequence errors
		coordinates = parent.coordinatesLB.text()
		for i in range(3):
			for j in range(6):
				if getattr(parent,f'c{i}_axis_{j}').currentData():
					home_sequence = getattr(parent,f'c{i}_homeSequence_{j}').text()
					axis = getattr(parent,f'c{i}_axis_{j}').currentData()
					if '-' in home_sequence and coordinates.count(axis) == 1:
						tabError = True
						configErrors.append(f'\tNegative Home Sequence on Joint {j} should only be used with multiple a joint Axis')

	if tabError:
		configErrors.insert(nextHeader, f'{tab} Tab:')
		nextHeader = len(configErrors)
		tabError = False
	# end of no Axis


	# check the Board Tabs for errors

	# check for data but no axis letter
	joint_items = ['_scale_', '_min_limit_', '_max_limit_', '_max_vel_',
		'_max_accel_', '_p_', '_i_', '_d_', '_ff0_', '_ff1_', '_ff2_', '_deadband_',
		'_bias_', '_maxOutput_', '_maxError_', '_min_ferror_', '_max_ferror_',
		'_StepTime_', '_StepSpace_', '_DirSetup_', '_DirHold_', '_analogMinLimit_',
		'_analogMaxLimit_', '_analogScaleMax_']
	for i in range(3):
		for j in range(6):
			if not getattr(parent,f'c{i}_axis_{j}').currentData():
				if i in range(1,3) and j == 5:
					if not getattr(parent, f'c{i}_spindle_cb').isChecked():
						for item in joint_items:
							if getattr(parent, f'c{i}{item}{j}').text():
								msg = (f'Joint{j} has data but no Axis Letter\n'
									'Delete that data?')
								if dialogs.errorMsgYesNo(msg, 'Error'):
									for item in joint_items:
										getattr(parent, f'c{i}{item}{j}').setText('')
								else: # change to offending tab
									parent.mainTW.setCurrentIndex(i + 3)
									getattr(parent, f'c{i}_JointTW').setCurrentIndex(j + 1)
									return

	for i in range(3):
		if parent.mainTW.isTabVisible(card_indexes[f'card_index_{i}']):
			tab = parent.mainTW.tabText(card_indexes[f'card_index_{i}'])
			for j in range(6): # Check for joint errors
				if getattr(parent, f'c{i}_axis_{j}').currentData(): # the axis has a letter
					if getattr(parent, f'c{i}_scale_{j}').isEnabled():
						if getattr(parent, f'c{i}_scale_{j}').text() == '':
							tabError = True
							configErrors.append(f'\tDrive {j} Scale must not be blank')
					if getattr(parent, f'c{i}_min_limit_{j}').text() == '':
						tabError = True
						configErrors.append(f'\tDrive {j} Min Limit must not be blank')
					if getattr(parent, f'c{i}_max_limit_{j}').text() == '':
						tabError = True
						configErrors.append(f'\tDrive {j} Max Limit must not be blank')
					if getattr(parent, f'c{i}_max_vel_{j}').text() == '':
						tabError = True
						configErrors.append(f'\tDrive {j} Max Velocity must not be blank')
					if getattr(parent, f'c{i}_max_accel_{j}').text() == '':
						tabError = True
						configErrors.append(f'\tDrive {j} Max Accel must not be blank')
					if getattr(parent, f'c{i}_p_{j}').text() == '':
						tabError = True
						configErrors.append(f'\tDrive {j} PID P must not be blank')
					if getattr(parent, f'c{i}_i_{j}').text() == '':
						tabError = True
						configErrors.append(f'\tDrive {j} PID I must not be blank')
					if getattr(parent, f'c{i}_d_{j}').text() == '':
						tabError = True
						configErrors.append(f'\tDrive {j} PID D must not be blank')
					if getattr(parent, f'c{i}_ff0_{j}').text() == '':
						tabError = True
						configErrors.append(f'\tDrive {j} PID FF0 must not be blank')
					if getattr(parent, f'c{i}_ff1_{j}').text() == '':
						tabError = True
						configErrors.append(f'\tDrive {j} PIF FF1 must not be blank')
					if getattr(parent, f'c{i}_ff2_{j}').text() == '':
						tabError = True
						configErrors.append(f'\tDrive {j} PID FF2 must not be blank')
					if getattr(parent, f'c{i}_deadband_{j}').text() == '':
						tabError = True
						configErrors.append(f'\tDrive {j} PID Deadband must not be blank')
					if getattr(parent, f'c{i}_bias_{j}').text() == '':
						tabError = True
						configErrors.append(f'\tDrive {j} PID Bias must not be blank')
					if getattr(parent, f'c{i}_maxOutput_{j}').text() == '':
						tabError = True
						configErrors.append(f'\tDrive {j} PID Max Output must not be blank')
					if getattr(parent, f'c{i}_settings_{j}').isTabVisible(2): # Stepgen Tab
						if getattr(parent, f'c{i}_maxError_{j}').text() == '':
							tabError = True
							configErrors.append(f'\tDrive {j} PID Max Error must not be blank')

					if '-' in getattr(parent, f'c{i}_min_ferror_{j}').text():
						tabError = True
						configErrors.append(f'\tDrive {j} Min Following Error must not be negative')
					else:
						if not utilities.is_number(getattr(parent, f'c{i}_min_ferror_{j}').text()):
							tabError = True
							configErrors.append(f'\tDrive {j} Min Following Error does not evaluate to a number')

					if '-' in getattr(parent, f'c{i}_max_ferror_{j}').text():
						tabError = True
						configErrors.append(f'\tDrive {j} Max Following Error must not be negative')
					else:
						if not utilities.is_number(getattr(parent, f'c{i}_max_ferror_{j}').text()):
							tabError = True
							configErrors.append(f'\tDrive {j} Max Following Error does not evaluate to a number')

					if getattr(parent, f'c{i}_settings_{j}').isTabVisible(2): # Stepgen Tab
						if getattr(parent, f'c{i}_StepTime_{j}').text() == '':
							tabError = True
							configErrors.append(f'\tDrive {j} Stepgen Step Time must not be blank')
						if getattr(parent, f'c{i}_StepSpace_{j}').text() == '':
							tabError = True
							configErrors.append(f'\tDrive {j} Stepgen Step Space must not be blank')
						if getattr(parent, f'c{i}_DirSetup_{j}').text() == '':
							tabError = True
							configErrors.append(f'\tDrive {j} Stepgen Direction Setup must not be blank')
						if getattr(parent, f'c{i}_DirHold_{j}').text() == '':
							tabError = True
							configErrors.append(f'\tDrive {j} Stepgen Direction Hold must not be blank')

					if getattr(parent, f'c{i}_settings_{j}').isTabVisible(3): # Analog Tab
						if getattr(parent, f'c{i}_analogMinLimit_{j}').text() == '':
							tabError = True
							configErrors.append(f'\tJoint {j} Analog Min Limit must not be blank')
						if getattr(parent, f'c{i}_analogMaxLimit_{j}').text() == '':
							tabError = True
							configErrors.append(f'\tDrive {j} Analog Max Limit must not be blank')
						if getattr(parent, f'c{i}_analogScaleMax_{j}').text() == '':
							tabError = True
							configErrors.append(f'\tDrive {j} Analog Scale Max must not be blank')

	# 7i77 drive 5 spindle checks
	for i in range(1,3):
		if getattr(parent, f'c{i}_spindle_cb').isChecked():
			if getattr(parent, f'c{i}_p_5').text() == '':
				tabError = True
				configErrors.append(f'\tDrive 5 PID P must not be blank')
			if getattr(parent, f'c{i}_i_5').text() == '':
				tabError = True
				configErrors.append(f'\tDrive 5 PID I must not be blank')
			if getattr(parent, f'c{i}_d_5').text() == '':
				tabError = True
				configErrors.append(f'\tDrive 5 PID D must not be blank')
			if getattr(parent, f'c{i}_ff0_5').text() == '':
				tabError = True
				configErrors.append(f'\tDrive 5 PID FF0 must not be blank')
			if getattr(parent, f'c{i}_ff1_5').text() == '':
				tabError = True
				configErrors.append(f'\tDrive 5 PIF FF1 must not be blank')
			if getattr(parent, f'c{i}_ff2_5').text() == '':
				tabError = True
				configErrors.append(f'\tDrive 5 PID FF2 must not be blank')
			if getattr(parent, f'c{i}_deadband_5').text() == '':
				tabError = True
				configErrors.append(f'\tDrive 5 PID Deadband must not be blank')
			if getattr(parent, f'c{i}_bias_5').text() == '':
				tabError = True
				configErrors.append(f'\tDrive 5 PID Bias must not be blank')
			if getattr(parent, f'c{i}_analogMinLimit_5').text() == '':
				tabError = True
				configErrors.append(f'\tDrive 5 Spindle Tab Min RPM Limit must not be blank')
			if getattr(parent, f'c{i}_analogMinLimit_5').text() == '':
				tabError = True
				configErrors.append(f'\tDrive 5 Spindle Tab Max RPM Limit must not be blank')
			if getattr(parent, f'c{i}_analogScaleMax_5').text() == '':
				tabError = True
				configErrors.append(f'\tDrive 5 Spindle Tab Scale Max must not be blank')




			#if getattr(parent, f'c{i}_maxOutput_5').text() == '':
			#	tabError = True
			#	configErrors.append(f'\tDrive 5 PID Max Output must not be blank')


		if tabError:
			configErrors.insert(nextHeader, f'{tab} Tab:')
			nextHeader = len(configErrors)
			tabError = False
		# end of joint Tab


	# check I/O for errors
	# get the joints
	joints = 0
	axes_list = list(parent.coordinatesLB.text())
	axes_set = set('ABCUVWXYZ')

	for i in range(3):
		for j in range(6):
			if getattr(parent, f'c{i}_axis_{j}').currentData():
				joints += 1

	# Inputs
	for i in range(3): # check for Joint n more than configured
		for j in range(32):
			selection = getattr(parent, f'c{i}_input_{j}').text()
			if selection.startswith('Joint'):
				if int(selection.split()[1]) > joints:
					tabError = True
					configErrors.append(f'\t{selection} is more than the number of joints')

			if axes_set & set(selection.split()):
				if not set(selection.split()) & set(axes_list): # check for axis not configured
					tabError = True
					configErrors.append(f'\t{selection} axis is not configured')

	if tabError:
		configErrors.insert(nextHeader, f'{tab} Inputs Tab:')
		nextHeader = len(configErrors)
		tabError = False
	# end of Inputs Tab

	# Outputs
	for i in range(3): # check for Joint n more than configured
		for j in range(16):
			selection = getattr(parent, f'c{i}_output_{j}').text()
			if selection.startswith('Joint'):
				if int(selection.split()[1]) > joints:
					tabError = True
					configErrors.append(f'\t{selection} is more than the number of joints')

	if tabError:
		configErrors.insert(nextHeader, f'{tab} Outputs Tab:')
		nextHeader = len(configErrors)
		tabError = False
	# end of Outputs Tab


	# check the Spindle Tab for errors
	if parent.spindleTypeCB.currentData() == 'pwm':
		if parent.spindleMaxRpmFwd.value() == 0:
			tabError = True
			configErrors.append(f'\tSpindle Settings Maximum Fwd can not be 0')
		if parent.maxOutput_s.value() == 0:
			tabError = True
			configErrors.append(f'\tPID Settings Max Output can not be 0')

	if tabError:
		configErrors.insert(nextHeader, 'Spindle Tab:')
		nextHeader = len(configErrors)
		tabError = False
	# end of Spindle Tab


	# check the SS Cards Tab for errors
	# end of SS Cards Tab

	# check the Options Tab for errors
	mdi_commands = []
	for i in range(mdi.get_mdi_commands_count(parent)):
		cmd = mdi.get_mdi_command(parent, i)
		if len(cmd) > 0:
			mdi_commands.append(i)
	if len(mdi_commands) > 0:
		if len(mdi_commands) != max(mdi_commands) + 1:
			tabError = True
			configErrors.append(f'\tMDI commands must start at 0 and not skip any')
		if not parent.haluiCB.isChecked():
			tabError = True
			configErrors.append(f'\tMDI commands require Hal User Interface to be checked')

	if tabError:
		configErrors.insert(nextHeader, 'Options Tab:')
		nextHeader = len(configErrors)
		tabError = False
	# end of Options Tab

	# check the PLC Tab for errors
	# end of PLC Tab

	# check the PC Tab for errors
	# end of PC Tab

	parent.info_pte.clear()
	parent.mainTW.setCurrentIndex(11)

	if configErrors:
		checkit.result = '\n'.join(configErrors)
		parent.info_pte.setPlainText(checkit.result)
		return False
	else:
		parent.info_pte.setPlainText('Configuration checked OK')
		return True




def checkit(parent):
	parent.mainTW.setCurrentIndex(10)
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
	if parent.daughterCB_1.isEnabled(): # P2 is enabled
		mb = parent.boardCB.currentData()
		p1b = parent.daughterCB_0.currentData()
		p2b = parent.daughterCB_1.currentData()
		one_ss = ['7i96', '7i96s']
		if mb not in one_ss and p1b and not p2b: # P1 is selected but P2 is not selected
			tabError = True
			configErrors.append('\tThe P2 Daughter must be selected to get the sserial ports for P1')

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
	if not parent.guiCB.currentData():
		tabError = True
		configErrors.append('\tA GUI must be selected')
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
	if set('XYZUVW')&set(parent.coordinatesLB.text()):
		if parent.defLinJogVelDSB.value() == 0.0:
			tabError = True
			configErrors.append('\tDefault Linear Jog Velocity must be greater than zero')
		if parent.maxLinJogVelDSB.value() == 0.0:
			tabError = True
			configErrors.append('\tMaximum Linear Jog Velocity must be greater than zero')
	if set('ABC')&set(parent.coordinatesLB.text()):
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

	# check the Joint Tabs for errors c0_axis_0 c0_max_vel_0
	if parent.boardCB.currentData(): # only check if a board is selected
		if len(parent.coordinatesLB.text()) == 0:
			tabError = True
			configErrors.append('\tAt least one Joint must be configured starting with Joint 0')

	'''
	For the common trivkins kinematics, joint numbers are assigned in sequence according to the trivkins parameter
	<Tom_L> so it looks like they do need to be consecutive
	<Tom_L>  It is permitted to write an axis name more than once (e.g., X Y Y Z for a gantry machine).
	'''

	# check each tab so error message is correct so loose the for i in range
	for i in range(3):
		tab = getattr(parent, 'mainTW').tabText(i + 3)
		for j in range(6):
			if getattr(parent, f'c{i}_axis_{j}').currentData():
				if getattr(parent, f'c{i}_scale_{j}').text() == '':
					tabError = True
					configErrors.append(f'\tJoint {j} Scale must not be blank')
				if getattr(parent, f'c{i}_min_limit_{j}').text() == '':
					tabError = True
					configErrors.append(f'\tJoint {j} Min Limit must not be blank')
				if getattr(parent, f'c{i}_max_limit_{j}').text() == '':
					tabError = True
					configErrors.append(f'\tJoint {j} Max Limit must not be blank')
				if getattr(parent, f'c{i}_max_vel_{j}').text() == '':
					tabError = True
					configErrors.append(f'\tJoint {j} Max Velocity must not be blank')
				if getattr(parent, f'c{i}_max_accel_{j}').text() == '':
					tabError = True
					configErrors.append(f'\tJoint {j} Max Accel must not be blank')

	# check I/O for errors
	# get the joints
	joints = 0
	for i in range(3):
		for j in range(6):
			if getattr(parent, f'c{i}_axis_{j}').currentData():
				joints += 1
				#print(f'Joint: {joints}')
	for i in range(3):
		for j in range(32):
			selection = getattr(parent, f'c{i}_input_{j}').text()
			if selection.startswith('Joint'):
				if int(selection.split()[1]) > joints:
					tabError = True
					configErrors.append(f'\t{selection} is more than the number of joints')

	for i in range(3):
		for j in range(16):
			selection = getattr(parent, f'c{i}_output_{j}').text()
			if selection.startswith('Joint'):
				if int(selection.split()[1]) > joints:
					tabError = True
					configErrors.append(f'\t{selection} is more than the number of joints')

	if tabError:
		tab = parent.boardCB.currentText()
		configErrors.insert(nextHeader, f'{tab} Tab:')
		nextHeader = len(configErrors)
		tabError = False
	# end of Joints Tab

	# check the SS Cards Tab for errors
	# end of SS Cards Tab
	# check the Options Tab for errors
	# end of Options Tab
	# check the PLC Tab for errors
	# end of PLC Tab
	# check the PC Tab for errors
	# end of PC Tab


	parent.info_pte.clear()
	if configErrors:
		checkit.result = '\n'.join(configErrors)
		parent.info_pte.setPlainText(checkit.result)
		return False
	else:
		parent.info_pte.setPlainText('Configuration checked OK')
		return True



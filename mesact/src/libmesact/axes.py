
from PyQt5.QtWidgets import QMessageBox

from libmesact import utilities

def axisChanged(parent):
	connector = parent.sender().objectName()[:3]
	joint = parent.sender().objectName()[-1]
	axis = parent.sender().currentText()
	if axis in ['X', 'Y', 'Z', 'U', 'V', 'W']:
		getattr(parent, f'{connector}axisType_{joint}').setText('LINEAR')
		parent.minAngJogVelDSB.setEnabled(False)
		parent.defAngJogVelDSB.setEnabled(False)
		parent.maxAngJogVelDSB.setEnabled(False)
	elif axis in ['A', 'B', 'C']:
		getattr(parent, f'{connector}axisType_{joint}').setText('ANGULAR')
		parent.minAngJogVelDSB.setEnabled(True)
		parent.defAngJogVelDSB.setEnabled(True)
		parent.maxAngJogVelDSB.setEnabled(True)
	else:
		getattr(parent, f'{connector}axisType_{joint}').setText('')
		parent.minAngJogVelDSB.setEnabled(False)
		parent.defAngJogVelDSB.setEnabled(False)
		parent.maxAngJogVelDSB.setEnabled(False)
	coordList = []

	for i in range(6): # Card 0
		axisLetter = getattr(parent, f'c0_axis_{i}').currentText()
		if axisLetter != 'Select':
			coordList.append(axisLetter)
		parent.coordinatesLB.setText(''.join(coordList))
		#parent.axes = len(parent.coordinatesLB.text())

	'''
	for i in range(6): # Card 1
		axisLetter = getattr(parent, f'c1_axisCB_{i}').currentText()
		if axisLetter != 'Select':
			coordList.append(axisLetter)
		parent.coordinatesLB.setText(''.join(coordList))
		parent.axes = len(parent.coordinatesLB.text())
	'''

def updateAxisInfo(parent):
	#if parent.sender().objectName() == 'actionOpen':
	#	return
	card = parent.sender().objectName()[:2]
	joint = parent.sender().objectName()[-1]
	scale = getattr(parent, f'{card}_scale_' + joint).text()
	if scale and utilities.isNumber(scale):
		scale = float(scale)
	else:
		return

	maxVelocity = getattr(parent, f'{card}_max_vel_' + joint).text()
	if maxVelocity and utilities.isNumber(maxVelocity):
		maxVelocity = float(maxVelocity)
	else:
		return

	maxAccel = getattr(parent, f'{card}_max_accel_' + joint).text()
	if maxAccel and utilities.isNumber(maxAccel):
		maxAccel = float(maxAccel)
	else:
		return

	if parent.linearUnitsCB.currentData():
		accelTime = maxVelocity / maxAccel
		getattr(parent, f'{card}_timeJoint_' + joint).setText(f'{accelTime:.2f} seconds')
		accelDistance = accelTime * 0.5 * maxVelocity
		getattr(parent, f'{card}_distanceJoint_' + joint).setText(f'{accelDistance:.2f} {parent.linearUnitsCB.currentData()}')
		stepRate = scale * maxVelocity
		getattr(parent, f'{card}_stepRateJoint_' + joint).setText(f'{abs(stepRate):.0f} pulses')

def pidSetDefault(parent):
	connector = parent.sender().objectName()[:2]
	joint = parent.sender().objectName()[-1]
	if not parent.linearUnitsCB.currentData():
		QMessageBox.warning(parent,'Warning', 'Settings Tab\nLinear Units\nmust be selected', QMessageBox.Ok)
		return
	if joint == 's':
		getattr(parent, 'p_s').setValue(0)
		getattr(parent, 'i_s').setValue(0)
		getattr(parent, 'd_s').setValue(0)
		getattr(parent, 'ff0_s').setValue(1)
		getattr(parent, 'ff1_s').setValue(0)
		getattr(parent, 'ff2_s').setValue(0)
		getattr(parent, 'bias_s').setValue(0)
		getattr(parent, 'maxOutput_s').setValue(parent.spindleMaxRpm.value())
		getattr(parent, 'maxError_s').setValue(0)
		getattr(parent, 'deadband_s').setValue(0)
		return

	p = int(1000/(int(parent.servoPeriodSB.cleanText())/1000000))
	getattr(parent,  f'{connector}_p_{joint}').setText(f'{p}')
	getattr(parent, f'{connector}_i_{joint}').setText('0')
	getattr(parent, f'{connector}_d_{joint}').setText('0')
	getattr(parent, f'{connector}_ff0_{joint}').setText('0')
	getattr(parent, f'{connector}_ff1_{joint}').setText('1')
	getattr(parent, f'{connector}_ff2_{joint}').setText('0')
	getattr(parent, f'{connector}_bias_{joint}').setText('0')
	getattr(parent, f'{connector}_maxOutput_{joint}').setText('0')
	if parent.linearUnitsCB.itemData(parent.linearUnitsCB.currentIndex()) == 'inch':
		maxError = '0.0005'
	else:
		maxError = '0.0127'
	getattr(parent, f'{connector}_maxError_{joint}').setText(maxError)
	getattr(parent, f'{connector}_deadband_{joint}').setText('0')

def ferrorSetDefault(parent):
	if not parent.linearUnitsCB.currentData():
		QMessageBox.warning(parent,'Warning', 'Machine Tab\nLinear Units\nmust be selected', QMessageBox.Ok)
		return
	connector = parent.sender().objectName()[:2]
	joint = parent.sender().objectName()[-1]
	if parent.linearUnitsCB.currentData() == 'inch':
		getattr(parent, f'{connector}_ferror_{joint}').setText(' 0.0002')
		getattr(parent, f'{connector}_min_ferror_{joint}').setText(' 0.0001')
	else:
		getattr(parent, f'{connector}_ferror_{joint}').setText(' 0.005')
		getattr(parent, f'{connector}_min_ferror_{joint}').setText(' 0.0025')

def analogSetDefault(parent): # think this is broken...
	#tab = parent.sender().objectName()[-1]
	connector = parent.sender().objectName()[:2]
	joint = parent.sender().objectName()[-1]
	getattr(parent, f'{connector}_analogMinLimit_{joint}').setText('-10')
	getattr(parent, f'{connector}_analogMaxLimit_{joint}').setText('10')
	getattr(parent, f'{connector}_analogScaleMax_{joint}').setText('10')

def driveChanged(parent):
	timing = parent.sender().currentData()
	connector = parent.sender().objectName()[:3]
	joint = f'_{parent.sender().objectName()[-1]}'
	if parent.sender().objectName() == 'spindleDriveCB':
		connector = 'spindle'
		joint = ''
	if timing:
		parent.sender().setEditable(False)
		getattr(parent, f'{connector}StepTime{joint}').setText(timing[0])
		getattr(parent, f'{connector}StepSpace{joint}').setText(timing[1])
		getattr(parent, f'{connector}DirSetup{joint}').setText(timing[2])
		getattr(parent, f'{connector}DirHold{joint}').setText(timing[3])
		getattr(parent, f'{connector}StepTime{joint}').setEnabled(False)
		getattr(parent, f'{connector}StepSpace{joint}').setEnabled(False)
		getattr(parent, f'{connector}DirSetup{joint}').setEnabled(False)
		getattr(parent, f'{connector}DirHold{joint}').setEnabled(False)
	else:
		parent.sender().setEditable(True)
		getattr(parent, f'{connector}StepTime{joint}').setEnabled(True)
		getattr(parent, f'{connector}StepSpace{joint}').setEnabled(True)
		getattr(parent, f'{connector}DirSetup{joint}').setEnabled(True)
		getattr(parent, f'{connector}DirHold{joint}').setEnabled(True)




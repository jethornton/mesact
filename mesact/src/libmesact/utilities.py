

def isNumber(s):
	try:
		s[-1].isdigit()
		float(s)
		return True
	except ValueError:
		return False

def unitsChanged(parent):
	if not parent.linearUnitsCB.currentData():
		unitsSecond = ''
		unitsMinute = ''
		for i in range(6):
			getattr(parent, f'c0_unitsLB_{i}').setText('Select Units\nMachine Tab')
		return
	if parent.linearUnitsCB.currentData() == 'mm':
		unitsSecond = 'mm/sec'
		unitsMinute = 'mm/min'
	elif parent.linearUnitsCB.currentData() == 'inch':
		unitsSecond = 'in/sec'
		unitsMinute = 'in/min'
	for i in range(4):
		getattr(parent, f'unitsLB_{i}').setText(f'Vel & Acc\n{unitsSecond}')
	parent.trajMaxLinVelDSB.setSuffix(f' {unitsSecond}')
	parent.minLinJogVelDSB.setSuffix(f' {unitsSecond}')
	parent.defLinJogVelDSB.setSuffix(f' {unitsSecond}')
	parent.maxLinJogVelDSB.setSuffix(f' {unitsSecond}')
	parent.minLinearVelLB.setText(f'{parent.minLinJogVelDSB.value() * 60:.1f} {unitsMinute}')
	parent.jogSpeedLB.setText(f'{parent.defLinJogVelDSB.value() * 60:.1f} {unitsMinute}')
	parent.maxLinearVelLB.setText(f'{parent.maxLinJogVelDSB.value() * 60:.1f} {unitsMinute}')
	if set('ABC')&set(parent.coordinatesLB.text()): # angular axis
		parent.defAngularVelLB.setText(f'{parent.defAngJogVelDSB.value() * 60:.1f} deg/min')

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



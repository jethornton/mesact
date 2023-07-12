from libmesact import utilities

# this file is for testing during initial programming

def default_settings(parent):
	utilities.new_config(parent)
	parent.guiCB.setCurrentIndex(parent.guiCB.findData('axis'))
	parent.linearUnitsCB.setCurrentIndex(parent.linearUnitsCB.findData('inch'))
	parent.positionOffsetCB.setCurrentIndex(parent.positionOffsetCB.findData('RELATIVE'))
	parent.positionFeedbackCB.setCurrentIndex(parent.positionFeedbackCB.findData('COMMANDED'))
	#parent..setCurrentIndex(parent..findData(''))
	parent.maxFeedOverrideSB.setValue(1.2)
	parent.defLinJogVelDSB.setValue(0.5)
	parent.maxLinJogVelDSB.setValue(1.0)
	parent.set_7i96s_pb.setEnabled(True)
	parent.set_7i96s_7i76_pb.setEnabled(True)
	parent.set_7i96s_7i77_pb.setEnabled(True)
	parent.set_7i92t_p1_7i76_pb.setEnabled(True)
	parent.set_7i92t_p2_7i76_pb.setEnabled(True)
	parent.set_7i92t_p1_7i77_pb.setEnabled(True)
	parent.set_7i92t_p2_7i77_pb.setEnabled(True)

def set_7i96s(parent):
	parent.boardCB.setCurrentIndex(parent.boardCB.findData('7i96s'))
	parent.ipAddressCB.setCurrentIndex(parent.ipAddressCB.findData('10.10.10.10'))
	set_joints(parent, 0, ['X', 'Y', 'Z'])
	parent.c0_homeSequence_0.setText('2')
	parent.c0_homeSequence_1.setText('1')
	parent.c0_homeSequence_2.setText('0')

def set_7i96s_7i76(parent):
	parent.boardCB.setCurrentIndex(parent.boardCB.findData('7i96s'))
	parent.ipAddressCB.setCurrentIndex(parent.ipAddressCB.findData('10.10.10.10'))
	parent.daughterCB_0.setCurrentIndex(parent.daughterCB_0.findData('7i76'))
	set_joints(parent, 0, ['X', 'Y', 'Z'])
	set_joints(parent, 1, ['U', 'V', 'W'])
	parent.c0_homeSequence_0.setText('2')
	parent.c0_homeSequence_1.setText('1')
	parent.c0_homeSequence_2.setText('0')
	parent.c1_homeSequence_0.setText('5')
	parent.c1_homeSequence_1.setText('4')
	parent.c1_homeSequence_2.setText('3')

def set_7i96s_7i77(parent):
	parent.boardCB.setCurrentIndex(parent.boardCB.findData('7i96s'))
	parent.ipAddressCB.setCurrentIndex(parent.ipAddressCB.findData('10.10.10.10'))
	parent.daughterCB_0.setCurrentIndex(parent.daughterCB_0.findData('7i77'))

def set_7i92t_p1_7i76(parent):
	parent.boardCB.setCurrentIndex(parent.boardCB.findData('7i92t'))
	parent.ipAddressCB.setCurrentIndex(parent.ipAddressCB.findData('10.10.10.10'))
	parent.daughterCB_0.setCurrentIndex(parent.daughterCB_0.findData('7i76'))
	set_joints(parent, 1, ['X', 'Y', 'Z'])
	parent.c1_homeSequence_0.setText('2')
	parent.c1_homeSequence_1.setText('1')
	parent.c1_homeSequence_2.setText('0')

def set_7i92t_p2_7i76(parent):
	parent.boardCB.setCurrentIndex(parent.boardCB.findData('7i92t'))
	parent.ipAddressCB.setCurrentIndex(parent.ipAddressCB.findData('10.10.10.10'))
	parent.daughterCB_1.setCurrentIndex(parent.daughterCB_1.findData('7i76'))
	set_joints(parent, 2, ['X', 'Y', 'Z'])
	parent.c2_homeSequence_0.setText('2')
	parent.c2_homeSequence_1.setText('1')
	parent.c2_homeSequence_2.setText('0')

def set_7i92t_p1_7i77(parent):
	parent.boardCB.setCurrentIndex(parent.boardCB.findData('7i92t'))
	parent.ipAddressCB.setCurrentIndex(parent.ipAddressCB.findData('10.10.10.10'))
	parent.daughterCB_0.setCurrentIndex(parent.daughterCB_0.findData('7i77'))
	set_joints(parent, 1, ['X', 'Y', 'Z'])
	parent.c1_homeSequence_0.setText('2')
	parent.c1_homeSequence_1.setText('1')
	parent.c1_homeSequence_2.setText('0')

def set_7i92t_p2_7i77(parent):
	parent.boardCB.setCurrentIndex(parent.boardCB.findData('7i92t'))
	parent.ipAddressCB.setCurrentIndex(parent.ipAddressCB.findData('10.10.10.10'))
	parent.daughterCB_1.setCurrentIndex(parent.daughterCB_1.findData('7i77'))
	set_joints(parent, 2, ['X', 'Y', 'Z'])
	parent.c2_homeSequence_0.setText('2')
	parent.c2_homeSequence_1.setText('1')
	parent.c2_homeSequence_2.setText('0')

def set_joints(parent, card, axes):
	# value = <value_if_true> if <expression> else <value_if_false>
	mb = parent.boardCB.currentText()
	p1 = parent.daughterCB_0.currentData()
	p2 = parent.daughterCB_1.currentData()
	mb = mb if mb else ''
	p1 = f' P1-{p1}' if p1 else ''
	p2 = f' P2-{p2}' if p2 else ''
	name = mb if mb else ''
	for joint, axis in enumerate(axes):
		#print(card, joint)
		getattr(parent, f'c{card}_scale_{joint}').setText('1000')
		getattr(parent, f'c{card}_axis_{joint}').setCurrentIndex(getattr(parent, f'c0_axis_{joint}').findData(axis))
		if axis == 'Z':
			getattr(parent, f'c{card}_min_limit_{joint}').setText('-5')
			getattr(parent, f'c{card}_max_limit_{joint}').setText('0')
		else:
			getattr(parent, f'c{card}_min_limit_{joint}').setText('0')
			getattr(parent, f'c{card}_max_limit_{joint}').setText('10')
		getattr(parent, f'c{card}_max_vel_{joint}').setText('1')
		getattr(parent, f'c{card}_max_accel_{joint}').setText('4')
		getattr(parent, f'c{card}_pidDefault_{joint}').click()
		getattr(parent, f'c{card}_ferrorDefault_{joint}').click()
		getattr(parent, f'c{card}_drive_{joint}').setCurrentIndex(getattr(parent, f'c{card}_drive_{joint}').findText('Gecko 203v'))
	parent.configNameLE.setText(f'{mb}{p1}{p2} {parent.coordinatesLB.text()}')



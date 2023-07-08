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
	parent.set_7i92t_7i76_pb.setEnabled(True)
	parent.set_7i92t_7i77_pb.setEnabled(True)
	parent.x_config_pb.setEnabled(True)
	parent.xyz_config_pb.setEnabled(True)
	parent.xyyz_config_pb.setEnabled(True)

def set_7i96s(parent):
	parent.boardCB.setCurrentIndex(parent.boardCB.findData('7i96s'))
	parent.ipAddressCB.setCurrentIndex(parent.ipAddressCB.findData('10.10.10.10'))

def set_7i96s_7i76(parent):
	parent.boardCB.setCurrentIndex(parent.boardCB.findData('7i96s'))
	parent.ipAddressCB.setCurrentIndex(parent.ipAddressCB.findData('10.10.10.10'))
	parent.daughterCB_0.setCurrentIndex(parent.daughterCB_0.findData('7i76'))

def set_7i96s_7i77(parent):
	parent.boardCB.setCurrentIndex(parent.boardCB.findData('7i96s'))
	parent.ipAddressCB.setCurrentIndex(parent.ipAddressCB.findData('10.10.10.10'))
	parent.daughterCB_0.setCurrentIndex(parent.daughterCB_0.findData('7i77'))

def set_7i92t_7i76(parent):
	parent.boardCB.setCurrentIndex(parent.boardCB.findData('7i92t'))
	parent.ipAddressCB.setCurrentIndex(parent.ipAddressCB.findData('10.10.10.10'))
	parent.daughterCB_1.setCurrentIndex(parent.daughterCB_1.findData('7i76'))

def set_7i92t_7i77(parent):
	parent.boardCB.setCurrentIndex(parent.boardCB.findData('7i92t'))
	parent.ipAddressCB.setCurrentIndex(parent.ipAddressCB.findData('10.10.10.10'))
	parent.daughterCB_1.setCurrentIndex(parent.daughterCB_1.findData('7i77'))

def x_config(parent):
	axes = ['X']
	set_joints(parent, axes)
	sequence = len(axes) -1
	parent.c0_homeSequence_0.setText('0')

def xyz_config(parent):
	axes = ['X', 'Y', 'Z']
	set_joints(parent, axes)
	sequence = len(axes) -1
	parent.c0_homeSequence_0.setText('2')
	parent.c0_homeSequence_1.setText('1')
	parent.c0_homeSequence_2.setText('0')

def xyyz_config(parent):
	axes = ['X', 'Y', 'Y', 'Z']
	set_joints(parent, axes)
	parent.c0_homeSequence_0.setText('2')
	parent.c0_homeSequence_1.setText('-1')
	parent.c0_homeSequence_2.setText('-1')
	parent.c0_homeSequence_3.setText('0')

def set_joints(parent, axes):
	# value = <value_if_true> if <expression> else <value_if_false>
	mb = parent.boardCB.currentText()
	p1 = parent.daughterCB_0.currentData()
	p2 = parent.daughterCB_1.currentData()
	mb = mb if mb else ''
	p1 = f' P1-{p1}' if p1 else ''
	p2 = f' P2-{p2}' if p2 else ''
	name = mb if mb else ''
	parent.configNameLE.setText(f'{mb}{p1}{p2} {"".join(axes)}')
	for joint, axis in enumerate(axes):
		getattr(parent, f'c0_scale_{joint}').setText('1000')
		getattr(parent, f'c0_axis_{joint}').setCurrentIndex(getattr(parent, f'c0_axis_{joint}').findData(axis))
		if axis == 'Z':
			getattr(parent, f'c0_min_limit_{joint}').setText('-5')
			getattr(parent, f'c0_max_limit_{joint}').setText('0')
		else:
			getattr(parent, f'c0_min_limit_{joint}').setText('0')
			getattr(parent, f'c0_max_limit_{joint}').setText('10')
		getattr(parent, f'c0_max_vel_{joint}').setText('1')
		getattr(parent, f'c0_max_accel_{joint}').setText('4')
		getattr(parent, f'c0_pidDefault_{joint}').click()
		getattr(parent, f'c0_ferrorDefault_{joint}').click()
		getattr(parent, f'c0_drive_{joint}').setCurrentIndex(getattr(parent, f'c0_drive_{joint}').findText('Gecko 203v'))



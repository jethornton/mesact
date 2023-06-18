# this file is for testing during initial programming

def set_7i96s(parent):
	parent.boardCB.setCurrentIndex(parent.boardCB.findData('7i96s'))
	parent.boardCB.setCurrentIndex(parent.boardCB.findData('7i96s'))
	parent.ipAddressCB.setCurrentIndex(parent.ipAddressCB.findData('10.10.10.10'))

def default_settings(parent):
	parent.guiCB.setCurrentIndex(parent.guiCB.findData('axis'))
	parent.linearUnitsCB.setCurrentIndex(parent.linearUnitsCB.findData('inch'))
	parent.positionOffsetCB.setCurrentIndex(parent.positionOffsetCB.findData('RELATIVE'))
	parent.positionFeedbackCB.setCurrentIndex(parent.positionFeedbackCB.findData('COMMANDED'))
	#parent..setCurrentIndex(parent..findData(''))
	parent.defLinJogVelDSB.setValue(0.5)
	parent.maxLinJogVelDSB.setValue(1.0)

def xyz_config(parent):
	axes = ['X', 'Y', 'Z']
	set_joints(parent, axes)

def xyyz_config(parent):
	axes = ['X', 'Y', 'Y', 'Z']
	set_joints(parent, axes)

def set_joints(parent, axes):
	parent.configNameLE.setText(f'{"".join(axes)}')
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



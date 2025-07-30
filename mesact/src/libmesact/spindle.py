from libmesact import dialogs

def spindle_enable(parent):
	if parent.spindle_enable_cb.isChecked():
		# set spindle PID enabled
		parent.spindle_pid_gb.setEnabled(True)
		# set spindle Feedback enabled
		parent.spindle_feedback_gb.setEnabled(True)
		parent.spindleTW.setEnabled(True)
		parent.spindle_feedback_gb.setEnabled(True)
		parent.spindle_pid_gb.setEnabled(True)
	else:
		# set spindle PID enabled
		parent.spindle_pid_gb.setEnabled(False)
		# set spindle Feedback enabled
		parent.spindle_feedback_gb.setEnabled(False)
		parent.spindleTW.setEnabled(False)
		parent.spindle_feedback_gb.setEnabled(False)
		parent.spindle_pid_gb.setEnabled(False)

def spindle_limits(parent, item):
	if parent.sender().isChecked():
		match item:
			case 'min_fwd':
				parent.spindle_fwd_min_rpm.setEnabled(True)
			case 'max_fwd':
				parent.spindle_fwd_max_rpm.setEnabled(True)
			case 'min_rev':
				parent.spindle_rev_min_rpm.setEnabled(True)
			case 'max_rev':
				parent.spindle_rev_max_rpm.setEnabled(True)
			case _:
				pass

	else:
		match item:
			case 'min_fwd':
				parent.spindle_fwd_min_rpm.setEnabled(False)
			case 'max_fwd':
				parent.spindle_fwd_max_rpm.setEnabled(False)
			case 'min_rev':
				parent.spindle_rev_min_rpm.setEnabled(False)
			case 'max_rev':
				parent.spindle_rev_max_rpm.setEnabled(False)
			case _:
				pass

def spindle_feedback(parent):
	if parent.spindleFeedbackCB.currentData():
		parent.spindleEncoderScale.setEnabled(True)
	else:
		parent.spindleEncoderScale.setEnabled(False)

def spindle_pid_default(parent):
	spindle = parent.sender().objectName()
	if spindle[-1] == 's' or spindle[:3] == 'set':
		getattr(parent, 'p_s').setValue(0)
		getattr(parent, 'i_s').setValue(0)
		getattr(parent, 'd_s').setValue(0)
		getattr(parent, 'ff0_s').setValue(1)
		getattr(parent, 'ff1_s').setValue(0)
		getattr(parent, 'ff2_s').setValue(0)
		getattr(parent, 'bias_s').setValue(0)
		getattr(parent, 'deadband_s').setValue(0)

	elif spindle[-1] == '5': # 7i77 spindle on drive 5
		card = spindle[:3]
		drive = spindle[-1]

		getattr(parent, f'{card}p_{drive}').setText('0')
		getattr(parent, f'{card}i_{drive}').setText('0')
		getattr(parent, f'{card}d_{drive}').setText('0')
		getattr(parent, f'{card}ff0_{drive}').setText('1')
		getattr(parent, f'{card}ff1_{drive}').setText('0')
		getattr(parent, f'{card}ff2_{drive}').setText('0')
		getattr(parent, f'{card}bias_{drive}').setText('0')
		getattr(parent, f'{card}deadband_{drive}').setText('0')

def spindleSettingsChanged(parent): # FIXME this is not used anymore
	if parent.spindleMinRpmFwd.value() > 0:
		parent.spindleMinRpsFwd.setText(f'{parent.spindleMinRpmFwd.value() / 60:.2f}')
	else:
		parent.spindleMinRpsFwd.setText('')
	if parent.spindleMinRpmRev.value() > 0:
		parent.spindleMinRpsRev.setText(f'{parent.spindleMinRpmRev.value() / 60:.2f}')
	else:
		parent.spindleMinRpsRev.setText('')
	if parent.spindleMaxRpmFwd.value() > 0:
		parent.spindleMaxRpsFwd.setText(f'{parent.spindleMaxRpmFwd.value() / 60:.2f}')
	else:
		parent.spindleMaxRpsFwd.setText('')
	if parent.spindleMaxRpmRev.value() > 0:
		parent.spindleMaxRpsRev.setText(f'{parent.spindleMaxRpmRev.value() / 60:.2f}')
	else:
		parent.spindleMaxRpsRev.setText('')
	if parent.spindleMaxAccel.value() > 0:
		parent.spindleMaxRpss.setText(f'{parent.spindleMaxAccel.value() / 60:.2f}')
	else:
		parent.spindleMaxRpss.setText('')

def spindle_cb_changed(parent): # 7i77 spindle
	axis_items = ['_axis_5', '_scale_5', '_min_limit_5', '_max_limit_5',
	'_max_vel_5', '_max_accel_5', '_options_gb', '_following_error_gb',
	'_analogDefault_5']
	card = parent.sender().objectName()[1]

	if parent.sender().isChecked():
		getattr(parent, f'c{card}_axisType_5').setText('Spindle')
		getattr(parent, f'c{card}_settings_5').setTabText(3, 'Spindle')
		getattr(parent, f'c{card}_min_limit_lb').setText('Min RPM Limit')
		getattr(parent, f'c{card}_max_limit_lb').setText('Max RPM Limit')
		getattr(parent, f'c{card}_scale_max_lb').setText('Scale Max')
		for item in axis_items: # disable axis items
			getattr(parent, f'c{card}{item}').setEnabled(False)
		getattr(parent,f'c{card}_pid_default_5').setVisible(True)

		spindle_instructions = ('''
		If spindle RPM is 0 to 6000 (0v to +10v
		Min RPM Limit = 0
		Max RPM Limit = 6000
		Scale Max = 6000
		
		If you have a bipolar spindle speed control (-10v to +10v)
		Min RPM Limit = -6000
		Max RPM Limit = 6000
		Scale Max = 6000
		''')
		getattr(parent, f'c{card}_spindle_lb').setText(spindle_instructions)

	else:
		getattr(parent, f'c{card}_axisType_5').clear()
		getattr(parent, f'c{card}_settings_5').setTabText(3, 'Analog')
		getattr(parent, f'c{card}_min_limit_lb').setText('Analog Min Limit')
		getattr(parent, f'c{card}_max_limit_lb').setText('Analog Max Limit')
		getattr(parent, f'c{card}_scale_max_lb').setText('Analog Scale Max')
		for item in axis_items: # enable axis items
			getattr(parent, f'c{card}{item}').setEnabled(False)
		getattr(parent,f'c{card}_pid_default_5').setVisible(True)
		getattr(parent, f'c{card}_spindle_lb').setText('')








from libmesact import dialogs

def spindle_pid_default(parent):
	if parent.spindleMaxRpmFwd.value() <= parent.spindleMinRpmFwd.value():
		msg = ('Spindle Maximum RPM must be higher\n'
		'than Spindle Minimum RPM')
		dialogs.errorMsgOk(msg, 'Configuration Error!')
		return
	getattr(parent, 'p_s').setValue(0)
	getattr(parent, 'i_s').setValue(0)
	getattr(parent, 'd_s').setValue(0)
	getattr(parent, 'ff0_s').setValue(1)
	getattr(parent, 'ff1_s').setValue(0)
	getattr(parent, 'ff2_s').setValue(0)
	getattr(parent, 'bias_s').setValue(0)
	getattr(parent, 'maxOutput_s').setValue(parent.spindleMaxRpmFwd.value())
	getattr(parent, 'maxError_s').setValue(0)
	getattr(parent, 'deadband_s').setValue(0)

# need to put spindle feedback in boards and daughters
def spindle_type_changed(parent):
	if parent.sender().currentData():
		spindle_type = parent.sender().currentData()
		if spindle_type == 'pwm':
			parent.output_type = '1'
			parent.pwmFrequencySB.setEnabled(True)
			if parent.emc_version >= (2, 9, 0):
				parent.spindleMinRpmFwd.setEnabled(True)
				parent.spindleMinRpmRev.setEnabled(True)
				parent.spindleMaxRpmRev.setEnabled(True)
			parent.spindleMaxRpmFwd.setEnabled(True)
			parent.spindle_feedback_gb.setEnabled(True)
			parent.spindle_pid_gb.setEnabled(True)
			parent.spindle_stepgen_gb.setEnabled(False)
		elif spindle_type == 'pwm_dir':
			parent.output_type = '1'
		elif spindle_type == 'up_down':
			parent.output_type = '2'
		elif spindle_type == 'pdm_dir':
			parent.output_type = '3'
		elif spindle_type == 'dir_pwm':
			parent.output_type = '4'
		elif spindle_type == 'stepgen':
			parent.pwmFrequencySB.setEnabled(False)
			parent.spindleMinRpm.setEnabled(True)
			parent.spindleMaxRpm.setEnabled(True)
			parent.spindle_feedback_gb.setEnabled(True)
			parent.spindle_pid_gb.setEnabled(True)
			parent.spindle_stepgen_gb.setEnabled(True)
	else: # disable everything
		parent.output_type = ''
		parent.pwmFrequencySB.setEnabled(False)
		parent.spindleMinRpmFwd.setEnabled(False)
		parent.spindleMinRpmRev.setEnabled(False)
		parent.spindleMaxRpmFwd.setEnabled(False)
		parent.spindleMaxRpmRev.setEnabled(False)
		parent.spindle_stepgen_gb.setEnabled(False)
		parent.spindle_feedback_gb.setEnabled(False)
		parent.spindle_pid_gb.setEnabled(False)

def spindle_pwm_changed(parent):
	if parent.sender().currentData():
		parent.spindle_feedback_gb.setEnabled(True)
		parent.spindle_pid_gb.setEnabled(True)
	else: # disable everything
		parent.spindle_feedback_gb.setEnabled(False)
		parent.spindle_pid_gb.setEnabled(False)

def spindleSettingsChanged(parent):
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



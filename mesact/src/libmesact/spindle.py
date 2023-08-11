from libmesact import dialogs

def spindle_pid_default(parent):
	if parent.spindleMaxRpm.value() <= parent.spindleMinRpm.value():
		msg = ('Spindle Maximum RPM must be higher\n'
		'than Spindle Minimum RPM')
		dialogs.errorMsgOk(parent, msg, 'Configuration Error!')
		return
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

def spindle_type_changed(parent):
	if parent.sender().currentData():
		spindle_type = parent.sender().currentData()
		if spindle_type == 'on_off':
			parent.pwmFrequencySB.setEnabled(False)
			parent.spindleMinRpm.setEnabled(True)
			parent.spindleMaxRpm.setEnabled(True)
			parent.spindle_feedback_gb.setEnabled(False)
			parent.spindle_pid_gb.setEnabled(False)
			parent.spindle_stepgen_gb.setEnabled(False)
		elif spindle_type == 'fwd_rev':
			parent.pwmFrequencySB.setEnabled(False)
			parent.spindleMinRpm.setEnabled(True)
			parent.spindleMaxRpm.setEnabled(True)
			parent.spindle_feedback_gb.setEnabled(False)
			parent.spindle_pid_gb.setEnabled(False)
			parent.spindle_stepgen_gb.setEnabled(False)
		elif spindle_type == 'pwm':
			parent.pwmFrequencySB.setEnabled(True)
			parent.spindleMinRpm.setEnabled(True)
			parent.spindleMaxRpm.setEnabled(True)
			parent.spindle_feedback_gb.setEnabled(True)
			parent.spindle_pid_gb.setEnabled(True)
			parent.spindle_stepgen_gb.setEnabled(False)
		elif spindle_type == 'stepgen':
			parent.pwmFrequencySB.setEnabled(False)
			parent.spindleMinRpm.setEnabled(True)
			parent.spindleMaxRpm.setEnabled(True)
			parent.spindle_feedback_gb.setEnabled(False)
			parent.spindle_pid_gb.setEnabled(False)
			parent.spindle_stepgen_gb.setEnabled(True)
	else: # disable everything
		parent.pwmFrequencySB.setEnabled(False)
		parent.spindleMinRpm.setEnabled(False)
		parent.spindleMaxRpm.setEnabled(False)
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




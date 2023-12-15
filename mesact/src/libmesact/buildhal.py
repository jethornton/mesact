import os, traceback
from datetime import datetime

def build(parent):
	board = parent.boardCB.currentData()
	aliasdict = {'7i92t': '7i92', '7i95t': '7i95'}
	if board in aliasdict:
		board = aliasdict[board]

	if parent.daughterCB_0.currentData():
		daughter_card = parent.daughterCB_0.currentData()
		if daughter_card == '7i77':
			port = '4'
		else:
			port = '3'
	elif parent.daughterCB_1.currentData():
		daughter_card = parent.daughterCB_1.currentData()
		port = '1'
	else:
		daughter_card = ''

	halFilePath = os.path.join(parent.configPath, 'main' + '.hal')
	parent.info_pte.appendPlainText(f'Building {halFilePath}')

	halContents = []
	halContents = ['# This file was created with the Mesa Configuration Tool on ']
	halContents.append(datetime.now().strftime('%b %d %Y %H:%M:%S') + '\n')
	halContents.append('# If you make changes to this file DO NOT run the configuration tool again!\n')
	halContents.append('# This file will be replaced with a new file if you do!\n\n')

	# build the standard header
	halContents.append('# kinematics\n')
	halContents.append('loadrt [KINS](KINEMATICS)\n\n')

	halContents.append('# motion controller\n')
	halContents.append('loadrt [EMCMOT](EMCMOT) ')
	halContents.append('servo_period_nsec=[EMCMOT](SERVO_PERIOD) ')
	halContents.append('num_joints=[KINS](JOINTS)\n\n')

	halContents.append('# hostmot2 driver\n')
	halContents.append('loadrt hostmot2\n')

	halContents.append('loadrt [HM2](DRIVER) ')
	if parent.boardType == 'eth':
		halContents.append('board_ip=[HM2](ADDRESS) ')

	encoders = parent.encoders_cb.currentData()
	pwmgens = parent.pwmgens_cb.currentData()
	stepgens = parent.stepgens_cb.currentData()
	halContents.append('config="')
	if encoders > 0:
		halContents.append(f'num_encoders={encoders} ')
	if pwmgens > 0:
		halContents.append(f'num_pwmgens={pwmgens} ')
	if stepgens > 0:
		halContents.append(f'num_stepgens={stepgens} ')

	if parent.firmwareCB.currentData(): # get smarter later for now just add all channels
		halContents.append('sserial_port_0=00000000"\n')
		'''
		max_channels = int(max(parent.p1_channels + parent.p2_channels))
		channels = ''
		for i in range(8):
			if i <= max_channels:
				channels += '0'
			else:
				channels += 'x'
		halContents.append(f'sserial_port_0={channels}"\n')
		'''
	else:
		halContents.append('sserial_port_0=00000000"\n')

	halContents.append(f'\nsetp hm2_[MESA](BOARD).0.watchdog.timeout_ns {parent.servoPeriodSB.value() * 5}\n')

	# loadrt pids
	pid_count = 0
	pid_string = ''
	for axis in parent.coordinatesLB.text():
		if parent.coordinatesLB.text().count(axis) == 1:
			pid_string += f'pid.{axis.lower()},'
		elif parent.coordinatesLB.text().count(axis) > 1:
			pid_string += f'pid.{axis.lower()}{pid_count},'
			pid_count += 1
	if parent.spindleTypeCB.currentData() == 'pwm':
		pid_string += f'pid.s,'
	halContents.append(f'\nloadrt pid names={pid_string[:-1]}\n')

	halContents.append('\n# THREADS\n')
	halContents.append(f'addf hm2_[MESA](BOARD).0.read servo-thread\n')
	halContents.append('addf motion-command-handler servo-thread\n')
	halContents.append('addf motion-controller servo-thread\n')

	pid_list = pid_string[:-1].split(',')
	for pid in pid_list:
		halContents.append(f'addf {pid}.do-pid-calcs servo-thread\n')
	halContents.append(f'addf hm2_[MESA](BOARD).0.write servo-thread\n')

	dpll = {'7i96':['stepgen', 'encoder'],
		'7i96s':['stepgen', 'encoder'],}
	stepgen_timer = ['7i76e', '7i95', '7i95t', '7i96', '7i96s']

	if parent.boardType == 'eth':
		halContents.append('\n# DPLL TIMER\n')
		halContents.append(f'setp hm2_[MESA](BOARD).0.dpll.01.timer-us -50\n')
		if board in stepgen_timer or daughter_card == '7i76':
			halContents.append(f'setp hm2_[MESA](BOARD).0.stepgen.timer-number 1\n')

		if encoders > 0:
			halContents.append(f'setp hm2_[MESA](BOARD).0.encoder.timer-number 1\n')

	# add special hal functions
	if parent.spindleMinRpmFwd.value() > 0: # use limit1
		halContents.append('\n# Setup Spindle Limits\n')
		halContents.append('loadrt limit1 names=spindle-limit\n')
		halContents.append('addf spindle-limit servo-thread\n')
		halContents.append(f'setp spindle-limit.min [SPINDLE_0](MIN_RPM)\n')
		halContents.append(f'setp spindle-limit.max [SPINDLE_0](MAX_RPM)\n')

	# finger out where the analog daughter_card is and which one...
	# P2 hm2_5i25.0.7i77.0.4.analogena

	analog_cards = ['7i77', '7i97']

	if daughter_card in analog_cards: # analog
		halContents.append('\n# amp enable\n')
		halContents.append(f'net motion-enable <= motion.motion-enabled\n')
		halContents.append(f'net motion-enable => hm2_[MESA](BOARD).0.{daughter_card}.0.{port}.analogena\n')

	# figure out which daughter_card each joint is on...
	joint_list = []
	for i in range(3):
		for j in range(6):
			if getattr(parent, f'c{i}_axis_{j}').currentData():
				joint_list.append(f'c{i}_axis_{j}')
	joints = len(parent.coordinatesLB.text())
	axes = parent.coordinatesLB.text()

	for i in range(joints): # Fix Me if two daughter cards we crash!
		halContents.append(f'\n# Joint {i} Axis {axes[i]}\n')
		halContents.append(f'# PID Setup\n')
		halContents.append(f'setp {pid_list[i]}.Pgain [JOINT_{i}](P)\n')
		halContents.append(f'setp {pid_list[i]}.Igain [JOINT_{i}](I)\n')
		halContents.append(f'setp {pid_list[i]}.Dgain [JOINT_{i}](D)\n')
		halContents.append(f'setp {pid_list[i]}.bias [JOINT_{i}](BIAS)\n')
		halContents.append(f'setp {pid_list[i]}.FF0 [JOINT_{i}](FF0)\n')
		halContents.append(f'setp {pid_list[i]}.FF1 [JOINT_{i}](FF1)\n')
		halContents.append(f'setp {pid_list[i]}.FF2 [JOINT_{i}](FF2)\n')
		halContents.append(f'setp {pid_list[i]}.deadband [JOINT_{i}](DEADBAND)\n')
		halContents.append(f'setp {pid_list[i]}.maxoutput [JOINT_{i}](MAX_OUTPUT)\n')
		if daughter_card not in analog_cards: # analog
			halContents.append(f'setp {pid_list[i]}.maxerror [JOINT_{i}](MAX_ERROR)\n')
		halContents.append(f'setp {pid_list[i]}.error-previous-target true\n')

		halContents.append(f'\n# joint-{i} enable chain\n')
		halContents.append(f'net joint-{i}-index-enable <=> {pid_list[i]}.index-enable\n')
		halContents.append(f'net joint-{i}-index-enable <=> joint.{i}.index-enable\n')
		if daughter_card in analog_cards: # analog
			halContents.append(f'net joint-{i}-index-enable <=> hm2_[MESA](BOARD).0.encoder.0{i}.index-enable\n')

		halContents.append(f'\nnet joint-{i}-enable <= joint.{i}.amp-enable-out\n')
		halContents.append(f'net joint-{i}-enable => {pid_list[i]}.enable\n')

		if getattr(parent, f'c{joint_list[i][1]}_settings_{i}').isTabVisible(2): # stepper
			if getattr(parent, f'c{joint_list[i][1]}_StepInvert_{i}').isChecked():
				halContents.append(f'setp hm2_[MESA](BOARD).0.stepgen.0{i}.step.invert_output True\n')
			if getattr(parent, f'c{joint_list[i][1]}_DirInvert_{i}').isChecked():
				halContents.append(f'setp hm2_[MESA](BOARD).0.stepgen.0{i}.direction.invert_output True\n')

			halContents.append(f'\nnet joint-{i}-enable => hm2_[MESA](BOARD).0.stepgen.0{i}.enable\n')

			halContents.append(f'\n# Joint {i} Step Generator Settings\n')
			halContents.append(f'setp hm2_[MESA](BOARD).0.stepgen.0{i}.dirsetup [JOINT_{i}](DIRSETUP)\n')
			halContents.append(f'setp hm2_[MESA](BOARD).0.stepgen.0{i}.dirhold [JOINT_{i}](DIRHOLD)\n')
			halContents.append(f'setp hm2_[MESA](BOARD).0.stepgen.0{i}.steplen [JOINT_{i}](STEPLEN)\n')
			halContents.append(f'setp hm2_[MESA](BOARD).0.stepgen.0{i}.stepspace [JOINT_{i}](STEPSPACE)\n')
			halContents.append(f'setp hm2_[MESA](BOARD).0.stepgen.0{i}.position-scale [JOINT_{i}](SCALE)\n')
			halContents.append(f'setp hm2_[MESA](BOARD).0.stepgen.0{i}.maxvel [JOINT_{i}](STEPGEN_MAX_VEL)\n')
			halContents.append(f'setp hm2_[MESA](BOARD).0.stepgen.0{i}.maxaccel [JOINT_{i}](STEPGEN_MAX_ACC)\n')
			halContents.append(f'setp hm2_[MESA](BOARD).0.stepgen.0{i}.step_type 0\n')
			halContents.append(f'setp hm2_[MESA](BOARD).0.stepgen.0{i}.control-type 1\n\n')


		halContents.append('\n# position command and feedback\n')
		halContents.append(f'net joint-{i}-pos-cmd <= joint.{i}.motor-pos-cmd\n')
		halContents.append(f'net joint-{i}-pos-cmd => {pid_list[i]}.command\n')

		# no encoder feedback
		if getattr(parent, f'c{joint_list[i][1]}_settings_{i}').isTabVisible(3): # analog
			halContents.append(f'\nnet joint-{i}-pos-fb <= hm2_[MESA](BOARD).0.encoder.0{i}.position\n')
		else:
			halContents.append(f'\nnet joint-{i}-pos-fb <= hm2_[MESA](BOARD).0.stepgen.0{i}.position-fb\n')
		halContents.append(f'net joint-{i}-pos-fb => joint.{i}.motor-pos-fb\n')
		halContents.append(f'net joint-{i}-pos-fb => {pid_list[i]}.feedback\n')

		halContents.append(f'\nnet joint.{i}.output <= {pid_list[i]}.output\n')
		if getattr(parent, f'c{joint_list[i][1]}_settings_{i}').isTabVisible(3): # analog
			halContents.append(f'net joint.{i}.output => hm2_[MESA](BOARD).0.{daughter_card}.0.{port}.analogout{i}\n')
		else:
			halContents.append(f'net joint.{i}.output => hm2_[MESA](BOARD).0.stepgen.0{i}.velocity-cmd\n')

		if getattr(parent, f'c{joint_list[i][1]}_settings_{i}').isTabVisible(3): # analog
			halContents.append(f'\n# Joint {i} Analog setup\n')
			halContents.append(f'setp hm2_[MESA](BOARD).0.{daughter_card}.0.{port}.analogout{i}-scalemax [JOINT_{i}](ANALOG_SCALE_MAX)\n')
			halContents.append(f'setp hm2_[MESA](BOARD).0.{daughter_card}.0.{port}.analogout{i}-minlim [JOINT_{i}](ANALOG_MIN_LIMIT)\n')
			halContents.append(f'setp hm2_[MESA](BOARD).0.{daughter_card}.0.{port}.analogout{i}-maxlim [JOINT_{i}](ANALOG_MAX_LIMIT)\n\n')


		if getattr(parent, f'c{joint_list[i][1]}_settings_{i}').isTabVisible(4): # encoder
			if getattr(parent, f'c{joint_list[i][1]}_encoderScale_{i}').text():
				halContents.append('\n# Encoder Setup\n')
				halContents.append(f'setp hm2_[MESA](BOARD).0.encoder.0{i}.scale  [JOINT_0](ENCODER_SCALE)\n')
				halContents.append(f'setp hm2_[MESA](BOARD).0.encoder.0{i}.counter-mode 0\n')
				halContents.append(f'setp hm2_[MESA](BOARD).0.encoder.0{i}.filter 1\n')
				halContents.append(f'setp hm2_[MESA](BOARD).0.encoder.0{i}.index-invert 0\n')
				halContents.append(f'setp hm2_[MESA](BOARD).0.encoder.0{i}.index-mask 0\n')
				halContents.append(f'setp hm2_[MESA](BOARD).0.encoder.0{i}.index-mask-invert 0\n')

	'''
			halContents.append('\n# Position Feedback\n')
			halContents.append(f'net joint-{i}-fb {pid_list[i]}.feedback <= hm2_[MESA](BOARD).0.encoder.0{i}.position\n')

			halContents.append('\n')

			net x-axis-enable pid.0.enable <= axis.0.amp-enable-out
			net x-axis-enable hm2_5i25.0.7i77.0.1.analogena
			net x-axis-fb pid.0.feedback <= hm2_5i25.0.encoder.00.position
			net x-axis-fb axis.0.motor-pos-fb
			net x-axis-pos-cmd axis.0.motor-pos-cmd => pid.0.command
			net x-axis-command  pid.0.output  =>  hm2_5i25.0.7i77.0.1.analogout0

			halContents.append('\n# Position Command and Feedback\n')
			halContents.append(f'net joint-{i}-fb <= hm2_[MESA](BOARD).0.encoder.0{i}.position\n')
			halContents.append(f'net joint-{i}-output => hm2_[MESA](BOARD).0.{card}.0.{port}.analogout{i}\n')
			halContents.append(f'net joint-{i}-pos-cmd <= joint.{i}.motor-pos-cmd\n')




	#mainboards = ['5i25', '7i80hd', '7i80db', '7i92', '7i93', '7i98']
	if parent.daughterCB_0.currentData():
		card = parent.daughterCB_0.currentData()
	elif parent.daughterCB_1.currentData():
		card = parent.daughterCB_1.currentData()
	#else:
	#	card = parent.boardCB.currentData()

	#card = parent.cardCB.currentText()
	#port = parent.analogPort

	# check for extra motion options
	#parent.numDioSB
	#parent.numAioSB
	#parent.numSpindlesSB
	#parent.numJointSB
	#parent.numExtraJointsSB
	if parent.spindleTypeCB.currentData():
		pids = len(parent.coordinatesLB.text()) + 1
	else:
		pids = len(parent.coordinatesLB.text())
	halContents.append(f'loadrt pid num_chan={pids} \n\n')

	config = False
	if parent.stepgensCB.currentData():
		config = True
	elif parent.pwmgensCB.currentData():
		config = True
	elif parent.encodersCB.currentData():
		config = True
	if config:
		halContents.append('config="')
	if parent.stepgensCB.currentData():
		halContents.append('num_stepgens=[HM2](STEPGENS)')
	if parent.encodersCB.currentData():
		if parent.stepgensCB.currentData():
			halContents.append(' ')
		halContents.append('num_encoders=[HM2](ENCODERS)')
	if parent.pwmgensCB.currentData():
		if parent.stepgensCB.currentData() or parent.encodersCB.currentData():
			halContents.append(' ')
		halContents.append('num_pwmgens=[HM2](PWMGENS)')
	if config:
		halContents.append('"\n')


	# loadrt [HM2](DRIVER) config="num_encoders=1 num_pwmgens=0 num_stepgens=5 sserial_port_0=00xxxx"
	#halContents.append('loadrt [HM2](DRIVER) ')



	for i in range(pids):
		halContents.append(f'addf pid.{i}.do-pid-calcs servo-thread\n')

	#print(f'board {parent.board}')
		if board == '7i92' and card:
			if card == '7i76':
				halContents.append(f'setp hm2_[MESA](BOARD).0.stepgen.timer-number 1\n')
				halContents.append(f'setp hm2_[MESA](BOARD).0.encoder.timer-number 1\n')
			elif card == '7i77':
				halContents.append(f'setp hm2_[MESA](BOARD).0.stepgen.timer-number 1\n')
				halContents.append(f'setp hm2_[MESA](BOARD).0.encoder.timer-number 1\n')

	if parent.daughterCB_0.currentData():
		port = '0'
	elif parent.daughterCB_0.currentData():
		port = '1'



		# getattr(parent, f'inputPB_{i}').setEnabled(True)
		if parent.cardType_0 == 'step' or parent.cardType_1 == 'step':
			if parent.daughterCB_0.currentData():
				port = '0'
			elif parent.daughterCB_1.currentData():
				port = '1'
			else:
				port = '0'



		#if parent.board in mainboards:
		#	card = parent.board
		if parent.cardType_0 == 'servo' or parent.cardType_1 == 'servo':
			if parent.cardType_0: port = '1'
			elif parent.cardType_1: port = '0'

			if board == '7i97':
				halContents.append(f'net joint-{i}-enable => hm2_[MESA](BOARD).0.pwmgen.0{i}.enable\n')

				halContents.append('\n# position command and feedback\n')
				halContents.append(f'net joint-{i}-pos-cmd => pid.{i}.command\n')
				halContents.append(f'net joint-{i}-pos-fb => pid.{i}.feedback\n')
				halContents.append(f'net joint-{i}-output <= pid.{i}.output\n')

				halContents.append('\n# PWM setup\n')
				halContents.append(f'setp hm2_[MESA](BOARD).0.pwmgen.0{i}.output-type 1 #PWM pin0\n')
				halContents.append(f'setp hm2_[MESA](BOARD).0.pwmgen.0{i}.offset-mode 1 # offset mode so 50% = 0\n')
				halContents.append(f'setp hm2_[MESA](BOARD).0.pwmgen.0{i}.scale [JOINT_{i}]SCALE\n')

				halContents.append('\n# Encoder Setup\n')
				halContents.append(f'setp hm2_[MESA](BOARD).0.encoder.0{i}.scale  [JOINT_{i}](ENCODER_SCALE)\n')
				halContents.append(f'setp hm2_[MESA](BOARD).0.encoder.0{i}.counter-mode 0\n')
				halContents.append(f'setp hm2_[MESA](BOARD).0.encoder.0{i}.filter 1\n')
				halContents.append(f'setp hm2_[MESA](BOARD).0.encoder.0{i}.index-invert 0\n')
				halContents.append(f'setp hm2_[MESA](BOARD).0.encoder.0{i}.index-mask 0\n')
				halContents.append(f'setp hm2_[MESA](BOARD).0.encoder.0{i}.index-mask-invert 0\n')

				halContents.append('\n# Position Command and Feedback\n')
				halContents.append(f'net joint-{i}-fb <= hm2_[MESA](BOARD).0.encoder.0{i}.position\n')
				halContents.append(f'net joint-{i}-pos-cmd <= joint.{i}.motor-pos-cmd\n')

			else:

				# halContents.append(f'\n')

	if parent.spindleTypeCB.currentData():
		halContents.append('\n# Spindle\n')
		halContents.append('\n# Spindle Velocity Pins\n')
		halContents.append('net spindle-vel-cmd-rps <=  spindle.0.speed-out-rps\n')
		halContents.append('net spindle-vel-cmd-rps-abs <= spindle.0.speed-out-rps-abs\n')
		halContents.append('net spindle-vel-cmd-rpm <= spindle.0.speed-out\n')
		halContents.append('net spindle-vel-cmd-rpm-abs <= spindle.0.speed-out-abs\n')
		halContents.append('\n# Spindle Command Pins\n')
		halContents.append('net spindle-cw <= spindle.0.forward\n')
		halContents.append('net spindle-ccw <= spindle.0.reverse\n')
		halContents.append('net spindle-brake <= spindle.0.brake\n')
		halContents.append('net spindle-revs => spindle.0.revs\n')
		halContents.append('net spindle-at-speed => spindle.0.at-speed\n')
		halContents.append('net spindle-vel-fb-rps => spindle.0.speed-in\n')
		halContents.append('net spindle-index-enable => spindle.0.index-enable\n')
		halContents.append('\n# Set spindle at speed signal\n')
		if not parent.spindleFeedbackCB.currentData():
			halContents.append('sets spindle-at-speed true\n')
	'''

	if parent.spindleTypeCB.currentData() == 'pwm':
		halContents.append('\n# Spindle PID Setup\n')
		halContents.append(f'setp pid.s.Pgain [SPINDLE_0](P)\n')
		halContents.append(f'setp pid.s.Igain [SPINDLE_0](I)\n')
		halContents.append(f'setp pid.s.Dgain [SPINDLE_0](D)\n')
		halContents.append(f'setp pid.s.bias [SPINDLE_0](BIAS)\n')
		halContents.append(f'setp pid.s.FF0 [SPINDLE_0](FF0)\n')
		halContents.append(f'setp pid.s.FF1 [SPINDLE_0](FF1)\n')
		halContents.append(f'setp pid.s.FF2 [SPINDLE_0](FF2)\n')
		halContents.append(f'setp pid.s.deadband [SPINDLE_0](DEADBAND)\n')
		halContents.append(f'setp pid.s.maxoutput [SPINDLE_0](MAX_OUTPUT)\n')
		halContents.append(f'setp pid.s.error-previous-target true\n')

		halContents.append('\n# Spindle PWM Setup\n')
		halContents.append(f'setp hm2_[MESA](BOARD).0.pwmgen.00.output-type [SPINDLE_0](PWM_TYPE)\n')
		halContents.append(f'setp hm2_[MESA](BOARD).0.pwmgen.pwm_frequency [SPINDLE_0](PWM_FREQUENCY)\n')
		halContents.append(f'setp hm2_[MESA](BOARD).0.pwmgen.00.scale [SPINDLE_0]SCALE\n')

		halContents.append('\n# Spindle Enable\n')
		halContents.append('net spindle-on <= spindle.0.on\n')
		halContents.append('net spindle-on => pid.s.enable\n')
		halContents.append(f'net spindle-on => hm2_[MESA](BOARD).0.pwmgen.00.enable\n')


		halContents.append('\n# Spindle Connections\n')
		halContents.append('net spindle-vel-cmd <= spindle.0.speed-out-abs\n')
		if parent.spindleMinRpmFwd.value() > 0: # use limit1
			halContents.append('net spindle-vel-cmd => spindle-limit.in\n')
			halContents.append('net spindle-limit-cmd <= spindle-limit.out\n')
			halContents.append('net spindle-limit-cmd => pid.s.command\n')
		else:
			halContents.append('net spindle-vel-cmd => pid.s.command\n')
		halContents.append('net spindle-pid-out <= pid.s.output\n')
		halContents.append('net spindle-pid-out => hm2_[MESA](BOARD).0.pwmgen.00.value\n')

		# for encoder feedback spindle at speed should use encoder speed
		halContents.append('\n# Spindle Feedback\n')
		halContents.append('setp spindle.0.at-speed true\n')

	'''
		if parent.spindleTypeCB.currentData()[:7] == 'stepgen':
			s = parent.spindleTypeCB.currentData()[-1]
			halContents.append(f'\nnet spindle-on hm2_[MESA](BOARD).0.stepgen.0{s}.enable\n')
			halContents.append(f'setp hm2_[MESA](BOARD).0.stepgen.0{s}.dirsetup [SPINDLE_0](DIRSETUP)\n')
			halContents.append(f'setp hm2_[MESA](BOARD).0.stepgen.0{s}.dirhold [SPINDLE_0](DIRHOLD)\n')
			halContents.append(f'setp hm2_[MESA](BOARD).0.stepgen.0{s}.steplen [SPINDLE_0](STEPLEN)\n')
			halContents.append(f'setp hm2_[MESA](BOARD).0.stepgen.0{s}.stepspace [SPINDLE_0](STEPSPACE)\n')
			halContents.append(f'setp hm2_[MESA](BOARD).0.stepgen.0{s}.position-scale [SPINDLE_0](SCALE)\n')
			halContents.append(f'setp hm2_[MESA](BOARD).0.stepgen.0{s}.position-scale [SPINDLE_0](SCALE)\n')
			halContents.append(f'setp hm2_[MESA](BOARD).0.stepgen.0{s}.maxvel [SPINDLE_0](MAX_RPS)\n')
			halContents.append(f'setp hm2_[MESA](BOARD).0.stepgen.0{s}.maxaccel [SPINDLE_0](MAX_ACCEL_RPS)\n')

			# need to set scale and other stuff first
			halContents.append(f'setp hm2_[MESA](BOARD).0.stepgen.0{s}.control-type 1\n\n')
			halContents.append(f'net spindle-vel-cmd-rps =>  hm2_[MESA](BOARD).0.stepgen.0{s}.velocity-cmd\n')

			# net s-output <= spindle.0.speed−out
			# hm2_7i96s.0.stepgen.04.velocity-cmd

	if parent.spindleFeedbackCB.currentData() == 'encoder':
		encoder00 = ['7i96', '7i96s']
		if board in encoder00:
			s = pids - 1

			halContents.append('# Encoder Setup\n')
			halContents.append(f'setp hm2_[MESA](BOARD).0.encoder.00.counter-mode 0\n')
			halContents.append(f'setp hm2_[MESA](BOARD).0.encoder.00.filter 1\n')
			halContents.append(f'setp hm2_[MESA](BOARD).0.encoder.00.index-invert 0\n')
			halContents.append(f'setp hm2_[MESA](BOARD).0.encoder.00.index-mask 0\n')
			halContents.append(f'setp hm2_[MESA](BOARD).0.encoder.00.index-mask-invert 0\n')
			halContents.append(f'setp hm2_[MESA](BOARD).0.encoder.00.scale [SPINDLE_0](ENCODER_SCALE)\n')

			halContents.append(f'\nnet spindle-index-enable <=> pid.{s}.index-enable\n')
			halContents.append(f'net spindle-index-enable <=> hm2_[MESA](BOARD).0.encoder.00.index-enable\n')
			halContents.append('net spindle-index-enable <=> spindle.0.index-enable\n')

			halContents.append(f'\nnet spindle-vel-cmd-rpm => pid.{s}.command\n')
			halContents.append(f'net spindle-vel-cmd-rpm <= spindle.0.speed-out\n')

			halContents.append(f'\nnet spindle-vel-fb-rpm => pid.{s}.feedback\n')
			halContents.append(f'net spindle-vel-fb-rpm <= hm2_[MESA](BOARD).0.encoder.00.velocity-rpm\n')

			#halContents.append(f'\nnet spindle-output <= pid.{s}.output\n')

			halContents.append(f'\nnet spindle-enable => pid.{s}.enable\n')

	'''


	externalEstop = False
	for i in range(3): # test for an external e stop input
		for j in range(16):
			key = getattr(parent, f'c{i}_input_{j}').text()
			if key[0:6] == 'E Stop':
				externalEstop = True
	if not externalEstop:
		halContents.append('\n# Standard I/O Block - EStop, Etc\n')
		halContents.append('# create a signal for the estop loopback\n')
		halContents.append('net estop-loopback iocontrol.0.emc-enable-in <= iocontrol.0.user-enable-out\n')

	if parent.manualToolChangeCB.isChecked():
		halContents.append('\n#  Manual Tool Change Dialog\n')

		halContents.append('loadusr -W hal_manualtoolchange\n')
		halContents.append('net tool-change-request    =>  hal_manualtoolchange.change\n')
		halContents.append('net tool-change-confirmed  <=  hal_manualtoolchange.changed\n')
		halContents.append('net tool-number            =>  hal_manualtoolchange.number\n')

		halContents.append('\n# create signals for tool loading loopback\n')
		halContents.append('net tool-prep-loop iocontrol.0.tool-prepare => iocontrol.0.tool-prepared\n')
		halContents.append('net tool-change-loop iocontrol.0.tool-change => iocontrol.0.tool-changed\n')

	if parent.ladderGB.isChecked():
		halContents.append('\n# # Load Classicladder without GUI\n')
		# this line needs to be built from the options if any are above 0
		ladderOptions = []
		for option in parent.ladderOptionsList:
			if getattr(parent, option).value() > 0:
				ladderOptions.append(getattr(parent, option).property('option') + '=' + str(getattr(parent, option).value()))
		if ladderOptions:
				halContents.append(f'loadrt classicladder_rt {" ".join(ladderOptions)}\n')
		else:
			halContents.append('loadrt classicladder_rt\n')
		halContents.append('addf classicladder.0.refresh servo-thread 1\n')

	try:
		with open(halFilePath, 'w') as halFile:
			halFile.writelines(halContents)
	except OSError:
		parent.info_pte.appendPlainText(f'OS error\n {traceback.print_exc()}')

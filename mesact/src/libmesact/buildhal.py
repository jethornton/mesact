import os, traceback
from datetime import datetime

def build(parent):
	board_list = []
	for card in range(3):
		board_list.append(getattr(parent, f'board_{card}'))

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

	encoders = parent.encoders_cb.currentData() or False
	pwmgens = parent.pwmgens_cb.currentData() or False
	stepgens = parent.stepgens_cb.currentData() or False
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

	step_boards  = ['7i76', '7i76e', '7i78', '7i95', '7i95t', '7i96', '7i96s']
	analog_boards = ['7i77', '7i97', '7i97t']
	pwmgen_boards = ['7i97', '7i97t']

	if parent.boardCB.currentData() in step_boards:
		halContents.append('\n# PID Information for Stepper Boards\n')
		halContents.append('# Mesa hardware step generators at every servo thread invocation, the step\n')
		halContents.append('# generator hardware is given a new velocity. Without feedback from the PID\n')
		halContents.append('# controller the hardware position would slowly drift because of clock speed and\n')
		halContents.append('# timing differences between LinuxCNC and the step generator hardware.\n')
		halContents.append('# The PID controller gets feedback from the actual (fractional) step position and\n')
		halContents.append('# corrects for these small differences.\n')

	halContents.append('\n# THREADS\n')
	halContents.append(f'addf hm2_[MESA](BOARD).0.read servo-thread\n')
	halContents.append('addf motion-command-handler servo-thread\n')
	halContents.append('addf motion-controller servo-thread\n')

	pid_list = pid_string[:-1].split(',')
	for pid in pid_list:
		halContents.append(f'addf {pid}.do-pid-calcs servo-thread\n')
	halContents.append(f'addf hm2_[MESA](BOARD).0.write servo-thread\n')


	if len(set(board_list) & set(step_boards)) > 0:
		halContents.append('\n# DPLL TIMER\n')
		halContents.append(f'setp hm2_[MESA](BOARD).0.dpll.01.timer-us -50\n')
		halContents.append(f'setp hm2_[MESA](BOARD).0.stepgen.timer-number 1\n')


	''' this needs fixin
	dpll = {'7i96':['stepgen', 'encoder'],
		'7i96s':['stepgen', 'encoder'],}
	stepgen_timer = ['7i76e', '7i95', '7i95t', '7i96', '7i96s']

	if parent.boardType == 'eth':

		if encoders > 0:
			halContents.append(f'setp hm2_[MESA](BOARD).0.encoder.timer-number 1\n')
			
		Get encoders working, scaled right and in the right directions
		Get drive enables controlled by linuxcnc
		Set per axis following error limits wide enough to allow tuning (say 1 inch or 20 mm)
		Verify feedback direction (expect runaways) you may have to change the sign of the analog outputs
	'''

	halContents.append('\n# amp enable\n')
	halContents.append(f'net motion-enable <= motion.motion-enabled\n')
	if board_list[2] == '7i77':
		halContents.append(f'net motion-enable => hm2_[MESA](BOARD).0.7i77.0.1.analogena\n')

	if parent.boardCB.currentData() == '7i97':
		#print(parent.boardCB.currentData())
		pwm_freq = 48000
	elif parent.boardCB.currentData() == '7i97t':
		#print(parent.boardCB.currentData())
		pwm_freq = 75000
	if parent.hal_name == '7i97':
		halContents.append('\n# Global PWM setup\n')
		halContents.append(f'setp hm2_[MESA](BOARD).0.pwmgen.pwm_frequency {pwm_freq}\n')

	# Joints and Axes
	joint = 0
	# analog ports are for 7i77 daughter cards only 7i97 is different
	# FIXME this is not correct for a 7i96s + 7i77
	analog_port = {'5i25': {1: 4, 2: 1}, '7i92': {1: 4, 2: 1}, '7i96s': {1: 1}}
	#analog_port = {1: 4, 2:1} # analog port dictonary usage analog_port[card]
	for card in range(3):
		board = getattr(parent, f'board_{card}')
		if board:
			halContents.append(f'\n# Board: {board}\n')
			for output in range(6):
				if getattr(parent, f'c{card}_axis_{output}').currentData():
					axis = getattr(parent, f"c{card}_axis_{output}").currentData()
					halContents.append(f'\n# Axis: {axis} Joint: {joint} Output: {output}\n')
					halContents.append(f'# PID Setup\n')
					halContents.append(f'setp {pid_list[joint]}.Pgain [JOINT_{joint}](P)\n')
					halContents.append(f'setp {pid_list[joint]}.Igain [JOINT_{joint}](I)\n')
					halContents.append(f'setp {pid_list[joint]}.Dgain [JOINT_{joint}](D)\n')
					halContents.append(f'setp {pid_list[joint]}.bias [JOINT_{joint}](BIAS)\n')
					halContents.append(f'setp {pid_list[joint]}.FF0 [JOINT_{joint}](FF0)\n')
					halContents.append(f'setp {pid_list[joint]}.FF1 [JOINT_{joint}](FF1)\n')
					halContents.append(f'setp {pid_list[joint]}.FF2 [JOINT_{joint}](FF2)\n')
					halContents.append(f'setp {pid_list[joint]}.deadband [JOINT_{joint}](DEADBAND)\n')
					halContents.append(f'setp {pid_list[joint]}.maxoutput [JOINT_{joint}](MAX_OUTPUT)\n')
					halContents.append(f'setp {pid_list[joint]}.error-previous-target True\n')

					if board in step_boards: # stepper
						halContents.append('# limit stepgen velocity corrections caused by position feedback jitter\n')
						halContents.append(f'setp {pid_list[joint]}.maxerror [JOINT_{joint}](MAX_ERROR)\n')

					halContents.append(f'\n# joint-{joint} enable chain\n')
					halContents.append(f'net joint-{joint}-index-enable <=> {pid_list[joint]}.index-enable\n')
					halContents.append(f'net joint-{joint}-index-enable <=> joint.{joint}.index-enable\n')

					if board in analog_boards: # analog
						halContents.append(f'net joint-{joint}-index-enable <=> hm2_[MESA](BOARD).0.encoder.0{joint}.index-enable\n')

					halContents.append(f'\nnet joint-{joint}-enable <= joint.{joint}.amp-enable-out\n')
					halContents.append(f'net joint-{joint}-enable => {pid_list[joint]}.enable\n')
					if parent.hal_name in pwmgen_boards:
						halContents.append(f'net joint-{joint}-enable => hm2_[MESA](BOARD).0.pwmgen.0{joint}.enable\n')

					if board in step_boards: # stepper c0_StepInvert_0
						if getattr(parent, f'c{card}_StepInvert_{output}').isChecked():
							halContents.append(f'setp hm2_[MESA](BOARD).0.stepgen.0{joint}.step.invert_output True\n')

						if getattr(parent, f'c{card}_DirInvert_{output}').isChecked():
							halContents.append(f'setp hm2_[MESA](BOARD).0.stepgen.0{joint}.direction.invert_output True\n')

						halContents.append(f'\nnet joint-{joint}-enable => hm2_[MESA](BOARD).0.stepgen.0{joint}.enable\n')
						halContents.append(f'\n# Joint {joint} Step Generator Settings\n')
						halContents.append(f'setp hm2_[MESA](BOARD).0.stepgen.0{joint}.dirsetup [JOINT_{joint}](DIRSETUP)\n')
						halContents.append(f'setp hm2_[MESA](BOARD).0.stepgen.0{joint}.dirhold [JOINT_{joint}](DIRHOLD)\n')
						halContents.append(f'setp hm2_[MESA](BOARD).0.stepgen.0{joint}.steplen [JOINT_{joint}](STEPLEN)\n')
						halContents.append(f'setp hm2_[MESA](BOARD).0.stepgen.0{joint}.stepspace [JOINT_{joint}](STEPSPACE)\n')
						halContents.append(f'setp hm2_[MESA](BOARD).0.stepgen.0{joint}.position-scale [JOINT_{joint}](SCALE)\n')
						halContents.append(f'setp hm2_[MESA](BOARD).0.stepgen.0{joint}.maxvel [JOINT_{joint}](STEPGEN_MAX_VEL)\n')
						halContents.append(f'setp hm2_[MESA](BOARD).0.stepgen.0{joint}.maxaccel [JOINT_{joint}](STEPGEN_MAX_ACC)\n')
						halContents.append(f'setp hm2_[MESA](BOARD).0.stepgen.0{joint}.step_type 0\n')
						halContents.append(f'setp hm2_[MESA](BOARD).0.stepgen.0{joint}.control-type 1\n\n')

					if parent.hal_name == '7i97':
						halContents.append('\n# PWM Generator setup\n')
						if parent.boardCB.currentData() == '7i97t':
							 halContents.append(f'setp hm2_[MESA](BOARD).0.pwmgen.0{joint}.dither true\n')
						halContents.append(f'setp hm2_[MESA](BOARD).0.pwmgen.0{output}.output-type 1 #PWM pin0\n')
						halContents.append(f'setp hm2_[MESA](BOARD).0.pwmgen.0{output}.offset-mode 1 # offset mode so 50% = 0\n')
						halContents.append(f'setp hm2_[MESA](BOARD).0.pwmgen.0{output}.scale [JOINT_0]SCALE\n')

						halContents.append('\n# ---Encoder feedback signals/setup---\n')
						halContents.append(f'setp hm2_[MESA](BOARD).0.encoder.0{output}.counter-mode 0\n')
						halContents.append(f'setp hm2_[MESA](BOARD).0.encoder.0{output}.filter 1\n')
						halContents.append(f'setp hm2_[MESA](BOARD).0.encoder.0{output}.index-invert 0\n')
						halContents.append(f'setp hm2_[MESA](BOARD).0.encoder.0{output}.index-mask 0\n')
						halContents.append(f'setp hm2_[MESA](BOARD).0.encoder.0{output}.index-mask-invert 0\n')
						halContents.append(f'setp hm2_[MESA](BOARD).0.encoder.0{output}.scale  [JOINT_0]ENCODER_SCALE\n')


					halContents.append('\n# position command and feedback\n')
					halContents.append(f'net joint-{joint}-pos-cmd <= joint.{joint}.motor-pos-cmd\n')
					halContents.append(f'net joint-{joint}-pos-cmd => {pid_list[joint]}.command\n')

					# no encoder feedback
					if board in analog_boards: # analog
						halContents.append(f'\nnet joint-{joint}-pos-fb <= hm2_[MESA](BOARD).0.encoder.0{joint}.position\n')
					else: # stepper
						halContents.append(f'\nnet joint-{joint}-pos-fb <= hm2_[MESA](BOARD).0.stepgen.0{joint}.position-fb\n')
					halContents.append(f'net joint-{joint}-pos-fb => joint.{joint}.motor-pos-fb\n')
					halContents.append(f'net joint-{joint}-pos-fb => {pid_list[joint]}.feedback\n')

					halContents.append('\n# PID Output\n')
					halContents.append(f'net joint.{joint}.output <= {pid_list[joint]}.output\n')
					if board in step_boards: # stepper
						halContents.append(f'net joint.{joint}.output => hm2_[MESA](BOARD).0.stepgen.0{joint}.velocity-cmd\n')
					# hm2_7i92.0.7i77.0.1.analogout0
					elif parent.hal_name == '7i97': # covers both 7i97 and 7i97T
						halContents.append(f'net joint.{joint}.output => hm2_[MESA](BOARD).0.pwmgen.0{output}.value\n')

					if board == '7i77': # analog daughter card setp   hm2_5i25.0.7i77.0.1.analogout0-scalemax  [JOINT_0]OUTPUT_SCALE
						port = analog_port[parent.hal_name][card]

						halContents.append(f'net joint.{joint}.output => hm2_[MESA](BOARD).0.{board}.0.{port}.analogout{joint}\n')
						halContents.append(f'\n# Joint {joint} Analog setup\n')
						halContents.append(f'setp hm2_[MESA](BOARD).0.{board}.0.{port}.analogout{joint}-scalemax')
						halContents.append(f' [JOINT_{joint}](ANALOG_SCALE_MAX)\n')
						halContents.append(f'setp hm2_[MESA](BOARD).0.{board}.0.{port}.analogout{joint}-minlim')
						halContents.append(f' [JOINT_{joint}](ANALOG_MIN_LIMIT)\n')
						halContents.append(f'setp hm2_[MESA](BOARD).0.{board}.0.{port}.analogout{joint}-maxlim')
						halContents.append(f' [JOINT_{joint}](ANALOG_MAX_LIMIT)\n\n')
						# hm2_7i92.0.7i77.0.1.analogout0-maxlim
						# hm2_7i92.0.7i77.0.1.analogout0-minlim
						# hm2_7i92.0.7i77.0.1.analogout0-scalemax
						print(f'card {card} analog_port {port}')
						print(f'board name {parent.hal_name}')

					if board in analog_boards: # analog
						if getattr(parent, f'c{card}_encoderScale_{joint}').text():
							halContents.append('\n# Encoder Setup\n')
							halContents.append(f'setp hm2_[MESA](BOARD).0.encoder.0{joint}.scale  [JOINT_{joint}](ENCODER_SCALE)\n')
							halContents.append(f'setp hm2_[MESA](BOARD).0.encoder.0{joint}.counter-mode 0\n')
							halContents.append(f'setp hm2_[MESA](BOARD).0.encoder.0{joint}.filter 1\n')
							halContents.append(f'setp hm2_[MESA](BOARD).0.encoder.0{joint}.index-invert 0\n')
							halContents.append(f'setp hm2_[MESA](BOARD).0.encoder.0{joint}.index-mask 0\n')
							halContents.append(f'setp hm2_[MESA](BOARD).0.encoder.0{joint}.index-mask-invert 0\n')

					joint += 1

	# Spindle
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
		halContents.append(f'setp hm2_[MESA](BOARD).0.pwmgen.00.scale [SPINDLE_0]MAX_OUTPUT\n')

		halContents.append('\n# Spindle Enable\n')
		halContents.append('net spindle-on <= spindle.0.on\n')
		halContents.append('net spindle-on => pid.s.enable\n')
		halContents.append(f'net spindle-on => hm2_[MESA](BOARD).0.pwmgen.00.enable\n')


		halContents.append('\n# Spindle Connections\n')
		halContents.append('net spindle-vel-cmd <= spindle.0.speed-out-abs\n')
		halContents.append('net spindle-vel-cmd => pid.s.command\n')
		halContents.append('net spindle-pid-out <= pid.s.output\n')
		halContents.append('net spindle-pid-out => hm2_[MESA](BOARD).0.pwmgen.00.value\n')

		# for encoder feedback spindle at speed should use encoder speed
		halContents.append('\n# Spindle Feedback\n')
		halContents.append('setp spindle.0.at-speed true\n')

	# E Stop
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

	# Manual Tool Change
	if parent.manualToolChangeCB.isChecked():
		halContents.append('\n#  Manual Tool Change Dialog\n')

		halContents.append('loadusr -W hal_manualtoolchange\n')
		halContents.append('net tool-change-request    =>  hal_manualtoolchange.change\n')
		halContents.append('net tool-change-confirmed  <=  hal_manualtoolchange.changed\n')
		halContents.append('net tool-number            =>  hal_manualtoolchange.number\n')

		halContents.append('\n# create signals for tool loading loopback\n')
		halContents.append('net tool-prep-loop iocontrol.0.tool-prepare => iocontrol.0.tool-prepared\n')
		halContents.append('net tool-change-loop iocontrol.0.tool-change => iocontrol.0.tool-changed\n')

	# ClassicLadder
	if parent.ladderGB.isChecked():
		ladderOptionsList = ['ladderRungsSB', 'ladderBitsSB', 'ladderWordsSB',
		'ladderTimersSB', 'iecTimerSB', 'ladderMonostablesSB', 'ladderCountersSB',
		'ladderInputsSB', 'ladderOutputsSB', 'ladderExpresionsSB',
		'ladderSectionsSB', 'ladderSymbolsSB', 'ladderS32InputsSB',
		'ladderS32OuputsSB', 'ladderFloatInputsSB', 'ladderFloatOutputsSB']

		halContents.append('\n# # Load Classicladder without GUI\n')
		# this line needs to be built from the options if any are above 0
		ladderOptions = []
		for option in ladderOptionsList:
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

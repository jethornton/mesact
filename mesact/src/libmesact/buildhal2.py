import os, traceback
from datetime import datetime

def build(parent):

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

	''' this needs fixin
	dpll = {'7i96':['stepgen', 'encoder'],
		'7i96s':['stepgen', 'encoder'],}
	stepgen_timer = ['7i76e', '7i95', '7i95t', '7i96', '7i96s']

	if parent.boardType == 'eth':
		halContents.append('\n# DPLL TIMER\n')
		halContents.append(f'setp hm2_[MESA](BOARD).0.dpll.01.timer-us -50\n')
		if parent.board_0 in stepgen_timer or daughter_card == '7i76':
			halContents.append(f'setp hm2_[MESA](BOARD).0.stepgen.timer-number 1\n')

		if encoders > 0:
			halContents.append(f'setp hm2_[MESA](BOARD).0.encoder.timer-number 1\n')
	'''

	joint = 0
	for card in range(3):
		board = getattr(parent, f'board_{card}')
		if board:
			halContents.append(f'\n# Board: {board}\n')
			for output in range(6):
				if getattr(parent, f'c{card}_axis_{output}').currentData():
					 halContents.append(f'\n# Axis: {getattr(parent, f"c{card}_axis_{output}").currentData()} Joint: {joint} Output: {output}\n')
					 joint += 1

	try:
		with open(halFilePath, 'w') as halFile:
			halFile.writelines(halContents)
	except OSError:
		parent.info_pte.appendPlainText(f'OS error\n {traceback.print_exc()}')

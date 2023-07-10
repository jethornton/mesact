import os
from datetime import datetime

from libmesact import firmware

def build(parent):
	#card = parent.cardCB.currentText()
	#port = parent.ioPort

	filePath = os.path.join(parent.configPath, 'io.hal')
	parent.info_pte.appendPlainText(f'Building {filePath}')
	contents = []
	contents = ['# This file was created with the Mesa Configuration Tool on ']
	contents.append(datetime.now().strftime('%b %d %Y %H:%M:%S') + '\n')
	contents.append('# If you make changes to this file DO NOT use the Configuration Tool\n\n')

	input_dict = {
		'Joint 0 Home':'net joint-0-home joint.0.home-sw-in <=',
		'Joint 1 Home':'net joint-1-home joint.1.home-sw-in <=',
		'Joint 2 Home':'net joint-2-home joint.2.home-sw-in <=',
		'Joint 3 Home':'net joint-3-home joint.3.home-sw-in <=',
		'Joint 4 Home':'net joint-4-home joint.4.home-sw-in <=',
		'Joint 5 Home':'net joint-5-home joint.5.home-sw-in <=',
		'Joint 6 Home':'net joint-6-home joint.6.home-sw-in <=',
		'Joint 7 Home':'net joint-7-home joint.7.home-sw-in <=',
		'Joint 8 Home':'net joint-8-home joint.8.home-sw-in <=',
		'Home All':'net home-all halui.home-all <=',

		'Joint 0 Plus':'net pos-limit-joint-0 joint.0.pos-lim-sw-in <=',
		'Joint 0 Minus':'net neg-limit-joint-0 joint.0.neg-lim-sw-in <=',
		'Joint 0 Both':'net both-limit-joint-0 joint.0.pos-lim-sw-in\n'
			'net both-limit-joint-0 joint.0.neg-lim-sw-in <=',
		'Joint 1 Plus':'net pos-limit-joint-1 joint.1.pos-lim-sw-in <=',
		'Joint 1 Minus':'net neg-limit-joint-1 joint.1.neg-lim-sw-in <=',
		'Joint 1 Both':'net both-limit-joint-1 joint.1.pos-lim-sw-in\n'
			'net both-limit-joint-1 joint.1.neg-lim-sw-in <=',
		'Joint 2 Plus':'net pos-limit-joint-2 joint.2.pos-lim-sw-in <=',
		'Joint 2 Minus':'net neg-limit-joint-2 joint.2.neg-lim-sw-in <=',
		'Joint 2 Both':'net both-limit-joint-2 joint.2.pos-lim-sw-in\n'
			'net both-limit-joint-2 joint.2.neg-lim-sw-in <=',
		'Joint 3 Plus':'net pos-limit-joint-3 joint.3.pos-lim-sw-in <=',
		'Joint 3 Minus':'net neg-limit-joint-3 joint.3.neg-lim-sw-in <=',
		'Joint 3 Both':'net both-limit-joint-3 joint.3.pos-lim-sw-in\n'
			'net both-limit-joint-3 joint..neg-lim-sw-in <=',
		'Joint 4 Plus':'net pos-limit-joint-4 joint.4.pos-lim-sw-in <=',
		'Joint 4 Minus':'net neg-limit-joint-4 joint.4.neg-lim-sw-in <=',
		'Joint 4 Both':'net both-limit-joint-4 joint.4.pos-lim-sw-in\n'
			'net both-limit-joint-4 joint.4.neg-lim-sw-in <=',
		'Joint 5 Plus':'net pos-limit-joint-5 joint.5.pos-lim-sw-in <=',
		'Joint 5 Minus':'net neg-limit-joint-5 joint.5.neg-lim-sw-in <=',
		'Joint 5 Both':'net both-limit-joint-5 joint.5.pos-lim-sw-in\n'
			'net both-limit-joint-5 joint.5.neg-lim-sw-in <=',
		'Joint 6 Plus':'net pos-limit-joint-6 joint.6.pos-lim-sw-in <=',
		'Joint 6 Minus':'net neg-limit-joint-6 joint.6.neg-lim-sw-in <=',
		'Joint 6 Both':'net both-limit-joint-6 joint.6.pos-lim-sw-in\n'
			'net both-limit-joint-6 joint.6.neg-lim-sw-in <=',
		'Joint 7 Plus':'net pos-limit-joint-7 joint.7.pos-lim-sw-in <=',
		'Joint 7 Minus':'net neg-limit-joint-7 joint.7.neg-lim-sw-in <=',
		'Joint 7 Both':'net both-limit-joint-7 joint.7.pos-lim-sw-in\n'
			'net both-limit-joint-7 joint.7.neg-lim-sw-in <=',
		'Joint 8 Plus':'net pos-limit-joint-8 joint.8.pos-lim-sw-in <=',
		'Joint 8 Minus':'net neg-limit-joint-8 joint.8.neg-lim-sw-in <=',
		'Joint 8 Both':'net both-limit-joint-8 joint.8.pos-lim-sw-in\n'
			'net both-limit-joint-8 joint.8.neg-lim-sw-in <=',

		'Joint 0 Plus and Home':'net pos-limit-and-home-joint-0 joint.0.pos-lim-sw-in\n'
			'net pos-limit-and-home-joint-0 joint.0.home-sw-in <=',
		'Joint 0 Minus and Home':'net neg-limit-and-home-joint-0 joint.0.neg-lim-sw-in\n'
			'net neg-limit-and-home-joint-0 joint.0.home-sw-in <=',
		'Joint 1 Plus and Home':'net pos-limit-and-home-joint-1 joint.1.pos-lim-sw-in\n'
			'net pos-limit-and-home-joint-1 joint.1.home-sw-in <=',
		'Joint 1 Minus and Home':'net neg-limit-and-home-joint-1 joint.1.neg-lim-sw-in\n'
			'net neg-limit-and-home-joint-1 joint.1.home-sw-in <=',
		'Joint 2 Plus and Home':'net pos-limit-and-home-joint-2 joint.2.pos-lim-sw-in\n'
			'net pos-limit-and-home-joint-2 joint.2.home-sw-in <=',
		'Joint 2 Minus and Home':'net neg-limit-and-home-joint-2 joint.2.neg-lim-sw-in\n'
			'net neg-limit-and-home-joint-2 joint.2.home-sw-in <=',
		'Joint 3 Plus and Home':'net pos-limit-and-home-joint-3 joint.3.pos-lim-sw-in\n'
			'net pos-limit-and-home-joint-3 joint.3.home-sw-in <=',
		'Joint 3 Minus and Home':'net neg-limit-and-home-joint-3 joint.3.neg-lim-sw-in\n'
			'net neg-limit-and-home-joint-3 joint.3.home-sw-in <=',
		'Joint 4 Plus and Home':'net pos-limit-and-home-joint-4 joint.4.pos-lim-sw-in\n'
			'net pos-limit-and-home-joint-4 joint.4.home-sw-in <=',
		'Joint 4 Minus and Home':'net neg-limit-and-home-joint-4 joint.4.neg-lim-sw-in\n'
			'net neg-limit-and-home-joint-4 joint.4.home-sw-in <=',
		'Joint 5 Plus and Home':'net pos-limit-and-home-joint-5 joint.5.pos-lim-sw-in\n'
			'net pos-limit-and-home-joint-5 joint.5.home-sw-in <=',
		'Joint 5 Minus and Home':'net neg-limit-and-home-joint-5 joint.5.neg-lim-sw-in\n'
			'net neg-limit-and-home-joint-5 joint.5.home-sw-in <=',
		'Joint 6 Plus and Home':'net pos-limit-and-home-joint-6 joint.6.pos-lim-sw-in\n'
			'net pos-limit-and-home-joint-6 joint.6.home-sw-in <=',
		'Joint 6 Minus and Home':'net neg-limit-and-home-joint-6 joint.6.neg-lim-sw-in\n'
			'net neg-limit-and-home-joint-6 joint.6.home-sw-in <=',
		'Joint 7 Plus and Home':'net pos-limit-and-home-joint-7 joint.7.pos-lim-sw-in\n'
			'net pos-limit-and-home-joint-7 joint.7.home-sw-in <=',
		'Joint 7 Minus and Home':'net neg-limit-and-home-joint-7 joint.7.neg-lim-sw-in\n'
			'net neg-limit-and-home-joint-7 joint.7.home-sw-in <=',
		'Joint 8 Plus and Home':'net pos-limit-and-home-joint-8 joint.8.pos-lim-sw-in\n'
			'net pos-limit-and-home-joint-8 joint.8.home-sw-in <=',
		'Joint 8 Minus and Home':'net neg-limit-and-home-joint-8 joint.8.neg-lim-sw-in\n'
			'net neg-limit-and-home-joint-8 joint.8.home-sw-in <=',

		'Jog X Plus':'net jog-x-plus halui.axis.x.plus <=',
		'Jog X Minus':'net jog-x-minus halui.axis.x.minus <=',
		'Jog Y Plus':'net jog-y-plus halui.axis.y.plus <=',
		'Jog Y Minus':'net jog-y-minus halui.axis.y.minus <=',
		'Jog Z Plus':'net jog-z-plus halui.axis.z.plus <=',
		'Jog Z Minus':'net jog-z-minus halui.axis.z.minus <=',
		'Jog A Plus':'net jog-a-plus halui.axis.a.plus <=',
		'Jog A Minus':'net jog-a-minus halui.axis.a.minus <=',
		'Jog B Plus':'net jog-b-plus halui.axis.b.plus <=',
		'Jog B Minus':'net jog-b-minus halui.axis.b.minus <=',
		'Jog C Plus':'net jog-c-plus halui.axis.c.plus <=',
		'Jog C Minus':'net jog-c-minus halui.axis.c.minus <=',
		'Jog U Plus':'net jog-u-plus halui.axis.u.plus <=',
		'Jog U Minus':'net jog-u-minus halui.axis.u.minus <=',
		'Jog V Plus':'net jog-v-plus halui.axis.v.plus <=',
		'Jog V Minus':'net jog-v-minus halui.axis.v.minus <=',
		'Jog W Plus':'net jog-w-plus halui.axis.w.plus <=',
		'Jog W Minus':'net jog-w-minus halui.axis.w.minus <=',


		'Probe Input':'net probe-input motion.probe-input <=',
		'Digital 0':'net digital-0-input motion.digital-in-00 <=',
		'Digital 1':'net digital-1-input motion.digital-in-01 <=',
		'Digital 2':'net digital-2-input motion.digital-in-02 <=',
		'Digital 3':'net digital-3-input motion.digital-in-03 <=',

		'Flood':'net coolant-flood iocontrol.0.coolant-flood <=',
		'Mist':'net coolant-mist iocontrol.0.coolant-mist <=',
		'Lube Level':'net lube-level iocontrol.0.lube_level <=',
		'Tool Changed':'net tool-changed iocontrol.0.tool-changed <=',
		'Tool Prepared':'net tool-prepared iocontrol.0.tool-prepared <=',
		'Tool Changer Fault':'iocontrol.0.toolchanger-fault <=',
		'Spindle Amp Fault':'spindle.0.amp-fault-in <=',
		'Spindle Inhibit':'spindle.0.inhibit <=',
		'Spindle Oriented':'spindle.0.is-oriented <=',
		'Spindle Orient Fault':'spindle.0.orient-fault <='
		}
	{'Spindle':['Spindle Amp Fault', 'Spindle Inhibit', 'Spindle Oriented', 'Spindle Orient Fault']},


	'''
	
	<pcw-home> I think  may help
	mesaflash --device 7i92t --addr 10.10.10.10 --readhmid --dbname1 7i77
	<pcw-home> The sserial channels are typically just in sequence:
	<pcw-home> 7I76+7I76 0,1 on first 7I76, 2,3 on second
	<pcw-home> 7I77+7I77 0,1,2 on first 7I77 3,4,5 on second
	<pcw-home> 7I76+7I77, 0,1 on 7I76, 2,3,4 on 7I77

	hm2_7i76e.0.7i76.0.0.input-00
	hm2_7i76e.0.7i76.0.0.input-00-not
	hm2_7i76e.0.7i76.0.0.output-00
	hm2_7i76e.0.7i76.0.0.spindir
	hm2_7i76e.0.7i76.0.0.spinena
	hm2_7i76e.0.7i76.0.0.spinout

	7i92
	hm2_7i92.0.7i76.0.0.input-00
	hm2_7i92.0.7i76.0.0.input-00-not
	hm2_7i92.0.7i76.0.0.output-00
	hm2_7i92.0.7i76.0.0.spindir
	hm2_7i92.0.7i76.0.0.spinena
	hm2_7i92.0.7i76.0.0.spinout

	7i92t P1
	hm2_7i92.0.7i76.0.2.input-00
	hm2_7i92.0.7i76.0.2.input-00-not
	hm2_7i92.0.7i76.0.2.output-00
	hm2_7i92.0.7i76.0.2.spindir
	hm2_7i92.0.7i76.0.2.spinena
	hm2_7i92.0.7i76.0.2.spinout
	hm2_7i92.0.7i77.0.3.input-00

	7i92t P2
	hm2_7i92.0.7i76.0.0.input-00
	hm2_7i92.0.7i76.0.0.input-00-not
	hm2_7i92.0.7i76.0.0.output-00
	hm2_7i92.0.7i76.0.0.spindir
	hm2_7i92.0.7i76.0.0.spinena
	hm2_7i92.0.7i76.0.0.spinout
	hm2_7i92.0.7i77.0.0.input-00

	hm2_7i95.0.inmux.00.input-00
	hm2_7i95.0.inmux.00.input-00-not
	hm2_7i95.0.inmux.00.input-00-slow


	hm2_7i96.0.gpio.000.in
	hm2_7i96.0.gpio.000.in_not

	hm2_7i96s.0.inm.00.input-01
	hm2_7i96s.0.inm.00.input-01-not
	hm2_7i96s.0.inm.00.input-00-slow
	hm2_7i96s.0.ssr.00.out-00 - 03
	hm2_7i96s.0.outm.00.out-04 - 05

	hm2_7i96s.0.7i76.0.1.input-00
	hm2_7i96s.0.7i76.0.1.input-00-not
	hm2_7i96s.0.7i76.0.1.output-00

	hm2_7i97.0.inmux.00.input-00
	hm2_7i97.0.inmux.00.input-00-not
	hm2_7i97.0.inmux.00.input-00-slow
	'''
	mother_boards = ['5i25', '7i80db', '7i80hd', '7i92', '7i93', '7i98']
	daughter_boards = ['7i76', '7i77', '7i78']
	combo_boards = ['7i76e', '7i95', '7i96', '7i96s', '7i97']

	# build inputs from qpushbutton menus, check for debounce c0_input_0
	hm2 = ''
	eStops = []
	# figure out board syntax
	# print(f'parent.board {parent.board}')


	#hm2 = f'hm2_{parent.board}.0.'
	# Inputs tab 3 main boards and all in one boards
	# tab 4 P1 & 5 P2 daughter boards
	'''
	if tab 4 is used we need to know what firmware is loaded to determine the 
	smart serial ports

	'''
	if parent.boardCB.currentData() == '7i92t':
		mb = '7i92'
	else:
		mb = parent.boardCB.currentData()
	p1b = parent.daughterCB_0.currentData()
	p2b = parent.daughterCB_1.currentData()

	#print(f'main_board {mb}')
	#print(f'p1_board {p1b}')
	#print(f'p2_board {p2b}')

	# build main board inputs if a combo card
	if mb in combo_boards:
		for i in range(32):
			key = getattr(parent, f'c0_input_{i}').text()
			if mb == '7i96':
				invert = '_not' if getattr(parent, f'c0_input_invert_{i}').isChecked() else ''
			else:
				invert = '-not' if getattr(parent, f'c0_input_invert_{i}').isChecked() else ''
			slow = '-slow' if getattr(parent, f'c0_input_debounce_{i}').isChecked() else ''
			#hm2input = f'hm2_{parent.board}.0.{daughter}.input-'
			#if key != 'Select':
				#print(f'Key: {key}')
				#print(f'HM2: {hm2input}{j:02d}{invert}{slow}')
			#	print(f'Input Dictionary: {input_dict[key]}')

			if input_dict.get(key, False): # return False if key is not in dictionary
				if mb == '7i76e':
					hm2 =  f'hm2_7i76e.0.7i76.0.0.input-{i:02}{invert}\n'
				if mb == '7i95':
					hm2 =  f'hm2_7i95.0.inmux.00.input-{i:02}{invert}\n'
				if mb == '7i96':
					hm2 =  f'hm2_7i96.0.gpio.{i:03}.in{invert}\n'
				if mb == '7i96s':
					hm2 = f'hm2_7i96s.0.inm.00.input-{i:02}{invert}\n'
				if mb == '7i97':
					hm2 =  f'hm2_7i97.0.inmux.00.input-{i:02}{invert}\n'

				#print(f'{input_dict[key]} {hm2}')
				contents.append(f'{input_dict[key]} {hm2}\n')

	if p2b: # daughter card on P2
		for i in range(32):
			key = getattr(parent, f'c2_input_{i}').text()
			invert = '-not' if getattr(parent, f'c2_input_invert_{i}').isChecked() else ''
			slow = '-slow' if getattr(parent, f'c2_input_debounce_{i}').isChecked() else ''
			if input_dict.get(key, False): # return False if key is not in dictionary
				hm2 = f'hm2_{mb}.0.{p2b}.0.0.input-{i:02}{invert}'
				#print(f'{input_dict[key]} {hm2}')
				contents.append(f'{input_dict[key]} {hm2}\n')

	if p1b: # daughter card on P1
		for i in range(32):
			key = getattr(parent, f'c1_input_{i}').text()
			invert = '-not' if getattr(parent, f'c1_input_invert_{i}').isChecked() else ''
			slow = '-slow' if getattr(parent, f'c1_input_debounce_{i}').isChecked() else ''
			if input_dict.get(key, False): # return False if key is not in dictionary
				hm2 = f'hm2_{mb}.0.{p1b}.0.0.input-{i:02}{invert}'
				print(f'{input_dict[key]} {hm2}')
				contents.append(f'{input_dict[key]} {hm2}\n')

	''' 

	return


	boards = []
	for i in range(3,6):
		if getattr(parent, 'mainTW').isTabVisible(i):
			boards.append(getattr(parent, 'mainTW').tabText(i).lower())
		else:
			boards.append(None)
	#print(f'boards {boards}')

	tabs = [3,4,5]
	for i in range(3):
		if getattr(parent, 'mainTW').isTabVisible(tabs[i]):
			if tabs[i] == 3: # it's either a combo or a main board
				print('')
				if parent.boardCB.currentData() in comboBoards:
					print('')
			#print(f'i {i}')
			#print(f'Board: {boards[i]}')
			#print(getattr(parent, 'mainTW').tabText(tabs[i]).lower())
			if getattr(parent, f'c{i}_JointTW').isTabVisible(7): # input tab
				#print(f'Input {i}')
				for j in range(32):
					key = getattr(parent, f'c{i}_input_{j}').text()
					invert = '-not' if getattr(parent, f'c{i}_input_invert_{j}').isChecked() else ''
					slow = '-slow' if getattr(parent, f'c{i}_input_debounce_{j}').isChecked() else ''
					#hm2input = f'hm2_{parent.board}.0.{daughter}.input-'
					if key != 'Select':
						#print(f'Key: {key}')
						#print(f'HM2: {hm2input}{j:02d}{invert}{slow}')
						print(f'Input Dictionary: {input_dict[key]}')

		if getattr(parent, "mainTW").isTabVisible(i):

	c0_JointTW.isTabVisible(7):

	for i in range(3):
		if getattr(parent, "mainTW").isTabVisible(i+3):
			print(getattr(parent, "mainTW").tabText(i+3).lower())
			if i > 0:
				daughter = getattr(parent, "mainTW").tabText(i+3).lower().split()[0]
				connector = getattr(parent, "mainTW").tabText(i+3).lower().split()[1]
			else:
				daughter = '0'
		

			for j in range(32):

	#print(f'Board: {parent.boardCB.currentData()}')
	#print(f'Parent Board: {parent.board}')

			if parent.board in motherBoards:
				if parent.daughterCB_0.currentData():
					card = parent.daughterCB_0.currentText()
				elif parent.daughterCB_1.currentData():
					card = parent.daughterCB_1.currentText()
					if card in daughterBoards: # use input-00-not and output-00
						hm2 =  f'hm2_{parent.board}.0.{card}.0.0.input-{i:02}{invert}\n'

			else: # handle special cases
				if key == 'Home All':
					contents.append('\n# Home All Joints\n')
					contents.append('net home-all ' + f'{hm2}\n')
					for i in range(6):
						if getattr(parent, 'axisCB_' + str(i)).currentData():
							contents.append('net home-all ' + f'joint.{i}.home-sw-in\n')
				elif key[0:6] == 'E Stop':
					eStops.append(hm2)


	#Build E-Stop Chain
	if len(eStops) > 0:
		contents.append('# E-Stop Chain\n')
		contents.append(f'loadrt estop_latch count={len(eStops)}\n')
		for i in range(len(eStops)):
			contents.append(f'addf estop-latch.{i} servo-thread\n')
		contents.append('\n# E-Stop Loop\n')
		contents.append('net estop-loopin iocontrol.0.user-enable-out => estop-latch.0.ok-in\n')
		for i in range(len(eStops) - 1):
			contents.append(f'net estop-{i}-out estop-latch.{i}.ok-out => estop-latch.{i+1}.ok-in\n')
		contents.append(f'net estop-loopout estop-latch.{len(eStops)-1}.ok-out => iocontrol.0.emc-enable-in\n')
		contents.append('\n# E-Stop Reset\n')
		contents.append(f'net estop-reset iocontrol.0.user-request-enable\n')
		for i in range(len(eStops)):
			contents.append(f'net estop-reset => estop-latch.{i}.reset\n')
			contents.append(f'net remote-estop{i} estop-latch.{i}.fault-in <= {eStops[i]}')

	output_dict = {
	'Coolant Flood': 'net flood-output iocontrol.0.coolant-flood => ',
	'Coolant Mist': 'net mist-output iocontrol.0.coolant-mist => ',
	'Spindle On': 'net spindle-on => ',
	'Spindle CW': 'net spindle-cw spindle.0.forward => ',
	'Spindle CCW': 'net spindle-ccw spindle.0.reverse => ',
	'Spindle Brake': 'net spindle-brake spindle.0.brake => ',
	'E-Stop Out': 'net estop-loopback => ',
	'Digital Out 0': 'net digital-out-0 motion.digital-out-00 => ',
	'Digital Out 1': 'net digital-out-1 motion.digital-out-01 => ',
	'Digital Out 2': 'net digital-out-2 motion.digital-out-02 => ',
	'Digital Out 3': 'net digital-out-3 motion.digital-out-03 => ',
	'Joint 0 Amp Enable': 'net joint-0-enable joint.0.amp-enable-out => ',
	'Joint 1 Amp Enable': 'net joint-1-enable joint.1.amp-enable-out => ',
	'Joint 2 Amp Enable': 'net joint-2-enable joint.2.amp-enable-out => ',
	'Joint 3 Amp Enable': 'net joint-3-enable joint.3.amp-enable-out => ',
	'Joint 4 Amp Enable': 'net joint-4-enable joint.4.amp-enable-out => ',
	'Joint 5 Amp Enable': 'net joint-5-enable joint.5.amp-enable-out => ',
	'Joint 6 Amp Enable': 'net joint-6-enable joint.6.amp-enable-out => ',
	'Joint 7 Amp Enable': 'net joint-7-enable joint.7.amp-enable-out => ',
	'Joint 8 Amp Enable': 'net joint-8-enable joint.8.amp-enable-out => ',
	}

	# build the outputs
	for i in range(16):
		# hm2_7i92.0.7i77.0.0.output-15
		key = getattr(parent, 'outputPB_' + str(i)).text()
		if output_dict.get(key, False): # return False if key is not in dictionary
			if parent.board == '7i76e':
				contents.append(output_dict[key] + f'hm2_7i76e.0.7i76.0.0.output-{i:02}\n')
			if parent.board == '7i95': # hm2_7i95.0.ssr.00.out-00
				contents.append(output_dict[key] + f'hm2_7i95.0.ssr.00.out-{i:02}\n')
			if parent.board == '7i96':
				contents.append(output_dict[key] + f'hm2_7i96.0.ssr.00.out-{i:02}\n')
			if parent.board == '7i96s':
				if i in range(4):
					contents.append(output_dict[key] + f'hm2_7i96s.0.ssr.00.out-{i:02}\n')
					if getattr(parent, f'outputInvertCB_{i}').isChecked():
						contents.append(f'setp hm2_7i96s.0.ssr.00.invert-{i:02} True\n')
				if i in range(4,6):
					contents.append(output_dict[key] + f'hm2_7i96s.0.outm.00.out-{i:02}\n')
					if getattr(parent, f'outputInvertCB_{i}').isChecked():
						contents.append(f'setp hm2_7i96s.0.outm.00.invert-{i:02} True\n')
			if parent.board == '7i97':
				contents.append(output_dict[key] + f'hm2_7i97.0.ssr.00.out-{i:02}\n')
	'''

	# testing
	parent.mainTW.setCurrentIndex(10)
	parent.info_pte.clear()
	parent.info_pte.appendPlainText('Build I/O Function')
	for line in contents:
		parent.info_pte.appendPlainText(line.strip())

	try:
		with open(filePath, 'w') as f:
			f.writelines(contents)
	except OSError:
		parent.info_pte.appendPlainText(f'OS error\n {traceback.print_exc()}')


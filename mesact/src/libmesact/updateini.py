import os
from datetime import datetime

from PyQt5.QtWidgets import QSpinBox

from libmesact import mdi


class updateini:
	generated_hal_items = [
		'main.hal',
		'io.hal',
		'sserial.hal',
		'custom.hal',
		'postgui.hal',
		'shutdown.hal',
		'HALUI'
	]

	def __init__(self):
		super().__init__()
		self.content = []
		self.sections = {}

	def update(self, parent, iniFile):
		with open(iniFile,'r') as file:
			self.content = file.readlines() # create a list of the ini file
		self.get_sections() # get all ini sections
		if self.content[0].startswith('# This file'):
			self.content[0] = ('# This file was updated with the Mesa Configuration'
				f' Tool on {datetime.now().strftime("%b %d %Y %H:%M:%S")}\n')

		# if the joint is in the ini but the axis is different just change the axis
		# need a list of axes then joints from tool then check to see if any are missing
		# and insert them at the correct place

		'''
		Joint/Axes rules
		Joints must be used starting at 0 and not skipping a number
		Joints can be added after the last joint
		Joints can be deleted starting at the highest number and working backwards
		Axis letters can be changed without changing number of joints
		'''

		# build the tool joints dictionary
		tool_joints = {}
		joint = 0
		for i in range(3):
			for j in range(6):
				if getattr(parent, f'c{i}_axis_{j}').currentData():
					axis = getattr(parent, f'c{i}_axis_{j}').currentData()
					tool_joints[f'[JOINT_{joint}]'] = f'{axis}'
					joint += 1

		# build the configuration joints dictionary
		ini_joints = {}
		for key, value in self.sections.items():
			if key.startswith('[JOINT_'):
				start = value[0]
				end = value[1] + 1
				for item in self.content[start: end]:
					if item.split(' = ')[0].strip() == 'AXIS':
						ini_joints[key] = item.split('=')[1].strip()

		# test for axis letter(s) changed
		if len(tool_joints) == len(ini_joints): # this has problems if many axes are changed
			for key, value in tool_joints.items():
				if tool_joints[key] != ini_joints[key]:
					new_axis = f'[AXIS_{tool_joints[key]}]'
					old_axis = f'[AXIS_{ini_joints[key]}]'
					# use the sections to find the axis maybe
					for line in self.content:
						if line.strip() == f'[AXIS_{ini_joints[key]}]':
							for index, line in enumerate(self.content):
								if line.strip() == old_axis:
									self.content[index] = f'{new_axis}\n'
									self.get_sections()
									for line in self.content:
										parent.info_pte.appendPlainText(line.strip())

		# test for joints and axes removed
		elif len(tool_joints) < len(ini_joints):
			for key, value in ini_joints.items():
				if key not in tool_joints:
					start = self.sections[key][0]
					end = self.sections[key][1] + 1
					del self.content[start:end]
					self.get_sections()
					if value not in tool_joints.values():
						axis = f'[AXIS_{value}]'
						start = self.sections[axis][0]
						end = self.sections[axis][1] + 1
						del self.content[start:end]
						self.get_sections()

			for line in self.content:
				parent.info_pte.appendPlainText(line.strip())

		# test for joints and axes added
		# gantry adds and extra [AXIS_ ]
		elif len(tool_joints) > len(ini_joints):
			for key, value in tool_joints.items():
				if key not in ini_joints:
					last_end = self.sections[last_key][1] + 1
					self.content.insert(last_end, f'{key}\n')
					self.content.insert(last_end + 1, '\n')
					self.get_sections()
					# need to check to see if the axis has been create
					if f'[AXIS_{value}]' not in self.sections:
						last_end = self.sections[last_key][1] + 1
						self.content.insert(last_end, f'[AXIS_{value}]\n')
						self.content.insert(last_end + 1, '\n')
						self.get_sections()

				last_key = key
				last_axis = f'[AXIS_{value}]'

		'''
		board_names = {'7i92t': '7i92', '7i95t': '7i95'}
		if parent.boardCB.currentData() in board_names:
			board = board_names[parent.boardCB.currentData()]
		else:
			board = parent.boardCB.currentData()
		'''

		mesa = [
		['MESA', 'VERSION', f'{parent.version}'],
		['MESA', 'BOARD', f'{parent.hal_name}'],
		['MESA', 'BOARD_NAME', f'{parent.boardCB.currentData()}'],
		['MESA', 'FIRMWARE', f'{parent.firmwareCB.currentText()}'],
		['MESA', 'CARD_0', f'{parent.daughterCB_0.currentData()}'],
		['MESA', 'CARD_1', f'{parent.daughterCB_1.currentData()}']
		]
		for item in mesa:
			self.update_key(item[0], item[1], item[2])

		emc = [
		['EMC', 'VERSION', f'{parent.emcVersion}'],
		['EMC', 'MACHINE', f'{parent.configNameLE.text()}'],
		['EMC', 'DEBUG', f'{parent.debugCB.currentData()}']
		]
		for item in emc:
			self.update_key(item[0], item[1], item[2])

		if parent.boardType == 'eth':
			hm2 = [
			['HM2', 'DRIVER', 'hm2_eth'],
			['HM2', 'ADDRESS', f'{parent.ipAddressCB.currentText()}']
			]
		else:
			self.delete_key('HM2', 'ADDRESS')
		if parent.boardType == 'pci':
			hm2 = [['HM2', 'DRIVER', 'hm2_pci']]
		#hm2.append(['HM2', 'STEPGENS', f'{parent.stepgens_cb.currentData()}'])
		#hm2.append(['HM2', 'PWMGENS', f'{parent.pwmgens_cb.currentData()}'])
		#hm2.append(['HM2', 'ENCODERS', f'{parent.encoders_cb.currentData()}'])
		for item in hm2:
			self.update_key(item[0], item[1], item[2])

		display = [
		['DISPLAY', 'PROGRAM_PREFIX', f'{os.path.expanduser("~/linuxcnc/nc_files")}'],
		['DISPLAY', 'POSITION_OFFSET', f'{parent.positionOffsetCB.currentData()}'],
		['DISPLAY', 'POSITION_FEEDBACK', f'{parent.positionFeedbackCB.currentData()}'],
		['DISPLAY', 'MAX_FEED_OVERRIDE', f'{parent.maxFeedOverrideSB.value()}'],
		['DISPLAY', 'CYCLE_TIME', '0.1'],
		['DISPLAY', 'INTRO_GRAPHIC', f'{parent.introGraphicLE.text()}'],
		['DISPLAY', 'INTRO_TIME', f'{parent.splashScreenSB.value()}'],
		['DISPLAY', 'OPEN_FILE', f'""']
		]

		if not parent.guiCB.currentData(): # use the user gui
			display.append(['DISPLAY', 'DISPLAY', f'{parent.guiCB.currentText()}'])
		else:
			display.append(['DISPLAY', 'DISPLAY', f'{parent.guiCB.currentData()}'])

		# Flex GUI
		if len(parent.flex_gui_le.text()) > 0:
			display.append(['DISPLAY', 'GUI', f'{parent.flex_gui_le.text()}'])

		if parent.keyboard_qss_cb.isChecked():
			display.append(['DISPLAY', 'INPUT', 'keyboard'])
		elif parent.touch_qss_cb.isChecked():
			display.append(['DISPLAY', 'INPUT', 'touch'])
		else:
			self.delete_key('DISPLAY', 'INPUT')

		if len(parent.custom_qss_le.text()) > 0:
			display.append(['DISPLAY', 'QSS', f'{parent.custom_qss_le.text()}'])
		else:
			self.delete_key('DISPLAY', 'QSS')

		if parent.flex_size_cb.currentData():
			display.append(['DISPLAY', 'SIZE',  f'{parent.flex_size_cb.currentData()}'])
		else:
			self.delete_key('DISPLAY', 'SIZE')

		if parent.editorCB.currentData(): # if an editor is not selected delete it
			display.append(['DISPLAY', 'EDITOR', f'{parent.editorCB.currentData()}'])
		else:
			self.delete_key('DISPLAY', 'EDITOR')

		if set('XYZUVW')&set(parent.coordinatesLB.text()): # if no linear axes delete linear velocitys
			display.append(['DISPLAY', 'MIN_LINEAR_VELOCITY', f'{parent.minLinJogVelDSB.value()}'])
			display.append(['DISPLAY', 'DEFAULT_LINEAR_VELOCITY', f'{parent.defLinJogVelDSB.value()}'])
			display.append(['DISPLAY', 'MAX_LINEAR_VELOCITY', f'{parent.maxLinJogVelDSB.value()}'])
		else:
			self.delete_key('DISPLAY', 'MIN_LINEAR_VELOCITY')
			self.delete_key('DISPLAY', 'DEFAULT_LINEAR_VELOCITY')
			self.delete_key('DISPLAY', 'MAX_LINEAR_VELOCITY')

		if set('ABC')&set(parent.coordinatesLB.text()): # if no angular axes delete angular velocitys
			display.append(['DISPLAY', 'MIN_ANGULAR_VELOCITY', f'{parent.minAngJogVelDSB.value()}'])
			display.append(['DISPLAY', 'DEFAULT_ANGULAR_VELOCITY', f'{parent.defAngJogVelDSB.value()}'])
			display.append(['DISPLAY', 'MAX_ANGULAR_VELOCITY', f'{parent.maxAngJogVelDSB.value()}'])
		else:
			self.delete_key('DISPLAY', 'MIN_ANGULAR_VELOCITY')
			self.delete_key('DISPLAY', 'DEFAULT_ANGULAR_VELOCITY')
			self.delete_key('DISPLAY', 'MAX_ANGULAR_VELOCITY')

		if parent.jog_increments.text(): # if no user jog increments delete increments
			display.append(['DISPLAY', 'INCREMENTS', f'{parent.jog_increments.text()}'])
		else:
			self.delete_key('DISPLAY', 'INCREMENTS')

		if parent.pyvcpCB.isChecked():
			display.append(['DISPLAY', 'PYVCP', f'{parent.configNameUnderscored}.xml'])
		else:
			self.delete_key('DISPLAY', 'PYVCP')
		if parent.frontToolLatheRB.isChecked():
			display.append(['DISPLAY', 'LATHE', '1'])
		else:
			self.delete_key('DISPLAY', 'LATHE')
		if parent.frontToolLatheRB.isChecked():
			display.append(['DISPLAY', 'BACK_TOOL_LATHE', '1'])
		else:
			self.delete_key('DISPLAY', 'BACK_TOOL_LATHE')
		if parent.foamRB.isChecked():
			display.append(['DISPLAY', 'FOAM', '1'])
			display.append(['DISPLAY', 'Geometry', f'{parent.coordinatesLB.text()[0:2]};{parent.coordinatesLB.text()[2:4]}'])
		else:
			self.delete_key('DISPLAY', 'FOAM')
			self.delete_key('DISPLAY', 'Geometry')
		for item in display:
			self.update_key(item[0], item[1], item[2])

		# [FILTER]
		if '[FILTER]' in self.sections:
			index = self.sections['[FILTER]']
			for i in range(index[0], index[1]):
				if 'G code Files' in self.content[i]:
					ext_list = []
					for j in range(3):
						ext = getattr(parent, f'filterExtLE_{j}').text()
						if ext:
							if not ext.startswith('.'):
								ext_list.append(f'.{ext}')
							else:
								ext_list.append(ext)
					if ext_list:
						self.content[i] = f'PROGRAM_EXTENSION = {", ".join(ext_list)} # G code Files\n'

		# [KINS]
		if len(set(parent.coordinatesLB.text())) == len(parent.coordinatesLB.text()): # 1 joint for each axis
			kins = [['KINS', 'KINEMATICS', f'trivkins coordinates={parent.coordinatesLB.text()}']]
		else: # more than one joint per axis
			kins = [['KINS', 'KINEMATICS', f'trivkins coordinates={parent.coordinatesLB.text()} kinstype=BOTH']]
		kins.append(['KINS', 'JOINTS', f'{len(parent.coordinatesLB.text())}'])
		for item in kins:
			self.update_key(item[0], item[1], item[2])

		emcio = [
		['EMCIO', 'EMCIO', 'iov2'],
		['EMCIO', 'CYCLE_TIME', '0.100'],
		['EMCIO', 'TOOL_TABLE', 'tool.tbl']
		]
		for item in emcio:
			self.update_key(item[0], item[1], item[2])

		rs274ngc = [
		['RS274NGC', 'PARAMETER_FILE', 'parameters.var'],
		['RS274NGC', 'SUBROUTINE_PATH', f'{os.path.expanduser("~/linuxcnc/subroutines")}']
		]

		for item in rs274ngc:
			self.update_key(item[0], item[1], item[2])

		emcmot = [
		['EMCMOT', 'EMCMOT', 'motmod'],
		['EMCMOT', 'COMM_TIMEOUT', '1.0'],
		['EMCMOT', 'SERVO_PERIOD', f'{parent.servoPeriodSB.value()}']
		]

		for item in emcmot:
			self.update_key(item[0], item[1], item[2])

		task = [
		['TASK', 'TASK', 'milltask'],
		['TASK', 'CYCLE_TIME', '0.010']
		]

		for item in task:
			self.update_key(item[0], item[1], item[2])

		traj = [
		['TRAJ', 'COORDINATES', f'{parent.coordinatesLB.text()}'],
		['TRAJ', 'LINEAR_UNITS', f'{parent.linearUnitsCB.currentData()}'],
		['TRAJ', 'ANGULAR_UNITS', 'degree'],
		['TRAJ', 'MAX_LINEAR_VELOCITY', f'{parent.trajMaxLinVelDSB.value()}'],
		]
		if parent.noforcehomingCB.isChecked():
			traj.append(['TRAJ','NO_FORCE_HOMING', '0'])
		else:
			traj.append(['TRAJ','NO_FORCE_HOMING', '1'])

		for item in traj:
			self.update_key(item[0], item[1], item[2])

		# Update [HAL] section using same rules as for INI file building
		start, end = self.get_section_bounds('[HAL]')
		# remove all generated files
		for i in reversed(range(start, end)):
			if any(hal_file in self.content[i] for hal_file in self.generated_hal_items):
				del self.content[i]

		self.get_sections()
		start, end = self.get_section_bounds('[HAL]')

		# add in reversed order to avoid indexes calculation
		if parent.haluiCB.isChecked():
			self.content.insert(end, 'HALUI = halui\n')
		if parent.shutdownCB.isChecked():
			self.content.insert(end, 'SHUTDOWN = shutdown.hal\n')
		if parent.postguiCB.isChecked():
			self.content.insert(end, 'POSTGUI_HALFILE = postgui.hal\n')
		if parent.customhalCB.isChecked():
			self.content.insert(start + 1, 'HALFILE = custom.hal\n')
		if parent.ssCardCB.currentData():
			self.content.insert(start + 1, 'HALFILE = sserial.hal\n')
		self.content.insert(start + 1, 'HALFILE = io.hal\n')
		self.content.insert(start + 1, 'HALFILE = main.hal\n')

		self.get_sections()

		# [HALUI]
		if parent.haluiCB.isChecked() and '[HALUI]' not in self.sections:
			section = '[HALUI]'
			index = self.sections['[HAL]'][1]
			self.insert_section(index, section)

		if '[HALUI]' in self.sections:
			index = self.sections['[HALUI]']
			if len(index) == 2:
				start = index[0]
				end = index[1]
				# remove all existing MDI commands
				for i in reversed(range(start, end)):
					if self.content[i].startswith('MDI_COMMAND'):
						del self.content[i]
				tool_mdi = []
				for i in range(mdi.get_mdi_commands_count(parent)):
					mdi_text = mdi.get_mdi_command(parent, i)
					if mdi_text:
						tool_mdi.append(mdi_text)
				for i in reversed(range(len(tool_mdi))):
					self.content.insert(start + 1, f'MDI_COMMAND = {tool_mdi[i]}\n')
				self.get_sections() # update section start/end

		############ Massive rework needed here
		# if the section exists and is in the tool update it
		# if the section exists but not in the tool delete it
		# if the section does not exist but is in the tool create it
		# coordinatesLB contains all the axes XYYZ
		# [AXIS_x] section

		# finally update the [AXIS_n] and [JOINT_n] sections
		axes = []
		n = 0 # joint number
		for i in range(3):
			for j in range(6):
				if getattr(parent, f'c{i}_axis_{j}').currentData():
					axis = getattr(parent, f'c{i}_axis_{j}').currentData()
					if axis not in axes:
						axes.append(axis)

						self.update_key(f'AXIS_{axis}', 'MIN_LIMIT', getattr(parent, f'c{i}_min_limit_{j}').text())
						self.update_key(f'AXIS_{axis}', 'MAX_LIMIT', getattr(parent, f'c{i}_max_limit_{j}').text())
						self.update_key(f'AXIS_{axis}', 'MAX_VELOCITY', getattr(parent, f'c{i}_max_vel_{j}').text())
						self.update_key(f'AXIS_{axis}', 'MAX_ACCELERATION', getattr(parent, f'c{i}_max_accel_{j}').text())

					self.update_key(f'JOINT_{n}', 'CARD', f'{i}')
					self.update_key(f'JOINT_{n}', 'TAB', f'{j}')
					self.update_key(f'JOINT_{n}', 'AXIS', getattr(parent, f'c{i}_axis_{j}').currentData())
					self.update_key(f'JOINT_{n}', 'MIN_LIMIT', getattr(parent, f'c{i}_min_limit_{j}').text())
					self.update_key(f'JOINT_{n}', 'MAX_LIMIT', getattr(parent, f'c{i}_max_limit_{j}').text())
					self.update_key(f'JOINT_{n}', 'MAX_VELOCITY', getattr(parent, f'c{i}_max_vel_{j}').text())
					self.update_key(f'JOINT_{n}', 'MAX_ACCELERATION', getattr(parent, f'c{i}_max_accel_{j}').text())
					self.update_key(f'JOINT_{n}', 'TYPE', getattr(parent, f'c{i}_axisType_{j}').text())

					if getattr(parent, f'c{i}_scale_{j}').isEnabled():
						self.update_key(f'JOINT_{n}', 'SCALE', f'{getattr(parent, f"c{i}_scale_{j}").text()}')

					if getattr(parent, f'c{i}_settings_{j}').isTabVisible(2): # Stepgen Tab
						self.update_key(f'JOINT_{n}', 'DRIVE', getattr(parent, f'c{i}_drive_{j}').currentText())
						self.update_key(f'JOINT_{n}', 'STEP_INVERT', getattr(parent, f'c{i}_StepInvert_{j}').isChecked())
						self.update_key(f'JOINT_{n}', 'DIR_INVERT', getattr(parent, f'c{i}_DirInvert_{j}').isChecked())
						self.update_key(f'JOINT_{n}', 'STEPGEN_MAX_VEL', f'{float(getattr(parent, f"c{i}_max_vel_{j}").text()) * 1.2:.2f}')
						self.update_key(f'JOINT_{n}', 'STEPGEN_MAX_ACC', f'{float(getattr(parent, f"c{i}_max_accel_{j}").text()) * 1.2:.2f}')
						self.update_key(f'JOINT_{n}', 'DIRSETUP', getattr(parent, f'c{i}_DirSetup_{j}').text())
						self.update_key(f'JOINT_{n}', 'DIRHOLD', getattr(parent, f'c{i}_DirHold_{j}').text())
						self.update_key(f'JOINT_{n}', 'STEPLEN', getattr(parent, f'c{i}_StepTime_{j}').text())
						self.update_key(f'JOINT_{n}', 'STEPSPACE', getattr(parent, f'c{i}_StepSpace_{j}').text())

					if getattr(parent, f'c{i}_settings_{j}').isTabVisible(3): # Analog Tab
						self.update_key(f'JOINT_{n}', 'ANALOG_SCALE_MAX', getattr(parent, f'c{i}_analogScaleMax_{j}').text())
						self.update_key(f'JOINT_{n}', 'ANALOG_MIN_LIMIT', getattr(parent, f'c{i}_analogMinLimit_{j}').text())
						self.update_key(f'JOINT_{n}', 'ANALOG_MAX_LIMIT', getattr(parent, f'c{i}_analogMaxLimit_{j}').text())

					if getattr(parent, f'c{i}_settings_{j}').isTabVisible(4): # Encoder Tab
						self.update_key(f'JOINT_{n}', 'ENCODER_SCALE', getattr(parent, f'c{i}_encoderScale_{j}').text())

					self.update_key(f'JOINT_{n}', 'FERROR', getattr(parent, f'c{i}_max_ferror_{j}').text())
					self.update_key(f'JOINT_{n}', 'MIN_FERROR', getattr(parent, f'c{i}_min_ferror_{j}').text())
					self.update_key(f'JOINT_{n}', 'DEADBAND', getattr(parent, f'c{i}_deadband_{j}').text())
					self.update_key(f'JOINT_{n}', 'P', getattr(parent, f'c{i}_p_{j}').text())
					self.update_key(f'JOINT_{n}', 'I', getattr(parent, f'c{i}_i_{j}').text())
					self.update_key(f'JOINT_{n}', 'D', getattr(parent, f'c{i}_d_{j}').text())
					self.update_key(f'JOINT_{n}', 'FF0', getattr(parent, f'c{i}_ff0_{j}').text())
					self.update_key(f'JOINT_{n}', 'FF1', getattr(parent, f'c{i}_ff1_{j}').text())
					self.update_key(f'JOINT_{n}', 'FF2', getattr(parent, f'c{i}_ff2_{j}').text())
					self.update_key(f'JOINT_{n}', 'BIAS', getattr(parent, f'c{i}_bias_{j}').text())
					self.update_key(f'JOINT_{n}', 'MAX_OUTPUT', getattr(parent, f'c{i}_maxOutput_{j}').text())
					self.update_key(f'JOINT_{n}', 'MAX_ERROR', getattr(parent, f'c{i}_maxError_{j}').text())
					if getattr(parent, f'c{i}_home_{j}').text():
						self.update_key(f'JOINT_{n}', 'HOME', getattr(parent, f"c{i}_home_{j}").text())
					else:
						self.delete_key(f'JOINT_{n}', 'HOME')
					if getattr(parent, f"c{i}_homeOffset_{j}").text():
						self.update_key(f'JOINT_{n}', 'HOME_OFFSET', getattr(parent, f"c{i}_homeOffset_{j}").text())
					else:
						self.delete_key(f'JOINT_{n}', 'HOME_OFFSET')
					if getattr(parent, f"c{i}_homeSearchVel_{j}").text():
						self.update_key(f'JOINT_{n}', 'HOME_SEARCH_VEL', getattr(parent, f"c{i}_homeSearchVel_{j}").text())
					else:
						self.delete_key(f'JOINT_{n}', 'HOME_SEARCH_VEL')
					if getattr(parent, f"c{i}_homeLatchVel_{j}").text():
						self.update_key(f'JOINT_{n}', 'HOME_LATCH_VEL', getattr(parent, f"c{i}_homeLatchVel_{j}").text())
					else:
						self.delete_key(f'JOINT_{n}', 'HOME_LATCH_VEL')
					if getattr(parent, f"c{i}_homeFinalVelocity_{j}").text():
						self.update_key(f'JOINT_{n}', 'HOME_FINAL_VEL', getattr(parent, f"c{i}_homeFinalVelocity_{j}").text())
					else:
						self.delete_key(f'JOINT_{n}', 'HOME_FINAL_VEL')
					if getattr(parent, f"c{i}_homeSequence_{j}").text():
						self.update_key(f'JOINT_{n}', 'HOME_SEQUENCE', getattr(parent, f"c{i}_homeSequence_{j}").text())
					else:
						self.delete_key(f'JOINT_{n}', 'HOME_SEQUENCE')
					if getattr(parent, f"c{i}_homeIgnoreLimits_{j}").isChecked():
						self.update_key(f'JOINT_{n}', 'HOME_IGNORE_LIMITS', getattr(parent, f"c{i}_homeIgnoreLimits_{j}").isChecked())
					else:
						self.delete_key(f'JOINT_{n}', 'HOME_IGNORE_LIMITS')
					if getattr(parent, f"c{i}_homeUseIndex_{j}").isChecked():
						self.update_key(f'JOINT_{n}', 'HOME_USE_INDEX', getattr(parent, f"c{i}_homeUseIndex_{j}").isChecked())
					else:
						self.delete_key(f'JOINT_{n}', 'HOME_USE_INDEX')
					if getattr(parent, f"c{i}_homeSwitchShared_{j}").isChecked():
						self.update_key(f'JOINT_{n}', 'HOME_IS_SHARED', getattr(parent, f"c{i}_homeSwitchShared_{j}").isChecked())
					else:
						self.delete_key(f'JOINT_{n}', 'HOME_IS_SHARED')
					n += 1 # add a joint

		# 7i77 spindle
		for i in range(1,3):
			if getattr(parent, f'c{i}_spindle_cb').isChecked():
				if '[SPINDLE_7I77]' not in self.sections:
					last_joint = None
					for key, value in self.sections.items():
						if key.startswith('[JOINT'):
							last_joint = key
					index = self.sections[last_joint][1]
					self.content.insert(index, '\n[SPINDLE_7I77]\n')
					self.get_sections() # update section start/end
				self.update_key(f'SPINDLE_7I77', 'CARD', f'{i}')
				self.update_key(f'SPINDLE_7I77', 'P', getattr(parent, f'c{i}_p_5').text())
				self.update_key(f'SPINDLE_7I77', 'I', getattr(parent, f'c{i}_i_5').text())
				self.update_key(f'SPINDLE_7I77', 'D', getattr(parent, f'c{i}_d_5').text())
				self.update_key(f'SPINDLE_7I77', 'FF0', getattr(parent, f'c{i}_ff0_5').text())
				self.update_key(f'SPINDLE_7I77', 'FF1', getattr(parent, f'c{i}_ff1_5').text())
				self.update_key(f'SPINDLE_7I77', 'FF2', getattr(parent, f'c{i}_ff2_5').text())
				self.update_key(f'SPINDLE_7I77', 'BIAS', getattr(parent, f'c{i}_bias_5').text())
				self.update_key(f'SPINDLE_7I77', 'DEADBAND', getattr(parent, f'c{i}_deadband_5').text())
				self.update_key(f'SPINDLE_7I77', 'MIN_RPM', getattr(parent, f'c{i}_analogMinLimit_5').text())
				self.update_key(f'SPINDLE_7I77', 'MAX_RPM', getattr(parent, f'c{i}_analogMaxLimit_5').text())
				self.update_key(f'SPINDLE_7I77', 'SCALE_MAX', getattr(parent, f'c{i}_analogScaleMax_5').text())

		# update the [SPINDLE_0] section
		if parent.spindleTypeCB.currentData() == 'pwm':
			# If SPINDLE_0 section does not exist insert it after the last joint
			if '[SPINDLE_0]' not in self.sections:
				last_joint = None
				for key, value in self.sections.items():
					if key.startswith('[JOINT'):
						last_joint = key
				index = self.sections[last_joint][1]
				self.content.insert(index, '[SPINDLE_0]\n')
				self.content.insert(index, '\n')
				self.get_sections() # update section start/end

			self.update_key(f'SPINDLE_0', 'TYPE', parent.spindleTypeCB.currentData())
			#self.update_key(f'SPINDLE_0', 'SPINDLE_PWM_TYPE', parent.spindleTypeCB.currentData())
			self.update_key(f'SPINDLE_0', 'PWM_FREQUENCY', parent.pwmFrequencySB.value())
			self.update_key(f'SPINDLE_0', 'P', parent.p_s.value())
			self.update_key(f'SPINDLE_0', 'I', parent.i_s.value())
			self.update_key(f'SPINDLE_0', 'D', parent.d_s.value())
			self.update_key(f'SPINDLE_0', 'FF0', parent.ff0_s.value())
			self.update_key(f'SPINDLE_0', 'FF1', parent.ff1_s.value())
			self.update_key(f'SPINDLE_0', 'FF2', parent.ff2_s.value())
			self.update_key(f'SPINDLE_0', 'BIAS', parent.bias_s.value())
			self.update_key(f'SPINDLE_0', 'DEADBAND', parent.deadband_s.value())
			self.update_key(f'SPINDLE_0', 'MAX_ERROR', parent.maxError_s.value())
			self.update_key(f'SPINDLE_0', 'MAX_OUTPUT', parent.maxOutput_s.value())
			self.update_key(f'SPINDLE_0', 'OUTPUT_TYPE', parent.maxOutput_s.value())
			self.update_key(f'SPINDLE_0', 'MIN_FORWARD_VELOCITY', parent.spindleMinRpmFwd.value())
			self.update_key(f'SPINDLE_0', 'MAX_FORWARD_VELOCITY', parent.spindleMaxRpmFwd.value())
			self.update_key(f'SPINDLE_0', 'MIN_REVERSE_VELOCITY', parent.spindleMinRpmRev.value())
			self.update_key(f'SPINDLE_0', 'MAX_REVERSE_VELOCITY', parent.spindleMaxRpmRev.value())

			self.update_key(f'SPINDLE_0', 'SCALE', parent.spindleEncoderScale.value())

		'''

		To set up really basic operation (ignoring the ini file values and the PID), at the minimum,
		you need to setup and connect PWMGen 00:

		setp hm2_7i96s.0.pwmgen.00.scale 24000
		setp hm2_7i96s.0.pwmgen.00.pwm_frequency 5000
		setp hm2_7i96s.0.pwmgen.00.output_type 1

		net spindle-vel-cmd-rpm-abs hm2_7i96s.0.pwmgen.00.value
		net spindle-on spindle.0.on
		net spindle-on hm2_7i96s.0.pwmgen.00.enable

			if parent.spindleTypeCB.currentData() == 'analog':
				self.update_key(f'SPINDLE_0', 'MAX_RPM', parent.spindleMaxRpm.value())
				self.update_key(f'SPINDLE_0', 'MIN_RPM', parent.spindleMinRpm.value())

			if parent.spindleFeedbackCB.currentData() == 'encoder':
				self.update_key(f'SPINDLE_0', 'FEEDBACK', parent.spindleFeedbackCB.currentData())
				self.update_key(f'SPINDLE_0', 'ENCODER_SCALE', parent.spindleEncoderScale.value())
			else: # remove the above from the ini
				self.delete_key('SPINDLE_0', 'FEEDBACK')
				self.delete_key('SPINDLE_0', 'P')
				self.delete_key('SPINDLE_0', 'I')
				self.delete_key('SPINDLE_0', 'D')
				self.delete_key('SPINDLE_0', 'FF0')
				self.delete_key('SPINDLE_0', 'FF1')
				self.delete_key('SPINDLE_0', 'FF2')
				self.delete_key('SPINDLE_0', 'BIAS')
				self.delete_key('SPINDLE_0', 'DEADBAND')
				self.delete_key('SPINDLE_0', 'MAX_ERROR')
				self.delete_key('SPINDLE_0', 'MAX_OUTPUT')
				self.delete_key('SPINDLE_0', 'OUTPUT_TYPE')
				self.delete_key('SPINDLE_0', 'ENCODER_SCALE')

			if parent.spindleTypeCB.currentData()[:7] == 'stepgen':
				self.update_key(f'SPINDLE_0', 'DRIVE', parent.spindleDriveCB.currentText())
				self.update_key(f'SPINDLE_0', 'SCALE', parent.spindleStepScale.text())
				self.update_key(f'SPINDLE_0', 'STEPLEN', parent.spindleStepTime.text())
				self.update_key(f'SPINDLE_0', 'STEPSPACE', parent.spindleStepSpace.text())
				self.update_key(f'SPINDLE_0', 'DIRSETUP', parent.spindleDirSetup.text())
				self.update_key(f'SPINDLE_0', 'DIRHOLD', parent.spindleDirHold.text())
				self.update_key(f'SPINDLE_0', 'STEP_INVERT', parent.spindleStepInvert.isChecked())
				self.update_key(f'SPINDLE_0', 'DIR_INVERT', parent.spindleDirInvert.isChecked())
				self.update_key(f'SPINDLE_0', 'MIN_RPM', parent.spindleMinRpm.value())
				self.update_key(f'SPINDLE_0', 'MAX_RPM', parent.spindleMaxRpm.value())
				self.update_key(f'SPINDLE_0', 'MIN_RPS', parent.spindleMinRps.text())
				self.update_key(f'SPINDLE_0', 'MAX_RPS', parent.spindleMaxRps.text())
				self.update_key(f'SPINDLE_0', 'MAX_ACCEL_RPM', parent.spindleMaxAccel.value())
				self.update_key(f'SPINDLE_0', 'MAX_ACCEL_RPS', parent.spindleMaxRpss.text())

		else: # if SPINDLE_0 is in ini delete it
			if '[SPINDLE_0]' in self.sections:
				self.delete_section('[SPINDLE_0]')
		'''
		# update the [INPUTS] section
		for i in range(3):
			for j in range(32):
				if getattr(parent, f'c{i}_input_{j}').text() != 'Select':
					self.update_key('INPUTS', f'INPUT_{i}_{j}', getattr(parent, f'c{i}_input_{j}').text())
					self.update_key('INPUTS', f'INPUT_INVERT_{i}_{j}', getattr(parent, f'c{i}_input_invert_{j}').isChecked())
					self.update_key('INPUTS', f'INPUT_SLOW_{i}_{j}', getattr(parent, f'c{i}_input_debounce_{j}').isChecked())
				else:
					self.delete_key('INPUTS', f'INPUT_{i}_{j}')
					self.delete_key('INPUTS', f'INPUT_INVERT_{i}_{j}')
					self.delete_key('INPUTS', f'INPUT_SLOW_{i}_{j}')

		# update the [OUTPUTS] section
		if parent.boardCB.currentText() == '7i76EU':
			sink = ''
			source = ''
			for i in range(16):
				sink += getattr(parent, f'c0_output_type_{i}').currentData()[0]
				source += getattr(parent, f'c0_output_type_{i}').currentData()[1]
			self.update_key('OUTPUTS', 'OUTPUT_SINK', sink)
			self.update_key('OUTPUTS', 'OUTPUT_SOURCE', source)

		for i in range(3):
			for j in range(16):
				if getattr(parent, f'c{i}_output_{j}').text() != 'Select':
					self.update_key('OUTPUTS', f'OUTPUT_{i}_{j}', getattr(parent, f'c{i}_output_{j}').text())
					self.update_key('OUTPUTS', f'OUTPUT_INVERT_{i}_{j}', getattr(parent, f'c{i}_output_invert_{j}').isChecked())
				else:
					self.delete_key('OUTPUTS', f'OUTPUT_{i}_{j}')
					self.delete_key('OUTPUTS', f'OUTPUT_INVERT_{i}_{j}')

		# update the [OPTIONS] section
		options = [
		['OPTIONS', 'LOAD_CONFIG', f'{parent.load_config_cb.isChecked()}'],
		['OPTIONS', 'INTRO_GRAPHIC', f'{parent.introGraphicLE.text()}'],
		['OPTIONS', 'INTRO_GRAPHIC_TIME', f'{parent.splashScreenSB.value()}'],
		['OPTIONS', 'MANUAL_TOOL_CHANGE', f'{parent.manualToolChangeCB.isChecked()}'],
		['OPTIONS', 'CUSTOM_HAL', f'{parent.customhalCB.isChecked()}'],
		['OPTIONS', 'POST_GUI_HAL', f'{parent.postguiCB.isChecked()}'],
		['OPTIONS', 'SHUTDOWN_HAL', f'{parent.shutdownCB.isChecked()}'],
		['OPTIONS', 'HALUI', f'{parent.haluiCB.isChecked()}'],
		['OPTIONS', 'PYVCP', f'{parent.pyvcpCB.isChecked()}'],
		['OPTIONS', 'GLADEVCP', f'{parent.gladevcpCB.isChecked()}'],
		['OPTIONS', 'LADDER', f'{parent.ladderGB.isChecked()}'],
		['OPTIONS', 'BACKUP', f'{parent.backupCB.isChecked()}']
		]
		for item in options:
			self.update_key(item[0], item[1], item[2])

		# update [PLC] section
		if parent.ladderGB.isChecked(): # check for any options
			# If [PLC] section does not exist insert it after [OPTIONS] section
			if '[PLC]' not in self.sections:
				index = self.sections['[OPTIONS]'][1]
				self.insert_section(index, '[PLC]')

			children = parent.ladderGB.findChildren(QSpinBox)
			for child in children:
				self.update_key('PLC', f'{getattr(parent, child.objectName()).property("item")}', f'{getattr(parent, child.objectName()).value()}')
		else: # remove PLC section if it's in the ini file
			if '[PLC]' in self.sections:
				self.delete_section('[PLC]')

		# update the [SSERIAL] section
		if parent.ssCardCB.currentData():
			if '[SSERIAL]' not in self.sections:
				if '[PLC]'in self.sections:
					index = self.sections['[PLC]'][1]
				else:
					index = self.sections['[OPTIONS]'][1]
				self.insert_section(index, '[SSERIAL]')

			self.update_key(f'SSERIAL', 'SS_CARD', parent.ssCardCB.currentText())

			if parent.ssCardCB.currentText() == '7i64':
				for i in range(24):
					if getattr(parent, f'ss7i64in_{i}').text() != 'Select':
						self.update_key(f'SSERIAL', f'ss7i64in_{i}', getattr(parent, f'ss7i64in_{i}').text())
					if getattr(parent, f'ss7i64out_{i}').text() != 'Select':
						self.update_key(f'SSERIAL', f'ss7i64out_{i}', getattr(parent, f'ss7i64out_{i}').text())
			elif parent.ssCardCB.currentText() == '7i69':
				for i in range(24):
					if getattr(parent, f'ss7i69in_{i}').text() != 'Select':
						self.update_key(f'SSERIAL', f'ss7i69in_{i}', getattr(parent, f'ss7i69in_{i}').text())
					if getattr(parent, f'ss7i69out_{i}').text() != 'Select':
						self.update_key(f'SSERIAL', f'ss7i69out_{i}', getattr(parent, f'ss7i69out_{i}').text())
			elif parent.ssCardCB.currentText() == '7i70':
				for i in range(48):
					if getattr(parent, f'ss7i70in_{i}').text() != 'Select':
						self.update_key(f'SSERIAL', f'ss7i70in_{i}', getattr(parent, f'ss7i70in_{i}').text())
			elif parent.ssCardCB.currentText() == '7i71':
				for i in range(48):
					if getattr(parent, f'ss7i71out_{i}').text() != 'Select':
						self.update_key(f'SSERIAL', f'ss7i71out_{i}', getattr(parent, f'ss7i71out_{i}').text())
			elif parent.ssCardCB.currentText() == '7i72':
				for i in range(48):
					if getattr(parent, f'ss7i72out_{i}').text() != 'Select':
						self.update_key(f'SSERIAL', f'ss7i72out_{i}', getattr(parent, f'ss7i72out_{i}').text())
			elif parent.ssCardCB.currentText() == '7i73':
				for i in range(16):
					if getattr(parent, f'ss7i73key_{i}').text() != 'Select':
						self.update_key(f'SSERIAL', f'ss7i73key_{i}', getattr(parent, f'ss7i73key_{i}').text())
				for i in range(12):
					if getattr(parent, f'ss7i73lcd_{i}').text() != 'Select':
						self.update_key(f'SSERIAL', f'ss7i73lcd_{i}', getattr(parent, f'ss7i73lcd_{i}').text())
				for i in range(16):
					if getattr(parent, f'ss7i73in_{i}').text() != 'Select':
						self.update_key(f'SSERIAL', f'ss7i73in_{i}', getattr(parent, f'ss7i73in_{i}').text())
				for i in range(2):
					if getattr(parent, f'ss7i64in_{i}').text() != 'Select':
						self.update_key(f'SSERIAL', f'ss7i73out_{i}', getattr(parent, f'ss7i73out_{i}').text())
			elif parent.ssCardCB.currentText() == '7i84':
				for i in range(32):
					if getattr(parent, f'ss7i84in_{i}').text() != 'Select':
						self.update_key(f'SSERIAL', f'ss7i84in_{i}', getattr(parent, f'ss7i84in_{i}').text())
				for i in range(16):
					if getattr(parent, f'ss7i84out_{i}').text() != 'Select':
						self.update_key(f'SSERIAL', f'ss7i84out_{i}', getattr(parent, f'ss7i84out_{i}').text())
			elif parent.ssCardCB.currentText() == '7i87':
				for i in range(8):
					if getattr(parent, f'ss7i87in_{i}').text() != 'Select':
						self.update_key(f'SSERIAL', f'ss7i87in_{i}', getattr(parent, f'ss7i87in_{i}').text())

		else: # remove the [SSERIAL] section
			if '[SSERIAL]' in self.sections:
				self.delete_section('[SSERIAL]')

		parent.info_pte.appendPlainText('Update INI Function')
		self.write_ini(parent, iniFile)

	def write_ini(self, parent, iniFile):
		with open(iniFile, 'w') as outfile:
			outfile.write(''.join(self.content))
		parent.info_pte.appendPlainText(f'Updated {iniFile}')

	def get_sections(self):
		self.sections = {}
		end = len(self.content)
		for index, line in enumerate(self.content):
			if line.strip().startswith('['):
				self.sections[line.strip()] = [index, end]
		# set start and stop index for each section
		previous = None
		for key, value in self.sections.items():
			if previous:
				self.sections[previous][1] = value[0] - 1
			previous = key

	def update_key(self, section, key, value):
		found = False
		start = self.sections[f'[{section}]'][0]
		end = self.sections[f'[{section}]'][1]
		for item in self.content[start:end]:
			if item.split('=')[0].strip() == key:
				index = self.content.index(item, start, end)
				self.content[index] = f'{key} = {value}\n'
				found = True
				break
		if not found:
			self.content.insert(end, f'{key} = {value}\n')
			self.get_sections() # update section start/end

	def delete_key(self, section, key):
		start = self.sections[f'[{section}]'][0]
		end = self.sections[f'[{section}]'][1]
		for item in self.content[start:end]:
			if item.split('=')[0].strip() == key:
				index = self.content.index(item)
				del self.content[index]
				self.get_sections() # update section start/end

	def insert_section(self, index, section):
		self.content.insert(index, f'{section}\n')
		self.content.insert(index, '\n')
		self.get_sections() # update section start/end

	def delete_section(self, section):
		start, end = self.get_section_bounds(section)
		del self.content[start:end]
		self.get_sections() # update section start/end

	def get_section_bounds(self, section):
		start = self.sections[section][0]
		end = self.sections[section][1]
		return start, end

import os
from datetime import datetime

from PyQt5.QtWidgets import QSpinBox

class updateini:
	def __init__(self):
		super().__init__()
		self.content = ''
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

		tool_joints = {}
		joint = 0
		for i in range(4):
			for j in range(6):
				if getattr(parent, f'c{i}_axis_{j}').currentData():
					axis = getattr(parent, f'c{i}_axis_{j}').currentData()
					tool_joints[f'[JOINT_{joint}]'] = f'{axis}'
					#if f'[JOINT_{joint}]' in self.sections:
					#	print(f'Joint {joint} exists in the ini')
					#else:
					#	print(f'Joint {joint} needs to be added to the ini')
					#print(f'Joint {joint} Axis {axis}')
					joint += 1

		for key, value in tool_joints.items():
			print(f'Tool: {key} {value}')

		ini_joints = {}
		for key, value in self.sections.items():
			if key.startswith('[JOINT_'):
				start = value[0]
				end = value[1] + 1
				#print(f'Start: {value[0]} End: {value[1]} Range End: {value[1] + 1}')
				for item in self.content[start: end]:
					if item.split(' = ')[0].strip() == 'AXIS':
						#print(item.split('=')[1].strip())
						ini_joints[key] = item.split('=')[1].strip()

		for key, value in ini_joints.items():
			print(f'Ini: {key} {value}')

		if len(tool_joints) == len(ini_joints):
			print('Same number of joints, checking Axis Letters')
			for key, value in tool_joints.items():
				if tool_joints[key] != ini_joints[key]:
					new_axis = f'[AXIS_{tool_joints[key]}]'
					old_axis = f'[AXIS_{ini_joints[key]}]'
					# use the sections to find the axis maybe
					for line in self.content:
						if line.strip() == f'[AXIS_{ini_joints[key]}]':
							for index, line in enumerate(self.content):
								if line.strip() == old_axis:
									print(f'Index: {index} Old: {old_axis} New: {new_axis}')
									self.content[index] = f'{new_axis}\n'
									for line in self.content:
										parent.info_pte.appendPlainText(line.strip())

		# test for joints and axes removed
		elif len(tool_joints) < len(ini_joints):
			print('Joints removed')
			for key, value in ini_joints.items():
				if key not in tool_joints:
					print(f'Removing {key}')
					print(self.sections[key])
					start = self.sections[key][0]
					end = self.sections[key][1] + 1
					print(f'{start}:{end}')
					del self.content[start:end]
					self.get_sections()
					if value not in tool_joints.values():
						print(f'Remvoing [AXIS_{value}]')
						axis = f'[AXIS_{value}]'
						print(self.sections[axis])
						start = self.sections[axis][0]
						end = self.sections[axis][1] + 1
						del self.content[start:end]

			for line in self.content:
				parent.info_pte.appendPlainText(line.strip())

		elif len(tool_joints) > len(ini_joints):
			print('Joints added')
			for key, value in tool_joints.items():
				if key not in ini_joints:
					print(f'Adding {key}')
					if value not in ini_joints.values():
						print(f'Adding {value}')

			for line in self.content:
				parent.info_pte.appendPlainText(line.strip())

		return

		# test for new joints
		for key in tool_joints:
			if key not in ini_joints:
				print(f'Need to add {key}')
				joint = int(f'{key.split("_")[1][:-1]}')
				if joint > 0:
					last_joint = joint - 1
				else:
					print('no last joint rut-ro')
					return
				print(last_joint)
				index = self.sections[f'[JOINT_{last_joint}]'][1]
				print(index)

				# test for new axis before adding the joint
				# need a map of axes and joints somehow...
				for key, value in self.sections.items():
					if key.startswith('[AXIS_'):
						print(key)


				if index:
					#print(f'Adding [JOINT_{joint}]')
					self.insert_section(index, f'[JOINT_{joint}]')
				#for key, value in self.sections.items():
				#	print(f'Key: {key} Value: {value}')


		# as this gets sorted out move stuff from below
		self.write_ini(parent, iniFile)


		# test for new axes and insert axis after previous joint



		# test for joints to remove
		for key in ini_joints:
			if key not in tool_joints:
				print(f'Need to remove {key}')


		if parent.boardCB.currentData() == '7i92t':
			board = '7i92'
		else:
			board = parent.boardCB.currentData()

		mesa = [
		['MESA', 'VERSION', f'{parent.version}'],
		['MESA', 'BOARD', f'{board}'],
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
			['HM2', 'IPADDRESS', f'{parent.ipAddressCB.currentText()}']
			]
		else:
			self.delete_key('HM2', 'IPADDRESS')
		if parent.boardType == 'pci':
			hm2 = [['HM2', 'DRIVER', 'hm2_pci']]
		hm2.append(['HM2', 'STEPGENS', f'{parent.stepgens_cb.currentData()}'])
		hm2.append(['HM2', 'PWMGENS', f'{parent.pwmgens_cb.currentData()}'])
		hm2.append(['HM2', 'ENCODERS', f'{parent.encoders_cb.currentData()}'])
		for item in hm2:
			self.update_key(item[0], item[1], item[2])

		display = [
		['DISPLAY', 'DISPLAY', f'{parent.guiCB.itemData(parent.guiCB.currentIndex())}'],
		['DISPLAY', 'PROGRAM_PREFIX', f'{os.path.expanduser("~/linuxcnc/nc_files")}'],
		['DISPLAY', 'POSITION_OFFSET', f'{parent.positionOffsetCB.currentData()}'],
		['DISPLAY', 'POSITION_FEEDBACK', f'{parent.positionFeedbackCB.currentData()}'],
		['DISPLAY', 'MAX_FEED_OVERRIDE', f'{parent.maxFeedOverrideSB.value()}'],
		['DISPLAY', 'CYCLE_TIME', '0.1'],
		['DISPLAY', 'INTRO_GRAPHIC', f'{parent.introGraphicLE.text()}'],
		['DISPLAY', 'INTRO_TIME', f'{parent.splashScreenSB.value()}'],
		['DISPLAY', 'OPEN_FILE', f'""']
		]
		if parent.editorCB.currentData():
			display.append(['DISPLAY', 'EDITOR', f'{parent.editorCB.currentData()}'])
		else:
			self.delete_key('DISPLAY', 'EDITOR')
		if set('XYZUVW')&set(parent.coordinatesLB.text()):
			display.append(['DISPLAY', 'MIN_LINEAR_VELOCITY', f'{parent.minLinJogVelDSB.value()}'])
			display.append(['DISPLAY', 'DEFAULT_LINEAR_VELOCITY', f'{parent.defLinJogVelDSB.value()}'])
			display.append(['DISPLAY', 'MAX_LINEAR_VELOCITY', f'{parent.maxLinJogVelDSB.value()}'])
		else:
			self.delete_key('DISPLAY', 'MIN_LINEAR_VELOCITY')
			self.delete_key('DISPLAY', 'DEFAULT_LINEAR_VELOCITY')
			self.delete_key('DISPLAY', 'MAX_LINEAR_VELOCITY')
		if set('ABC')&set(parent.coordinatesLB.text()):
			display.append(['DISPLAY', 'MIN_ANGULAR_VELOCITY', f'{parent.minAngJogVelDSB.value()}'])
			display.append(['DISPLAY', 'DEFAULT_ANGULAR_VELOCITY', f'{parent.defAngJogVelDSB.value()}'])
			display.append(['DISPLAY', 'MAX_ANGULAR_VELOCITY', f'{parent.maxAngJogVelDSB.value()}'])
		else:
			self.delete_key('DISPLAY', 'MIN_ANGULAR_VELOCITY')
			self.delete_key('DISPLAY', 'DEFAULT_ANGULAR_VELOCITY')
			self.delete_key('DISPLAY', 'MAX_ANGULAR_VELOCITY')
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
		['RS274NGC', 'PARAMETER_FILE', f'{parent.configNameUnderscored}.var'],
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

		# [HAL]
		if parent.haluiCB.isChecked():
			self.update_key('HAL', 'HALUI', 'halui')

		# [HALUI]
		if parent.haluiCB.isChecked() and '[HALUI]' not in self.sections:
			section = '[HALUI]'
			index = self.sections['[HAL]'][1]
			self.insert_section(index, section)

		if '[HALUI]' in self.sections:
			index = self.sections['[HALUI]']
			if len(index) == 2:
				ini_mdi = []
				for i in range(index[0], index[1]):
					if self.content[i].startswith('MDI_COMMAND'):
						ini_mdi.append(self.content[i].split('=')[1].strip())
				tool_mdi = []
				for i in range(6):
					mdi_text = f'{getattr(parent, f"mdiCmdLE_{i}").text()}'
					if mdi_text:
						tool_mdi.append(f'{getattr(parent, f"mdiCmdLE_{i}").text()}')

				if len(ini_mdi) == len(tool_mdi):
					for i, j in enumerate(range(index[0] + 1, index[1])):
						if self.content[j].startswith('MDI_COMMAND'):
							self.content[j] = f'MDI_COMMAND = {getattr(parent, f"mdiCmdLE_{i}").text()}\n'
				elif len(ini_mdi) > len(tool_mdi):
					remove = len(ini_mdi) - len(tool_mdi)
					for i in reversed(range(index[0] + 1, index[1])):
						if self.content[i].startswith('MDI_COMMAND') and remove > 0:
							del self.content[i]
							remove -= 1
					self.get_sections() # update section start/end
				elif len(ini_mdi) < len(tool_mdi):
					add = len(tool_mdi) - len(ini_mdi)
					for i, j in enumerate(range(index[0] + 1, index[1] + add)):
						if self.content[j].startswith('MDI_COMMAND'): # replace it
							self.content[j] = f'MDI_COMMAND = {getattr(parent, f"mdiCmdLE_{i}").text()}\n'
						elif self.content[j].strip() == '': # insert it
							self.content.insert(j, f'MDI_COMMAND = {getattr(parent, f"mdiCmdLE_{i}").text()}\n')
					self.get_sections() # update section start/end

		############ Massive rework needed here
		# if the section exists and is in the tool update it
		# if the section exists but not in the tool delete it
		# if the section does not exist but is in the tool create it
		# coordinatesLB contains all the axes XYYZ
		# [AXIS_x] section

		# build axis joint(s) dictionaries
		tool_ja = {}
		joint = 0
		for i in range(4):
			for j in range(6):
				if getattr(parent, f'c{i}_axis_{j}').currentData():
					tool_ja[f'[JOINT_{joint}]'] = f'[AXIS_{getattr(parent, f"c{i}_axis_{j}").currentData()}]'
					joint += 1
		#for key, value in tool_ja.items():
		#	print(f'key: {key} value: {value}')

		ini_ja = {}
		for key, value in self.sections.items():
			if key.startswith('[JOINT'):
				for i in range(value[0], value[1]):
					if self.content[i].startswith('AXIS'):
						axis = self.content[i].strip()
						axis = axis.split()
						axis = f'[AXIS_{axis[-1]}]'
						ini_ja[key] = axis

		if len(tool_ja) == len(ini_ja):
			if tool_ja != ini_ja:
				for key in tool_ja.keys():
					if tool_ja[key] != ini_ja[key]:
						index = self.content.index(f'{ini_ja[key]}\n')
						if index:
							self.content[index] = f'{tool_ja[key]}\n'
							self.get_sections() # update section start/end

		elif len(tool_ja) > len(ini_ja):
			for key in ini_ja.keys(): # check for axis letter changed
				if tool_ja[key] != ini_ja[key]:
					index = self.content.index(f'{ini_ja[key]}\n')
					if index:
						self.content[index] = f'{tool_ja[key]}\n'
						self.get_sections() # update section start/end

			ini_axes = []
			for key, value in ini_ja.items(): # get a list of axes
				if value not in ini_axes:
					ini_axes.append(value)

			last_axis = ''
			last_joint = ''
			# this fails if more than one joint is added !!!!!!!!!!!
			for key, value in tool_ja.items(): # add missing axis
				if tool_ja[key] not in ini_axes:
					print(f'key: {key}')
					index = self.sections[last_joint][1]
					if index:
						self.insert_section(index, f'{tool_ja[key]}')
				last_joint = key

			for key, value in tool_ja.items(): # add missing joint after last axis
				if key not in ini_ja.keys():
					index = self.sections[value][1]
					self.insert_section(index, f'{key}')

		elif len(tool_ja) < len(ini_ja): # joint removed
			for joint, axis in ini_ja.items():
				if joint not in tool_ja:
					self.delete_section(joint)
					self.delete_section(axis)

		# finally update the [AXIS_n] and [JOINT_n] sections
		axes = []
		n = 0 # joint number
		for i in range(4):
			for j in range(6):
				axis = getattr(parent, f'c{i}_axis_{j}').currentData()
				if axis and axis not in axes:
					axes.append(axis)
					self.update_key(f'AXIS_{axis}', 'MIN_LIMIT', getattr(parent, f'c{i}_min_limit_{j}').text())
					self.update_key(f'AXIS_{axis}', 'MAX_LIMIT', getattr(parent, f'c{i}_max_limit_{j}').text())
					self.update_key(f'AXIS_{axis}', 'MAX_VELOCITY', getattr(parent, f'c{i}_max_vel_{j}').text())
					self.update_key(f'AXIS_{axis}', 'MAX_ACCELERATION', getattr(parent, f'c{i}_max_accel_{j}').text())
				#iniContents.append(f'CARD = {i}\n')
				#iniContents.append(f'TAB = {j}\n')

				if getattr(parent, f'c{i}_axis_{j}').currentData():
					self.update_key(f'JOINT_{n}', 'CARD', f'{i}')
					self.update_key(f'JOINT_{n}', 'TAB', f'{j}')
					self.update_key(f'JOINT_{n}', 'AXIS', getattr(parent, f'c{i}_axis_{j}').currentData())
					self.update_key(f'JOINT_{n}', 'MIN_LIMIT', getattr(parent, f'c{i}_min_limit_{j}').text())
					self.update_key(f'JOINT_{n}', 'MAX_LIMIT', getattr(parent, f'c{i}_max_limit_{j}').text())
					self.update_key(f'JOINT_{n}', 'MAX_VELOCITY', getattr(parent, f'c{i}_max_vel_{j}').text())
					self.update_key(f'JOINT_{n}', 'MAX_ACCELERATION', getattr(parent, f'c{i}_max_accel_{j}').text())
					self.update_key(f'JOINT_{n}', 'TYPE', getattr(parent, f'c{i}_axisType_{j}').text())
					if getattr(parent, f'c{i}_reverse_{j}').isChecked():
						self.update_key(f'JOINT_{n}', 'SCALE', f'-{getattr(parent, f"c{i}_scale_{j}").text()}')
					else:
						self.update_key(f'JOINT_{n}', 'SCALE', f'{getattr(parent, f"c{i}_scale_{j}").text()}')

					if not getattr(parent, f'c{i}_stepgenGB_{j}').isHidden():
						self.update_key(f'JOINT_{n}', 'DRIVE', getattr(parent, f'c{i}_drive_{j}').currentText())
						self.update_key(f'JOINT_{n}', 'STEP_INVERT', getattr(parent, f'c{i}_StepInvert_{j}').isChecked())
						self.update_key(f'JOINT_{n}', 'DIR_INVERT', getattr(parent, f'c{i}_DirInvert_{j}').isChecked())
						self.update_key(f'JOINT_{n}', 'STEPGEN_MAX_VEL', f'{float(getattr(parent, f"c{i}_max_vel_{j}").text()) * 1.2:.2f}')
						self.update_key(f'JOINT_{n}', 'STEPGEN_MAX_ACC', f'{float(getattr(parent, f"c{i}_max_accel_{j}").text()) * 1.2:.2f}')
						self.update_key(f'JOINT_{n}', 'DIRSETUP', getattr(parent, f'c{i}_DirSetup_{j}').text())
						self.update_key(f'JOINT_{n}', 'DIRHOLD', getattr(parent, f'c{i}_DirHold_{j}').text())
						self.update_key(f'JOINT_{n}', 'STEPLEN', getattr(parent, f'c{i}_StepTime_{j}').text())
						self.update_key(f'JOINT_{n}', 'STEPSPACE', getattr(parent, f'c{i}_StepSpace_{j}').text())

					if not getattr(parent, f'c{i}_analogGB_{j}').isHidden():
						self.update_key(f'JOINT_{n}', 'ENCODER_SCALE', getattr(parent, f'c{i}_encoderScale_{j}').text())
						self.update_key(f'JOINT_{n}', 'ANALOG_SCALE_MAX', getattr(parent, f'c{i}_analogScaleMax_{j}').text())
						self.update_key(f'JOINT_{n}', 'ANALOG_MIN_LIMIT', getattr(parent, f'c{i}_analogMinLimit_{j}').text())
						self.update_key(f'JOINT_{n}', 'ANALOG_MAX_LIMIT', getattr(parent, f'c{i}_analogMaxLimit_{j}').text())

					self.update_key(f'JOINT_{n}', 'FERROR', getattr(parent, f'c{i}_ferror_{j}').text())
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
					if getattr(parent, f"c{i}_home_" + str(i)).text():
						self.update_key(f'JOINT_{n}', 'HOME', getattr(parent, f"c{i}_home_{j}").text())
					if getattr(parent, f"c{i}_homeOffset_{j}").text():
						self.update_key(f'JOINT_{n}', 'HOME_OFFSET', getattr(parent, f"c{i}_homeOffset_{j}").text())
					if getattr(parent, f"c{i}_homeSearchVel_{j}").text():
						self.update_key(f'JOINT_{n}', 'HOME_SEARCH_VEL', getattr(parent, f"c{i}_homeSearchVel_{j}").text())
					if getattr(parent, f"c{i}_homeLatchVel_{j}").text():
						self.update_key(f'JOINT_{n}', 'HOME_LATCH_VEL', getattr(parent, f"c{i}_homeLatchVel_{j}").text())
					if getattr(parent, f"c{i}_homeFinalVelocity_{j}").text():
						self.update_key(f'JOINT_{n}', 'HOME_FINAL_VEL', getattr(parent, f"c{i}_homeFinalVelocity_{j}").text())
					if getattr(parent, f"c{i}_homeSequence_{j}").text():
						self.update_key(f'JOINT_{n}', 'HOME_SEQUENCE', getattr(parent, f"c{i}_homeSequence_{j}").text())
					if getattr(parent, f"c{i}_homeIgnoreLimits_{j}").isChecked():
						self.update_key(f'JOINT_{n}', 'HOME_IGNORE_LIMITS', True)
					if getattr(parent, f"c{i}_homeUseIndex_{j}").isChecked():
						self.update_key(f'JOINT_{n}', 'HOME_USE_INDEX', True)
					if getattr(parent, f"c{i}_homeSwitchShared_{j}").isChecked():
						self.update_key(f'JOINT_{n}', 'HOME_IS_SHARED', True)
					n += 1 # add a joint

		'''
		# update the [SPINDLE_0] section
		if parent.spindleTypeCB.currentData():
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

			self.update_key(f'SPINDLE_0', 'SPINDLE_TYPE', parent.spindleTypeCB.currentData())
			if parent.spindlePwmTypeCB.currentText() != 'Select':
				self.update_key(f'SPINDLE_0', 'SPINDLE_PWM_TYPE', parent.spindlePwmTypeCB.currentData())
				self.update_key(f'SPINDLE_0', 'PWM_FREQUENCY', parent.pwmFrequencySB.value())

			if parent.spindleTypeCB.currentData() == 'analog':
				self.update_key(f'SPINDLE_0', 'MAX_RPM', parent.spindleMaxRpm.value())
				self.update_key(f'SPINDLE_0', 'MIN_RPM', parent.spindleMinRpm.value())

			if parent.spindleFeedbackCB.currentData() == 'encoder':
				self.update_key(f'SPINDLE_0', 'FEEDBACK', parent.spindleFeedbackCB.currentData())
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
		for i in range(4):
			for j in range(32):
				if getattr(parent, f'c{i}_input_{j}').text() != 'Select':
					self.update_key('INPUTS', f'INPUT_{i}_{j}', getattr(parent, f'c{i}_input_{j}').text())
					self.update_key('INPUTS', f'INPUT_INVERT_{i}_{j}', getattr(parent, f'c{i}_input_invert_{j}').isChecked())
					self.update_key('INPUTS', f'INPUT_SLOW_{i}_{j}', getattr(parent, f'c{i}_input_debounce_{j}').isChecked())

		# update the [OUTPUTS] section
		for i in range(4):
			for j in range(16):
				if getattr(parent, f'c{i}_output_{j}').text() != 'Select':
					self.update_key('OUTPUTS', f'OUTPUT_{i}_{j}', getattr(parent, f'c{i}_output_{j}').text())
					self.update_key('OUTPUTS', f'OUTPUT_INVERT_{i}_{j}', getattr(parent, f'c{i}_output_invert_{j}').isChecked())

		# update the [OPTIONS] section
		options = [
		['OPTIONS', 'LOAD_CONFIG', f'{parent.loadConfigCB.isChecked()}'],
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
				index = self.content.index(item)
				self.content[index] = f'{key} = {value}\n'
				found = True
				break
			else:
				found = False
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
		#print(f'index {index} section {section}')
		self.content.insert(index, f'{section}\n')
		self.content.insert(index, '\n')
		#print(self.content)
		self.get_sections() # update section start/end
		#print(self.sections)

	def delete_section(self, section):
		start = self.sections[section][0]
		end = self.sections[section][1]
		del self.content[start:end]
		self.get_sections() # update section start/end



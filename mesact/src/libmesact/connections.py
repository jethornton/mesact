

def connect(parent):
	# Menu Items
	parent.actionNew.triggered.connect(partial(utilities.new_config, parent))
	parent.actionOpen.triggered.connect(partial(parent.loadini.checkini, parent))
	parent.actionCheck.triggered.connect(partial(check.checkit, parent))
	parent.actionBuild.triggered.connect(partial(buildconfig.build, parent))
	#parent.actionTabHelp.triggered.connect(partial(parent.help, 0))
	parent.actionMesaCT_PC_64_bit.triggered.connect(partial(downloads.downloadAmd64Deb, parent))
	parent.actionMesaCT_Rpi_32_bit.triggered.connect(partial(downloads.downloadArmhDeb, parent))
	parent.actionMesaCT_Rpi_64_bit.triggered.connect(partial(downloads.downloadArm64Deb, parent))
	parent.actionFirmware.triggered.connect(partial(downloads.downloadFirmware, parent))
	parent.actionDocuments.triggered.connect(partial(documents.openDoc, parent))
	parent.actionCheckUpdates.triggered.connect(partial(updates.checkUpdates, parent))
	parent.actionAboutMesaCT.triggered.connect(partial(dialogs.aboutDialog, parent))
	#parent.actionBoardImages.triggered.connect(partial(updates.boardImages, parent))
	parent.timer.timeout.connect(partial(downloads.clearProgressBar, parent))

	# Machine Tab
	parent.configNameLE.textChanged[str].connect(partial(machine.configNameChanged, parent))
	parent.boardCB.currentIndexChanged.connect(partial(boards.boardChanged, parent))
	for i in range(2):
		getattr(parent, f'daughterCB_{i}').currentIndexChanged.connect(partial(daughters.changed, parent))
	parent.checkBoardPB.clicked.connect(partial(flash.checkCard, parent))

	'''
	parent.enableMesaflashCB.clicked.connect(partial(utilities.firmwareTools, parent))
	parent.enableMesaflashCB.clicked.connect(partial(settings.update_value, parent))
	parent.backupCB.clicked.connect(partial(utilities.backup, parent))
	'''
	parent.default_imperial_pb.clicked.connect(partial(testing.default_imperial, parent))
	parent.default_metric_pb.clicked.connect(partial(testing.default_metric, parent))
	parent.set_7i96s_x_pb.clicked.connect(partial(testing.set_7i96s_x, parent))
	parent.set_7i96s_xyz_pb.clicked.connect(partial(testing.set_7i96s_xyz, parent))
	parent.set_7i96s_xyyz_pb.clicked.connect(partial(testing.set_7i96s_xyyz, parent))
	parent.set_7i96s_7i77_pb.clicked.connect(partial(testing.set_7i96s_7i77, parent))
	parent.set_7i92t_p1_7i76_pb.clicked.connect(partial(testing.set_7i92t_p1_7i76, parent))
	parent.set_7i92t_p2_7i76_pb.clicked.connect(partial(testing.set_7i92t_p2_7i76, parent))
	parent.set_7i92t_p2_7i77_pb.clicked.connect(partial(testing.set_7i92t_p2_7i77, parent))

	# Settings Tab
	parent.minLinJogVelDSB.valueChanged.connect(partial(utilities.unitsChanged, parent))
	parent.defLinJogVelDSB.valueChanged.connect(partial(utilities.unitsChanged, parent))
	parent.maxLinJogVelDSB.valueChanged.connect(partial(utilities.unitsChanged, parent))
	parent.minAngJogVelDSB.valueChanged.connect(partial(utilities.unitsChanged, parent))
	parent.defAngJogVelDSB.valueChanged.connect(partial(utilities.unitsChanged, parent))
	parent.maxAngJogVelDSB.valueChanged.connect(partial(utilities.unitsChanged, parent))
	parent.axisButtonGroup.setExclusive(False)  # Radio buttons are not exclusive
	parent.axisButtonGroup.buttonClicked.connect(partial(utilities.axisDisplayChanged, parent))
	parent.linearUnitsCB.currentIndexChanged.connect(partial(utilities.unitsChanged, parent))
	parent.trajMaxLinVelDSB.valueChanged.connect(partial(utilities.maxVelChanged, parent))

	'''
	#parent.frontToolLatheRB.buttonClicked.connect(partial(utilities.axisDisplayChanged, parent))
	#parent.backToolLatheRB.buttonClicked.connect(partial(utilities.axisDisplayChanged, parent))
	#parent.foamRB.buttonClicked.connect(partial(utilities.axisDisplayChanged, parent))
	'''

	# Firmware Tab
	parent.firmwareCB.currentIndexChanged.connect(partial(firmware.firmwareChanged, parent))
	parent.readhmidPB.clicked.connect(partial(flash.readhmid, parent))
	parent.readpdPB.clicked.connect(partial(flash.readpd, parent))
	parent.flashPB.clicked.connect(partial(flash.flashCard, parent))
	parent.reloadPB.clicked.connect(partial(flash.reloadCard, parent))
	parent.verifyPB.clicked.connect(partial(flash.verifyFirmware, parent))
	parent.copyPB.clicked.connect(partial(flash.copyOutput, parent))

	# Info Tab

	# Axes Tab
	# for now just do one card
	#j = 0
	for j in range(3):
		for i in range(5):
			getattr(parent, f'c{j}_copy_values_{i}').clicked.connect(partial(utilities.copyValues, parent))

	for i in range(6):
		for j in range(3): # <-- change when more cards are added
			getattr(parent, f'c{j}_axis_{i}').currentIndexChanged.connect(partial(axes.axisChanged, parent))
			getattr(parent, f'c{j}_scale_{i}').textChanged.connect(partial(axes.updateAxisInfo, parent))
			getattr(parent, f'c{j}_max_vel_{i}').textChanged.connect(partial(axes.updateAxisInfo, parent))
			getattr(parent, f'c{j}_max_accel_{i}').textChanged.connect(partial(axes.updateAxisInfo, parent))
			getattr(parent, f'c{j}_pidDefault_{i}').clicked.connect(partial(axes.pidSetDefault, parent))
			getattr(parent, f'c{j}_ferrorDefault_{i}').clicked.connect(partial(axes.ferrorSetDefault, parent))
			getattr(parent, f'c{j}_analogDefault_{i}').clicked.connect(partial(axes.analogSetDefault, parent))
			getattr(parent, f'c{j}_drive_{i}').currentIndexChanged.connect(partial(axes.driveChanged, parent))

	# I/O Tab
	for i in range(3):
		for j in range(32):
			getattr(parent, f'c{i}_input_invert_{j}').stateChanged.connect(partial(utilities.inputChanged, parent))
			getattr(parent, f'c{i}_input_debounce_{j}').stateChanged.connect(partial(utilities.inputChanged, parent))

	# Spindle Tab
	parent.output_type = '' # hostmot2 output-type
	parent.spindleTypeCB.currentIndexChanged.connect(partial(spindle.spindle_type_changed, parent))
	parent.pidDefault_s.clicked.connect(partial(spindle.spindle_pid_default, parent))
	'''
	parent.spindleFeedbackCB.currentIndexChanged.connect(partial(utilities.spindleFeedbackChanged, parent))
	parent.spindleDriveCB.currentIndexChanged.connect(partial(utilities.driveChanged, parent))
	parent.spindleMinRpm.valueChanged.connect(partial(utilities.spindleSettingsChanged, parent))
	parent.spindleMaxRpm.valueChanged.connect(partial(utilities.spindleSettingsChanged, parent))
	parent.spindleMaxAccel.valueChanged.connect(partial(utilities.spindleSettingsChanged, parent))
	'''
	# Smart Serial Tab
	parent.ssCardCB.currentIndexChanged.connect(partial(sscards.ssCardChanged, parent))
	parent.ss7i73_keypadCB.currentIndexChanged.connect(partial(sscards.ss7i73Changed, parent))
	parent.ss7i73lcdCB.currentIndexChanged.connect(partial(sscards.ss7i73Changed, parent))
	'''

	# HAL Tab
	parent.buildHalPB.clicked.connect(partial(hal.buildHal, parent))
	for i in range(6):
		getattr(parent, f'halFunctionCB_{i}').currentIndexChanged.connect(partial(hal.functionChanged, parent))
	for i in range(4):
		getattr(parent, f'functionCountSB_{i}').valueChanged.connect(partial(hal.countChanged, parent))

	# Pins Tab
	parent.cardPinsPB.clicked.connect(partial(card.getCardPins, parent))
	'''
	# PC Tab st_cpu_speed_pb
	parent.mb_info_PB.clicked.connect(partial(pcinfo.mbInfo, parent))
	parent.nic_cpu_speed_pb.clicked.connect(partial(pcinfo.cpuSpeed, parent))
	parent.nicPB.clicked.connect(partial(pcinfo.nicInfo, parent))
	parent.ip_nic_PB.clicked.connect(partial(pcinfo.ipInfo, parent))
	parent.servoThreadTmaxPB.clicked.connect(partial(pcinfo.servoTmax, parent))
	parent.st_cpu_speed_pb.clicked.connect(partial(pcinfo.cpuSpeed, parent))
	parent.calcServoPB.clicked.connect(partial(pcinfo.calcServoPercent, parent))
	parent.readTmaxPB.clicked.connect(partial(pcinfo.readTmax, parent))
	parent.writeTmaxPB.clicked.connect(partial(pcinfo.writeTmax, parent))
	parent.calcNicPB.clicked.connect(partial(pcinfo.nicCalc, parent))
	parent.cpu_info_pb.clicked.connect(partial(pcinfo.cpuInfo, parent))
	#parent.latencyTestPB.clicked.connect(partial(tools.runLatencyHisogram, parent))

	# Options Tab
	parent.no_check_firmware_cb.clicked.connect(partial(settings.update_settings, parent))
	# check load_config_cb when building only...
	#parent.load_config_cb.toggled.connect(partial(settings.update_settings, parent))
	#parent.checkMesaflashCB.clicked.connect(partial(settings.update_value, parent))
	#parent.newUserCB.clicked.connect(partial(settings.update_value, parent))


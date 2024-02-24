import os, subprocess, sysconfig
from platform import python_version
from functools import partial

from PyQt5.QtCore import qVersion, QRegExp, QLocale
from PyQt5.QtGui import  QIcon, QIntValidator, QDoubleValidator, QRegExpValidator
from PyQt5.QtWidgets import QAction, QCheckBox, QLineEdit, QPlainTextEdit
from PyQt5.QtWidgets import QComboBox, QSpinBox, QDoubleSpinBox, QCheckBox

from libmesact import combos
from libmesact import menus
from libmesact import updates
from libmesact import utilities

def setup(parent):

	# setup must have variables
	# board names must be set before loading a config at startup
	parent.board_0 = False
	parent.board_1 = False
	parent.board_2 = False

	parent.platformLB.setText(sysconfig.get_platform())
	parent.pythonLB.setText(python_version())
	parent.pyqt5LB.setText(qVersion())

	try: # need to set this before building combos
		jet = subprocess.check_output(['apt-cache', 'policy', 'jet'], text=True)
		if len(jet) > 0:
			version = jet.split()[2]
			parent.jet_gui_lb.setText(f'{version}')
			parent.jet_gui = True
		else:
			parent.jet_gui_lb.setText('Not Installed')
			parent.jet_gui = False
	except:
		#jet = None
		pass

	combos.build(parent)
	# disable some boards until programmed
	#parent.boardCB.model().item(1).setEnabled(False) # 5i24/6i24
	#parent.boardCB.model().item(6).setEnabled(False) # 7i80db16
	#parent.boardCB.model().item(7).setEnabled(False) # 7i80db25
	#parent.boardCB.model().item(8).setEnabled(False) # 7i80hd16
	#parent.boardCB.model().item(9).setEnabled(False) # 7i80hd25
	#parent.boardCB.model().item(10).setEnabled(False) # 7i80hdts

	menus.build(parent)

	# set tab visibility
	parent.mainTW.setTabVisible(3, False)
	parent.mainTW.setTabVisible(4, False)
	parent.mainTW.setTabVisible(5, False)

	parent.hal_tw.setTabVisible(1, False)
	parent.hal_tw.setTabVisible(2, False)
	parent.hal_tw.setTabVisible(3, False)

	libpath = os.path.join(os.path.expanduser('~'), '.local/lib/libmesact/boards')
	if not os.path.exists(libpath):
		os.makedirs(libpath)

	try:
		parent.resize(parent.settings.value('GUI/window_size'))
		parent.move(parent.settings.value('GUI/window_position'))
		parent.no_check_firmware_cb.setChecked(True if parent.settings.value('NAGS/firmware') == "true" else False)
	except:
		pass

	if parent.settings.contains('STARTUP/config'):
		if parent.settings.value('STARTUP/config', False, type=bool):
			config_file = parent.settings.value('STARTUP/config')
			if os.path.isfile(config_file):
				parent.loadini.load_ini(parent, config_file)

	parent.configNameLE.setFocus()

	exitAction = QAction(QIcon.fromTheme('application-exit'), 'Exit', parent)
	exitAction.setStatusTip('Exit application')
	exitAction.triggered.connect(parent.close)
	parent.menuFile.addAction(exitAction)

	docsAction = QAction(QIcon.fromTheme('document-open'), 'Mesa Manuals', parent)
	docsAction.setStatusTip('Download Mesa Documents')
	docsAction.triggered.connect(partial(updates.downloadDocs, parent))
	parent.menuDownloads.addAction(docsAction)

	# Firmware tab

	# get emc version if installed
	parent.emcVersionLB.clear()
	parent.emc_version = (0, 0, 0)
	try: # don't crash if your not running debian
		emc = subprocess.check_output(['apt-cache', 'policy', 'linuxcnc-uspace'], encoding='UTF-8')
	except:
		emc = False
		pass

	if emc.count('\n') > 1:
		# get second line
		line = emc.split('\n')[1]
		version = line.split()[1]

		if ':' in version:
			version = version.split(':')[1]
			version = '.'.join(version.split('.', 3)[:3])
		if '~' in version:
			version = version.split('~')[0]
		# make damn sure version is valid
		if all(c in "0123456789." for c in version) and version.count('.') > 1:
			parent.emcVersionLB.setText(version)
			parent.emc_version = tuple(int(i) for i in version.split('.'))
		else:
			parent.emcVersionLB.setText('Version Error')
	else:
		parent.emcVersionLB.setText('Not Installed')

	try:
		mf = subprocess.check_output('mesaflash', encoding='UTF-8')
		if len(mf) > 0:
			version = mf.split()[2]
			parent.mesaflash_version = tuple(int(i) for i in version.split('.'))
			parent.mesaflashVersionLB.setText(version)
			parent.mesaflash = True
	except FileNotFoundError as error:
		parent.firmwareGB.setEnabled(False)
		parent.verify_board_pb.setEnabled(False)
		parent.mesaflashVersionLB.setText('Not Installed')
		parent.mesaflash = False
		parent.mesaflash_version = ()

	try:
		os_name = subprocess.check_output(['lsb_release', '-is'], encoding='UTF-8').split()
		os_version = subprocess.check_output(['lsb_release', '-rs'], encoding='UTF-8').split()
		parent.os_name_lb.setText(f'{os_name[0]} {os_version[0]}')
		code_name = subprocess.check_output(['lsb_release', '-cs'], encoding='UTF-8').split()
		parent.os_code_name_lb.setText(f'{code_name[0].title()}')
	except:
		parent.os_name_lb.setText('OS Unknown')
		parent.os_code_name_lb.setText('No Codename')

	# Change Events
	for child in parent.findChildren(QPlainTextEdit):
		child.textChanged.connect(partial(utilities.changed, parent))
	for child in parent.findChildren(QLineEdit):
		child.textChanged.connect(partial(utilities.changed, parent))
	for child in parent.findChildren(QComboBox):
		child.currentIndexChanged.connect(partial(utilities.changed, parent))
	for child in parent.findChildren(QSpinBox):
		child.valueChanged.connect(partial(utilities.changed, parent))
	for child in parent.findChildren(QDoubleSpinBox):
		child.valueChanged.connect(partial(utilities.changed, parent))
	for child in parent.findChildren(QCheckBox):
		child.stateChanged.connect(partial(utilities.changed, parent))

	# allow only integers
	only_int = QIntValidator()
	c_locale = QLocale(QLocale.C)
	only_int.setLocale(c_locale)

	only_numbers = QDoubleValidator()
	#only_numbers.setNotation(QDoubleValidator.StandardNotation)
	only_numbers.setLocale(c_locale)
	#validator = QRegExpValidator(QRegExp(r'[0-9].+'))
	#self.lineEdit.setValidator(validator)

	#only_numbers.setNumberOptions(QLocale.RejectGroupSeparator)
	parent.lin_steps_rev_le.setValidator(only_int)
	parent.lin_microsteps_le.setValidator(only_int)
	parent.lin_stepper_teeth_le.setValidator(only_int)
	parent.lin_leadscrew_teeth_le.setValidator(only_int)
	parent.lin_leadscrew_pitch_le.setValidator(only_numbers)
	parent.angular_steps_rev_le.setValidator(only_int)

	# c0_scale_0 c0_min_limit_0 c0_max_limit_0 c0_max_vel_0 c0_max_accel_0
	float_list = ['_scale_', '_min_limit_', '_max_limit_', '_max_vel_',
	'_max_accel_']
	for item in float_list:
		for i in range(3):
			for j in range(6):
				getattr(parent, f'c{i}{item}{j}').setValidator(only_numbers)



import os, subprocess, sysconfig
from platform import python_version
from functools import partial

from PyQt5.QtCore import qVersion
from PyQt5.QtGui import  QIcon
from PyQt5.QtWidgets import QAction, QCheckBox, QLineEdit, QPlainTextEdit
from PyQt5.QtWidgets import QComboBox, QSpinBox, QDoubleSpinBox, QCheckBox

from libmesact import combos
from libmesact import menus
from libmesact import updates
from libmesact import utilities

def setup(parent):

	parent.platformLB.setText(sysconfig.get_platform())
	parent.pythonLB.setText(python_version())
	parent.pyqt5LB.setText(qVersion())

	combos.build(parent)
	# disable some boards until programmed
	parent.boardCB.model().item(1).setEnabled(False) # 5i24/6i24
	parent.boardCB.model().item(5).setEnabled(False) # 7i80db25
	parent.boardCB.model().item(6).setEnabled(False) # 7i80hd16
	parent.boardCB.model().item(7).setEnabled(False) # 7i80hd25
	parent.boardCB.model().item(8).setEnabled(False) # 7i80hdts

	menus.build(parent)

	# set tab visibility
	parent.mainTW.setTabVisible(3, False)
	parent.mainTW.setTabVisible(4, False)
	parent.mainTW.setTabVisible(5, False)

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
				parent.loadini.loadini(parent, config_file)

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
	try: # don't crash if your not running debian
		emc = subprocess.check_output(['apt-cache', 'policy', 'linuxcnc-uspace'], encoding='UTF-8')
	except:
		emc = None
		pass

	if emc:
		# get second line
		line = emc.split('\n')[1]
		version = line.split()[1]
		if ':' in version:
			version = version.split(':')[1]
		if '+' in version:
			version = version.split('+')[0]
		if 'none' in version:
			parent.emcVersionLB.setText('Not Installed')
		else:
			parent.emcVersionLB.setText(version)

	try:
		mf = subprocess.check_output('mesaflash', encoding='UTF-8')
		if len(mf) > 0:
			version = mf.split()[2]
			parent.mesaflash_version = tuple(int(i) for i in version.split('.'))
			parent.mesaflashVersionLB.setText(version)
			parent.mesaflash = True
	except FileNotFoundError as error:
		parent.firmwareGB.setEnabled(False)
		parent.checkBoardPB.setEnabled(False)
		parent.mesaflashVersionLB.setText('Not Installed')
		parent.mesaflash = False
		parent.mesaflash_version = ()

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


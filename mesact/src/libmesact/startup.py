import os, subprocess, sysconfig
from platform import python_version
from functools import partial

from PyQt5.QtCore import qVersion
from PyQt5.QtGui import  QIcon
from PyQt5.QtWidgets import QAction

from libmesact import combos
from libmesact import menus
from libmesact import updates

def setup(parent):

	parent.platformLB.setText(sysconfig.get_platform())
	parent.pythonLB.setText(python_version())
	parent.pyqt5LB.setText(qVersion())

	combos.build(parent)
	menus.build(parent)

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

	# set tab visibility
	parent.mainTW.setTabVisible(3, False)
	parent.mainTW.setTabVisible(4, False)
	parent.mainTW.setTabVisible(5, False)

	# Firmware tab

	# get emc version if installed
	parent.emcVersionLB.clear()
	try: # don't crash if your not running debian
		emc = subprocess.check_output(['apt-cache', 'policy', 'linuxcnc-uspace'], encoding='UTF-8')
	except:
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
			installed = mf.split()[2]
			parent.mesaflashVersionLB.setText(installed)
			parent.firmwareGB.setEnabled(True)
			parent.checkBoardPB.setEnabled(True)
	except FileNotFoundError as error:
		parent.firmwareGB.setEnabled(False)
		parent.checkBoardPB.setEnabled(False)
		parent.mesaflashVersionLB.setText('Not Installed')



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

	libpath = os.path.join(os.path.expanduser('~'), '.local/lib/libmesact/boards')
	if not os.path.exists(libpath):
		os.makedirs(libpath)

	try:
		parent.resize(parent.settings.value('window size'))
		parent.move(parent.settings.value('window position'))
	except:
		pass
	parent.configNameLE.setFocus()

	# tests
	msg = ('Current Tests\n'
	'Copy example configs into ~/linuxcnc/configs\n'
	'Open 1 = single axis Open 2 = two axes Open 3 = 3 axes Open 3G = 3 axes 4 joints gantry\n'
	'\n'
	'Open a sample config and change the axis letter(s),and/or\n'
	'add or delete axis or axes then Build Config.\n'
	'\n'
	'Note: to delete an axis just change the axis to Select\n'
	'\n'
	'Check the generated INI in the Info tab for correct\n'
	'axis and joint entries\n'
	'\n'
	'Correct is axis then the jointfor gantry one axis then the two or more joints\n'
	'for that axis\n'
	'\n'
	'Note: the only required entries are Max Vel and Max Accel\n'
	'use the Copy Values button to copy to the next joint\n'
	'\n'
	'To build the INI file when updating check the Update Build INI in the Settings Tab\n'
	)
	parent.tests_pte.setPlainText(msg)
	parent.mainTW.setCurrentIndex(12)

	# temp show progress
	msg = ('Item Status\n'
	'Only currently avaliable boards are supported\n'
	'at this time, more will be added in the future.\n'
	'Build deb and install: Complete and Tested\n'
	'Build, Load & Update ini: Partial in progress\n'
	'\tAxes: Complete and Tested\n'
	'\tInputs: Complete and Tested\n'
	'\tOutputs: Complete and Tested\n'
	'\tPLC: Complete and Tested\n'
	'\tSmart Serial: Complete and Tested\n'
	'\tSpindle: Partial in progress\n'
	'Build hal: To Do\n'
	'Build io: To Do\n'
	'Build ss: To Do\n'
	'Firmware: Complete but untested\n'
	'Download Manuals and Firmware: Complete and Tested\n'
	)
	parent.info_pte.setPlainText(msg)
	#parent.mainTW.setCurrentIndex(11)

	exitAction = QAction(QIcon.fromTheme('application-exit'), 'Exit', parent)
	#exitAction.setShortcut('Ctrl+Q')
	exitAction.setStatusTip('Exit application')
	exitAction.triggered.connect(parent.close)
	parent.menuFile.addAction(exitAction)

	docsAction = QAction(QIcon.fromTheme('document-open'), 'Mesa Manuals', parent)
	docsAction.setStatusTip('Download Mesa Documents')
	#preferencesAction.triggered.connect(partial(menu.edit_preferences, parent))
	docsAction.triggered.connect(partial(updates.downloadDocs, parent))
	parent.menuDownloads.addAction(docsAction)

	# set tab visibility
	parent.mainTW.setTabVisible(3, False)
	parent.mainTW.setTabVisible(4, False)
	parent.mainTW.setTabVisible(5, False)
	parent.mainTW.setTabVisible(6, False)

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

	parent.platformLB.setText(sysconfig.get_platform())
	parent.pythonLB.setText(python_version())
	parent.pyqt5LB.setText(qVersion())

	combos.build(parent)
	menus.build(parent)

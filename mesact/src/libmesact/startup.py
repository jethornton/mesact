import os, subprocess
from functools import partial

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

	# temp show progress
	msg = ('Item Status\n'
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
	emc = subprocess.check_output(['apt-cache', 'policy', 'linuxcnc-uspace'], encoding='UTF-8')
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

	combos.build(parent)
	menus.build(parent)

import os, subprocess
from functools import partial

from libmesact import combos

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
	'Build deb and install: Complete and tested\n'
	'Build ini: Partial in progress\n'
	'Open ini: Partial in progress\n'
	'Update ini: Partial in progress\n'
	'Build hal: To Do\n'
	'Configure ss: To Do\n'
	'Build ss: To Do\n'
	'Firmware: Complete but untested\n'
	)
	parent.infoPTE.setPlainText(msg)
	parent.mainTW.setCurrentIndex(11)

	# set tab visibility
	parent.mainTW.setTabVisible(3, False)
	parent.mainTW.setTabVisible(4, False)
	parent.mainTW.setTabVisible(5, False)
	parent.mainTW.setTabVisible(6, False)

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

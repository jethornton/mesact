import os, traceback

from libmesact import settings

from libmesact import check
from libmesact import buildini
from libmesact import buildhal
from libmesact import buildhal2
from libmesact import buildio
from libmesact import buildmisc
from libmesact import utilities

def build(parent):
	if not parent.testing:
		if not check.checkit(parent):
			return

	if parent.backupCB.isChecked():
		utilities.backupFiles(parent)

	# check for linuxcnc paths
	if not os.path.exists(os.path.expanduser('~/linuxcnc')):
		try:
			os.mkdir(os.path.expanduser('~/linuxcnc'))
		except OSError:
			parent.info_pte.appendPlainText(f'OS error\n {traceback.print_exc()}')

	if not os.path.exists(os.path.expanduser('~/linuxcnc/configs')):
		try:
			os.mkdir(os.path.expanduser('~/linuxcnc/configs'))
		except OSError:
			parent.info_pte.appendPlainText(f'OS error\n {traceback.print_exc()}')

	if not os.path.exists(os.path.expanduser('~/linuxcnc/nc_files')):
		try:
			os.mkdir(os.path.expanduser('~/linuxcnc/nc_files'))
		except OSError:
			parent.info_pte.appendPlainText(f'OS error\n {traceback.print_exc()}')

	if parent.subroutineCB.isChecked():
		if not os.path.exists(os.path.expanduser('~/linuxcnc/subroutines')):
			try:
				os.mkdir(os.path.expanduser('~/linuxcnc/subroutines'))
			except OSError:
				parent.info_pte.appendPlainText(f'OS error\n {traceback.print_exc()}')

	# build configuration directory if it doesn't exist
	# parent.configPath is updated when the machine name changes
	if not os.path.exists(parent.configPath):
		try:
			os.mkdir(parent.configPath)
		except OSError:
			parent.info_pte.appendPlainText(f'OS error\n {traceback.print_exc()}')

	iniFile = os.path.join(parent.configPath, parent.configNameUnderscored + '.ini')

	if parent.load_config_cb.isChecked():
		parent.settings.setValue('STARTUP/config', iniFile)
	else:
		parent.settings.setValue('STARTUP/config', False)

	if parent.testing: # testing
		buildhal2.build(parent)
		return
	

	if os.path.exists(iniFile):
		parent.updateini.update(parent, iniFile)
	else:
		buildini.build(parent)

	buildhal.build(parent)
	buildio.build_io(parent)
	buildio.build_ss(parent)
	buildmisc.build(parent)
	parent.mainTW.setCurrentIndex(11)
	parent.status_lb.setText('Saved')
	parent.actionBuild.setText('Build Config')





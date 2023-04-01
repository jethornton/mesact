import os, traceback

from libmesact import settings

from libmesact import check
from libmesact import buildini
from libmesact import buildhal
#from libmesact import buildio
#from libmesact import buildmisc
#from libmesact import buildss
from libmesact import utilities

def build(parent):
	build_all = True
	build_ini = True
	if not check.checkit(parent):
		parent.mainTW.setCurrentIndex(11)
		parent.info_pte.appendPlainText('Build Failed')
		build_all = False
		build_ini = False
		if parent.configNameLE.text() != '':
			msg = ('There are Errors in the Config\n'
				'Do you want to save the ini file\n'
				'and come back later to fix the Errors?')
			result = parent.errorMsgYesNo(msg, 'Build Errors')
			if result:
				build_ini = True
			else:
				parent.info_pte.appendPlainText('Build Aborted')
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

	if build_ini:
		iniFile = os.path.join(parent.configPath, parent.configNameUnderscored + '.ini')
		if os.path.exists(iniFile):
			parent.updateini.update(parent, iniFile)
		else:
			buildini.build(parent)

	if build_all:
		print('Building All')
		buildhal.build(parent)
		#buildio.build(parent)
		#buildmisc.build(parent)
		#buildss.build(parent)





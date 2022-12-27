import subprocess
from functools import partial

from PyQt5.QtWidgets import QAction, QWidget
from PyQt5.QtGui import QIcon

from libmesact import menu

def restore(parent):
	try:
		parent.resize(parent.settings.value('window size'))
		parent.move(parent.settings.value('window position'))
	except:
		pass

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
			parent.emcVersionLB.setText(f'LinuxCNC Uspace {version}')

	try:
		mf = subprocess.check_output('mesaflash', encoding='UTF-8')
		if len(mf) > 0:
			installed = mf.split()[2]
			parent.mesaflashVersionLB.setText(installed)
	except FileNotFoundError as error:
		parent.mesaflashVersionLB.setText('Not Installed')

def menus(parent):
	mainMenu = parent.menuBar()

	fileMenu = mainMenu.addMenu('File')
	newAction = QAction(QIcon.fromTheme('document-new'), 'New', parent)
	#newAction.setShortcut('Ctrl+N')
	newAction.setStatusTip('Create a New Configuration')
	newAction.triggered.connect(menu.new)
	fileMenu.addAction(newAction)

	openAction = QAction(QIcon.fromTheme('document-open'), 'Open', parent)
	#openAction.setShortcut('Ctrl+O')
	openAction.setStatusTip('Open a Configuration')
	openAction.triggered.connect(menu.open)
	fileMenu.addAction(openAction)

	fileMenu.addMenu('&Open Recent')

	saveAction = QAction(QIcon.fromTheme('document-save'), 'Save', parent)
	#saveAction.setShortcut('Ctrl+S')
	saveAction.setStatusTip('Save this Configuration')
	saveAction.triggered.connect(menu.save)
	fileMenu.addAction(saveAction)

	saveAsAction = QAction(QIcon.fromTheme('document-save-as'), 'Save As', parent)
	#saveAsAction.setShortcut('Ctrl+A')
	saveAsAction.setStatusTip('Save this Configuration with a new name')
	saveAsAction.triggered.connect(menu.save_as)
	fileMenu.addAction(saveAsAction)

	exitAction = QAction(QIcon.fromTheme('application-exit'), 'Exit', parent)
	#exitAction.setShortcut('Ctrl+Q')
	exitAction.setStatusTip('Exit application')
	exitAction.triggered.connect(parent.close)
	fileMenu.addAction(exitAction)

	editMenu = mainMenu.addMenu('Edit')

	preferencesAction = QAction(QIcon.fromTheme('document-save'), 'Preferences', parent)
	#preferencesAction.setShortcut('Ctrl+S')
	preferencesAction.setStatusTip('Edit Preferences')
	preferencesAction.triggered.connect(partial(menu.edit_preferences, parent))
	editMenu.addAction(preferencesAction)

	viewMenu = mainMenu.addMenu('View')

	searchMenu = mainMenu.addMenu('Search')

	toolsMenu = mainMenu.addMenu('Tools')

	helpMenu = mainMenu.addMenu('Help')

	#fileMenu = menubar.addMenu('&File')
	
	#parent.menuBar.addMenu('&Admin')
	#parent.closeAction = QAction('Closing', parent)
	#parent.menuBar.addAction(parent.closeAction)


def checkmesaflash(parent, required=None, board=None):
	installed = False
	flashOk = False
	try:
		mf = subprocess.check_output('mesaflash', encoding='UTF-8')
		if len(mf) > 0:
			installed = mf.split()[2]
			parent.mesaflashVersionLB.setText(installed)
			parent.firmwareGB.setEnabled(True)
			parent.checkBoardPB.setEnabled(True)
			flashOk = True
	except FileNotFoundError as error:
		parent.firmwareGB.setEnabled(False)
		parent.checkBoardPB.setEnabled(False)
		parent.mesaflashVersionLB.setText('Not Installed')
		t = ('Mesaflash not found! Flashing and reading cards is not possible.\n'
			'Either install from the Synaptic Package Manager\n'
			'or install with apt\nsudo apt install mesaflash\nor go to\n'
			'https://github.com/LinuxCNC/mesaflash\n'
			'to build and install the lastest mesaflash.\n')
		parent.machinePTE.appendPlainText(t)
		parent.statusbar.showMessage('Mesaflash not found!')

	if required and installed:
		ivers = installed.split('.')
		rvers = required.split('.')
		items = len(ivers)
		for i in range(items):
			if ivers[i] < rvers[i]:
				flashOk = False
				t = (f'The Mesa {board} requires Mesaflash {required} or later.\n'
					f'The installed version of Mesaflash is {installed}\n'
					'Try updating the PC with sudo apt update in a terminal\n'
					'or go to https://github.com/LinuxCNC/mesaflash\n'
					'for installation/update instructions.')
				parent.machinePTE.appendPlainText(t)
				parent.firmwareGB.setEnabled(False)
				parent.checkBoardPB.setEnabled(False)
				parent.errorMsgOk(t, 'Mesaflash Version')

	return flashOk


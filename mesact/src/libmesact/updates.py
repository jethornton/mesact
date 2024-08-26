import os, requests, subprocess, tarfile

from PyQt5.QtWidgets import QApplication, QFileDialog, QComboBox

from libmesact import documents
from libmesact import utilities
from libmesact import boards
from libmesact import startup
from libmesact import dialogs

def downloadFirmware(parent):
	board = parent.boardCB.currentData()
	if board:
		libpath = os.path.join(os.path.expanduser('~'), '.local/lib/libmesact')
		firmware_url = f'https://github.com/jethornton/mesact_firmware/releases/download/1.0.0/{board}.tar.xz'
		destination = os.path.join(os.path.expanduser('~'), f'.local/lib/libmesact/{board}.tar.xz')
		utilities.download(parent, firmware_url, destination)
		with tarfile.open(destination) as f:
			f.extractall(libpath)
		if os.path.isfile(destination):
			os.remove(destination)
		# update firmware tab
		boards.loadFirmware(parent)
	else:
		dialogs.infoMsgOk('Select a Board', 'Board')

def checkUpdates(parent):
	response = requests.get(f"https://api.github.com/repos/jethornton/mesact/releases/latest")
	repoVersion = response.json()["name"]
	parent.mainTW.setCurrentIndex(11)
	if tuple(repoVersion.split('.')) > tuple(parent.version.split('.')):
		parent.info_pte.appendPlainText(f'A newer version {repoVersion} is available for download')
	elif tuple(repoVersion.split('.')) == tuple(parent.version.split('.')):
		parent.info_pte.appendPlainText(f'This version {repoVersion} is the latest avaliable')

def downloadAmd64Deb(parent):
	directory = str(QFileDialog.getExistingDirectory(parent, "Select Directory"))
	if directory != '':
		parent.statusbar.showMessage('Checking Repo')
		response = requests.get("https://api.github.com/repos/jethornton/mesact/releases/latest")
		repoVersion = response.json()["name"]
		parent.statusbar.showMessage(f'Mesa Configuration Tool Version {repoVersion} amd64 Download Starting')
		destination = os.path.join(directory, 'mesact_' + repoVersion + '_amd64.deb')
		deburl = f'https://github.com/jethornton/mesact/releases/download/{repoVersion}/mesact_{repoVersion}_amd64.deb'
		utilities.download(parent, deburl, destination)
		parent.statusbar.showMessage(f'Mesa Configuration Tool Version {repoVersion} Download Complete')
		dialogs.infoMsgOk('Close the Configuration tool and reinstall', 'Download Complete')
	else:
		parent.statusbar.showMessage('Download Cancled')

def downloadArmhDeb(parent):
	directory = str(QFileDialog.getExistingDirectory(parent, "Select Directory"))
	if directory != '':
		parent.statusbar.showMessage('Checking Repo')
		response = requests.get("https://api.github.com/repos/jethornton/mesact/releases/latest")
		repoVersion = response.json()["name"]
		parent.statusbar.showMessage(f'Mesa Configuration Tool Version {repoVersion} armhf Download Starting')
		destination = os.path.join(directory, 'mesact_' + repoVersion + '_armhf.deb')
		deburl = f'https://github.com/jethornton/mesact/releases/download/{repoVersion}/mesact_{repoVersion}_armhf.deb'
		utilities.download(parent, deburl, destination)
		parent.statusbar.showMessage(f'Mesa Configuration Tool Version {repoVersion} Download Complete')
		dialogs.infoMsgOk('Close the Configuration tool and reinstall', 'Download Complete')
	else:
		parent.statusbar.showMessage('Download Cancled')

def downloadArm64Deb(parent):
	directory = str(QFileDialog.getExistingDirectory(parent, "Select Directory"))
	if directory != '':
		parent.statusbar.showMessage('Checking Repo')
		response = requests.get("https://api.github.com/repos/jethornton/mesact/releases/latest")
		repoVersion = response.json()["name"]
		parent.statusbar.showMessage(f'Mesa Configuration Tool Version {repoVersion} arm64 Download Starting')
		destination = os.path.join(directory, 'mesact_' + repoVersion + '_arm64.deb')
		deburl = f'https://github.com/jethornton/mesact/releases/download/{repoVersion}/mesact_{repoVersion}_arm64.deb'
		utilities.download(parent, deburl, destination)
		dialogs.statusbar.showMessage(parent, f'Mesa Configuration Tool Version {repoVersion} Download Complete')
		parent.infoMsgOk('Close the Configuration tool and reinstall', 'Download Complete')
	else:
		parent.statusbar.showMessage('Download Cancled')

def clearProgressBar(parent):
	parent.progressBar.setValue(0)
	parent.statusbar.clearMessage()
	parent.timer.stop()

def showDocs(parent, pdfDoc):
	docPath = False
	if isinstance(pdfDoc, str):
		docPath = os.path.join(parent.docs_path, pdfDoc)
	if docPath:
		subprocess.call(('xdg-open', docPath))

def openDoc(parent):
	if parent.installed:
		doc = os.path.join(parent.docs_path, 'mesact.pdf.gz')
	else:
		doc = os.path.join(parent.docs_path, 'mesact.pdf')
	subprocess.call(('xdg-open', doc))

def downloadDocs(parent):
	dialog = documents.dialog(parent)
	dialog.exec()

def boardImages(parent):
	libpath = os.path.join(os.path.expanduser('~'), '.local/lib/libmesact/boards')
	if not os.path.exists(libpath):
		os.makedirs(libpath)
	boards_url = f'https://github.com/jethornton/mesact_firmware/releases/download/1.0.0/boards.tar.xz'
	destination = os.path.join(os.path.expanduser('~'), f'.local/lib/libmesact/boards.tar.xz')
	utilities.download(parent, boards_url, destination)
	with tarfile.open(destination) as f:
		f.extractall(libpath)
	if os.path.isfile(destination):
		os.remove(destination)
	startup.loadBoards(parent)



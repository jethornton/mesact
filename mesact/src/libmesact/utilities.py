import os, subprocess
import urllib.request
from datetime import datetime

from PyQt5.QtWidgets import (QApplication, QInputDialog, QLineEdit, QComboBox,
	QDoubleSpinBox, QCheckBox)

def isNumber(s):
	try:
		s[-1].isdigit()
		float(s)
		return True
	except ValueError:
		return False

def check_emc():
	if "0x48414c32" in subprocess.getoutput('ipcs'):
		return True
	else:
		return False

def download(parent, down_url, save_loc):
	def Handle_Progress(blocknum, blocksize, totalsize):
		## calculate the progress
		readed_data = blocknum * blocksize
		if totalsize > 0:
			download_percentage = readed_data * 100 / totalsize
			parent.progressBar.setValue(int(download_percentage))
			QApplication.processEvents()
	urllib.request.urlretrieve(down_url, save_loc, Handle_Progress)
	parent.progressBar.setValue(100)
	parent.timer.start(1000)

def getPassword(parent):
	dialog = 'You need root privileges\nfor this operation.\nEnter your Password:'
	password, okPressed = QInputDialog.getText(parent, 'Password Required', dialog, QLineEdit.Password, "")
	if okPressed and password != '':
		return password

def unitsChanged(parent):
	if not parent.linearUnitsCB.currentData():
		unitsSecond = ''
		unitsMinute = ''
		for i in range(3):
			getattr(parent, f'unitsLB_{i}').setText('Select Units\nSettings Tab')
		return
	if parent.linearUnitsCB.currentData() == 'mm':
		unitsSecond = 'mm/sec'
		unitsMinute = 'mm/min'
	elif parent.linearUnitsCB.currentData() == 'inch':
		unitsSecond = 'in/sec'
		unitsMinute = 'in/min'
	for i in range(3):
		getattr(parent, f'unitsLB_{i}').setText(f'Vel & Acc\n{unitsSecond}')
	parent.trajMaxLinVelDSB.setSuffix(f' {unitsSecond}')
	parent.minLinJogVelDSB.setSuffix(f' {unitsSecond}')
	parent.defLinJogVelDSB.setSuffix(f' {unitsSecond}')
	parent.maxLinJogVelDSB.setSuffix(f' {unitsSecond}')
	parent.minLinearVelLB.setText(f'{parent.minLinJogVelDSB.value() * 60:.1f} {unitsMinute}')
	parent.defLinearVelLB.setText(f'{parent.defLinJogVelDSB.value() * 60:.1f} {unitsMinute}')
	parent.maxLinearVelLB.setText(f'{parent.maxLinJogVelDSB.value() * 60:.1f} {unitsMinute}')
	if set('ABC')&set(parent.coordinatesLB.text()): # angular axis
		parent.minAngularVelLB.setText(f'{parent.minAngJogVelDSB.value() * 60:.1f} deg/min')
		parent.defAngularVelLB.setText(f'{parent.defAngJogVelDSB.value() * 60:.1f} deg/min')
		parent.maxAngularVelLB.setText(f'{parent.maxAngJogVelDSB.value() * 60:.1f} deg/min')

	maxVelChanged(parent)

def maxVelChanged(parent):
	if parent.trajMaxLinVelDSB.value() > 0:
		val = parent.trajMaxLinVelDSB.value()
		if parent.linearUnitsCB.currentData() == 'mm':
			parent.mlvPerMinLB.setText(F'{val * 60:.1f} mm/min')
		if parent.linearUnitsCB.currentData() == 'inch':
			parent.mlvPerMinLB.setText(F'{val * 60:.1f} in/min')
	else:
		parent.mlvPerMinLB.setText('')

def backupFiles(parent, configPath=None):
	if not configPath:
		configPath = parent.configPath
	if not os.path.exists(configPath):
		parent.info_pte.setPlainText('Nothing to Back Up')
		return
	backupDir = os.path.join(configPath, 'backups')
	if not os.path.exists(backupDir):
		os.mkdir(backupDir)
	p1 = subprocess.Popen(['find',configPath,'-maxdepth','1','-type','f','-print'], stdout=subprocess.PIPE)
	backupFile = os.path.join(backupDir, f'{datetime.now():%m-%d-%y-%H:%M:%S}')
	p2 = subprocess.Popen(['zip','-j',backupFile,'-@'], stdin=p1.stdout, stdout=subprocess.PIPE)
	p1.stdout.close()
	parent.info_pte.appendPlainText('Backing up Confguration')
	output = p2.communicate()[0]
	parent.info_pte.appendPlainText(output.decode())

def axisDisplayChanged(parent, radioButton):
	for button in parent.axisButtonGroup.buttons():
		if button is not radioButton:
			button.setChecked(False)

def copyValues(parent):
	entries = ['_scale_', 
	'_min_limit_', 
	'_max_limit_', 
	'_max_vel_', 
	'_max_accel_', ]
	button = parent.sender().objectName()
	card = button[:2]
	joint = button[-1]
	for item in entries:
		getattr(parent, f'{card}{item}{int(joint) + 1}').setText(getattr(parent, f'{card}{item}{joint}').text())

def new_config(parent):
	for child in parent.findChildren(QLineEdit):
		child.clear()
	for child in parent.findChildren(QComboBox):
		child.setCurrentIndex(0)
	for child in parent.findChildren(QDoubleSpinBox):
		child.setValue(0)
	for child in parent.findChildren(QCheckBox):
		child.setChecked(False)
	parent.servoPeriodSB.setValue(1000000)
	parent.introGraphicLE.setText('emc2.gif')





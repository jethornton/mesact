import os
import urllib.request

from PyQt5.QtWidgets import QApplication

def isNumber(s):
	try:
		s[-1].isdigit()
		float(s)
		return True
	except ValueError:
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


def unitsChanged(parent):
	if not parent.linearUnitsCB.currentData():
		unitsSecond = ''
		unitsMinute = ''
		for i in range(4):
			getattr(parent, f'unitsLB_{i}').setText('Select Units\nSettings Tab')
		return
	if parent.linearUnitsCB.currentData() == 'mm':
		unitsSecond = 'mm/sec'
		unitsMinute = 'mm/min'
	elif parent.linearUnitsCB.currentData() == 'inch':
		unitsSecond = 'in/sec'
		unitsMinute = 'in/min'
	for i in range(4):
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
		parent.infoPTE.setPlainText('Nothing to Back Up')
		return
	backupDir = os.path.join(configPath, 'backups')
	if not os.path.exists(backupDir):
		os.mkdir(backupDir)
	p1 = subprocess.Popen(['find',configPath,'-maxdepth','1','-type','f','-print'], stdout=subprocess.PIPE)
	backupFile = os.path.join(backupDir, f'{datetime.now():%m-%d-%y-%H:%M:%S}')
	p2 = subprocess.Popen(['zip','-j',backupFile,'-@'], stdin=p1.stdout, stdout=subprocess.PIPE)
	p1.stdout.close()
	parent.infoPTE.appendPlainText('Backing up Confguration')
	output = p2.communicate()[0]
	parent.infoPTE.appendPlainText(output.decode())

def axisDisplayChanged(parent, radioButton):
	for button in parent.axisButtonGroup.buttons():
		if button is not radioButton:
			button.setChecked(False)



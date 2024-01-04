import os, traceback
from datetime import datetime

def build(parent):

	halFilePath = os.path.join(parent.configPath, 'main' + '.hal')
	parent.info_pte.appendPlainText(f'Building {halFilePath}')

	halContents = []
	halContents = ['# This file was created with the Mesa Configuration Tool on ']
	halContents.append(datetime.now().strftime('%b %d %Y %H:%M:%S') + '\n')
	halContents.append('# If you make changes to this file DO NOT run the configuration tool again!\n')
	halContents.append('# This file will be replaced with a new file if you do!\n\n')

	

	joint = 0
	for card in range(3):
		board = getattr(parent, f'board_{card}')
		if board:
			halContents.append(f'\n# Board: {board}\n')
			for output in range(6):
				if getattr(parent, f'c{card}_axis_{output}').currentData():
					 halContents.append(f'\n# Axis: {getattr(parent, f"c{card}_axis_{output}").currentData()} Joint: {joint} Output: {output}\n')
					 joint += 1

	try:
		with open(halFilePath, 'w') as halFile:
			halFile.writelines(halContents)
	except OSError:
		parent.info_pte.appendPlainText(f'OS error\n {traceback.print_exc()}')

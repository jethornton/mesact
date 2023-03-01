

def changed(parent):
	stepper = ['7i76', '7i78']
	analog = ['7i77']
	index = int(parent.sender().objectName()[-1])
	if parent.sender().currentData():
		board = parent.sender().currentData()
		parent.mainTW.setTabVisible(4 + index, True)
		for i in range(6):
			if board in stepper:
				getattr(parent, f'c{index + 1}_stepgenGB_{i}').setVisible(True)
				getattr(parent, f'c{index + 1}_analogGB_{i}').setVisible(False)
	else:
		parent.mainTW.setTabVisible(4 + index, False)



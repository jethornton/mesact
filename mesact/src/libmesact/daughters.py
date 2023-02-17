

def changed(parent):
	index = int(parent.sender().objectName()[-1])
	if parent.sender().currentData():
		parent.mainTW.setTabVisible(3 + index, True)
	else:
		parent.mainTW.setTabVisible(3 + index, False)



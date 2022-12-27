import os

def firmwareChanged(parent):
	if parent.firmwareCB.currentData():
		parent.firmwareLB.setText(parent.firmwareCB.currentText())
		path = os.path.splitext(parent.firmwareCB.currentData())[0]
		pinfile = os.path.join(path + '.pin')
		descfile = os.path.join(path + '.txt')
		if os.path.exists(pinfile):
			with open(pinfile, 'r') as file:
				data = file.read()
			parent.hmidPTE.clear()
			parent.hmidPTE.setPlainText(data)
		if os.path.exists(descfile):
			with open(descfile, 'r') as file:
				data = file.read()
			parent.firmwareDescPTE.clear()
			parent.firmwareDescPTE.setPlainText(data)
		else:
			parent.firmwareDescPTE.clear()
			parent.firmwareDescPTE.setPlainText(f'No description file found\nfor {parent.firmwareCB.currentText()}')

	else:
		pass


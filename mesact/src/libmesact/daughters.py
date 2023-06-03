
'''
7i76 5 step/dir 32 inputs 16 outputs 1 spindle 1 encoder
7i77 6 analog  32 inputs 16 outputs 1 spindle 1 encoder
7i78 4 step/dir 1 spindle 1 encoder
parent.mainTW.setTabText(4, 'P1')
parent.mainTW.setTabText(5, 'P2')

'''

def changed(parent):
	index = int(parent.sender().objectName()[-1])
	tab = int(parent.sender().objectName()[-1]) + 4
	if parent.sender().currentData():
		#print(parent.sender().objectName())
		stepper = ['7i76', '7i78']
		analog = ['7i77']
		board = parent.sender().currentData()
		parent.mainTW.setTabVisible(tab, True)
		connector = getattr(parent, f'daughterLB_{index}').text()
		#print(connector)
		parent.mainTW.setTabText(tab, f'{board} {connector}')
		# daughter_info_pte_0
		info = (f'Connector: {connector}'
		)
		getattr(parent, f'daughter_info_pte_{index}').setPlainText(info)
		for i in range(6):
			if board in stepper:
				getattr(parent, f'c{index + 1}_stepgenGB_{i}').setVisible(True)
				getattr(parent, f'c{index + 1}_analogGB_{i}').setVisible(False)
	else:
		parent.mainTW.setTabVisible(4 + index, False)



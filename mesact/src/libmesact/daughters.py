
def changed(parent):
	index = int(parent.sender().objectName()[-1])
	if parent.sender().currentData(): # daughter card selected
		board = parent.sender().currentData()
		tab = int(parent.sender().objectName()[-1]) + 4
		card = int(parent.sender().objectName()[-1]) + 1
		stepper = ['7i76', '7i78', '7i85s']
		analog = ['7i77', '7i85']
		#print(f'tab: {tab}')
		#print(f'index: {index}')
		#print(f'card: {card}')
		#print(parent.sender().objectName())
		parent.mainTW.setTabVisible(tab, True)
		connector = getattr(parent, f'daughterLB_{index}').text()
		#print(f'connector: {connector}')
		parent.mainTW.setTabText(tab, f'{board}')
		# daughter_info_pte_0
		info = (f'Connector: {connector}'
		)
		getattr(parent, f'daughter_info_pte_{index}').setPlainText(info)
		for i in range(6): # hide stepper tab
			if board in analog: getattr(parent, f'c{card}_settings_{i}').setTabVisible(2, False)
			if board in stepper: getattr(parent, f'c{card}_settings_{i}').setTabVisible(3, False)
			if board in stepper: getattr(parent, f'c{card}_settings_{i}').setTabVisible(4, False)

	else:
		parent.mainTW.setTabVisible(4 + index, False)


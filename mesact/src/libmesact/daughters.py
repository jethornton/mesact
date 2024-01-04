
def changed(parent):
	# daughter tab indexes start at 1
	if parent.sender().currentData(): # daughter card selected
		port = int(parent.sender().objectName()[-1])
		daughter_tab = port + 1
		board = parent.sender().currentData()
		setattr(parent, f'board_{daughter_tab}', board)
		#print(f'board_{daughter_tab}')
		main_tw_tab = int(parent.sender().objectName()[-1]) + 4
		# daughterLB_0
		card = parent.sender().objectName()[-1]
		connector = getattr(parent, f'daughterLB_{card}').text()
		# connector = int(parent.sender().objectName()[-1]) + 1
		getattr(parent, f'c{int(card) + 1 }_JointTW').setTabText(0, parent.sender().currentText())
		cards = {
			'7i76':{'axis':5, 'stepgen':5, 'analog':0, 'encoder':0, 'spinenc':1, 'spinana':1, 'inputs':32, 'outputs':16},
			'7i77':{'axis':6, 'stepgen':0, 'analog':6, 'encoder':6, 'spinenc':1, 'spinana':1, 'inputs':32, 'outputs':16},
			'7i78':{'axis':4, 'stepgen':4, 'analog':0, 'encoder':0, 'spinenc':1, 'spinana':1, 'inputs':0, 'outputs':0},
			'7i85':{'axis':4, 'stepgen':4, 'analog':0, 'encoder':0, 'spinenc':1, 'spinana':1, 'inputs':0, 'outputs':0},
			'7i85s':{'axis':4, 'stepgen':4, 'analog':0, 'encoder':4, 'spinenc':1, 'spinana':1, 'inputs':0, 'outputs':0}
			}
		parent.mainTW.setTabVisible(main_tw_tab, True)
		parent.mainTW.setTabText(main_tw_tab, f'{connector} {parent.sender().currentText()}')
		axis = cards[board]['axis']
		stepgen = cards[board]['stepgen']
		analog = cards[board]['analog']
		encoder = cards[board]['encoder']
		spinenc = cards[board]['spinenc']
		spinana = cards[board]['spinana']
		inputs = cards[board]['inputs']
		outputs = cards[board]['outputs']

		for i in range(1,7): # show/hide axis tabs
			if i <= axis:
				getattr(parent, f'c{daughter_tab}_JointTW').setTabVisible(i, True)
			else:
				getattr(parent, f'c{daughter_tab}_JointTW').setTabVisible(i, False)

		for i in range(6): # show/hide stepgen tabs c0_pidDefault_0
			if stepgen > 0 and i <= stepgen:
				getattr(parent, f'c{daughter_tab}_settings_{i}').setTabVisible(2, True)
				getattr(parent, f'c{daughter_tab}_pidDefault_{i}').setEnabled(True)
			else:
				getattr(parent, f'c{daughter_tab}_settings_{i}').setTabVisible(2, False)
				getattr(parent, f'c{daughter_tab}_pidDefault_{i}').setEnabled(False)

		for i in range(6): # show/hide analog tabs
			if analog > 0 and i <= analog:
				getattr(parent, f'c{daughter_tab}_settings_{i}').setTabVisible(3, True)
				getattr(parent, f'c{daughter_tab}_scale_{i}').setEnabled(False)
			else:
				getattr(parent, f'c{daughter_tab}_settings_{i}').setTabVisible(3, False)
				getattr(parent, f'c{daughter_tab}_scale_{i}').setEnabled(True)

		for i in range(6): # show/hide encoder tabs
			if encoder > 0 and i <= encoder:
				getattr(parent, f'c{daughter_tab}_settings_{i}').setTabVisible(4, True)
			else:
				getattr(parent, f'c{daughter_tab}_settings_{i}').setTabVisible(4, False)

		for i in range(32): # hide debounce check boxes
			getattr(parent, f'c{daughter_tab}_input_debounce_{i}').setEnabled(False)

		for i in range(32): # enable/disable inputs
			if inputs > 0 and i <= inputs:
				getattr(parent, f'c{daughter_tab}_input_{i}').setEnabled(True)
				getattr(parent, f'c{daughter_tab}_input_invert_{i}').setEnabled(True)
			else:
				getattr(parent, f'c{daughter_tab}_input_{i}').setEnabled(False)
				getattr(parent, f'c{daughter_tab}_input_invert_{i}').setEnabled(False)

		for i in range(16): # enable/disable outputs
			if outputs > 0 and i <= outputs:
				getattr(parent, f'c{daughter_tab}_output_{i}').setEnabled(True)
				getattr(parent, f'c{daughter_tab}_output_invert_{i}').setEnabled(True)
			else:
				getattr(parent, f'c{daughter_tab}_output_{i}').setEnabled(False)
				getattr(parent, f'c{daughter_tab}_output_invert_{i}').setEnabled(False)

	else:
		parent.mainTW.setTabVisible(4 + int(parent.sender().objectName()[-1]), False)


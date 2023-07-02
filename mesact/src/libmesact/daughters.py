
def changed(parent):
	# daughter card indexes start at 1
	index = int(parent.sender().objectName()[-1])
	if parent.sender().currentData(): # daughter card selected
		daughter = int(getattr(parent, f'daughterLB_{index}').text()[-1])
		#print(daughter)
		board = parent.sender().currentData()
		tab = int(parent.sender().objectName()[-1]) + 4
		connector = int(parent.sender().objectName()[-1]) + 1
		cards = {'7i76':{'axis':5, 'stepgen':5, 'analog':0, 'encoder':0, 'spinenc':1, 'spinana':1},
			'7i77':{'axis':6, 'stepgen':0, 'analog':6, 'encoder':6, 'spinenc':1, 'spinana':1},
			'7i78':{'axis':4, 'stepgen':4, 'analog':0, 'encoder':0, 'spinenc':1, 'spinana':1},
			'7i85':{'axis':4, 'stepgen':4, 'analog':0, 'encoder':0, 'spinenc':1, 'spinana':1},
			'7i85s':{'axis':4, 'stepgen':4, 'analog':0, 'encoder':4, 'spinenc':1, 'spinana':1}
			}
		parent.mainTW.setTabVisible(tab, True)
		parent.mainTW.setTabText(tab, f'{parent.sender().currentText()}')
		axis = cards[board]['axis']
		stepgen = cards[board]['stepgen']
		analog = cards[board]['analog']
		encoder = cards[board]['encoder']
		spinenc = cards[board]['spinenc']
		spinana = cards[board]['spinana']

		for i in range(1,7): # show/hide axis tabs
			if i <= axis:
				getattr(parent, f'c{daughter}_JointTW').setTabVisible(i, True)
			else:
				getattr(parent, f'c{daughter}_JointTW').setTabVisible(i, False)

		for i in range(6): # show/hide stepgen tabs
			if stepgen > 0 and i <= stepgen:
				getattr(parent, f'c{daughter}_settings_{i}').setTabVisible(2, True)
			else:
				getattr(parent, f'c{daughter}_settings_{i}').setTabVisible(2, False)

		for i in range(6): # show/hide analog tabs
			if analog > 0 and i <= analog:
				getattr(parent, f'c{daughter}_settings_{i}').setTabVisible(3, True)
			else:
				getattr(parent, f'c{daughter}_settings_{i}').setTabVisible(3, False)

		for i in range(6): # show/hide encoder tabs
			if encoder > 0 and i <= encoder:
				getattr(parent, f'c{daughter}_settings_{i}').setTabVisible(4, True)
			else:
				getattr(parent, f'c{daughter}_settings_{i}').setTabVisible(4, False)

	else:
		parent.mainTW.setTabVisible(4 + index, False)


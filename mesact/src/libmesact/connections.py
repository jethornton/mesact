from functools import partial

from libmesact import menu
from libmesact import utilities
from libmesact import boards
from libmesact import firmware


def connect(parent):
	# menu items
	parent.actionNew.triggered.connect(partial(menu.new, parent))
	parent.actionRecent.triggered.connect(partial(menu.update, parent))
	#parent.actionOpen.triggered.connect(partial(parent.loadini.getini, parent))


	parent.configNameLE.textChanged[str].connect(partial(utilities.configNameChanged, parent))
	parent.boardCB.currentIndexChanged.connect(partial(boards.boardChanged, parent))
	parent.firmwareCB.currentIndexChanged.connect(partial(firmware.firmwareChanged, parent))



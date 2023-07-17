

def save_settings(parent):
	parent.settings.setValue('window_size', parent.size())
	parent.settings.setValue('window_position', parent.pos())

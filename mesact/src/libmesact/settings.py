
# Do all config settings here.

def update_settings(parent):
	print('update_settings')
	parent.settings.setValue('NAGS/firmware', parent.no_check_firmware_cb.isChecked())





# Do all config settings here.

def update_settings(parent):
	parent.settings.setValue('NAGS/firmware', parent.no_check_firmware_cb.isChecked())
	if not parent.load_config_cb.isChecked(): # turn this off without saving the config
		parent.settings.setValue('STARTUP/config', False)




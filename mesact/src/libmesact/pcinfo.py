import subprocess
from subprocess import Popen, PIPE

from libmesact import utilities

def ipInfo(parent):
	ip = subprocess.check_output(['ip', '-br', 'addr', 'show'], text=True)
	parent.ipInfoPTE.setPlainText(ip)

def mbInfo(parent):
	if not parent.password:
		password = utilities.getPassword(parent)
		parent.password = password
	if parent.password != None:
		p = Popen(['sudo', '-S', 'dmidecode', '-t 2'],
			stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
		prompt = p.communicate(parent.password + '\n')

		if prompt:
			parent.pc_info_pte.clear()
			if p.returncode == 0:
				output = prompt[0]
			else:
				output = prompt[1]
			parent.pc_info_pte.setPlainText(f'Return Code: {p.returncode}')
			parent.pc_info_pte.appendPlainText(output)

def cpuInfo(parent): # output dynamic property is the pte to set the result in.
	result = subprocess.check_output("lscpu",shell=True, text=True)
	getattr(parent, f'{parent.sender().property("output")}').setPlainText(result)

def nicInfo(parent):
	result = subprocess.check_output("lspci | grep -i 'ethernet'",shell=True, text=True)
	parent.pc_info_pte.setPlainText(result)

def servoTmax(parent):
	if "0x48414c32" in subprocess.getoutput('ipcs'):
		p = Popen(['halcmd', 'show', 'param', 'servo-thread.tmax'],
			stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
		prompt = p.communicate()
		if prompt:
			parent.servo_thread_pte.appendPlainText(prompt[0])
			ret = prompt[0].splitlines()
			parent.st_thread_tmax_sb.setValue(int(ret[2].split()[3]))
	else:
		parent.errorMsgOk('LinuxCNC must be running this configuration!','Error')

def calcServoPercent(parent):
	error_text = []
	if parent.st_thread_tmax_sb.value() <= 0:
		error_text.append('Servo Thread tmax must be greater than 0')
	if parent.st_cpu_speed.value() <= 0:
		error_text.append('CPU Speed must be greater than 0')
	if error_text:
		parent.errorMsgOk('\n'.join(error_text), 'Missing Entries')
		return
	cpu_speed_hz = parent.st_cpu_speed.value() * parent.st_cpu_units_cb.currentData()
	cpu_clock_time = 0.000000001 * parent.servoPeriodSB.value()
	clocks_per_period = cpu_speed_hz * cpu_clock_time
	servoTmax = parent.st_thread_tmax_sb.value()
	cpu_clocks_used = servoTmax / clocks_per_period
	result = cpu_clocks_used * 100
	parent.servoResultLB.setText(f'{result:.0f}%')

def cpuSpeed(parent): # output spinbox units
	# linux-x86_64
	# linux-armv7l
	# linux-aarch64

	prompt = None
	if not parent.password:
		password = utilities.getPassword(parent)
		parent.password = password
	if parent.password != None:
		p = Popen(['sudo', '-S', 'dmidecode', '-t', 'processor'],
			stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
		prompt = p.communicate(parent.password + '\n')
	if prompt:
		ret = prompt[0].splitlines()
		for line in ret:
			if 'Speed' in line:
				getattr(parent, f'{parent.sender().property("output")}').appendPlainText(line.strip())
			if 'Current Speed' in line:
				getattr(parent, f'{parent.sender().property("spinbox")}').setValue(int(line.split()[2]))
				getattr(parent, f'{parent.sender().property("units")}').setCurrentText(line.split()[3])

def readTmax(parent):
	if not utilities.check_emc():
		parent.errorMsgOk(f'LinuxCNC must be running\nto get read.tmax', 'Error')
		return

	p = Popen(['halcmd', 'show', 'param', 'hm2*read.tmax'],
		stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
	prompt = p.communicate()
	if prompt:
		parent.nic_test_pte.appendPlainText(prompt[0])
		if 'hm2' in prompt[0]:
			ret = prompt[0].splitlines()
			parent.read_tmax_sb.setValue(int(ret[2].split()[3]))
		else:
			parent.errorMsgOk(f'LinuxCNC must be running\na Mesa Ethernet configuration\nto get read.tmax', 'Error')

def writeTmax(parent):
	if not utilities.check_emc():
		parent.errorMsgOk(f'LinuxCNC must be running\nto get write.tmax', 'Error')
		return
	p = Popen(['halcmd', 'show', 'param', 'hm2*write.tmax'],
		stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
	prompt = p.communicate()
	if prompt:
		parent.nic_test_pte.appendPlainText(prompt[0])
		if 'hm2' in prompt[0]:
			ret = prompt[0].splitlines()
			parent.write_tmax_sb.setValue(int(ret[2].split()[3]))
	else:
		parent.errorMsgOk(f'LinuxCNC must be running\na Mesa Ethernet configuration\nto get write.tmax', 'Error')

def nicCalc(parent):
	error_text = []
	if parent.nt_cpu_speed_sb.value() > 0:
		cpu_speed_hz = parent.nt_cpu_speed_sb.value() * parent.nt_cpu_units_cb.currentData()
	else:
		error_text.append('CPU Speed can not be empty')

	servo_period_seconds = parent.servoPeriodSB.value() / 1000000000

	if parent.read_tmax_sb.value() > 0:
		read_tmax = parent.read_tmax_sb.value()
	else:
		error_text.append('read.tmax can not be empty')

	if parent.write_tmax_sb.value() > 0:
		write_tmax = parent.write_tmax_sb.value()
	else:
		error_text.append('write.tmax can not be empty')

	if not error_text:
		rw_tmax = read_tmax + write_tmax
		cpu_clocks_per_period = int(servo_period_seconds * cpu_speed_hz)
		packet_time_percent = rw_tmax / cpu_clocks_per_period
		parent.packetTimeLB.setText(f'{packet_time_percent:.1%}')

	else:
		parent.errorMsgOk('\n'.join(error_text))

def cpuInfo(parent):
	result = subprocess.check_output('lscpu',shell=True, text=True)
	parent.pc_info_pte.setPlainText(result)




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

def readServoTmax(parent):
	if "0x48414c32" in subprocess.getoutput('ipcs'):
		p = Popen(['halcmd', 'show', 'param', 'servo-thread.tmax'],
			stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
		prompt = p.communicate()
		if prompt:
			parent.servo_thread_PTE.appendPlainText(prompt[0])
			ret = prompt[0].splitlines()
			parent.servoThreadTmaxLB.setText(ret[2].split()[3])
	else:
		parent.errorMsgOk('LinuxCNC must be running this configuration!','Error')

def calcServoPercent(parent):
	error_text = []
	if parent.cpuSpeedLE.text() != '':
		cpu_speed_Hz = int(parent.cpuSpeedLE.text()) * parent.cpuSpeedCB.currentData()
	cpu_clock_time = 0.000000001 * parent.servoPeriodSB.value()
	clocks_per_period = int(cpu_speed_Hz * cpu_clock_time)
	servoTmax = 1747291
	cpu_clocks_used = servoTmax / clocks_per_period
	result = cpu_clocks_used * 100
	parent.servoResultLB.setText(f'{result:.0f}%')

def cpuSpeed(parent):
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




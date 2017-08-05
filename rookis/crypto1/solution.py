import socket
import struct
import sys

# 16 byte blocks
# format id-pw-cookie
# brute force cookie one byte at a time
# recieve encrypted block including one letter of cookie
# brute force byte and match encrypted block (encyrpted blocks hex-encoded)


def connect_receive(num_a, letter, cookie):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('pwnable.kr', 9006))
    s.recv(512)
    # blank id
    s.send("\n")
    s.recv(512)
    if letter is "":
        s.send("a"*num_a + "\n")
    else:
        s.send("a"*num_a + "-" + cookie + letter + "\n")

    data =  s.recv(512)
    #print data
    if num_a < 15:
        e_packet =  data.split("(")[1][0:32]
    else:
        e_packet =  data.split("(")[1][33:64]
    s.close()
    return e_packet

def sys_write(s):
    sys.stdout.write(s)
    sys.stdout.flush()

if __name__ == "__main__":
    characters = '1234567890abcdefghijklmnopqrstuvwxyz-_'
    num_a = 13
    cookie = ""
    block = 1
    while (True):
        e_packet  = connect_receive(num_a, "", cookie)
        sys_write(e_packet + "\n")
        sys_write("Trying characters: ")
        for letter in characters:
            sys_write(letter)
            e_packet_try = connect_receive(num_a, letter, cookie)
            if e_packet_try == e_packet:
                sys_write("\nFound byte: " + letter + "\n")
                cookie += letter
                sys_write("cookie = : " + cookie + "\n")
                num_a-=1
                if (num_a < 0):
                    num_a = 18
                break










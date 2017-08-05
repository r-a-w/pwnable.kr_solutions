from nonblockingstream import nonblockingstream as nbsr
from nonblockingsocket import nonblockingsocket as nbsocket
import subprocess
import socket

#p = subprocess.Popen("/home/raw/Documents/pwnable/grotesque/lokihardt/lokihardt", stdin=subprocess.PIPE, stdout=subprocess.PIPE)
#stream = nbsr(p.stdout)
#data = stream.read(8)
#print data

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("pwnable.kr",9019))

s_stream = nbsocket(s)

data = s_stream.readuntil("pwnable",True)

print data

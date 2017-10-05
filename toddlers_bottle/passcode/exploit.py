import subprocess
import os

p = subprocess.Popen(['./passcode'], stdin=subprocess.PIPE)



#p.stdin.write("ass\r")
#p.stdin.write("12345\r")
#p.stdin.write("6789\r")
p.stdin.write(os.linesep.join(["ass", "8", "56"]))
#p.communicate(os.linesep.join(["ass", "8", "56"])) 


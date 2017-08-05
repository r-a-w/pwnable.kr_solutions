import subprocess, random, time

#random.seed(time.time())

p = subprocess.Popen(["/home/raw/Documents/pwnable/rookis/md5_calculator/c_random"], stdout=subprocess.PIPE)



x = subprocess.Popen(["/home/raw/Documents/pwnable/rookis/md5_calculator/c_random"], stdout=subprocess.PIPE)

output = p.stdout.read()
while output:
	print output
	output = p.stdout.read()

print "------------------------------------------------"
output = x.stdout.read()
while output:
	print output
	output = p.stdout.read()





#while output:
#	print output
#	output = p.stdout.read()
#
#for i in range(0,8):
#	print random.random()

# solution for solving coin challenge on pwnable.kr
import os,sys,time

pipe1_stdin, pipe1_stdout = os.pipe()
pipe2_stdin, pipe2_stdout = os.pipe()


pid = os.fork()
if pid:
	# child process
	os.close(pipe1_stdout)
	os.close(pipe2_stdin)
	os.dup2(pipe1_stdin, 0)
	os.dup2(pipe2_stdout, 1)
	os.close(pipe1_stdin)
	os.close(pipe2_stdout)
	args = ["nc", "pwnable.kr", "9007"] 
	os.execv("/bin/nc", args)
	
else:
	# parent process
	os.close(pipe1_stdin)
	os.close(pipe2_stdout)
	index = 1
	while True:
		output = os.read(pipe2_stdin, 512)
		lines =  output.splitlines()	
		line = lines[0]
		if "expired" in line:
			break
		if not(line.isdigit() or line.startswith("N=")):
			print line
			continue
		if "N=" in line:
			N = int(line[line.index("N")+2:line.index(" ")])
			C = int( line[line.index("C")+2:])

			l = 0  
			r = N
				
			m = r/2 +r%2
			
			output = " ".join(str(x) for x in range(l,m)) + "\r\n"
			os.write(pipe1_stdout, output)


		if line.isdigit():
			weight = int(line)
			if weight%10 == 0: 
				l = m
			else:
				r = m
			m = l + (r-l)/2 + (r-l)%2
			output = " ".join(str(x) for x in range(l,m)) + "\r\n"
			print output
			os.write(pipe1_stdout, output)
			
			#os.write(pipe1_stdout, str(l)+"\r\n")
			#break



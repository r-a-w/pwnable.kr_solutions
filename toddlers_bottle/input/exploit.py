#include<stdlib.h>
#include<unistd.h>
#include<sys/types.h>
#include<stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h>

int main(void){
	
	char *argv[101] = {"./input1", [1 ... 99] = "A", NULL};
	char *envp[2] = {"\xde\xad\xbe\xef=\xca\xfe\xba\xbe", NULL}; 
	argv['A'] = "\x00";
	argv['B'] = "\x20\x0a\x0d";
	argv['C'] = "55555";	

	FILE* fp=fopen("\x0a", "w");
	if(!fp){
		printf("error opening file\n");
		exit(1);
	}
	fwrite("\x00\x00\x00\x00", 4, 1, fp);
	fclose(fp);

	// Create pipe
	int pipe_stdin[2], pipe_stderr[2];

	if(pipe(pipe_stdin) < 0 || pipe(pipe_stderr) < 0){
		printf("error creating pipe\n");
		exit(1);
	}

	// Fork process
	pid_t child_pid;
	if((child_pid = fork()) < 0){
		printf("error forking\n");
		exit(1);
	}
	
	if(child_pid == 0){
		// close parent pipe stdin
		close(pipe_stdin[0]);
		close(pipe_stderr[0]);
		write(pipe_stdin[1], "\x00\x0a\x00\xff", 4);
		write(pipe_stderr[1], "\x00\x0a\x02\xff", 4);

	}else{
		// close child pipe stdout
		close(pipe_stdin[1]);
		close(pipe_stderr[1]);
		dup2(pipe_stdin[0],0);
		dup2(pipe_stderr[0],2);
		close(pipe_stdin[0]);
		close(pipe_stderr[0]);
		execve("/home/raw/Documents/pwnable/input/input1", argv, envp);

	}	


	// network
	sleep(5);
        int sd, cd;
        struct sockaddr_in saddr, caddr;
        sd = socket(AF_INET, SOCK_STREAM, 0);
        if(sd == -1){
                printf("creating socket error\n");
                exit(1);
        }
        saddr.sin_family = AF_INET;
        saddr.sin_addr.s_addr = inet_addr("127.0.0.1");
        saddr.sin_port = htons(55555);
       	cd = connect(sd, (struct sockaddr *)&saddr,  sizeof(struct sockaddr_in));
        if(cd < 0){
                printf("connecting socket error\n");
                exit(1);
        }
	write(sd, "\xde\xad\xbe\xef", 4); 
	

	return 0;
	  	

}

#include <stdio.h>
int main(){
	setresuid(getegid(), getegid(), getegid());
	setresgid(getegid(), getegid(), getegid());
	system("/home/raw/Documents/pwnable/shellshock/bash -c 'echo shock_me'");
	return 0;
}


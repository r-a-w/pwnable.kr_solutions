#include<stdio.h>

int main(void){
	char buffer[100];
	gets(buffer);
	system("/bin/sh\r\n");

	return 0;

}

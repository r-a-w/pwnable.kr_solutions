#include<stdlib.h>
#include<stdio.h>

int main(void){
	printf("0x%08x\n", getenv("PATH"));
	return 0;
}

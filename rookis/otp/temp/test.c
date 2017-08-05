#include<string.h>
#include<stdio.h>


int overflow(char *input){
	char buffer[8];
	strcpy(buffer, input);

}
int main(int argc, char *argv[]){
	overflow(argv[1]);
	printf("hey\n");
	return 0;
}

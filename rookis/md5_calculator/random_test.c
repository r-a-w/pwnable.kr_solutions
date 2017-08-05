#include<time.h>
#include<stdio.h>
#include<stdlib.h>

int main(int argc, char *argv[]){
	int i;
	//srand(atoi(argv[1]));
	srand(time(NULL));
	for(i=0;i<8;i++){
		printf("%d\n", rand());
	}
	return 0;
}


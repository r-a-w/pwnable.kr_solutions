#include<time.h>
#include<stdio.h>

int main(void){
	unsigned int random;
	random = rand();
	printf("unseeded random: %d\n",random);
	printf("%d ^ 0xdeadbeef: %d\n", random, random ^ 0xdeadbeef);

}

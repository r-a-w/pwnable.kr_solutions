#include <stdio.h>
#include <fcntl.h>

#define PW_LEN 10
#define XORKEY 1

void xor(char* s, int len){
        int i;
        for(i=0; i<len; i++){
                s[i] ^= XORKEY;
        }
}

int main(void){
	char buffer[PW_LEN+1];
	scanf("%10s", buffer);

	
	xor(buffer, 10);

	return 0;
}

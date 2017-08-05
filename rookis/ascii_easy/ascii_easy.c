#include <sys/mman.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

#define BASE ((void*)0x80000000)

int is_ascii(int c){
    if(c>=0x20 && c<=0x7f) return 1;
    return 0;
}

void vuln(){
    int a[40];
    strcpy((char*)a, (char*)BASE);
}

void main(int argc, char** arg, char** env){
    char* res = mmap(BASE, 4096, 7, MAP_ANONYMOUS | MAP_FIXED | MAP_PRIVATE, -1, 0);
    if(res != BASE){
        printf("mmap failed. tell admin\n");
        _exit(1);
    }

    printf("Input text : ");
    unsigned int n=0;
    while( n<400 && is_ascii(res[n++]=getchar()) );
    printf("triggering bug...\n");
    vuln();
}


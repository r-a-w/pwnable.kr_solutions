#include<stdio.h>
#include<stdlib.h>

int main(){
  char buffer[32];

  //printf("buffer at %p\n", buffer);
  //printf("ebp at %p\n", buffer+40);
  printf("XDG_VTNR @ %p\n", getenv("XDG_VTNR"));

  return 0;
}

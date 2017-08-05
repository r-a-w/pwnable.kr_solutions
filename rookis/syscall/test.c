#include<stdio.h>
#include<string.h>
#include<stdlib.h>

int test_function(){
  printf("heyooooo\n");
  return 0;
}

int main(){
  __asm__("ldr r3,=%0\n\t"\
          "mov pc,r3\n\t"\
          :               \
          :"r" (test_function) \
          :"r0", "pc" \
          )

}

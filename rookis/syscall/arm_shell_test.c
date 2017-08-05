#include<stdio.h>
#include<string.h>
#include<unistd.h>
#include<sys/mman.h>

int test_function(){
  printf("Hello World!\n");
  return 0;
}

/*
e5 1f 00 00·
e1 a0 f0 00
44 43 42 41
*/
//char shellcode[] = "\xe5\x1f\x00\x00\xe1\xa0\xf0\x00" \
                   "BBBB";
//char shellcode[] = "\xb8\x41\x41\x41\x41\xff\xe0";
char shellcode[]="\x41\x04\xa0\xe3\x42\x08\x80\xe3\x43\x0c\x80\xe3\x44\x00\x80\xe3\x00\xf0\xa0\xe1";
//char shellcode[]="\xe3\xa0\x04\x41\xe3\x80\x08\x42\xe3\x80\x0c\x43\xe3\x80\x00\x44\xe1\xa0\xf0\x00";

unsigned int address = 0x13371110;
int map_memory_shellcode(){
  unsigned int pagesize = getpagesize();
  unsigned int pagemask = ~(pagesize -1);
  unsigned int rounded_addr = address & pagemask;
  unsigned int diff = address - rounded_addr;
  unsigned int len = (sizeof(shellcode) + diff + (pagesize - 1)) & pagemask;

  char *buffer = (char *) mmap((void *) rounded_addr, (size_t) len, PROT_EXEC|PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS|MAP_FIXED, 0, 0);

  memcpy((char *) address, shellcode, sizeof(shellcode));
}

int main(){
  char *pointer, *addr;
  unsigned int func_addr;

  func_addr = (unsigned int) test_function;
  printf("test function %p, func_addr %p\n", test_function, (void *) func_addr);
  addr = (char *) &func_addr+3;

  pointer = shellcode;

  int i;
  for(i=0;i<4;i++){
    *pointer = *addr;
    pointer+=4;
    addr = addr-1;
  }

  printf("overwritten\n");

  map_memory_shellcode();

  printf("memory mapped\n");

  int (*other_function)();
  other_function = (int (*)()) address;
  other_function();
}


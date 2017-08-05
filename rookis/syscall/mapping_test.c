#include<stdio.h>
#include<sys/mman.h>

int main(){

  size_t address = 0x13371111;
  size_t page_size = getpagesize();
  size_t page_mask = ~(page_size - 1);
  size_t rounded_addr = address & page_mask;
  unsigned diff = address - rounded_addr;
  unsigned len =(diff + (page_size -1)) & page_mask;

  char *buffer = mmap((void *) rounded_addr, (size_t) len, PROT_READ|PROT_WRITE|PROT_EXEC, MAP_FIXED|MAP_ANONYMOUS|MAP_PRIVATE, 0, 0);

  printf("[+] mapped %p\n", buffer);

  printf("[+] address = %p, rounded address = %p, buffer + diff = %p\n", address, rounded_addr, buffer+diff);


}

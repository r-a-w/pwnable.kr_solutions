#include<unistd.h>

int main(void){
  char *arg[]={"./dragon", NULL};
  char *env[]={NULL};


  execve("/home/raw/Documents/pwnable/rookis/dragon/dragon", arg, env);
  write(1,"hey\n",4);
}

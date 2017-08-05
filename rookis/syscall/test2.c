#include<stdio.h>
#include<stdlib.h>

void foo(){
  //do nothing
}
/*
int main(){
  size_t *pointer;

  pointer = malloc(5);

  *pointer = (size_t ) foo;

  //printf("%p %p %p\n", foo, test, *test);
  printf("%p\n", foo);
  printf("%p\n", pointer);
  printf("%p\n", *pointer);
  return 0;
}
*/

/*
int main(){
  char pointer[5];
  size_t *temp;

  temp = (size_t *) pointer;
  *temp = (size_t) foo;

  printf("%p\n", foo);
  printf("%p\n", pointer);
  printf("%p\n", *temp);
}
*/

int main(){
  size_t pointer[1];

  *pointer = (size_t) foo;

  printf("%p\n", foo);
  printf("%p\n", pointer);
  printf("%p\n", *pointer);
}

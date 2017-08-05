#include<alloca.h>
#include<stdio.h>

int main(){
  //int value;
  size_t value;
  printf("Enter value: ", &value);
  scanf("%d", &value);
  alloca(value);
  return 0;
}

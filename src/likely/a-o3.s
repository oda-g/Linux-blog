	.file	"a.c"
	.text
	.p2align 4
	.globl	f
	.type	f, @function
f:
.LFB0:
	.cfi_startproc
	endbr64
	subq	$8, %rsp
	.cfi_def_cfa_offset 16
	xorl	%eax, %eax
	testl	%edi, %edi
	jle	.L2
	call	x@PLT
	addq	$8, %rsp
	.cfi_remember_state
	.cfi_def_cfa_offset 8
	addl	$1, %eax
	ret
	.p2align 4,,10
	.p2align 3
.L2:
	.cfi_restore_state
	call	y@PLT
	addq	$8, %rsp
	.cfi_def_cfa_offset 8
	addl	$1, %eax
	ret
	.cfi_endproc
.LFE0:
	.size	f, .-f
	.ident	"GCC: (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0"
	.section	.note.GNU-stack,"",@progbits
	.section	.note.gnu.property,"a"
	.align 8
	.long	1f - 0f
	.long	4f - 1f
	.long	5
0:
	.string	"GNU"
1:
	.align 8
	.long	0xc0000002
	.long	3f - 2f
2:
	.long	0x3
3:
	.align 8
4:

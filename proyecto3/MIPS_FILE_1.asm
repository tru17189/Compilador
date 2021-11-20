.data

funcion: 

	li $t0,  fp[0] 
	li $t1,  10

	syscall
	mul t2, t0, t1
	li $t3,  fp[0] 
	li $t4,  10

	syscall
	div t5, t3, t4
	li $t6,  t0 
	li $t7,  t1

	syscall
	sub s0, t6, t7
	beq $ fp[0], $0, L1
	syscall
	jal $L1

	jal $L2

	L1: 

	jr $10
	L2: 

	jr $fp[0]
	jal $L3

	L3:

	jr $t4
main: 

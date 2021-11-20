.data

funcion: 

	li $t0, fp[0]
	li $t1, 10
	syscall
	mul $t2, $fp[0], $10
	li $t3, t0
	li $t4, t1
	syscall
	div $t5, $t0, $t1
	li $t6, t2
	li $t7, t4
	syscall
	sub $s0, $t2, $t4
	beq $t3 , $fp[0], L0
	syscall
	jal L1

	jal L2

	L1: 

	jr $ra
	L2: 

	jr $ra
	jal L3

	L3:

	jr $ra
main: 

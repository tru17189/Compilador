###############################
#Comienza el Tercer proyecto #
###############################

# Lista para mandar instrucciones al archivo final con primera instruccion
from os import PRIO_PGRP, replace
from tkinter.constants import X


send_final = []
send_final.append(".data\n")

last_line = ""

# array para lineas del codigo
LINEA_ACTUAL = []

# string para lineas del codigo
LINEA_ACTUAL_PLANO = ""

LINEA_ACTUAL_PARAMETRO = ""
LINEA_ACTUAL_CALL = ""

#Numero de L
LN = 0

# Pila para guardar registros
PilaDictionary = {
    "Pila": [],
    "Significado": []
}

def call_function(operaciones, tabs, direcciones_memoria, posicion_memoria, X, Y, Z, OPERADOR, send_final):
    PL = 0
    # Recolectamos X
    while LINEA_ACTUAL_PLANO[PL] != "=":
        X += LINEA_ACTUAL_PLANO[PL]
        PL += 1
    PL += 1

    # Recolectamos Y
    while LINEA_ACTUAL_PLANO[PL] not in operaciones:
        Y += LINEA_ACTUAL_PLANO[PL]
        PL += 1
                
    # Recolectamos el operador
    OPERADOR = LINEA_ACTUAL_PLANO[PL]
    PL += 1

    # Recolectamos Z
    while PL != len(LINEA_ACTUAL_PLANO):
        Z += LINEA_ACTUAL_PLANO[PL]
        PL += 1

    print("\n%s, %s, %s" %(X, Y, Z))
                
    # Guardamos en memoria Y
    send_final.append("\n%sli $%s, %s" % (tabs, direcciones_memoria[posicion_memoria], Y))
    Y = direcciones_memoria[posicion_memoria]
    posicion_memoria += 1
    # Guardamos en memoria Z
    send_final.append("\n%sli $%s, %s" % (tabs, direcciones_memoria[posicion_memoria], Z))
    Z = direcciones_memoria[posicion_memoria]
    posicion_memoria += 1
    send_final.append("\n%ssyscall" % tabs)

    #Elejimos el tipo de operacion
    if OPERADOR == "+":
        send_final.append("\n%sadd $%s, $%s, $%s" % (tabs, direcciones_memoria[posicion_memoria], Y, Z))
        posicion_memoria += 1
    elif OPERADOR == "-":
        send_final.append("\n%ssub $%s, $%s, $%s" % (tabs, direcciones_memoria[posicion_memoria], Y, Z))
        posicion_memoria += 1
    elif OPERADOR == "*":
        send_final.append("\n%smul $%s, $%s, $%s" % (tabs, direcciones_memoria[posicion_memoria], Y, Z))
        posicion_memoria += 1
    elif OPERADOR == "/":
        send_final.append("\n%sdiv $%s, $%s, $%s" % (tabs, direcciones_memoria[posicion_memoria], Y, Z))
        posicion_memoria += 1
    
    return send_final, posicion_memoria

def param_and_call(espacios_memoria_1, posicion_1, send_final, tabs, LINEA_ACTUAL_PARAMETRO, CALL_WORD):
    send_final.append("\n%saddi $%s, $zero, $%s" %(tabs, espacios_memoria_1[posicion_1], LINEA_ACTUAL_PARAMETRO))
    posicion_1 += 1
    send_final.append("\n%sjal %s" %(tabs, CALL_WORD))
    return send_final, posicion_1

def getreg(VARIABLE_MEMORIA_ID, VARIABLE_MEMORIA_DIRRECCION):
    #Elementos que se pueden ignorar durante la lectura de lineas
    elementos_ignorados = ['', ' ', '\n']
    #Espacios de memoria usados para guardar valores temporales:\
    espacios_memoria_1 = ["v0", "v1", "a0", "a1", "a2"]
    posicion_1 = 0
    #Operadores reconocidos
    operaciones = ["+", "-", "*", "/"]
    #Instrucciones
    instrucciones_2 = ["if", "while"]
    instrucciones = ["=", "==", ">", "<", ">=", "<="]

    #Instrucciones para el archivo
    global send_final

    global last_line

    #posiciones de memoria
    posicion_memoria = 0
    direcciones_memoria = ["t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7", "s0", 
                        "s1", "s2", "s3", "s4", "s5", "s6", "s7", "t8", "t9"]

    global LINEA_ACTUAL
    global LINEA_ACTUAL_PLANO
    global LN
    global LINEA_ACTUAL_PARAMETRO
    global LINEA_ACTUAL_CALL

    tabs = "\t"

    file_codigo_intermedio = open("Codigo_3_direcciones.txt", "r")
    for i in file_codigo_intermedio:
        LINEA_ACTUAL_PLANO = i
        for e in LINEA_ACTUAL_PLANO:
            if e in elementos_ignorados:
                pass
            else:
                LINEA_ACTUAL.append(e)
        
        # Reiniciamos posicion_1
        if posicion_memoria > len(direcciones_memoria):
            posicion_memoria = 0
        if posicion_1 > 4:
            posicion_1 = 0


        # declaramos una etiqueta
        if len(LINEA_ACTUAL) > 0:
            if LINEA_ACTUAL[-1] == ':':
                if LINEA_ACTUAL_PLANO == "	L1:":
                    tabs += "\t"
                elif LINEA_ACTUAL_PLANO[1] != "L":
                    tabs = "\t"
                send_final.append("\n%s" % LINEA_ACTUAL_PLANO)
                LN = 0

        # comenzamos la revision (x = y + z)
        X = ""
        Y = ""
        OPERADOR = ""
        Z = ""

        IsOperation = False
        for u in operaciones:
            if u in LINEA_ACTUAL:
                IsOperation = True

        if IsOperation == True:
            send_final, posicion_memoria = call_function(operaciones, tabs, direcciones_memoria, posicion_memoria, X, Y, Z, OPERADOR, send_final)

        #Agregamos instrucciones
        IsInstruction = False
        for u in instrucciones_2:
            if u in LINEA_ACTUAL_PLANO:
                IsInstruction = True

        if IsInstruction == True:
            PL = 0
            X = ""
            Y = ""
            OPERADOR = ""
            Z = ""
            LN += 1

            if len(last_line) > 0:
                while last_line[PL] != "=":
                    X += last_line[PL]
                    PL += 1
                PL += 1

                while last_line[PL] not in instrucciones:
                    Y += last_line[PL]
                    PL += 1
                while last_line[PL] in instrucciones:
                    PL += 1
                    
                while PL != len(last_line):
                    Z += last_line[PL]
                    PL+= 1
                Z = Z.replace("\n", "")

                if "==" in last_line:
                    send_final.append("\n%sbeq $%s, $%s, L%s" % (tabs, Y, Z, LN))
                elif "!=" in last_line: 
                    send_final.append("\n%sbne $%s, $%s, L%s" % (tabs, Y, Z, LN))
                elif ">" in last_line:
                    send_final.append("\n%sbgt $%s, $%s, L%s" % (tabs, Y, Z, LN))
                elif ">=" in last_line:
                    send_final.append("\n%sbge $%s, $%s, L%s" % (tabs, Y, Z, LN))
                elif "<" in last_line:
                    send_final.append("\n%sblt $%s, $%s, L%s" % (tabs, Y, Z, LN))
                elif "<=" in last_line:
                    send_final.append("\n%sble $%s, $%s, L%s" % (tabs, Y, Z, LN))
                send_final.append("\n%ssyscall" % tabs)
        
        # comparaciones
        if " = " in LINEA_ACTUAL_PLANO:
            if len(LINEA_ACTUAL_PLANO) < 9:
                print(LINEA_ACTUAL_PLANO)

        #Goto
        if "goto" in LINEA_ACTUAL_PLANO:
            Next_Goto = False
            w = ""
            w1 = ""
            for u in LINEA_ACTUAL_PLANO:
                if Next_Goto == False:
                   w += u
                   if "goto" in w:
                       Next_Goto = True
                elif Next_Goto == True:
                    if u == " ":
                        pass
                    else:
                        w1 += u
            send_final.append("\n%sjal %s" % (tabs, w1))

        #Returns
        if "return" in LINEA_ACTUAL_PLANO:
            a = LINEA_ACTUAL_PLANO
            a = a.replace("return ", "")
            a = a.replace("\t", "")
            a = a.replace("\n", "")
            a = a.replace(" ", "")
            if a in VARIABLE_MEMORIA_ID:
                PE = VARIABLE_MEMORIA_ID.index(a)
                a = VARIABLE_MEMORIA_DIRRECCION[PE]
            # send_final.append("\n%sjr $%s" % (tabs, a))
            send_final.append("\n%sjr $ra" % tabs)
        # reiniciamos la lista para revisar la siguiente linea en limpio
        LINEA_ACTUAL = []
        last_line = LINEA_ACTUAL_PLANO

        # Call with param
        if "param" in LINEA_ACTUAL_PLANO:
            LINEA_ACTUAL_PARAMETRO = LINEA_ACTUAL_PLANO
        if "call" in LINEA_ACTUAL_PLANO:
            LINEA_ACTUAL_CALL = LINEA_ACTUAL_PLANO
        
        if len(LINEA_ACTUAL_PARAMETRO) and len(LINEA_ACTUAL_CALL):
            CALL_WORD = ""
            LINEA_ACTUAL_PARAMETRO = LINEA_ACTUAL_PARAMETRO.replace("param ", "")
            LINEA_ACTUAL_PARAMETRO = LINEA_ACTUAL_PARAMETRO.replace("\t", "")
            for u in LINEA_ACTUAL_CALL:
                CALL_WORD += u
                if u == ",":
                    CALL_WORD = CALL_WORD.replace(",", "")
                    break
                if "call " in CALL_WORD:
                    CALL_WORD = ""
            send_final, posicion_1 = param_and_call(espacios_memoria_1, posicion_1, send_final, tabs, LINEA_ACTUAL_PARAMETRO, CALL_WORD)
            LINEA_ACTUAL_CALL = ""
            LINEA_ACTUAL_PARAMETRO = ""

    file = open("MIPS_FILE.asm", "w")
    for i in send_final:
        file.write(i)

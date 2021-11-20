###############################
#Comienza el Tercer proyecto #
###############################
from os import PRIO_PGRP, linesep, replace, umask
from tkinter.constants import X

# Lista para mandar instrucciones al archivo final con primera instruccion
send_final = []
send_final.append(".data\n")

# array para lineas del codigo
LINEA_ACTUAL = []
# string para lineas del codigo
LINEA_ACTUAL_PLANO = ""

#Elementos que se pueden ignorar durante la lectura de lineas
elementos_ignorados = [' ', '\n']
#Operadores reconocidos
simbolos = ["+", "-", "*", "/"]
#posiciones de memoria
posicion_memoria = 0
direcciones_memoria = ["t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7", "s0", 
                    "s1", "s2", "s3", "s4", "s5", "s6", "s7", "t8", "t9"]
#Instrucciones
instrucciones_2 = ["if", "while"]
comparaciones = ["==", ">", "<", ">=", "<="]

# Pila para guardar registros
PilaDictionary = {
    "Pila": [],
    "Significado": []
}

#Elementos varios
#Numero de L que toca
LN = 0

#Valores para recolecar X, Y, Z
X = ""
Y = ""
Z = ""
OPERADOR = ""

# tabs
tabs = "\t"

#obtenemos los valores para comparaciones e intrucciones
def ValoresGetReg(LINEA_ACTUAL, LINEA_ACTUAL_PLANO, X, Y ,Z, OPERADOR):
    if "\t" in LINEA_ACTUAL_PLANO:
        LINEA_ACTUAL_PLANO = LINEA_ACTUAL_PLANO.replace("\t", "")
        
    u = 0
    while (LINEA_ACTUAL_PLANO[u] != "=") or (LINEA_ACTUAL_PLANO[u] in comparaciones)or (LINEA_ACTUAL_PLANO[u] in instrucciones_2):
        X += LINEA_ACTUAL_PLANO[u]
        u += 1
    u += 1
    
    while (LINEA_ACTUAL_PLANO[u] != "=") or (LINEA_ACTUAL_PLANO[u] in comparaciones)or (LINEA_ACTUAL_PLANO[u] in instrucciones_2):
        if LINEA_ACTUAL_PLANO[u] == " ":
            pass
        else:
            Y += LINEA_ACTUAL_PLANO[u]
        u += 1

    while LINEA_ACTUAL_PLANO[u] == "=":
        OPERADOR += LINEA_ACTUAL_PLANO[u]
        u += 1
    
    while u != len(LINEA_ACTUAL_PLANO):
        if LINEA_ACTUAL_PLANO[u] == "\n":
            pass
        else:
            Z += LINEA_ACTUAL_PLANO[u]
        u += 1

    return X, Y ,Z, OPERADOR

# Obtenemos X, Y, Z y OPERADOR
def RealGetReg(simbolos, X, Y, Z, OPERADOR, LINEA_ACTUAL, LINEA_ACTUAL_PLANO):
    PL = 0
    # Recolectamos X
    while LINEA_ACTUAL_PLANO[PL] != "=":
        X += LINEA_ACTUAL_PLANO[PL]
        X = X.replace("\t", "")
        X = X.replace("\n", "")
        X = X.replace(" ", "")
        PL += 1
    PL += 1

    # Recolectamos Y
    while LINEA_ACTUAL_PLANO[PL] not in simbolos:
        Y += LINEA_ACTUAL_PLANO[PL]
        Y = Y.replace("\t", "")
        Y = Y.replace("\n", "")
        Y = Y.replace(" ", "")
        PL += 1
                
    # Recolectamos el operador
    OPERADOR = LINEA_ACTUAL_PLANO[PL]
    PL += 1

    # Recolectamos Z
    while PL != len(LINEA_ACTUAL_PLANO):
        Z += LINEA_ACTUAL_PLANO[PL]
        Z = Z.replace("\n", "")
        Z = Z.replace("\t", "")
        Z = Z.replace(" ", "")
        PL += 1

    return X, Y, Z, OPERADOR

# llamamos un metodo
def call_function(tabs, direcciones_memoria, posicion_memoria, X, Y, Z, OPERADOR, send_final, PilaDictionaryPila, PilaDictionarySignificado):
    # Guardamos en memoria Y
    send_final.append("\n%sli $%s, %s" % (tabs, direcciones_memoria[posicion_memoria], Y))
    if (Y in PilaDictionaryPila) or (direcciones_memoria[posicion_memoria] in PilaDictionarySignificado):
        pass
    else:
        PilaDictionaryPila.append(Y)
        PilaDictionarySignificado.append(direcciones_memoria[posicion_memoria])
    posicion_memoria += 1

    # Guardamos en memoria Z
    send_final.append("\n%sli $%s, %s" % (tabs, direcciones_memoria[posicion_memoria], Z))
    if (Z in PilaDictionaryPila) or (direcciones_memoria[posicion_memoria] in PilaDictionarySignificado):
        pass
    else:
        PilaDictionaryPila.append(Z)
        PilaDictionarySignificado.append(direcciones_memoria[posicion_memoria])
    posicion_memoria += 1
    send_final.append("\n%ssyscall" % tabs)

    #Elejimos el tipo de operacion
    if OPERADOR == "+":
        send_final.append("\n%sadd $%s, $%s, $%s" % (tabs, direcciones_memoria[posicion_memoria], Y, Z))
        if (X in PilaDictionaryPila) or (direcciones_memoria[posicion_memoria] in PilaDictionarySignificado):
            pass
        else:
            PilaDictionaryPila.append(X)
            PilaDictionarySignificado.append(direcciones_memoria[posicion_memoria])
        posicion_memoria += 1
    elif OPERADOR == "-":
        send_final.append("\n%ssub $%s, $%s, $%s" % (tabs, direcciones_memoria[posicion_memoria], Y, Z))
        if (X in PilaDictionaryPila) or (direcciones_memoria[posicion_memoria] in PilaDictionarySignificado):
            pass
        else:
            PilaDictionaryPila.append(X)
            PilaDictionarySignificado.append(direcciones_memoria[posicion_memoria])
        posicion_memoria += 1
    elif OPERADOR == "*":
        send_final.append("\n%smul $%s, $%s, $%s" % (tabs, direcciones_memoria[posicion_memoria], Y, Z))
        if (X in PilaDictionaryPila) or (direcciones_memoria[posicion_memoria] in PilaDictionarySignificado):
            pass
        else:
            PilaDictionaryPila.append(X)
            PilaDictionarySignificado.append(direcciones_memoria[posicion_memoria])
        posicion_memoria += 1
    elif OPERADOR == "/":
        send_final.append("\n%sdiv $%s, $%s, $%s" % (tabs, direcciones_memoria[posicion_memoria], Y, Z))
        if (X in PilaDictionaryPila) or (direcciones_memoria[posicion_memoria] in PilaDictionarySignificado):
            pass
        else:
            PilaDictionaryPila.append(X)
            PilaDictionarySignificado.append(direcciones_memoria[posicion_memoria])
        posicion_memoria += 1
    
    return send_final, posicion_memoria, PilaDictionaryPila, PilaDictionarySignificado

# Se reajusta el texto segun los registros
def ChangeLine(LINEA_ACTUAL, LINEA_ACTUAL_PLANO, PilaDictionaryPila, PilaDictionarySignificado):
    e = 0
    for i in LINEA_ACTUAL:
        if i in PilaDictionaryPila:
            a = PilaDictionaryPila.index(i)
            b = PilaDictionarySignificado[a]
            LINEA_ACTUAL_PLANO = LINEA_ACTUAL_PLANO.replace(i, b)
            LINEA_ACTUAL[e] = b
        e += 1
    return LINEA_ACTUAL, LINEA_ACTUAL_PLANO

#comparaciones
def Comparaciones(X, Y ,Z, OPERADOR, send_final):
    if "==" == OPERADOR:
        send_final.append("\n%sbeq $%s, $%s, L%s" % (tabs, X, Y, Z))
    elif "!=" == OPERADOR: 
        send_final.append("\n%sbne $%s, $%s, L%s" % (tabs, X, Y, Z))
    elif ">" == OPERADOR:
        send_final.append("\n%sbgt $%s, $%s, L%s" % (tabs, X, Y, Z))
    elif ">=" == OPERADOR:
        send_final.append("\n%sbge $%s, $%s, L%s" % (tabs, X, Y, Z))
    elif "<" == OPERADOR:
        send_final.append("\n%sblt $%s, $%s, L%s" % (tabs, X, Y, Z))
    elif "<=" == OPERADOR:
        send_final.append("\n%sble $%s, $%s, L%s" % (tabs, X, Y, Z))
    send_final.append("\n%ssyscall" % tabs)

    return send_final

#devoluciones
def ReturnOrGoto(LINEA_ACTUAL, LINEA_ACTUAL_PLANO, send_final):
    word = ""
    word2 = ""
    if "goto" in LINEA_ACTUAL_PLANO:
        for u in LINEA_ACTUAL_PLANO:
            word += u
            if "goto " in word:
                if u == " ":
                    pass
                else:
                    word2 += u
            else:
                pass
        send_final.append("\n%sjal %s" % (tabs, word2))
    elif "return" in LINEA_ACTUAL_PLANO:
        for u in LINEA_ACTUAL_PLANO:
            word += u
            if "return " in word:
                if u == " ":
                    pass
                else:
                    word2 += u
            else:
                pass
        send_final.append("\n%sjr $ra" % tabs)

    return send_final

def getreg(VARIABLE_MEMORIA_ID, VARIABLE_MEMORIA_DIRRECCION):
    global send_final
    global LINEA_ACTUAL
    global LINEA_ACTUAL_PLANO

    global posicion_memoria
    global LN

    global X
    global Y
    global Z
    global OPERADOR

    global tabs

    # lectura de lineas
    file_codigo_intermedio = open("Codigo_3_direcciones.txt", "r")
    word = ""
    for i in file_codigo_intermedio:
        LINEA_ACTUAL_PLANO = i
        LINEA_ACTUAL = []
        for e in LINEA_ACTUAL_PLANO:
            if (e in elementos_ignorados) or (e == "\t") or (e == ''):
                pass
            else:
                word += e
            if e in elementos_ignorados:
                LINEA_ACTUAL.append(word)
                word = ""
            else:
                pass
        
        # Re escribimos las lineas para ajustarla a los registros
        LINEA_ACTUAL, LINEA_ACTUAL_PLANO = ChangeLine(LINEA_ACTUAL, LINEA_ACTUAL_PLANO, PilaDictionary["Pila"], PilaDictionary["Significado"])
        # declaramos etiquetas
        if len(LINEA_ACTUAL) > 0:
            if ":" in LINEA_ACTUAL[0]:
                if LINEA_ACTUAL_PLANO == "	L1:":
                    tabs += "\t"
                elif LINEA_ACTUAL_PLANO[1] != "L":
                    tabs = "\t"
                send_final.append("\n%s" % LINEA_ACTUAL_PLANO)
                LN = 0

        # Recoleccion de X, Y, Z
        X = ""
        Y = ""
        OPERADOR = ""
        Z = ""
        IsOperation = False
        for u in simbolos:
            if u in LINEA_ACTUAL:
                IsOperation = True

        if IsOperation == True:
            X, Y, Z, OPERADOR = RealGetReg(simbolos, X, Y, Z, OPERADOR, LINEA_ACTUAL, LINEA_ACTUAL_PLANO)
            send_final, posicion_memoria, PilaDictionary["Pila"], PilaDictionary["Significado"] = call_function(tabs, direcciones_memoria, posicion_memoria, X, Y, Z, OPERADOR, send_final, PilaDictionary["Pila"], PilaDictionary["Significado"])

        # comparaciones
        IsInstruction = False
        for u in comparaciones:
            if u in LINEA_ACTUAL_PLANO:
                IsInstruction = True

        if IsInstruction == True:
            X, Y ,Z, OPERADOR = ValoresGetReg(LINEA_ACTUAL, LINEA_ACTUAL_PLANO, X, Y ,Z, OPERADOR)
            send_final = Comparaciones(X, Y ,Z, OPERADOR, send_final)

        # instrucciones
        IsInstruction = False
        for u in instrucciones_2:
            if u in LINEA_ACTUAL_PLANO:
                IsInstruction = True

        if IsInstruction == True:
            #print(LINEA_ACTUAL_PLANO)
            pass

        # return or goto
        if ("goto" in LINEA_ACTUAL_PLANO) or ("return" in LINEA_ACTUAL_PLANO):
            send_final = ReturnOrGoto(LINEA_ACTUAL, LINEA_ACTUAL_PLANO, send_final)

    # mandamos todo el mensaje recolectado
    file = open("MIPS_FILE.asm", "w")
    for i in send_final:
        file.write(i)
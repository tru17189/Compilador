from codecs import decode
from os import SCHED_BATCH, stat, truncate
import os
from tkinter import *
from typing import Counter, get_origin
from antlr4 import *
from antlr4.tree.Trees import  TerminalNode
from DecafLexer import DecafLexer
from DecafParser import DecafParser
from DecafListener import DecafListener
import time
from GetReg_1 import getreg

varDeclaration = False
parameterType = False
parameterType2 = False
varType = False
program = "Program"
methodDeclaration = False
structDeclaration = False
offset = 0
methodDeclaration2 = False
MethodId = ""
MethodType = ""
structD = False
structId = ""
structIDD = ""
contador = 0
contador2 = 0
contador3 = 0

VarSymbolTable = {
    "VarId": [],
    "VarType": [],
    "Scope": [],
    "offset": []
}
MethodSymbolTable = {
    "methodId": [],
    "methodType": []
}
StructSymbolTable = {
    "VarId": [],
    "VarType": [],
    "StructId": []
}

def clean():
    VarSymbolTable["VarId"] = []
    VarSymbolTable["VarType"] = []
    VarSymbolTable["Scope"] = []
    VarSymbolTable["offset"] = []

    MethodSymbolTable["methodId"] = []
    MethodSymbolTable["methodType"] = []

    StructSymbolTable["VarId"] = []
    StructSymbolTable["VarType"] = []
    StructSymbolTable["StructId"] = []

class KeyPrinter(DecafListener):
    def exitKey(self, ctx):
        print("Hello: %s" % ctx.ID())

def main(argv):
    input_stream = FileStream(argv)
    lexer = DecafLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = DecafParser(stream)
    tree = parser.program()  

    printer = KeyPrinter()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)
    traverse(tree, parser.ruleNames)

def traverse(tree, rule_names, indent = 0):
    global varDeclaration
    global contador
    global contador2 
    global contador3
    global varType
    global parameterType
    global parameterType2
    global program
    global methodDeclaration
    global structDeclaration
    global offset
    global methodDeclaration2
    global MethodId
    global MethodType
    global structD
    global structId
    global structIDD

    if tree.getText() == "<EOF>":
        return
    elif isinstance(tree, TerminalNode):
        ProbablyWord = "T='{1}'".format("  " * indent, tree.getText())

        if (methodDeclaration == True) or (structDeclaration == True):
            contador2 += 1
            if methodDeclaration2 == True:
                if contador2 == 2:
                    MethodId = tree.getText()
                    MethodSymbolTable["methodId"].append(MethodId)
                    methodDeclaration2 = False
                elif contador2 == 1:
                    MethodType = tree.getText()
                    MethodSymbolTable["methodType"].append(MethodType)

            if contador2 == 2:
                program = tree.getText()
                methodDeclaration = False
                structDeclaration = False
                contador2 = 0

        if (varType == True) or (parameterType2 == True):
            contador += 1
            if contador == 1:
                varTy = tree.getText()
                VarSymbolTable["VarType"].append(varTy)
                if varTy == "int":
                    offset = 4
                elif varTy == "boolean":
                    offset = 2
                elif varTy == "char":
                    offset = 2
                elif varTy == "struct":
                    offset = 8
                varType = False
                parameterType2 = False
                contador = 0

        if (varDeclaration == True) or (parameterType == True):
            contador += 1
            if contador == 2:
                varId = tree.getText()
                VarSymbolTable["VarId"].append(varId)
                VarSymbolTable["Scope"].append(program)
                VarSymbolTable["offset"].append(offset)
                varDeclaration = False
                parameterType = False
                contador = 0

        if structD == True:
            contador3 += 1
            if contador3 == 1:
                structId = tree.getText()
                StructSymbolTable["VarId"].append(structId)
                StructSymbolTable["VarType"].append(program)
            elif contador3 == 2:
                structIDD = tree.getText()
                StructSymbolTable["StructId"].append(structIDD)
                structD = False
                contador3 = 0
        
        if ProbablyWord == "T='struct'":
            structD = True 
        
        # print("{0}T='{1}'".format("  " * indent, tree.getText()))

    else:
        ProbablyWord = "R='{1}'".format("  " * indent, rule_names[tree.getRuleIndex()])

        if ProbablyWord == "R='varDeclaration'":
            varDeclaration = True
        if ProbablyWord == "R='parameterType'":
            parameterType = True
            parameterType2 = True
        if ProbablyWord == "R='varType'":
            varType = True
        if ProbablyWord == "R='methodDeclaration'":
            methodDeclaration = True
            methodDeclaration2 = True
        if ProbablyWord == "R='structDeclaration'":
            structDeclaration = True
        # print("{0}R='{1}'".format("  " * indent, rule_names[tree.getRuleIndex()]))
        if (tree.children != None):
            for child in tree.children:
                traverse(child, rule_names, indent + 1)

IsThereRightKey = False
varDeclaration = False 
methodDeclaration = False
MethodType = ""
MethodTypeReturn = False
IsThereReturn = False
methodCall = False
methodCallName = ""
eq_op = False
location = False
LeftWord = ""
RightWord = ""
PositionI = 0
PositionE = 0
PositionIStruct = 0
PositionEStruct = 0
statement = False
location3 = False
rel_op = False
contador = 0
contador2 = 0
contador3 = 0

def SecondMain(argv_2):
    global PositionI
    global PositionE
    global PositionIStruct
    global PositionEStruct
    input_stream_2 = FileStream(argv_2)
    lexer_2 = DecafLexer(input_stream_2)
    stream_2 = CommonTokenStream(lexer_2)
    parser_2 = DecafParser(stream_2)
    tree_2 = parser_2.program()  

    printer_2 = KeyPrinter()
    walker_2 = ParseTreeWalker()
    walker_2.walk(printer_2, tree_2)

    # Metodo main sin paramentros 
    ThereIsMain = False
    ThereIsVoid = False
    for i, e in zip(MethodSymbolTable["methodId"], MethodSymbolTable["methodType"]):
        if i == 'main':
            ThereIsMain = True
        if e == 'void':
            ThereIsVoid = True
        
    if (ThereIsVoid == True) and (ThereIsMain == True):
        pass
    else: 
        print("\n***No hay método main sin parámetros en el inicio del programa***\n")
        input()
    
    # Ningún identificador es declarado dos veces en el mismo ámbito
    for i in VarSymbolTable["VarId"]:
        CantidadVeces = VarSymbolTable["VarId"].count(i)
        if CantidadVeces >= 2:
            for e in VarSymbolTable["VarId"]:
                if (i == e) and (PositionI != PositionE):
                    try:
                        if (i in StructSymbolTable["VarId"]) and (e in StructSymbolTable["VarId"]):
                            for u in StructSymbolTable["VarId"]:
                                CantidadVeces2 = StructSymbolTable["VarId"].count(u)
                                if CantidadVeces2 >= 2:
                                    for k in StructSymbolTable["VarId"]:
                                        if (u == k) and (PositionIStruct != PositionEStruct):
                                            try:
                                                if StructSymbolTable["StructId"][PositionIStruct] == StructSymbolTable["StructId"][PositionEStruct]:
                                                    print("\n***Ningún identificador es declarado dos veces en el mismo ámbito***")
                                                    print("***El valor que esta fallando es: %s y %s***\n" %(i, e))
                                                    input()
                                                else:
                                                    pass
                                            except:
                                                pass
                                        PositionEStruct += 1
                                PositionIStruct += 1
                                PositionEStruct = 0
                        elif VarSymbolTable["Scope"][PositionI] == VarSymbolTable["Scope"][PositionE]:
                            print("\n***Ningún identificador es declarado dos veces en el mismo ámbito***")
                            print("***El valor que esta fallando es: %s y %s***\n" %(i, e))
                            input()
                        else:
                            pass
                    except:
                        pass
                PositionE += 1
        PositionI += 1
        PositionE = 0

    Second_Run(tree_2, parser_2.ruleNames)

def Second_Run(tree_2, rule_names, indent = 0):
    global IsThereRightKey
    global varDeclaration
    global methodDeclaration
    global MethodType
    global MethodTypeReturn
    global IsThereReturn
    global methodCall
    global methodCallName 
    global eq_op
    global location 
    global LeftWord
    global RightWord
    global statement
    global location3
    global rel_op
    global contador
    global contador2
    global contador3
    simbolos_ignorados = [";", "!", "," ".", "[", "]", "{", "}", "(", ")", "*", "-", ".", "+", "/", ","]
    lista_numeros = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    lista_letras = ["q", "Q", "w", "W", "e", "E", "r", "R", "t", "T", "y", "Y", "u", "U", "i", "I",
                    "p", "P", "a", "A", "d", "D", "f", "F", "g", "G", "h", "H", "j", "J", "k", "K",
                    "l", "L", "z", "Z", "x", "X", "c", "C", "v", "V", "b", "B", "n", "N", "m", "M"]
    lista_booleana = ["false", "true"]

    if tree_2.getText() == "<EOF>":
        return
    elif isinstance(tree_2, TerminalNode):
        ProbablyWord = "T='{1}'".format("  " * indent, tree_2.getText())

        # num en la declaración de un arreglo debe ser mayor a 0
        if (IsThereRightKey == True) and (varDeclaration == True):
            contador += 1
            if contador == 1:
                numero = tree_2.getText()
                try: 
                    numero = int(numero)
                    if numero < 0:
                       print("\n***num en la declaración de un arreglo debe ser mayor a 0***")
                       print("***El valor que esta fallando es: %s***\n" % numero)
                       input()
                    else:
                        pass 
                except:
                    print("\n***num en la declaración de un arreglo debe ser mayor a 0***\n")
                    print("***El valorrrrrrr que esta fallando es: %s***\n" % numero)
                    input()
                IsThereRightKey = False
                varDeclaration = False
                contador = 0
        
        # Si el método es de tipo void no tiene valor de retorno en instrucción return
        if methodDeclaration == True:
            contador += 1
            if contador == 1:
                MethodType = tree_2.getText()
                methodDeclaration = False
                contador = 0
        if MethodType == "void":
            if ProbablyWord == "T='return'":
                MethodTypeReturn = True
        if MethodTypeReturn == True:
            contador2 += 1
            if contador2 == 2:
                NextSymbolReturn = tree_2.getText()
                if NextSymbolReturn in simbolos_ignorados:
                    pass
                else:
                    print("\n***Si el método es de tipo void no tiene valor de retorno en instrucción return***")
                    print("***Valor que esta fallando es: %s***\n" % NextSymbolReturn)
                    input()
                contador2 = 0
                MethodTypeReturn = False
        
        # El valor de retorno de un método debe de ser del mismo tipo con que fue declarado el método.
        if IsThereReturn == True:
            NextSymbolReturn = tree_2.getText()
            if NextSymbolReturn in simbolos_ignorados:
                pass
            elif NextSymbolReturn in StructSymbolTable["StructId"]:
                pass
            else:
                NextSymbolType = ""
                if NextSymbolReturn in VarSymbolTable["VarId"]:
                    NextSymbolType = VarSymbolTable["VarType"][VarSymbolTable["VarId"].index(NextSymbolReturn)]
                elif NextSymbolReturn in MethodSymbolTable['methodId']:
                    NextSymbolType = MethodSymbolTable['methodType'][MethodSymbolTable['methodId'].index(NextSymbolReturn)]
                elif NextSymbolReturn in StructSymbolTable["VarId"]:
                    NextSymbolType = "struct"
                elif NextSymbolReturn in lista_numeros:
                    NextSymbolType = "int"
                if MethodType == NextSymbolType:
                    pass
                else:
                    #print("\n***El valor de retorno de un método debe de ser del mismo tipo con que fue declarado el método***")
                    #print("***Valor que esta fallando es: %s****\n" %tree_2.getText())
                    #input()
                    pass
            if ProbablyWord == "T=';'":
                IsThereReturn = False

        #El número y tipos de argumentos en la llamada a un método deben de ser los mismos que los argumentos formales
        if methodCall == True:
            if methodCallName == True:
                methodCallName = tree_2.getText()

            IntoMethodType = ""
            IntoMethod = tree_2.getText()
            if IntoMethod in simbolos_ignorados:
                pass
            elif IntoMethod in StructSymbolTable["StructId"]:
                pass
            elif IntoMethod in MethodSymbolTable["methodId"]:
                pass
            else:
                NextSymbolType = ""
                if IntoMethod in VarSymbolTable["VarId"]:
                    NextSymbolType = VarSymbolTable["VarType"][VarSymbolTable["VarId"].index(IntoMethod)]
                elif IntoMethod in MethodSymbolTable['methodId']:
                    NextSymbolType = MethodSymbolTable['methodType'][MethodSymbolTable['methodId'].index(IntoMethod)]
                elif IntoMethod in StructSymbolTable["VarId"]:
                    NextSymbolType = "struct"
                elif IntoMethod in lista_numeros:
                    NextSymbolType = "int"
                IntoMethodType = MethodSymbolTable["methodType"][MethodSymbolTable["methodId"].index(methodCallName)]
                if IntoMethodType == NextSymbolType:
                    pass
                elif IntoMethodType == "void":
                    idd = VarSymbolTable["VarId"].index(VarSymbolTable["VarId"][VarSymbolTable["Scope"].index(methodCallName)])
                    typpe = VarSymbolTable["VarType"][idd]
                    if typpe == NextSymbolType:
                        pass
                    else:
                        print("\n***El número y tipos de argumentos en la llamada a un método deben de ser los mismos que los argumentos formales***")
                        print("***Valor que esta fallando es: %s****\n" %tree_2.getText())
                        input()
                else:
                    print("\n***El número y tipos de argumentos en la llamada a un método deben de ser los mismos que los argumentos formales***")
                    print("***Valor que esta fallando es: %s****\n" %tree_2.getText())
                    input()
            if ProbablyWord == "T=';'":
                methodCall = False

        # Los tipos de operandos para los operadores <eq_ops> deben de ser int, char o boolean, 
        # y además ambos operandos deben de ser del mismo tipo.
        if location == True:
            if tree_2.getText() == "==":
                pass
            else:
                LeftWord = tree_2.getText()
            location = False
        if eq_op == True:
            LeftType = ""
            RightType = ""
            contador3 += 1
            if contador3 == 2:
                RightWord = tree_2.getText()
                if LeftWord in VarSymbolTable["VarId"]:
                    LeftType = VarSymbolTable["VarType"][VarSymbolTable["VarId"].index(LeftWord)]
                else:
                    if LeftWord in lista_numeros:
                        LeftType = "int"
                    elif LeftWord in lista_letras:
                        LeftType = "char"
                    elif LeftWord in lista_booleana:
                        LeftType = "boolean"
                    else:
                        LeftType = "NO TYPE"
                
                if RightWord in VarSymbolTable["VarId"]:
                    RightType = VarSymbolTable["VarType"][VarSymbolTable["VarId"].index(RightWord)]
                else:
                    if RightWord in lista_numeros:
                        RightType = "int"
                    elif RightWord in lista_letras:
                        RightType = "char"
                    elif RightWord in lista_booleana:
                        RightType = "boolean"
                    else:
                        RightType = "NO TYPE"

                if LeftType == RightType:
                    pass
                elif (LeftType == "NO TYPE") or (RightType == "NO TYPE"):
                    print("\n***Los tipos de operandos para los operadores <eq_ops> deben de ser int, char o boolean***")
                    print("***Valor que esta fallando es: %s y % s****\n" %(LeftType, RightType))
                    input()
                else:
                    print("\n***Los tipos de operandos para los operadores <eq_ops> ambos operandos deben de ser del mismo tipo***")
                    print("***Valor que esta fallando es: %s y % s****\n" %(LeftType, RightType))
                    input()
                eq_op = False
                contador3 = 0

        # Ningún identificador es utilizado antes de ser declarado.
        if (statement == True) and (location3 == True):
            contador3 += 1
            if contador3 == 1:
                variableLlamada = tree_2.getText()
                if variableLlamada in simbolos_ignorados:
                    pass
                elif (variableLlamada == "return") or (variableLlamada == "if") or (variableLlamada == "while"):
                    pass
                elif variableLlamada in VarSymbolTable["Scope"]:
                    pass
                else:
                    if variableLlamada in VarSymbolTable["VarId"]:
                        pass
                    elif variableLlamada in StructSymbolTable["StructId"]:
                        pass
                    else:
                        print("\n***Ningún identificador es utilizado antes de ser declarado.***")
                        print("***Valor que esta fallando es: %s****\n" % variableLlamada)
                        input()
                contador3 = 0
                statement = False
                location3 = False
        
        # Los tipos de operandos para los operadores <arith_op> y <rel_op> deben de ser int.
        '''if location == True:
            if tree_2.getText() == "<":
                pass
            else:
                LeftWord = tree_2.getText()
            location = False
        if rel_op == True:
            contador3 += 1
            if contador3 == 1:
                RightWord = tree_2.getText()
                print(LeftWord)
                print(RightWord)
                rel_op = False
                contador3 = 0'''

        if ProbablyWord == "T='['":
            IsThereRightKey = True
        if ProbablyWord == "T=']'":
            IsThereRightKey = False
        if ProbablyWord == "T='return'":
            IsThereReturn = True
        # print("{0}T='{1}'".format("  " * indent, tree_2.getText()))
        pass
    else:
        ProbablyWord = "R='{1}'".format("  " * indent, rule_names[tree_2.getRuleIndex()])

        if ProbablyWord == "R='expression'":
            varDeclaration = False
        if ProbablyWord == "R='varDeclaration'":
            varDeclaration = True
        if ProbablyWord == "R='methodDeclaration'":
            methodDeclaration = True
        if ProbablyWord == "R='methodCall'":
            methodCall = True
            methodCallName = True
        if ProbablyWord == "R='eq_op'":
            eq_op = True
        if ProbablyWord == "R='location'":
            location = True
            location3 = True
        if ProbablyWord == "R='statement'":
            statement = True
        if ProbablyWord == "R='rel_op'":
            rel_op = True
        # print("{0}R='{1}'".format("  " * indent, rule_names[tree_2.getRuleIndex()]))
        if (tree_2.children != None):
            for child in tree_2.children:
                Second_Run(child, rule_names, indent + 1)    

###############################
#Comienza el segundo proyecto #
###############################

# Esta lista almacenara las instrucciones del codigo de 3 direcciones
send_file = []

# Esta variable es para llevar control del tamano del offset
offset = 0
function_counter = 1

# Este diccionario es para llevar registro de los elementos encontrados durante la construccion del arbol
trunk = {
    "type1": [],
    "type2": [],
    "content": []
}

# Los simbolos dentro de esta lista indican el fin de una linea o instruccion
end_line = ["{", ";"]
line = ""
line_split = []
line_split_function = []
line_split_return = []
line_split_accion = []
end_fuction = False

# Variables de control
Puente_Tipo = False
identificadores = ["R='declaration'", "R='methodDeclaration'", "R='statement'", "R='location'", "R='expression'"]
identificadores2 = ["R='location'", "R='methodCall'"]
ArgFun1 = ""
ArgFun2 = ""
ArgFun3 = ""
last_type_3 = ""
last_type_return = ""
last_type_accion = ""
final_accion = ""
wordArg3 = ""

# para llevar control de las ranuras
posicion_memoria = 0
direcciones_memoria = ["t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7", "s0", 
                        "s1", "s2", "s3", "s4", "s5", "s6", "s7", "t8", "t9"]
posibles_acciones = ["if", "while", "for"]

# extras
fin_global_status = False

# Variables en el lenguaje intermedio
Variable_Memoria = {
    "id": [],
    "direccion": []
}

def clean2():
    trunk["type1"] = []
    trunk["type2"] = []
    trunk["content"] = []
    Variable_Memoria["id"] = []
    Variable_Memoria["direccion"] = []

# definicion para reiniciar la recoleccion
def cleaner(list1, list2, list3, array, sentence):
    for i in array:
        sentence += "%s " %i
    list3.append(sentence)
    list1.append(" ")
    list2.append(" ")
    list3.append(" ")
    sentence = ""
    return list1, list2, list3, array, sentence

# Definicion para la declaracion de metodo
def DeclaracionMetodo(send_file, fuction_counter, content, methodId):
    for i in content:
        if i in methodId:
            ans = "\n%s: " % i
            send_file.append(ans)
    return send_file, fuction_counter

# declaracion de variables (procedencia operadores)
def Variables(send_file, direcciones_memoria, posicion_memoria, content, varid, offset, offset_list, id, direccion):
    content_in_one_line = ""
    c = 0
    end_line = ["{", ";"]
    offset_array = 1
    
    # revisamos si la variable es un array para tomar el valor del array
    if ("[" in content) and ("]" in content):
        for i in content:
            if i == "]":
                break
            elif i == "[":
                try:
                    offset_array = int(content[c+1])
                except:
                    offset_array = 1
            c += 1
    c= 0

    for i in content:
        if (i in varid) and (i not in id):
            id.append(i)
            p = varid.index(i)
            elemento = VarSymbolTable["Scope"][p]
            if elemento == "Program":
                direccion.append("sp[%s]" % offset)
            else: 
                direccion.append("fp[%s]" % offset)
            if offset_array > 1:
                valor = offset_list[p] + (offset_array * offset_list[p])
            else:
                valor = offset_list[p]
            offset += valor
    
    for i in content:
        if i in id:
            p = id.index(i)
            content[c] = direccion[p]
        c += 1
    c = 0

    for i in content:
        content_in_one_line += i

    ultima_declaracion = ""
    for i in content_in_one_line:
        if i == "=":
            break
        else:
            ultima_declaracion += i    
    
    # Precedencia de operadores
    simbolos = ["*", "/", "+", "-"]
    arg1 = ""
    op = ""
    arg2 = ""
    status = "arg1"

    # Declaracion comun
    status1 = False
    for i in simbolos:
        if i in content:
            status1 = True
    if "return" in content:
        status1 = True

    if status1 == False:
        status = False
        declaracion_simple = ""
        for i in content:
            if i in simbolos:
                status = True
            declaracion_simple += "%s " %i

        if status == False:
            ans = "\n\t%s" % declaracion_simple
            send_file.append(ans)
        else:
            status = False

    # multiplicaciones -> *
    if "*" in content:
        for i in content_in_one_line:
            if status == "arg1":
                if i != "*":
                    if i in simbolos:
                        arg1 = ""
                if i == "*":
                    pass
                else:
                    arg1 += i
            elif status == "arg2":
                if i in simbolos:
                    break
                else:
                    arg2 += i
            
            if (i == "="):
                arg1 = ""
            elif i == "*":
                status = "arg2"
                op = "*"
        replace_sentence = "%s%s%s" %(arg1, op, arg2)
        ans = "\n\t%s = %s %s %s" %(direcciones_memoria[posicion_memoria], arg1, op, arg2)
        send_file.append(ans)
        content_in_one_line = content_in_one_line.replace(replace_sentence, direcciones_memoria[posicion_memoria])
        posicion_memoria += 1
        status = "arg1"
        arg1 = ""
        arg2 = ""

    # divisiones -> /
    if "/" in content:
        for i in content_in_one_line:
            if status == "arg1":
                if i != "/":
                    if i in simbolos:
                        arg1 = ""
                    else:
                        arg1 += i
                else:
                    pass
            elif status == "arg2":
                if i in simbolos:
                    break
                else:
                    arg2 += i
            
            if (i == "="):
                arg1 = ""
            elif i == "/":
                status = "arg2"
                op = "/"
        replace_sentence = "%s%s%s" %(arg1, op, arg2)
        ans = "\n\t%s = %s %s %s" %(direcciones_memoria[posicion_memoria], arg1, op, arg2)
        send_file.append(ans)
        content_in_one_line = content_in_one_line.replace(replace_sentence, direcciones_memoria[posicion_memoria])
        posicion_memoria += 1
        status = "arg1"
        arg1 = ""
        arg2 = ""
    
    # divisiones -> +
    if "+" in content:
        for i in content_in_one_line:
            if status == "arg1":
                if i != "+":
                    if i in simbolos:
                        arg1 = ""
                    else:
                        arg1 += i
                else:
                    pass
            elif status == "arg2":
                if i in simbolos:
                    break
                else:
                    arg2 += i
            
            if (i == "="):
                arg1 = ""
            elif i == "+":
                status = "arg2"
                op = "+"
        replace_sentence = "%s%s%s" %(arg1, op, arg2)
        ans = "\n\t%s = %s %s %s" %(direcciones_memoria[posicion_memoria], arg1, op, arg2)
        send_file.append(ans)
        content_in_one_line = content_in_one_line.replace(replace_sentence, direcciones_memoria[posicion_memoria])
        posicion_memoria += 1
        status = "arg1"
        arg1 = ""
        arg2 = ""
    
    # divisiones -> -
    if "-" in content:
        for i in content_in_one_line:
            if status == "arg1":
                if i != "-":
                    if i in simbolos:
                        arg1 = ""
                    else:
                        arg1 += i
                else:
                    pass
            elif status == "arg2":
                if i in simbolos:
                    break
                else:
                    arg2 += i
            
            if (i == "="):
                arg1 = ""
            elif i == "-":
                status = "arg2"
                op = "-"
        replace_sentence = "%s%s%s" %(arg1, op, arg2)
        ans = "\n\t%s = %s %s %s" %(direcciones_memoria[posicion_memoria], arg1, op, arg2)
        send_file.append(ans)
        content_in_one_line = content_in_one_line.replace(replace_sentence, direcciones_memoria[posicion_memoria])
        posicion_memoria += 1
        status = "arg1"
        arg1 = ""
        arg2 = ""

    # send_file.append("\n\t%s" % content_in_one_line)
    return send_file, posicion_memoria, offset, id, direccion

# llamadas de funciones
def CallFuction(send_file, line_split, id, direccion, methodid, direcciones_memoria, posicion_memoria, ArgFun1, ArgFun3):
    sentence = ""
    parametros = []
    types_variable = ["int", "char", "struct", "boolean"]
    numero_parametros = 1
    c = 0
    ans = ""
    # Parametros
    status = False
    for i in line_split:
        if (status == True) and (i != ")"):
            if "," in i:
                numero_parametros += 1
            parametros.append(i)

        if i == "(":
            status = True
        elif i == ")":
            status = False
    
    if len(parametros) <= 0:
        ans = "\n\tparam %s" % sentence

    for i in parametros:
        if i in types_variable:
            parametros[c] = ""
        elif i == "(":
            parametros[c] = ""
        c += 1
    c = 0

    for i in parametros:
        if i in id:
            p = id.index(i)
            parametros[c] = direccion[p]
            i = parametros[c]
        sentence += i
        ans = "\n\tparam %s" % sentence
        c+=1
    c = 0
    send_file.append(ans)

    # Llamada a la funcion
    for i in line_split:
        if i in methodid:
            # ans = "\ny = call %s, %s" % (i, numero_parametros)
            ans = "\n\tcall %s, %s" % (i, numero_parametros)
    send_file.append(ans)

    # Asignacion de la funcion llamada a un espacio de memoria 
    ans = "\n\t%s = y" % direcciones_memoria[posicion_memoria]
    send_file.append(ans)
    posicion_memoria += 1

    # print("argfun3: ", ArgFun1, ArgFun2, ArgFun3)
    # return o asignacion?
    if ArgFun1 == "return":
        ans = "\n\treturn %s" % direcciones_memoria[posicion_memoria-1]
    else:
        if ArgFun3 in id:
            p = id.index(ArgFun3)
            ArgFun3 = direccion[p]
        if "}" in ArgFun3:
            ArgFun3 = ArgFun3.replace("}", "")
        ans = "\n\t%s = %s" % (ArgFun3, direcciones_memoria[posicion_memoria-1])
    send_file.append(ans)

    return send_file, id, direccion, posicion_memoria

# Return comun
def Return(send_file, line_split_return, methodid):
    sentence = ""
    for i in line_split_return:
        if i in methodid:
            sentence = ""
            break
        else:
            sentence += "%s " %i
    
    send_file.append("\n\t%s" % sentence)
    return send_file

# acciones
def Instruccion(send_file, line_split_accion, posibles_acciones, direcciones_memoria, posicion_memoria, id, direccion, fuction_counter, offset, offset_list, varid):
    condicion = []
    condicion_sentence = ""
    final_accion = ""
    c = 0
    # obtenemos la condicion
    status = False
    for i in line_split_accion:
        if status == True:
            if i == ")":
                pass
            else:
                condicion.append(i)

        if i == "(":
            status = True
        elif i == ")":
            status = False
    
    for i in condicion:
        if (i in varid) and (i not in id):
            id.append(i)
            p = varid.index(i)
            direccion.append("fp[%s]" % offset)
            offset += offset_list[p]
    
    for i in condicion:
        if i in id:
            p = id.index(i)
            condicion[c] = direccion[p]
        c += 1
    c = 0

    for i in condicion:
        condicion_sentence += i

    # indentificamos el tipo de accion
    for i in line_split_accion:
        if i in posibles_acciones:
            if i == "if":
                ans = "\n\t%s = %s" % (direcciones_memoria[posicion_memoria], condicion_sentence)
                send_file.append(ans)
                ans = "\n\tif %s goto L%s" % (direcciones_memoria[posicion_memoria], fuction_counter)
                real = "\n\tL%s: " % fuction_counter
                posicion_memoria += 1
                fuction_counter += 1
                send_file.append(ans)
                ans = "\n\tgoto L%s" % fuction_counter
                falso = "\n\tL%s: " % fuction_counter
                fuction_counter += 1
                send_file.append(ans)
                fuction_counter += 1
                send_file.append(real)
                final_accion  = falso

            elif i == "while":
                ans = "\n\t%s = %s" % (direcciones_memoria[posicion_memoria], condicion_sentence)
                send_file.append(ans)
                ans = "\n\tL%s: " % fuction_counter
                fuction_counter += 1
                send_file.append(ans)
                ans = "\n\twhile %s goto L%s" % (direcciones_memoria[posicion_memoria], fuction_counter)
                posicion_memoria += 1
                fuction_counter += 1
                send_file.append(ans)
                ans = "\n\tgoto L%s" % fuction_counter
                fuction_counter += 1
                send_file.append(ans)
                p = fuction_counter - 2
                ans = "\n\tL%s:" % p
                send_file.append(ans)
                p = fuction_counter - 3
                p1 = fuction_counter - 1
                final_accion = "\n\tgoto L%s\n\tL%s:" % (p, p1)
    
    return send_file, direcciones_memoria, posicion_memoria, fuction_counter, final_accion, id, direccion, offset

# structs
def Structs_Varibles(send_file, line_split, id, direccion, direcciones_memoria, posicion_memoria):
    sentence = ""
    Nombre_Struct = ""
    c = 0
    for i in line_split:
        sentence += i
    
    # Separamos la variable de tipo struct
    status = False
    for i in line_split:
        if i == "=":
            status = True
        if status == False:
            Nombre_Struct += i
        else:
            break

    # Revisamos si ya tiene un id
    for i in line_split:
        if i in id:
            p = id.index(i)
            p = direccion[p]
            ans = "\n\tfp[%s]" % p
            sentence = sentence.replace(Nombre_Struct, ans)
    # Lo configuramos por si no tiene un id    
        else: 
            ans = "\n\t%s = 0 + 0" % direcciones_memoria[posicion_memoria]
            ans1 = "\n\tfp[%s]" % direcciones_memoria[posicion_memoria]
            sentence = sentence.replace(Nombre_Struct, ans1)
            id.append(Nombre_Struct)
            direccion.append(ans1)

    posicion_memoria += 1
    send_file.append(ans)
    send_file.append(sentence)
    return send_file, posicion_memoria, id, direccion

def ThirdMain(argv):
    input_stream = FileStream(argv)
    lexer = DecafLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = DecafParser(stream)
    tree = parser.program()  

    printer = KeyPrinter()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)

    CodigoTresDirreciones(tree, parser.ruleNames)

def CodigoTresDirreciones(tree, rule_names, indent = 0):
    global send_file

    global offset
    global function_counter

    global end_line
    global line
    global line_split
    global line_split_function
    global line_split_return
    global line_split_accion

    global Puente_Tipo
    global identificadores
    global identificadores2
    global ArgFun1
    global ArgFun2
    global ArgFun3
    global last_type_3
    global last_type_return
    global last_type_accion
    global final_accion
    global wordArg3

    global posicion_memoria
    global direcciones_memoria
    global posibles_acciones

    global fin_global_status

    if tree.getText() == "<EOF>":
        return
    elif isinstance(tree, TerminalNode):
        ProbablyWord = "T='{1}'".format("  " * indent, tree.getText())
        word = tree.getText()
        # Evaluamos acciones como if o while
        if word in posibles_acciones:
            last_type_accion = "accionCall"
        if (word == "}") or (word == "else"):
            if len(final_accion) > 0:
                send_file.append(final_accion)
                final_accion = ""
        if word == "else":
            p = function_counter - 1
            final_accion = "\n\tgoto L%s\n\tL%s:" % (p, p)
            function_counter += 1

        # Terminamos globales
        if word in VarSymbolTable["VarId"]:
            global_index = VarSymbolTable["VarId"].index(word)
            if VarSymbolTable["Scope"][global_index] == "Program":
                fin_global_status = True
        
        # Evaluamos si el tipo de return (con funcion o sin)
        if word == "return":
            last_type_return = "returnCall"

        # Buscamos funciones
        if (word in ["=", "return"]) or (word in MethodSymbolTable["methodId"]):
            ArgFun1 = ArgFun2
            ArgFun2 = word
            if (ArgFun1 in ["=", "return"]) and (ArgFun2 in MethodSymbolTable["methodId"]):
                last_type_3 = "methodCall"
        
        if word in end_line:
            wordArg3 = ""
        else:
            if word != "=":
                wordArg3 += word
            else:
                for i in wordArg3:
                    if i in Variable_Memoria["id"]:
                        p = Variable_Memoria["id"].index(i)
                        wordArg3 = wordArg3.replace(i, Variable_Memoria["direccion"][p])
                ArgFun3 = wordArg3
                wordArg3 = ""
    
        '''if (word in VarSymbolTable["VarId"]) and (last_type_3 != "methodCall"):
            ArgFun3 = word'''

        # Evaluamos tipos         
        try:
            last_type_1 = trunk["type1"][-1]
            last_type_2 = trunk["type2"][-1]
        except:
            last_type_1 = ""
            last_type_2 = ""
        # Guardamos el contenido para una definicion
        if ((last_type_1 == 'declaration') and (last_type_2 == 'methodDeclaration')) or ((fin_global_status == True) and (last_type_1 == 'methodDeclaration') and (last_type_2 == 'declaration')):
            if word in end_line:
                trunk["type1"], trunk["type2"], trunk["content"], line_split, line = cleaner(trunk["type1"], trunk["type2"], trunk["content"], line_split, line)
                send_file, function_counter = DeclaracionMetodo(send_file, function_counter, line_split, MethodSymbolTable["methodId"])
                line_split = []
                offset = 0
            else:
                line_split.append(word)
        # Declaracion de una variable o declaracion en general 
        elif ((last_type_1 == 'statement') and (last_type_2 == 'location')) or ((fin_global_status == True) and (last_type_1 == 'location') and (last_type_2 == 'statement')):
            if word in end_line:
                trunk["type1"], trunk["type2"], trunk["content"], line_split, line = cleaner(trunk["type1"], trunk["type2"], trunk["content"], line_split, line)
                struct_declaration = False
                
                # buscamos si la variables es de tipo struct
                for i in line_split:
                    if i in StructSymbolTable["StructId"]:
                        struct_declaration = True

                if struct_declaration == True:
                    send_file, posicion_memoria, Variable_Memoria["id"], Variable_Memoria["direccion"] = Structs_Varibles(send_file, line_split, Variable_Memoria["id"], Variable_Memoria["direccion"], direcciones_memoria, posicion_memoria)
                else:
                    send_file, posicion_memoria, offset, Variable_Memoria["id"], Variable_Memoria["direccion"] = Variables(send_file, direcciones_memoria, posicion_memoria, line_split, VarSymbolTable["VarId"], offset, VarSymbolTable["offset"], Variable_Memoria["id"], Variable_Memoria["direccion"])
                line_split = []
                Puente_Tipo = False
                struct_declaration = False
            else:
                Puente_Tipo = "Cerrado"
                line_split.append(word)
        # Llamadas de metodo
        if last_type_3 == "methodCall":
            if word in end_line:
                forgiben_types = ["void", "int", "char"]
                trunk["type1"], trunk["type2"], trunk["content"], line_split_function, line = cleaner(trunk["type1"], trunk["type2"], trunk["content"], line_split_function, line)
                for i in forgiben_types:
                    if i in line_split_function:
                        line_split_function = []
                if len(line_split_function) > 0:
                    send_file, Variable_Memoria["id"], Variable_Memoria["direccion"], posicion_memoria = CallFuction(send_file, line_split_function, Variable_Memoria["id"], Variable_Memoria["direccion"], MethodSymbolTable["methodId"], direcciones_memoria, posicion_memoria, ArgFun1, ArgFun3)
                else:
                    pass
                line_split_function = []
                Puente_Tipo = False
                last_type_3 = ""
            else:
                Puente_Tipo = "Cerrado"
                line_split_function.append(word)
        # llamada para hacer un return
        if last_type_return == "returnCall":
            if word in end_line:
                send_file = Return(send_file, line_split_return, MethodSymbolTable["methodId"])
                line_split_return = []
                last_type_return = ""
            else:
                line_split_return.append(word)
        # llamada de una accion
        if last_type_accion == "accionCall":
            if word in end_line:
                send_file, direcciones_memoria, posicion_memoria, function_counter, final_accion, Variable_Memoria["id"], Variable_Memoria["direccion"], offset = Instruccion(send_file, line_split_accion, posibles_acciones, direcciones_memoria, posicion_memoria, Variable_Memoria["id"], Variable_Memoria["direccion"], function_counter, offset, VarSymbolTable["offset"], VarSymbolTable["VarId"])
                line_split_accion = []
                last_type_accion = ""
            else:
                line_split_accion.append(word)
        # print("{0}T='{1}'".format("  " * indent, tree.getText()))
    else:
        ProbablyWord = "R='{1}'".format("  " * indent, rule_names[tree.getRuleIndex()])

        if ProbablyWord in identificadores:
            if Puente_Tipo == False:
                trunk["type1"].append(rule_names[tree.getRuleIndex()])
                Puente_Tipo = True
            elif Puente_Tipo == True:
                trunk["type2"].append(rule_names[tree.getRuleIndex()])
                Puente_Tipo = False
        #print("{0}R='{1}'".format("  " * indent, rule_names[tree.getRuleIndex()]))
        if (tree.children != None):
            for child in tree.children:
                CodigoTresDirreciones(child, rule_names, indent + 1)

def Take_input():
	global send_file
	global posicion_memoria
	global function_counter
	global line_split
	global last_type_accion
	global last_type_3
	global line
	clean()
	clean2()
	archivo = FilenameInput.get("1.0", "end-1c")
	archivo2 = FilenameInput.get("1.0", "end-1c")
	if __name__ == '__main__':
		main(archivo)

        #Se imprime las tablas para revisarlas
		print("\n\n")
		print("Tabla de simbolos (variables)")
		print(VarSymbolTable)
		print("\n\n")
		print("Tabla de simbolos (metodos)")
		print(MethodSymbolTable)
		print("\n\n")
		print("Tabla de simbolos (struct)")
		print(StructSymbolTable)
		SecondMain(archivo2)
		print("\nComienzo codigo de 3 dirrecciones\n")
		ThirdMain(archivo2)
		send_file.append("\n\nEND")
		f = open("Codigo_3_direcciones.txt", "w")
		for i in send_file:
			f.write(i)

		print("\nComienzo traduccion a MIPS\n")

		print("FIN DEL RECORRIDO")
		send_file = []
		posicion_memoria = 0
		function_counter = 1
		line_split = []
		last_type_accion = ""
		last_type_3 = ""
		line = ""

def Take_input_v2():
	global send_file
	global send_final
	global posicion_memoria
	global function_counter
	global line_split
	global last_type_accion
	global last_type_3
	global line
	clean()
	clean2()
	archivo = Output.get("1.0", "end-1c")
	f = open("ArchivoGenerado.txt", "w")
	f.write("%s" % archivo)
	f.close()
	archivo = "ArchivoGenerado.txt"
	if __name__ == '__main__':
		main(archivo)

        #Se imprime las tablas para revisarlas
		print("\n\n")
		print("Tabla de simbolos (variables)")
		print(VarSymbolTable)
		print("\n\n")
		print("Tabla de simbolos (metodos)")
		print(MethodSymbolTable)
		print("\n\n")
		print("Tabla de simbolos (struct)")
		print(StructSymbolTable)
		SecondMain(archivo)
		print("\nComienzo codigo de 3 dirrecciones\n")
		ThirdMain(archivo)
		send_file.append("\n\nEND")
		f = open("Codigo_3_direcciones.txt", "w")
		for i in send_file:
			f.write(i)

		send_file = []
		posicion_memoria = 0
		function_counter = 1
		line_split = []
		last_type_accion = ""
		last_type_3 = ""
		line = ""

		print("FIN DEL RECORRIDO")

def Take_input_and_getreg():
    Take_input()
    getreg(Variable_Memoria["id"], Variable_Memoria["direccion"])

root = Tk()
root.geometry("800x500")
root.title(" Q&A ")
	
l = Label(text = "Escribe el nombre del archivo que quieres analizar o pega el texto aqui: ")

FilenameInput = Text(root, height = 2,
				width = 90,
				bg = "light yellow")
Output = Text(root, height = 20,
			width = 90,
			bg = "light cyan")
Display = Button(root, height = 2,
				width = 20,
				text ="Primera option",
				command = lambda:Take_input_and_getreg())
Display2 = Button(root, height = 2,
				width = 20,
				text ="Segunda option",
				command = lambda:Take_input_v2())

l.pack()
FilenameInput.pack()
Output.pack()
Display.pack()
Display2.pack()
mainloop()
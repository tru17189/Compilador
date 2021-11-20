from codecs import decode
from os import truncate
import sys
from tkinter import *
from typing import get_origin
from antlr4 import *
from antlr4.tree.Trees import  TerminalNode
from DecafLexer import DecafLexer
from DecafParser import DecafParser
from DecafListener import DecafListener

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
                    print("\n***El valor de retorno de un método debe de ser del mismo tipo con que fue declarado el método***")
                    print("***Valor que esta fallando es: %s****\n" %tree_2.getText())
                    input()
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

def Function(arg):
    send_file = []
    ans1 = "\n\n.globl %s" % arg
    send_file.append(ans1)
    ans = "\n%s: " % arg
    send_file.append(ans)
    return send_file

def Variables(declaration2, global_counter, posicion_memoria, direcciones_memoria, MemoryElements):
    n = ""
    if global_counter == 4:
        for i in declaration2:
            if i == ";":
                break
            elif i == "=":
                n = ""
            n += i
        n = n.replace("=", "")
        ans = "\n%s = %s" % (direcciones_memoria[posicion_memoria], n)
        for i in declaration2:
            if i == "=":
                break
            n = i
        MemoryElements["ValuesPerMemory"].append(n)
        posicion_memoria += 1
        return ans, posicion_memoria
    else:
        return "", posicion_memoria

def Commmon_Declaration(declaration, posicion_memoria, direcciones_memoria):
    begin = False
    sentence = ""
    send_file = []
    initial_component = ""

    for i in declaration:
        if i in MemoryElements["ValuesPerMemory"]:
            p = MemoryElements["ValuesPerMemory"].index(i)
            declaration = declaration.replace(i, direcciones_memoria[p])
    for i in declaration:
        if i == "=":
            break
        else:
            initial_component += i

    a = ""
    b = ""
    c = 0
    # procedencia de operadores -> ()
    for i in declaration:
        if i == ")":
            send_file.append("\n%s = %s" %(direcciones_memoria[posicion_memoria], sentence))
            a = "(%s)" % sentence
            declaration = declaration.replace(a, direcciones_memoria[posicion_memoria])
            posicion_memoria += 1
            begin = False
        if begin == True:
            sentence += i
        if i == "(":
            sentence = ""
            begin = True
    
    # procedencia de operadores -> *
    for i in declaration:
        if i == "*":
            if (declaration[c-2] == "t") or (declaration[c-2] == "s"):
                a = declaration[c-2]+declaration[c-1]
            else:
                a = declaration[c-1]
            if (declaration[c+1] == "t") or (declaration[c+1] == "s"):
                b = declaration[c+1]+declaration[c+2]
            else:
                b = declaration[c+1]
            sentence = "%s%s%s" % (a, i, b)

            send_file.append("\n%s = %s" % (direcciones_memoria[posicion_memoria], sentence))
            declaration = declaration.replace(sentence, direcciones_memoria[posicion_memoria])
            posicion_memoria += 1
        c += 1
    c = 0
    
    # procedencia de operadores -> /
    for i in declaration:
        if i == "/":
            if (declaration[c-2] == "t") or (declaration[c-2] == "s"):
                a = declaration[c-2]+declaration[c-1]
            else:
                a = declaration[c-1]
            if (declaration[c+1] == "t") or (declaration[c+1] == "s"):
                b = declaration[c+1]+declaration[c+2]
            else:
                b = declaration[c+1]
            sentence = "%s%s%s" % (a, i, b)

            send_file.append("\n%s = %s" % (direcciones_memoria[posicion_memoria], sentence))
            declaration = declaration.replace(sentence, direcciones_memoria[posicion_memoria])
            posicion_memoria += 1
        c += 1
    c = 0

    # procedencia de operadores -> +
    for i in declaration:
        if i == "+":
            if (declaration[c-2] == "t") or (declaration[c-2] == "s"):
                a = declaration[c-2]+declaration[c-1]
            else:
                a = declaration[c-1]
            if (declaration[c+1] == "t") or (declaration[c+1] == "s"):
                b = declaration[c+1]+declaration[c+2]
            else:
                b = declaration[c+1]
            sentence = "%s%s%s" % (a, i, b)

            send_file.append("\n%s = %s" % (direcciones_memoria[posicion_memoria], sentence))
            declaration = declaration.replace(sentence, direcciones_memoria[posicion_memoria])
            posicion_memoria += 1
        c += 1
    c = 0

    # procedencia de operadores -> -
    for i in declaration:
        if i == "-":
            if (declaration[c-2] == "t") or (declaration[c-2] == "s"):
                a = declaration[c-2]+declaration[c-1]
            else:
                a = declaration[c-1]
            if (declaration[c+1] == "t") or (declaration[c+1] == "s"):
                b = declaration[c+1]+declaration[c+2]
            else:
                b = declaration[c+1]
            sentence = "%s%s%s" % (a, i, b)
            
            send_file.append("\n%s = %s" % (direcciones_memoria[posicion_memoria], sentence))
            declaration = declaration.replace(sentence, direcciones_memoria[posicion_memoria])
            posicion_memoria += 1
        c += 1
    c = 0    

    # procedencia de operadores -> OR
    if "||" in declaration:
        declaration = declaration.replace("||", "@")
    for i in declaration:
        if i == "@":
            if (declaration[c-2] == "t") or (declaration[c-2] == "s"):
                a = declaration[c-2]+declaration[c-1]
            else:
                a = declaration[c-1]
            if (declaration[c+1] == "t") or (declaration[c+1] == "s"):
                b = declaration[c+1]+declaration[c+2]
            else:
                b = declaration[c+1]
            sentence = "%s%s%s" % (a, i, b)

            sentence = sentence.replace("@", "||")
            send_file.append("\n%s = %s" % (direcciones_memoria[posicion_memoria], sentence))
            declaration = declaration.replace(sentence, direcciones_memoria[posicion_memoria])
            posicion_memoria += 1
        c += 1
    c = 0    

    # procedencia de operadores -> AND
    if "&&" in declaration:
        declaration = declaration.replace("&&", "@")
    for i in declaration:
        if i == "@":
            if (declaration[c-2] == "t") or (declaration[c-2] == "s"):
                a = declaration[c-2]+declaration[c-1]
            else:
                a = declaration[c-1]
            if (declaration[c+1] == "t") or (declaration[c+1] == "s"):
                b = declaration[c+1]+declaration[c+2]
            else:
                b = declaration[c+1]
            sentence = "%s%s%s" % (a, i, b)

            sentence = sentence.replace("@", "&&")
            send_file.append("\n%s = %s" % (direcciones_memoria[posicion_memoria], sentence))
            declaration = declaration.replace(sentence, direcciones_memoria[posicion_memoria])
            posicion_memoria += 1
        c += 1
    c = 0    

    if initial_component == direcciones_memoria[posicion_memoria-1]:
        pass
    else:
        send_file.append("\n%s = %s" %(initial_component, direcciones_memoria[posicion_memoria-1]))

    return send_file, posicion_memoria, declaration

def Acciones(next_to_action, fuction_counter, posicion_memoria):
    send_file = []
    acciones = ["if", "while", "for", "else"]
    options = ["<", ">", "<=", ">=", "=="]
    direcciones_memoria = ["t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7", "s0", 
                        "s1", "s2", "s3", "s4", "s5", "s6", "s7", "t8", "t9"]
    arg1 = ""
    arg2 = ""
    arg3 = ""
    c = 0
    Into_Parentesis = False

    for i in next_to_action:
        if i in MemoryElements["ValuesPerMemory"]:
            p = MemoryElements["ValuesPerMemory"].index(i)
            next_to_action[c] = direcciones_memoria[p]
        c += 1
    
    ans = "\n\nL%s: " % fuction_counter
    fuction_counter += 1
    arg3 = "L%s" % fuction_counter
    send_file.append(ans)
    
    for i in next_to_action:
        if i == ")":
            Into_Parentesis = False
        if i in acciones:
            arg1 = i
        if Into_Parentesis == True:
            arg2 += i
        if i == "(":
            Into_Parentesis = True
        
    if "<" in arg2:
        arg2 = arg2.replace("<", " blt ")
    elif ">" in arg2:
        arg2 = arg2.replace(">", " bgt ")
    elif "<=" in arg2:
        arg2 = arg2.replace("<=", " ble ")
    elif ">=" in arg2:
        arg2 = arg2.replace(">=", " bge ")
    elif "==" in arg2:
        arg2 = arg2.replace("==", " beq ")
    
    arg4 = "\n%s = %s" % (direcciones_memoria[posicion_memoria], arg2)
    send_file.append(arg4)
    posicion_memoria += 1
    arg4 = arg4.replace("\n", "")

    ans = "\n%s %s goto %s" % (arg1, direcciones_memoria[posicion_memoria-1], arg3)
    m = fuction_counter - 1
    Next_Fuction = "\nL%s" % m
    send_file.append(ans)
    return fuction_counter, send_file, posicion_memoria, Next_Fuction
    

varDeclaration = False
SignDeclaration = False
methodDeclaration = False
methodType = False 

statement = False
location = False 
statement2 = False
location2 = False 
statement3 = False
ThereIsAccion = False

expression = False
literal = False

send_file = []
arg1 = ""
arg2 = ""
arg3 = ""
doing = ""
offset_counter = 0
posicion_memoria = 0
direcciones_memoria = ["t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7", "s0", 
                        "s1", "s2", "s3", "s4", "s5", "s6", "s7", "t8", "t9"]
MemoryElements = {
    "DM": ["t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7", "s0", "s1", "s2", 
            "s3", "s4", "s5", "s6", "s7", "t8", "t9"],
    "ValuesPerMemory": []
}

declaration = ""
declaration2 = ""
fuction_counter = 1
next_to_action = []
Next_Fuction = ""
global_counter = 0

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
    global arg1
    global arg2
    global arg3
    global doing 
    global varDeclaration
    global SignDeclaration
    global methodDeclaration
    global methodType
    global send_file
    global statement
    global location
    global statement2
    global location2
    global statement3
    global ThereIsAccion
    global expression 
    global literal

    global declaration
    global declaration2
    global posicion_memoria
    global fuction_counter
    global next_to_action
    global Next_Fuction
    global global_counter
    simbolos_ignorados = [";", "!", "," ".", "[", "]", "{", "}", "(", ")", "*", "-", ".", "+", "/", ","]
    acciones = ["if", "while", "for", "else"]
    if tree.getText() == "<EOF>":
        return
    elif isinstance(tree, TerminalNode):
        ProbablyWord = "T='{1}'".format("  " * indent, tree.getText())
        arg3 = arg2
        arg2 = arg1 
        arg1 = tree.getText()

        # Globales
        if location2 == True and statement2 == True:
            declaration2 += tree.getText()
            global_counter += 1
            if tree.getText() == ";":
                m, posicion_memoria = Variables(declaration2, global_counter, posicion_memoria, direcciones_memoria, MemoryElements)
                if len(m) > 0:
                    send_file.append(m)
                global_counter = 0
                declaration2 = ""
                location2 = False
                statement2 = False

        # Creacion de definicion
        if (methodDeclaration == True) and (SignDeclaration == True):
            if arg1 in MethodSymbolTable["methodId"]:
                n = Function(arg1)
                for i in n:
                    send_file.append(i)
                methodDeclaration = False
                SignDeclaration = False
        
        # Acciones
        if statement3 == True:
            if tree.getText() in acciones:
                ThereIsAccion = True
            elif tree.getText() == "{":
                ThereIsAccion = False
                statement3 = False
                fuction_counter, n, posicion_memoria, Next_Fuction = Acciones(next_to_action, fuction_counter, posicion_memoria)
                for i in n:
                    send_file.append(i)
                next_to_action = []
            if ThereIsAccion == True:
                next_to_action.append(tree.getText())
        
        if len(Next_Fuction) > 0:
            if tree.getText() == "}":
                send_file.append(Next_Fuction)
                Next_Fuction = ""
        
        if location == True and statement == True:
            if len(doing) <= 0:
                if tree.getText() == "{":
                    declaration = ""
                elif tree.getText() != ";":
                    declaration += tree.getText()
                else: 
                    n, posicion_memoria, ans = Commmon_Declaration(declaration, posicion_memoria, direcciones_memoria)
                    for i in n:
                        send_file.append(i)
                    declaration = ""
                    location = False
                    statement = False

        print("{0}T='{1}'".format("  " * indent, tree.getText()))
    else:
        ProbablyWord = "R='{1}'".format("  " * indent, rule_names[tree.getRuleIndex()])
        if ProbablyWord == "R='methodDeclaration'":
            methodDeclaration = True
        if ProbablyWord == "R='declaration'":
            SignDeclaration = True
        if ProbablyWord == "R='methodType'":
            methodType = True
        if ProbablyWord == "R='statement'":
            statement = True
            statement2 = True
            statement3 = True
        if ProbablyWord == "R='location'":
            location = True 
            location2 = True 
        if ProbablyWord == "R='expression'":
            expression = True
        if ProbablyWord == "R='literal'":
            literal = True
        if ProbablyWord == "R='varDeclaration'":
            varDeclaration = True

        print("{0}R='{1}'".format("  " * indent, rule_names[tree.getRuleIndex()]))
        if (tree.children != None):
            for child in tree.children:
                CodigoTresDirreciones(child, rule_names, indent + 1)

def Take_input():
	clean()
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
		input()
		print("\nComienzo codigo de 3 dirrecciones\n")
		ThirdMain(archivo2)
		f = open("Codigo_3_direcciones.txt", "w")
		send_file.append("\n\nL%s:" % fuction_counter)
		send_file.append("\nEND;")
		for i in send_file:
			f.write(i)
		print("FIN DEL RECORRIDO")

def Take_input_v2():
	archivo = Output.get("1.0", "end-1c")
	f = open("ArchivoGenerado.txt", "w")
	f.write("%s" % archivo)
	f.close()
	archivo = "ArchivoGenerado.txt"
	if __name__ == '__main__':
		main(archivo)

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
				command = lambda:Take_input())
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
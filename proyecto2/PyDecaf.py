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
        print("{0}T='{1}'".format("  " * indent, tree.getText()))

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
        print("{0}R='{1}'".format("  " * indent, rule_names[tree.getRuleIndex()]))
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
contador = 0
contador2 = 0
contador3 = 0

def SecondMain(argv_2):
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
                if RightWord in VarSymbolTable["VarId"]:
                    RightType = VarSymbolTable["VarType"][VarSymbolTable["VarId"].index(RightWord)]
                else:
                    RightWord = tree_2.getText()
                    if LeftWord in lista_numeros:
                        LeftType = "int"
                    elif LeftWord in lista_letras:
                        LeftType = "char"
                    elif LeftWord in lista_booleana:
                        LeftType = "boolean"
                    else:
                        LeftType = "NO TYPE"
                
                if LeftWord in VarSymbolTable["VarId"]:
                    LeftType = VarSymbolTable["VarType"][VarSymbolTable["VarId"].index(LeftWord)]
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

        if ProbablyWord == "T='['":
            IsThereRightKey = True
        if ProbablyWord == "T=']'":
            IsThereRightKey = False
        if ProbablyWord == "T='return'":
            IsThereReturn = True
        print("{0}T='{1}'".format("  " * indent, tree_2.getText()))
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
        print("{0}R='{1}'".format("  " * indent, rule_names[tree_2.getRuleIndex()]))
        if (tree_2.children != None):
            for child in tree_2.children:
                Second_Run(child, rule_names, indent + 1)    

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
		print("\nComienzo del segundo recorrido\n")
	input()
	SecondMain(archivo2)
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
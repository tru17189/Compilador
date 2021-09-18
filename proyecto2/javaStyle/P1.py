import sys
import os
from antlr4 import *
from antlr4.tree.Trees import  TerminalNode
from DecafLexer import DecafLexer
from DecafParser import DecafParser
from DecafListener import DecafListener

IsThereVoid = False
IsThereMain = False

IsThereDeclaration = False
IsThereVarDeclaration = False
IsThereVarType = False

IsThereExpressionOom = False
IsThereExpression = False
IsThereLocation = False
IntoReturn = False
NoMainReturn = []
NumArrayCero = []
numberOfParentesis = 0

MDeclaration = False
MMethodDeclaration = False
MMethodType = False

literal = False
NowVariable = ""

# Diccionario para la tabla de simbolos
varTypeFind = False
varTypeFind2 = False
varTypeFind3 = False
varTypeFind4 = False
contador = 0
scope = ""
MethodType = ""
VarSymbolTable = {
    "VarId": [],
    "VarType": [],
    "Scope": [],
    "offset": []
}

MethodfirstTime = False
MethodCall = False
Statement = False
location = False
MethodName = ""
MethodName2 = ""
IsThereReturn = False
AnswerReturn = []
MethodSymbolTable = {
    "methodId": [],
    "methodType": []
}

varEnterStruct = False
struct = ''
StructSymbolTable = {
    "VarId": [],
    "VarType": [],
    "StructId": []
}

#Pedimos el programa que se va analizar (interfaz basica)
archivo = input("Escribe el nombre del archivo que deseas analizar: ")
f = open(archivo, 'r')

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
    global NoMainReturn
    global NumArrayCero
    global IntoReturn
    global IsThereExpressionOom
    global IsThereExpression
    global IsThereLocation
    global IsThereDeclaration
    global IsThereVarDeclaration
    global IsThereVarType
    global numberOfParentesis

    global VarSymbolTable
    global MethodSymbolTable
    global varTypeFind 
    global varTypeFind2
    global varTypeFind3
    global varTypeFind4
    global contador
    global scope
    global methodType
    global literal
    global NowVariable

    global struct 
    global varEnterStruct 
    global MethodCall
    global Statement
    global location 
    global MethodName
    global MethodName2
    global IsThereReturn
    global AnswerReturn

    global MDeclaration
    global MMethodDeclaration
    global MMethodType
    global MethodfirstTime
    ignore_elements = ["(", ")", "{", "}", ";", "if", "while", "return", "."]

    if tree.getText() == "<EOF>":
        return
    elif isinstance(tree, TerminalNode):
        # vamos asegurarnos de que el programa tenga una  definición  de  un  método main sin  parámetros
        ProbablyWord = "T='{1}'".format("  " * indent, tree.getText())
        if ProbablyWord == "T='void'":
            global IsThereVoid
            IsThereVoid = True
        if ProbablyWord == "T='main'":
            global IsThereMain
            IsThereMain = True
        
        #Recolectamos datos para la tabla
        if varTypeFind3 == True:
            methodType = "%s" % tree.getText()
            if varTypeFind4 == True:
                #scope = "%s" % tree.getText()
                #VarSymbolTable["Scope"].append(scope)
                varTypeFind4 = False
            varTypeFind4 = True
        if (varTypeFind2 == True) and (varTypeFind == False):
            VarSymbolTable["VarId"].append(tree.getText())
            VarSymbolTable["Scope"].append(scope)
            varTypeFind2 = False
        if varTypeFind == True:
            if tree.getText() == 'int':
                VarSymbolTable["offset"].append(4)
            elif tree.getText() == 'boolean':
                VarSymbolTable["offset"].append(2)
            elif tree.getText() == 'char':
                VarSymbolTable["offset"].append(2)
            elif tree.getText() == 'float':
                VarSymbolTable["offset"].append(8)
            elif tree.getText() == 'struct':
                VarSymbolTable["offset"].append(8)
                varEnterStruct = True
            VarSymbolTable["VarType"].append(tree.getText())
            varTypeFind = False
            varTypeFind2 = True
        StructName = ""
        if varEnterStruct == True:
            contador += 1
            if contador == 2:
                StructName = tree.getText()
                contador = 0
            if tree.getText() != StructName:
                if tree.getText() != "struct":
                    struct = tree.getText()
                    StructSymbolTable["VarId"].append(VarSymbolTable["VarId"][-1])
                    scope = VarSymbolTable["VarId"][-1]
                    StructSymbolTable["VarType"].append(VarSymbolTable["VarType"][-1])
                    StructSymbolTable["StructId"].append(struct)
            if (tree.getText() == ";") or (tree.getText() == "[" ):
                varEnterStruct = False

        # Recolectamos para la tabla de metodos
        if (MDeclaration == True) and (MMethodDeclaration == True) and (MMethodType == True):
            scope = "%s" % tree.getText()
            if MethodfirstTime == False:
                MethodSymbolTable["methodType"].append(scope)
                MethodfirstTime = True
            elif MethodfirstTime == True:
                MethodSymbolTable["methodId"].append(scope)
                MDeclaration = False
                MMethodDeclaration = False
                MMethodType = False
                MethodfirstTime = False

        # Vamos a condicionar para que los metodos void main no tengan un return, primero encontraos el return
        if (IsThereVoid == True):
            if ProbablyWord == "T='{'":
                numberOfParentesis += 1
            if (ProbablyWord == "T='return'") and (numberOfParentesis == 1):
                NoMainReturn.append(1)
                IntoReturn = True
            if ProbablyWord == "T='}'":
                numberOfParentesis -= 1
        
        # Vamos a verficar si el array tiene num 0
        if (IsThereVarDeclaration == True) and (IsThereVarDeclaration == True) and (IsThereVarType == True):
            arrayNumber = "%s" % tree.getText()
            try: 
                if ProbablyWord == "T='['":
                    NumArrayCero.append(1)
                elif ProbablyWord == "T=']'":
                    NumArrayCero.append(1)
                elif tree.getText() == '0':
                    NumArrayCero.append(1)
                    NumArrayCero.append(1)
                    NumArrayCero.append(1)
                elif tree.getText() == ";":
                    NumArrayCero = []
                    IsThereDeclaration = False
                    IsThereVarDeclaration = False
                    IsThereVarType = False
                if len(NumArrayCero) == 5:
                    print(NumArrayCero)
                    print("\n\t****el numero en la declaracion no es mayor a 0****\n")
                    input()
                    NumArrayCero = []
                    IsThereDeclaration = False
                    IsThereVarDeclaration = False
                    IsThereVarType = False
            except:
                pass
        
        # Verificamos que cuando se llame un metodo los argumentos sean los mismos que los formales
        if (Statement == True) and (MethodCall == True):
            u = 0
            t = 0
            if tree.getText() == ")":
                for i in MethodSymbolTable["methodId"]:
                    if i == MethodSymbolTable["methodId"][u]:
                        MethodName2 = MethodSymbolTable["methodType"][u]
                    u += 1
                for i in MethodName:
                    if (i == "+") or (i == "-") or (i == "*") or (i == "/") or (i in ignore_elements):
                        pass
                    elif i in VarSymbolTable["VarId"]:
                        for e in VarSymbolTable["VarId"]:
                            if i == e:
                                try:
                                    if (MethodName2 == VarSymbolTable["VarType"][t]) or (MethodName2 == "void"):
                                        pass
                                    else:
                                        print("\n\t***El tipo del argumento formal no es el mismo que el de la llamada***")
                                        print("\tEL valor del problema es: "+VarSymbolTable["VarId"][t]+"\n")
                                        input()
                                except:
                                    pass
                            t += 1
                    else:
                        if MethodName2 == "int":
                            try:
                                int(i)
                            except:
                                print("\n\t***El tipo del argumento formal no es el mismo que el de la llamada***")
                                print("\tEL valor del problema es: "+i+"\n")
                                input()
                                MethodName2 = ""
                        elif MethodName2 == "boolean":
                            try:
                                bool(i)
                            except:
                                print("\n\t***El tipo del argumento formal no es el mismo que el de la llamada***")
                                print("\tEL valor del problema es: "+i+"\n")
                                input()
                                MethodName2 = ""
                        elif MethodName2 == "char":
                            try:
                                chr(i)
                            except:
                                print("\n\t***El tipo del argumento formal no es el mismo que el de la llamada***")
                                print("\tEL valor del problema es: "+i+"\n")
                                input()
                                MethodName2 = ""
                        elif MethodName2 == "string":
                            try:
                                str(i)
                            except:
                                print("\n\t***El tipo del argumento formal no es el mismo que el de la llamada***")
                                print("\tEL valor del problema es: "+i+"\n")
                                input()
                                MethodName2 = ""
                Statement = False
                MethodCall = False
            elif tree.getText() in MethodSymbolTable["methodId"]:
                MethodName2 = tree.getText()
            elif tree.getText() in ignore_elements:
                pass
            else:
                MethodName = MethodName + "%s" % tree.getText()
        
        # El valor de retorno de un método debe de ser del mismo tipo con que fue declarado el método.
        if ProbablyWord == "T='return'":
            IsThereReturn = True
        if IsThereReturn == True:
            u = 0
            if (tree.getText() == "return") or (tree.getText() == ")") or (tree.getText() == "(") or (tree.getText() == "+") or (tree.getText() == "-") or (tree.getText() == "*") or (tree.getText() == "/"):
                pass
            elif tree.getText() == ";":
                for i in AnswerReturn:
                    if i in MethodSymbolTable["methodId"]:
                        position = MethodSymbolTable["methodId"].index(str(i))
                        TYPE = MethodSymbolTable["methodType"][position]
                        if TYPE == MethodSymbolTable["methodType"][MethodSymbolTable["methodId"].index(scope)]:
                            pass
                        else:
                            print("***Valor de retorno del metodo no es el mismo tipo del metodo declarado***")
                            input()
                    elif i in VarSymbolTable["VarId"]:
                        position = VarSymbolTable["VarId"].index(str(i))
                        TYPE = VarSymbolTable["VarType"][position]
                        if TYPE == MethodSymbolTable["methodType"][MethodSymbolTable["methodId"].index(scope)]:
                            pass
                        else:
                            print("***Valor de retorno del metodo no es el mismo tipo del metodo declarado***")
                            input()
                    else:
                        TYPE = MethodSymbolTable["methodType"][MethodSymbolTable["methodId"].index(scope)]
                        if (i in ignore_elements) or (i in StructSymbolTable["StructId"]):
                            TYPE = ""
                        if TYPE == "int":
                            try:
                                int(i)
                            except:
                                print("***Valor de retorno del metodo no es el mismo tipo del metodo declarado***")
                                input()
                        elif TYPE == "boolean":
                            try:
                                bool(i)
                            except:
                                print("***Valor de retorno del metodo no es el mismo tipo del metodo declarado***")
                                input()
                        elif TYPE == "char":
                            try:
                                chr(i)
                            except:
                                print("***Valor de retorno del metodo no es el mismo tipo del metodo declarado***")
                                input()
                        elif TYPE == "string":
                            try:
                                str(i)
                            except:
                                print("***Valor de retorno del metodo no es el mismo tipo del metodo declarado***")
                                input()
                    u += 1
                AnswerReturn = []
                IsThereReturn = False
            else:
                AnswerReturn.append(tree.getText())

        # Ningún identificador es utilizado antes de ser declarado.
        if (Statement == True) and (location == True) and (MethodCall != True):
            if (tree.getText() in ignore_elements) or (tree.getText() in MethodSymbolTable["methodId"]):
                pass
            else:
                if (tree.getText() in VarSymbolTable["VarId"]) or (tree.getText() in StructSymbolTable["StructId"]) or (tree.getText() in VarSymbolTable["VarType"]):
                    pass
                elif tree.getText() in ignore_elements:
                    pass
                else:
                    print("\n\t***EL indentificador no ha sido aun declarado***")
                    print("\tEL valor del problema es: "+tree.getText()+"\n")
                    input()
                Statement = False
                location = False

        
        # Revisamos que el tipo del valor del RETURN sea el mismo que de la funcion a la que pertenece
        print("{0}T='{1}'".format("  " * indent, tree.getText()))
    else:
        # El valor del lado derecho de la asignación no es el mismo del izquierdo
        if literal == True:
            option1= ""
            NowType = rule_names[tree.getRuleIndex()]
            if NowVariable in VarSymbolTable["VarId"]:
                option1 = VarSymbolTable["VarType"][VarSymbolTable["VarId"].index(NowVariable)]
            if NowType == "int_literal":
                NowType = "int"
            elif NowType == "bool_literal":
                NowType = "boolean"
            elif NowType == "char_literal":
                NowType = "char"
            if option1 == NowType:
                pass
            else:
                print("\n\t***El valor del lado derecho de la asignación no es el mismo del izquierdo***")
                print("\tEL valor del problema es: "+NowVariable+"\n")
                input()
            literal = False

        ProbablyWord = "R='{1}'".format("  " * indent, rule_names[tree.getRuleIndex()])
        # Vamos a revisar si se cumple las condiciones para un array 
        if ProbablyWord == "R='declaration'":
            IsThereDeclaration = True
            MDeclaration = True
        if ProbablyWord == "R='varDeclaration'":
            IsThereVarDeclaration = True
        if ProbablyWord == "R='varType'":
            IsThereVarType = True
            varTypeFind = True
        if ProbablyWord == "R='methodDeclaration'":
            IsThereDeclaration = False
            IsThereVarDeclaration = False
            IsThereVarType = False
            MMethodDeclaration = True
        if ProbablyWord == "R='methodType'":
            varTypeFind3 = True
            MMethodType = True
        if ProbablyWord == "R='program'":
            varTypeFind3 = True
        if ProbablyWord == "R='statement'":
            Statement = True
        if ProbablyWord == "R='methodCall'":
            MethodCall = True
        if ProbablyWord == "R='parameterType'":
            varTypeFind = True
        if ProbablyWord == "R='program'":
            scope = "program"
        if ProbablyWord == "R='location'":
            location = True
        if ProbablyWord == "R='literal'":
            literal = True
        
        if location == True:
            NowVariable =""
            for i in tree.getText():
                if i in VarSymbolTable["VarId"]:
                    NowVariable += i
            location = False

        # Vamos a revisar si el return en el metodo void regresa un valor
        if IntoReturn == True:
            if ProbablyWord == "R='expressionOom'":
                IsThereExpressionOom = True
                NoMainReturn.append(1)
            if ProbablyWord == "R='expression'":
                IsThereExpression = True
                NoMainReturn.append(1)
            if ProbablyWord == "R='location'":
                IsThereLocation = True
                NoMainReturn.append(1)
            
            if (IsThereExpressionOom == True) and (IsThereExpression == True) and (IsThereLocation == True):
                back = tree.getText()
                if back in VarSymbolTable["VarId"]:
                    method = VarSymbolTable["Scope"][VarSymbolTable["VarId"].index(back)]
                else:
                    method = ""
                # NoMainReturn se puede borrar
                if (len(NoMainReturn) == 4) and (method == "void"):
                    print("\n\t****el metodo void devuelve un return con un valor****\n")
                    input()
                    NoMainReturn = []
                IsThereExpressionOom = False
                IsThereExpression = False
                IsThereLocation = False
    
        print("{0}R='{1}'".format("  " * indent, rule_names[tree.getRuleIndex()]))
        if (tree.children != None):
            for child in tree.children:
                traverse(child, rule_names, indent + 1)

if __name__ == '__main__':
    main(archivo)
    # Aqui avisamos si no se cumplio con la condicion del void main 
    if (IsThereVoid == False) or (IsThereMain == False):
        print("\n\t****No se encuentra declaro un metodo main sin parametors****\n")
        input()
    
    # Ningún identificador es declarado dos veces en el mismo ámbito
    apariciones = 0
    posiciones = []
    for i in VarSymbolTable["VarId"]:
        if VarSymbolTable["VarId"].count(i) >= 2:
            for u in VarSymbolTable["VarId"]:
                if u == i:
                    posiciones.append(apariciones)
                apariciones += 1 
            option1 = VarSymbolTable["Scope"][posiciones[0]]
            option2 = VarSymbolTable["Scope"][posiciones[1]]
            if option1 == option2:
                print("\n\t****Identificador declarado dos veces****")
                print("Variable que se repite de mal manera: "+i+"\n")
                input()
            else:
                pass
            apariciones = 0
            posiciones = []     

print("\n\n")
print("Tabla de simbolos (variables)")
print(VarSymbolTable)
print("\n\n")
print("Tabla de simbolos (metodos)")
print(MethodSymbolTable)
print("\n\n")
print("Tabla de simbolos (struct)")
print(StructSymbolTable)
while True:
    os.system("python3 P1.py")
    print("cerrando...")
    exit()
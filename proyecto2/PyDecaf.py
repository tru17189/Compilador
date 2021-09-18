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

def main2(argv):
    input_stream = FileStream(argv)
    lexer = DecafLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = DecafParser(stream)
    tree = parser.program()  

    printer = KeyPrinter()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)
    traverse_2(tree, parser.ruleNames)

def traverse_2(tree, rule_names, indent = 0):
    if tree.getText() == "<EOF>":
        return
    elif isinstance(tree, TerminalNode):
        print("{0}T='{1}'".format("  " * indent, tree.getText()))
        pass
    else:
        print("{0}R='{1}'".format("  " * indent, rule_names[tree.getRuleIndex()]))
        if (tree.children != None):
            for child in tree.children:
                traverse(child, rule_names, indent + 1)

def Take_input():
	archivo = FilenameInput.get("1.0", "end-1c")
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
		main2(archivo)

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
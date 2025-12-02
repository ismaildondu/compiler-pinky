import sys
from lexer import Lexer
from tokens import Token
from parser import Parser
from interpreter import Interpreter
from model import *
from utils import *

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python pinky.py <filename>")
        sys.exit(1)
    filename = sys.argv[1]
    print(filename)
    with open(filename, 'r') as file:
        content = file.read()
        print("LEXER: ")
        tokens = Lexer(content).tokenize()
        for token in tokens:
            print(token)
    print("PARSED AST: ")
    ast = Parser(tokens).parse()
    pretty_ast(ast)

    print("INTERPRETER: ")
    interpreter = Interpreter()
    interpreter.interpret(ast)
    
    
    

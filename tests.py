import unittest

from tokens import *
from lexer import *
from parser import *
from model import *
from interpreter import *

class Tests(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
    
    def test_float(self):
        source = '7.72'
        lexer = Lexer(source).tokenize()
        ast = Parser(lexer).parse()
        interpreter = Interpreter()
        result = interpreter.interpret(ast)
        self.assertEqual(result, (TYPE_NUMBER, 7.72))
    
    def test_integer(self):
        source = '42'
        lexer = Lexer(source).tokenize()
        ast = Parser(lexer).parse()
        interpreter = Interpreter()
        result = interpreter.interpret(ast)
        self.assertEqual(result, (TYPE_NUMBER, 42.0))

    def test_boolean_true(self):
        source = 'true != false'
        lexer = Lexer(source).tokenize()
        ast = Parser(lexer).parse()
        interpreter = Interpreter()
        result = interpreter.interpret(ast)
        self.assertEqual(result, (TYPE_BOOLEAN, True))
    
    def test_basic_addition(self):
        source = '5 + 3'
        lexer = Lexer(source).tokenize()
        ast = Parser(lexer).parse()
        interpreter = Interpreter()
        result = interpreter.interpret(ast)
        self.assertEqual(result, (TYPE_NUMBER, 8.0))

    def test_string_concatenation(self):
        source = '"Hello, " + "World!"'
        lexer = Lexer(source).tokenize()
        ast = Parser(lexer).parse()
        interpreter = Interpreter()
        result = interpreter.interpret(ast)
        self.assertEqual(result, (TYPE_STRING, "Hello, World!"))

    def test_complex_expression(self):
        source = '(2 + 3) * 4.5 - 1'
        lexer = Lexer(source).tokenize()
        ast = Parser(lexer).parse()
        interpreter = Interpreter()
        result = interpreter.interpret(ast)
        self.assertEqual(result, (TYPE_NUMBER, 21.5))

    def test_complex_boolean_expression(self):
        source = 'true == false or false == false and true'
        lexer = Lexer(source).tokenize()
        ast = Parser(lexer).parse()
        interpreter = Interpreter()
        result = interpreter.interpret(ast)
        self.assertEqual(result, (TYPE_BOOLEAN, True))
    
    def test_power_operation(self):
        source = '2 ^ 3 ^ 2'
        lexer = Lexer(source).tokenize()
        ast = Parser(lexer).parse()
        interpreter = Interpreter()
        result = interpreter.interpret(ast)
        self.assertEqual(result, (TYPE_NUMBER, 512.0))
        
    def test_division_by_zero(self):
        source = '10 / 0'
        lexer = Lexer(source).tokenize()
        ast = Parser(lexer).parse()
        interpreter = Interpreter()
        with self.assertRaises(SystemExit) as cm:
            interpreter.interpret(ast)
        self.assertEqual(cm.exception.code, 1)


if __name__ == '__main__':
    unittest.main()

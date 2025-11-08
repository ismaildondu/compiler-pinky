from model import *
from tokens import *
from utils import *
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.curr = 0

    def advance(self):
        token = self.tokens[self.curr]
        self.curr += 1
        return token 

    def peek(self):
        if self.curr >= len(self.tokens):
            return Token('EOF', '', -1)
        return self.tokens[self.curr]

    def is_next(self, type):
        if self.curr >= len(self.tokens):
            return False
        return self.peek().token_type == type

    def expect(self, type):
        if not self.match(type):
            if self.curr >= len(self.tokens):
                parser_error(f"Expected token of type {type} but reached end of input.", self.previous().line)
            else:
                parser_error(f"Expected token of type {type} but {self.tokens[self.curr].token_type} found.", self.peek().line)
        

    def match(self, type):
        if self.peek().token_type == type:
            self.advance()
            return True
        return False

    def previous(self):
        return self.tokens[self.curr - 1]
    
    def primary(self):
        if self.match(TOK_INTEGER):
            return IntegerModel(int(self.previous().lexeme), self.previous().line)
        if self.match(TOK_FLOAT):
            return FloatModel(float(self.previous().lexeme), self.previous().line)
        if self.match(TOK_LPAREN):
            expr = self.expression()
            self.expect(TOK_RPAREN)
            return GroupingModel(expr, self.previous().line)
        parser_error(f"Unexpected token: {self.peek().lexeme}", self.peek().line)

    def unary(self):
        if self.match(TOK_MINUS) or self.match(TOK_PLUS) or self.match(TOK_NOT):
            operator = self.previous()
            operand = self.unary()
            return UnaryOperationModel(operator, operand, operator.line)
        return self.primary()
    
    def multiplication(self):
        expr = self.unary()
        while self.match(TOK_STAR) or self.match(TOK_SLASH):
            operator = self.previous()
            right = self.unary()
            expr = BinaryOperationModel(operator, expr, right, operator.line)
        return expr

    def addition(self):
        expr = self.multiplication()
        while self.match(TOK_PLUS) or self.match(TOK_MINUS):
            operator = self.previous()
            right = self.multiplication()
            expr = BinaryOperationModel(operator, expr, right, operator.line)
        return expr

    def expression(self):
        return self.addition()

    def parse(self):
        ast = self.expression()
        if self.curr < len(self.tokens):
            parser_error(f"Unexpected token at end: {self.peek().lexeme}", self.peek().line)
        return ast



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
        if self.match(TOK_TRUE):
            return BooleanModel(True, self.previous().line)
        if self.match(TOK_FALSE):
            return BooleanModel(False, self.previous().line)
        if self.match(TOK_STRING):
            return StringModel(str(self.previous().lexeme[1:-1]), self.previous().line)
        if self.match(TOK_LPAREN):
            expr = self.expression()
            self.expect(TOK_RPAREN)
            return GroupingModel(expr, self.previous().line)
        parser_error(f"Unexpected token: {self.peek().lexeme}", self.peek().line)
    
    def exponentiation(self):
        expr = self.primary()
        if self.match(TOK_CARET):
            operator = self.previous()
            right = self.exponentiation()
            expr = BinaryOperationModel(operator, expr, right, operator.line)
        return expr

    def unary(self):
        if self.match(TOK_MINUS) or self.match(TOK_PLUS) or self.match(TOK_NOT):
            operator = self.previous()
            operand = self.unary()
            return UnaryOperationModel(operator, operand, operator.line)
        return self.exponentiation()
    
    def modulo(self):
        expr = self.unary()
        while self.match(TOK_MOD):
            operator = self.previous()
            right = self.unary()
            expr = BinaryOperationModel(operator, expr, right, operator.line)
        return expr

    def multiplication(self):
        expr = self.modulo()
        while self.match(TOK_STAR) or self.match(TOK_SLASH):
            operator = self.previous()
            right = self.modulo()
            expr = BinaryOperationModel(operator, expr, right, operator.line)
        return expr

    def addition(self):
        expr = self.multiplication()
        while self.match(TOK_PLUS) or self.match(TOK_MINUS):
            operator = self.previous()
            right = self.multiplication()
            expr = BinaryOperationModel(operator, expr, right, operator.line)
        return expr

    def comparison(self):
        expr = self.addition()
        while self.match(TOK_GT) or self.match(TOK_GE) or self.match(TOK_LT) or self.match(TOK_LE):
            operator = self.previous()
            right = self.addition()
            expr = BinaryOperationModel(operator, expr, right, operator.line)
        return expr

    def equality(self):
        expr = self.comparison()
        while self.match(TOK_EQ) or self.match(TOK_NE):
            operator = self.previous()
            right = self.comparison()
            expr = BinaryOperationModel(operator, expr, right, operator.line)
        return expr

    def and_expression(self):
        expr = self.equality()
        while self.match(TOK_AND):
            operator = self.previous()
            right = self.equality()
            expr = LogicalOperationModel(operator, expr, right, operator.line)
        return expr

    def or_expression(self):
        expr = self.and_expression()
        while self.match(TOK_OR):
            operator = self.previous()
            right = self.and_expression()
            expr = LogicalOperationModel(operator, expr, right, operator.line)
        return expr

    def expression(self):
        return self.or_expression()

    def print_stmt(self):
        if self.match(TOK_PRINT):
            val = self.expression()
            return PrintStatementModel(val, self.previous().line)
            
    def println_stmt(self):
        if self.match(TOK_PRINTLN):
            val = self.expression()
            return PrintlnStatementModel(val, self.previous().line)

    def stmt(self):
        if self.peek().token_type == TOK_PRINT:
            return self.print_stmt()
        elif self.peek().token_type == TOK_PRINTLN:
            return self.println_stmt()

    def stmts(self):
        stmts = []
        while(self.curr < len(self.tokens)):
            stmt = self.stmt()
            stmts.append(stmt)
        return Statements(stmts, self.previous().line)

    def program(self):
        stmts = self.stmts()
        return stmts

    def parse(self):
        ast = self.program()
        if self.curr < len(self.tokens):
            parser_error(f"Unexpected token at end: {self.peek().lexeme}", self.peek().line)
        return ast



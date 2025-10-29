from model import *
from token import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.curr = 0
    
    def primary(self):
        pass

    def unary(self):
        pass

    def factor(self):
        pass
    
    def term(self):
        pass

    def expression(self):
        pass

    def parse(self):
        ast = self.expression()
        return ast


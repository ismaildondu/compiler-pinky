from model import *
from tokens import *

class Interpreter:
    def __init__(self):
        pass
    
    def interpret(self, astNode):
        if isinstance(astNode, IntegerModel):
            return float(astNode.value)
        if isinstance(astNode, FloatModel):
            return float(astNode.value)
        if isinstance(astNode, GroupingModel):
            return self.interpret(astNode.expression)
        if isinstance(astNode, BinaryOperationModel):
            right = self.interpret(astNode.right)
            left = self.interpret(astNode.left)
            if astNode.operator.token_type == TOK_PLUS:
                return left + right
            elif astNode.operator.token_type == TOK_MINUS:
                return left - right
            elif astNode.operator.token_type == TOK_STAR:
                return left * right
            elif astNode.operator.token_type == TOK_SLASH:
                return left / right
        if isinstance(astNode, UnaryOperationModel):
            operand = self.interpret(astNode.operand)
            if astNode.operator.token_type == TOK_MINUS:
                return -operand
            elif astNode.operator.token_type == TOK_PLUS:
                return +operand
            #elif astNode.operator.token_type == TOK_NOT:
            #    TODO: implement not operation
                

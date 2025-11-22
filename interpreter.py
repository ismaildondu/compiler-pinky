from model import *
from tokens import *
from utils import *

TYPE_NUMBER = 'TYPE_NUMBER' # 64 bit float acording to pinky design doc
TYPE_STRING = 'TYPE_STRING' # string that is managed by python
TYPE_BOOLEAN = 'TYPE_BOOLEAN' # true | false 

class Interpreter:
    def __init__(self):
        pass
    
    def interpret(self, astNode):
        if isinstance(astNode, IntegerModel):
            return (TYPE_NUMBER, float(astNode.value))
        if isinstance(astNode, FloatModel):
            return (TYPE_NUMBER, float(astNode.value))
        if isinstance(astNode, GroupingModel):
            return self.interpret(astNode.expression)
        if isinstance(astNode, BinaryOperationModel):
            rightType, rightVal = self.interpret(astNode.right)
            leftType, leftVal = self.interpret(astNode.left)
            if astNode.operator.token_type == TOK_PLUS:
                if rightType == TYPE_NUMBER and leftType == TYPE_NUMBER:
                    return (TYPE_NUMBER, leftVal + rightVal)
                elif rightType == TYPE_STRING or leftType == TYPE_STRING:
                    return (TYPE_STRING, (str(leftVal) + str(rightVal)))
                else:
                    runtime_error(f"Unsupported operand types for +: '{leftType}' and '{rightType}'", astNode.line)
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
                

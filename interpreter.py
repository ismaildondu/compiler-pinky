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
        if isinstance(astNode, StringModel):
            return (TYPE_STRING, str(astNode.value))
        if isinstance(astNode, BooleanModel):
            return (TYPE_BOOLEAN, bool(astNode.value))
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
                if rightType == TYPE_NUMBER and leftType == TYPE_NUMBER:
                    return (TYPE_NUMBER, leftVal - rightVal)
                else:
                    runtime_error(f"Unsupported operand types for -: '{leftType}' and '{rightType}'", astNode.line)
            elif astNode.operator.token_type == TOK_STAR:
                if rightType == TYPE_NUMBER and leftType == TYPE_NUMBER:
                    return (TYPE_NUMBER, leftVal * rightVal)
                else:
                    runtime_error(f"Unsupported operand types for *: '{leftType}' and '{rightType}'", astNode.line)
            elif astNode.operator.token_type == TOK_MOD:
                if rightType == TYPE_NUMBER and leftType == TYPE_NUMBER:
                    if rightVal == 0:
                        runtime_error("Modulo by zero", astNode.line)
                    return (TYPE_NUMBER, leftVal % rightVal)
                else:
                    runtime_error(f"Unsupported operand types for %: '{leftType}' and '{rightType}'", astNode.line)
            elif astNode.operator.token_type == TOK_CARET:
                if rightType == TYPE_NUMBER and leftType == TYPE_NUMBER:
                    return (TYPE_NUMBER, leftVal ** rightVal)
                else:
                    runtime_error(f"Unsupported operand types for ^: '{leftType}' and '{rightType}'", astNode.line)
            elif astNode.operator.token_type == TOK_SLASH:
                if rightType == TYPE_NUMBER and leftType == TYPE_NUMBER:
                    if rightVal == 0:
                        runtime_error("Division by zero", astNode.line)
                    return (TYPE_NUMBER, leftVal / rightVal)
                else:
                    runtime_error(f"Unsupported operand types for /: '{leftType}' and '{rightType}'", astNode.line)
            else:
                runtime_error(f"Unsupported binary operator: {astNode.operator.lexeme!r}", astNode.line)
        if isinstance(astNode, UnaryOperationModel):
            operandType, operandVal = self.interpret(astNode.operand)
            if astNode.operator.token_type == TOK_MINUS and operandType == TYPE_NUMBER:
                return (TYPE_NUMBER, float(-operandVal))
            elif astNode.operator.token_type == TOK_PLUS and operandType == TYPE_NUMBER:
                return (TYPE_NUMBER, float(+operandVal))
            elif astNode.operator.token_type == TOK_NOT and operandType == TYPE_BOOLEAN:
                return (TYPE_BOOLEAN, bool(not operandVal))
            else:
                runtime_error(f"Unsupported operand type for {astNode.operator.lexeme!r}: '{operandType}'", astNode.line)
            
                

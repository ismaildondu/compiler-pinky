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
                    # TODO: consider IEEE 754 behavior
                    if rightVal == 0:
                        runtime_error("Division by zero", astNode.line)
                    return (TYPE_NUMBER, leftVal / rightVal)
                else:
                    runtime_error(f"Unsupported operand types for /: '{leftType}' and '{rightType}'", astNode.line)
            elif astNode.operator.token_type == TOK_GT:
                if (rightType == TYPE_NUMBER and leftType == TYPE_NUMBER) or (rightType == TYPE_STRING and leftType == TYPE_STRING):
                    return (TYPE_BOOLEAN, leftVal > rightVal)
                else:
                    runtime_error(f"Unsupported operand types for >: '{leftType}' and '{rightType}'", astNode.line)
            elif astNode.operator.token_type == TOK_LT:
                if (rightType == TYPE_NUMBER and leftType == TYPE_NUMBER) or (rightType == TYPE_STRING and leftType == TYPE_STRING):
                    return (TYPE_BOOLEAN, leftVal < rightVal)
                else:
                    runtime_error(f"Unsupported operand types for <: '{leftType}' and '{rightType}'", astNode.line)
            elif astNode.operator.token_type == TOK_GE:
                if (rightType == TYPE_NUMBER and leftType == TYPE_NUMBER) or (rightType == TYPE_STRING and leftType == TYPE_STRING):
                    return (TYPE_BOOLEAN, leftVal >= rightVal)
                else:
                    runtime_error(f"Unsupported operand types for >=: '{leftType}' and '{rightType}'", astNode.line)
            elif astNode.operator.token_type == TOK_LE:
                if (rightType == TYPE_NUMBER and leftType == TYPE_NUMBER) or (rightType == TYPE_STRING and leftType == TYPE_STRING):
                    return (TYPE_BOOLEAN, leftVal <= rightVal)
                else:
                    runtime_error(f"Unsupported operand types for <=: '{leftType}' and '{rightType}'", astNode.line)
            elif astNode.operator.token_type == TOK_EQ:
                if rightType != leftType:
                    return (TYPE_BOOLEAN, False)
                return (TYPE_BOOLEAN, leftVal == rightVal)
            elif astNode.operator.token_type == TOK_NE:
                if rightType != leftType:
                    return (TYPE_BOOLEAN, True)
                return (TYPE_BOOLEAN, leftVal != rightVal)
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
        if isinstance(astNode, LogicalOperationModel):
            leftType, leftVal = self.interpret(astNode.left)
            rightType, rightVal = self.interpret(astNode.right)
            if astNode.operator.token_type == TOK_AND:
                if leftType == TYPE_BOOLEAN and leftVal == False:
                    return (TYPE_BOOLEAN, False)
                if leftType == TYPE_BOOLEAN and rightType == TYPE_BOOLEAN:
                    return (TYPE_BOOLEAN, leftVal and rightVal)
                else:
                    runtime_error(f"Unsupported operand types for and: '{leftType}' and '{rightType}'", astNode.line)
            elif astNode.operator.token_type == TOK_OR:
                if leftType == TYPE_BOOLEAN and leftVal == True:
                    return (TYPE_BOOLEAN, True)
                if leftType == TYPE_BOOLEAN and rightType == TYPE_BOOLEAN:
                    return (TYPE_BOOLEAN, leftVal or rightVal)
                else:
                    runtime_error(f"Unsupported operand types for or: '{leftType}' and '{rightType}'", astNode.line)
            else:
                runtime_error(f"Unsupported logical operator: {astNode.operator.lexeme!r}", astNode.line)
        if isinstance(astNode, Statements):
            for stmt in astNode.stmts:
                self.interpret(stmt)
        if isinstance(astNode, PrintStatementModel):
            _Type, _Val = self.interpret(astNode.value)
            print(_Val)
                
            
            
                

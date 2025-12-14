from model import *
from tokens import *
from utils import *
from state import *

TYPE_NUMBER = 'TYPE_NUMBER' # 64 bit float acording to pinky design doc
TYPE_STRING = 'TYPE_STRING' # string that is managed by python
TYPE_BOOLEAN = 'TYPE_BOOLEAN' # true | false 

class Interpreter:
    def __init__(self):
        pass
    
    def interpret(self, astNode, env):
        if isinstance(astNode, IdentifierModel):
            value = env.get_variable(astNode.name)
            if value is None:
                runtime_error(f"Undefined variable '{astNode.name}'", astNode.line)
            if value[0] is None:
                runtime_error(f"Uninitialized variable '{astNode.name}'", astNode.line)
            return value
        if isinstance(astNode, AssignmentModel):
            rightType, rightVal = self.interpret(astNode.right, env)
            if not isinstance(astNode.left, IdentifierModel):
                runtime_error("Invalid assignment target", astNode.line)
            env.set_variable(astNode.left.name, (rightType, rightVal))
            return (rightType, rightVal)
        if isinstance(astNode, IntegerModel):
            return (TYPE_NUMBER, float(astNode.value))
        if isinstance(astNode, FloatModel):
            return (TYPE_NUMBER, float(astNode.value))
        if isinstance(astNode, StringModel):
            return (TYPE_STRING, stringify(astNode.value))
        if isinstance(astNode, BooleanModel):
            return (TYPE_BOOLEAN, bool(astNode.value))
        if isinstance(astNode, GroupingModel):
            return self.interpret(astNode.expression, env)
        if isinstance(astNode, BinaryOperationModel):
            rightType, rightVal = self.interpret(astNode.right, env)
            leftType, leftVal = self.interpret(astNode.left, env)
            if astNode.operator.token_type == TOK_PLUS:
                if rightType == TYPE_NUMBER and leftType == TYPE_NUMBER:
                    return (TYPE_NUMBER, leftVal + rightVal)
                elif rightType == TYPE_STRING or leftType == TYPE_STRING:
                    return (TYPE_STRING, (stringify((leftVal)) + stringify((rightVal))))
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
            operandType, operandVal = self.interpret(astNode.operand, env)
            if astNode.operator.token_type == TOK_MINUS and operandType == TYPE_NUMBER:
                return (TYPE_NUMBER, float(-operandVal))
            elif astNode.operator.token_type == TOK_PLUS and operandType == TYPE_NUMBER:
                return (TYPE_NUMBER, float(+operandVal))
            elif astNode.operator.token_type == TOK_NOT and operandType == TYPE_BOOLEAN:
                return (TYPE_BOOLEAN, bool(not operandVal))
            else:
                runtime_error(f"Unsupported operand type for {astNode.operator.lexeme!r}: '{operandType}'", astNode.line)
        if isinstance(astNode, LogicalOperationModel):
            leftType, leftVal = self.interpret(astNode.left, env)
            rightType, rightVal = self.interpret(astNode.right, env)
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
                self.interpret(stmt, env)
        if isinstance(astNode, PrintStatementModel):
            # TODO: Merge PrintlnStatementModel and PrintStatementModel in a single class add just type I did not know why I have created this kind of function :D I was slepy I guess
            _Type, _Val = self.interpret(astNode.value, env)
            _Val = stringify(_Val)
            _Val = str(_Val).encode("utf-8").decode("unicode_escape")
 
            print(_Val,end="")
        if isinstance(astNode, PrintlnStatementModel):
            _Type, _Val = self.interpret(astNode.value, env)
            _Val = stringify(_Val)
            _Val = str(_Val).encode("utf-8").decode("unicode_escape")

            print(_Val) 
        # TODO: implement switch case with jump table O(1) 
        if isinstance(astNode, IfStatementModel):
            conditionType, conditionVal = self.interpret(astNode.condition, env)
            if conditionType != TYPE_BOOLEAN:
                runtime_error(f"If condition must be boolean, got '{conditionType}'", astNode.line)
            if conditionVal == True:
                self.interpret(astNode.then_stmts, env.new_environment())
            else:
                if astNode.else_stmts is not None:
                    self.interpret(astNode.else_stmts, env.new_environment())
        if isinstance(astNode, WhileStatementModel):
            while True:
                conditionType, conditionVal = self.interpret(astNode.condition, env)
                if conditionType != TYPE_BOOLEAN:
                    runtime_error(f"While condition must be boolean, got '{conditionType}'", astNode.line)
                if conditionVal == False:
                    break
                self.interpret(astNode.body_stmts, env.new_environment())
        if isinstance(astNode, ForStatementModel):
            startType, startVal = self.interpret(astNode.start_expr, env)
            endType, endVal = self.interpret(astNode.end_expr, env)
            incrementType, incrementVal = self.interpret(astNode.increment_expr, env)
            if startType != TYPE_NUMBER or endType != TYPE_NUMBER or incrementType != TYPE_NUMBER:
                runtime_error(f"For loop expressions must be numbers", astNode.line)
            if incrementVal == 0:
                runtime_error(f"For loop increment value cannot be zero", astNode.line)
            varName = astNode.variable_token.lexeme
            currentVal = startVal
            while True:
                if (incrementVal > 0 and currentVal > endVal) or (incrementVal < 0 and currentVal < endVal):
                    break
                loopEnv = env.new_environment()
                loopEnv.set_variable(varName, (TYPE_NUMBER, currentVal))
                self.interpret(astNode.body_stmts, loopEnv)
                currentVal += incrementVal
    def interpret_ast(self, ast):
        environment = Environment()
        self.interpret(ast, environment)
                
        

                
            
            
                

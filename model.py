from tokens import Token

class AST_NODE:
    pass

class Expression(AST_NODE):
    pass

class Statement(AST_NODE):
    pass

class Statements(AST_NODE):
    def __init__(self,stmts,line):
        assert all( isinstance(stmt,Statement) for stmt in stmts), stmts
        self.stmts = stmts
        self.line = line
    def __repr__(self):
        return f"Statements({self.stmts}, line={self.line})"


class IntegerModel(Expression):
    def __init__(self, value, line):
        assert isinstance(value, int), value
        self.value = value
        self.line = line
    def __repr__(self):
        return f"IntegerModel({self.value}, line={self.line})"

class FloatModel(Expression):
    def __init__(self, value, line):
        assert isinstance(value, float), value
        self.value = value
        self.line = line
    def __repr__(self):
        return f"FloatModel({self.value}, line={self.line})"

class UnaryOperationModel(Expression):
    def __init__(self, operator: Token, operand: Expression, line):
        assert isinstance(operator, Token), operator
        assert isinstance(operand, Expression), operand
        self.operator = operator
        self.operand = operand
        self.line = line
    def __repr__(self):
        return f"UnaryOperationModel(operator='{self.operator.lexeme!r}', operand={self.operand}, line={self.line})"

class LogicalOperationModel(Expression):
    def __init__(self, operator: Token, left: Expression, right: Expression, line):
        assert isinstance(operator, Token), operator
        assert isinstance(left, Expression), left
        assert isinstance(right, Expression), right
        self.operator = operator
        self.left = left
        self.right = right
        self.line = line
    def __repr__(self):
        return f"LogicalOperationModel(operator='{self.operator.lexeme!r}', left={self.left}, right={self.right}, line={self.line})"

class GroupingModel(Expression):
    # In Grammar: "(" expression ")"
    def __init__(self, expression: Expression, line):
        assert isinstance(expression, Expression), expression
        self.expression = expression
        self.line = line
    def __repr__(self):
        return f"GroupingModel(expression={self.expression}, line={self.line})"

class BinaryOperationModel(Expression):
    def __init__(self, operator: Token, left: Expression, right: Expression, line):
        assert isinstance(operator, Token), operator
        assert isinstance(left, Expression), left
        assert isinstance(right, Expression), right
        self.operator = operator
        self.left = left
        self.right = right
        self.line = line
    def __repr__(self):
        return f"BinaryOperationModel(operator='{self.operator.lexeme!r}', left={self.left}, right={self.right}, line={self.line})"

class WhileStatementModel(Statement):
    pass

class IfStatementModel(Statement):
    pass

class PrintStatementModel(Statement):
    def __init__(self, value, line):
        assert isinstance(value, Expression), value
        self.value = value
        self.line = line
    def __repr__(self):
        return f"PrintStatementModel({self.value}, line={self.line})"
        
class PrintlnStatementModel(Statement):
    def __init__(self, value, line):
        assert isinstance(value, Expression), value
        self.value = value
        self.line = line
    def __repr__(self):
        return f"PrintlnStatementModel({self.value}, line={self.line})"


class BooleanModel(Expression):
    def __init__(self, value, line):
        assert isinstance(value, bool), value
        self.value = value
        self.line = line
    def __repr__(self):
        return f"BooleanModel({self.value}, line={self.line})"
class StringModel(Expression):
    def __init__(self, value, line):
        assert isinstance(value, str), value
        self.value = value
        self.line = line
    def __repr__(self):
        return f"StringModel({self.value!r}, line={self.line})"

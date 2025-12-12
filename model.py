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
    def __init__(self, condition, body_stmts, line):
        assert isinstance(condition, Expression), condition
        assert isinstance(body_stmts, Statements), body_stmts
        self.condition = condition
        self.body_stmts = body_stmts
        self.line = line
    def __repr__(self):
        return f"WhileStatementModel(condition={self.condition}, body_stmts={self.body_stmts}, line={self.line})"
class ForStatementModel(Statement):
    def __init__(self, variable_token, start_expr, end_expr, increment_expr, body_stmts, line):
        assert isinstance(variable_token, Token), variable_token
        assert isinstance(start_expr, Expression), start_expr
        assert isinstance(end_expr, Expression), end_expr
        assert isinstance(increment_expr, Expression), increment_expr
        assert isinstance(body_stmts, Statements), body_stmts
        self.variable_token = variable_token
        self.start_expr = start_expr
        self.end_expr = end_expr
        self.increment_expr = increment_expr
        self.body_stmts = body_stmts
        self.line = line
    def __repr__(self):
        return f"ForStatementModel(variable_token={self.variable_token}, start_expr={self.start_expr}, end_expr={self.end_expr}, increment_expr={self.increment_expr}, body_stmts={self.body_stmts}, line={self.line})"
class IfStatementModel(Statement):
    def __init__(self, condition, then_stmts, else_stmts, line):
        assert isinstance(condition, Expression), condition
        assert isinstance(then_stmts, Statements), then_stmts
        assert (else_stmts is None) or isinstance(else_stmts, Statements), else_stmts
        self.condition = condition
        self.then_stmts = then_stmts
        self.else_stmts = else_stmts
        self.line = line
    def __repr__(self):
        return f"IfStatementModel(condition={self.condition}, then_stmts={self.then_stmts}, else_stmts={self.else_stmts}, line={self.line})"

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

class IdentifierModel(Expression):
    def __init__(self, name, line):
        assert isinstance(name, str), name
        self.name = name
        self.line = line
    def __repr__(self):
        return f"IdentifierModel({self.name!r}, line={self.line})"

class StringModel(Expression):
    def __init__(self, value, line):
        assert isinstance(value, str), value
        self.value = value
        self.line = line
    def __repr__(self):
        return f"StringModel({self.value!r}, line={self.line})"

class AssignmentModel(Statement):
    def __init__(self, left, right, line):
        assert isinstance(left, Expression), left
        assert isinstance(right, Expression), right
        self.left = left
        self.right = right
        self.line = line
    def __repr__(self):
        return f"AssignmentModel(left={self.left}, right={self.right}, line={self.line})"

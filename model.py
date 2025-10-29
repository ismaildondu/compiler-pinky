from tokens import Token

class Expression:
    pass

class Statement:
    pass

class IntegerModel(Expression):
    def __init__(self, value):
        assert isinstance(value, int), value
        self.value = value
    def __repr__(self):
        return f"IntegerModel({self.value})"

class FloatModel(Expression):
    def __init__(self, value):
        assert isinstance(value, float), value
        self.value = value
    def __repr__(self):
        return f"FloatModel({self.value})"

class UnaryOperationModel(Expression):
    def __init__(self, operator: Token, operand: Expression):
        assert isinstance(operator, Token), operator
        assert isinstance(operand, Expression), operand
        self.operator = operator
        self.operand = operand
    def __repr__(self):
        return f"UnaryOperationModel(operator='{self.operator.lexeme!r}', operand={self.operand})"

class GroupingModel(Expression):
    # In Grammar: "(" expression ")"
    def __init__(self, expression: Expression):
        assert isinstance(expression, Expression), expression
        self.expression = expression
    def __repr__(self):
        return f"GroupingModel(expression={self.expression})"

class BinaryOperationModel(Expression):
    def __init__(self, operator: Token, left: Expression, right: Expression):
        assert isinstance(operator, Token), operator
        assert isinstance(left, Expression), left
        assert isinstance(right, Expression), right
        self.operator = operator
        self.left = left
        self.right = right
    def __repr__(self):
        return f"BinaryOperationModel(operator='{self.operator.lexeme!r}', left={self.left}, right={self.right})"

class WhileStatementModel(Statement):
    pass

class IfStatementModel(Statement):
    pass
       

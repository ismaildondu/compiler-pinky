import sys

def pretty_ast(ast):
    spaceCount = 0
    stringRep = str(ast)
    for char in stringRep:
        if char == '(':
            spaceCount += 2
            print(char)
            print(' ' * spaceCount, end='')
        elif char == ')':
            spaceCount -= 2
            print()
            print(' ' * spaceCount, end='')
            print(char, end='')
        elif char == ',':
            print(char)
            print(' ' * spaceCount, end='')
        else:
            print(char, end='')
    print()

ERROR_RED = "\033[91m"
def parser_error(message, line=None):
    if line is not None:
        print(f"{ERROR_RED}Parser Error [Line {line}]: {message}\033[0m")
    else:
        print(f"{ERROR_RED}Parser Error: {message}\033[0m")
    sys.exit(1)
    
def lexer_error(message, line=None):
    if line is not None:
        print(f"{ERROR_RED}Lexer Error [Line {line}]: {message}\033[0m")
    else:
        print(f"{ERROR_RED}Lexer Error: {message}\033[0m")
    sys.exit(1)

def runtime_error(message, line=None):
    if line is not None:
        print(f"{ERROR_RED}Runtime Error [Line {line}]: {message}\033[0m")
    else:
        print(f"{ERROR_RED}Runtime Error: {message}\033[0m")
    sys.exit(1)

def stringify(value):
    if value is None:
        return "nil"
    elif isinstance(value, bool):
        return "true" if value else "false"
    elif isinstance(value, float):
        text = str(value)
        if text.endswith(".0"):
            text = text[:-2]
        return text
    else:
        return str(value)


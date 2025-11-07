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


class Environment:
    def __init__(self, parent=None):
        self.variables = {}
        self.parent = parent
    
    def get_variable(self, name):
        if name in self.variables:
            return self.variables[name]
        elif self.parent is not None:
            return self.parent.get_variable(name)
        else:
            return None
    
    def set_variable(self, name, value):
        self.variables[name] = value

    def new_environment(self):
        return Environment(parent=self)

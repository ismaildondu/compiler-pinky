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
        if name in self.variables:
            self.variables[name] = value
        elif self.parent is not None and self.parent.get_variable(name) is not None:
            self.parent.set_variable(name, value)
        else:
            self.variables[name] = value

    def new_environment(self):
        return Environment(parent=self)

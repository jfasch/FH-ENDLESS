class EndlessException(Exception): pass

class ReceptacleAlreadyConnected(EndlessException): pass
class ReceptacleNotConnected(EndlessException): pass
class ReceptacleMultiReturnsValue(EndlessException): pass
class ReceptacleAttributeNotMethod(EndlessException): pass
class ReceptacleAttributeNotInBasetype(EndlessException): pass

class MappedMethodNotAsync(TypeError):
    def __init__(self, baseclass, componentmethodname):
        super().__init__(f'Component method {componentmethodname} is not "async" as defined in base class {baseclass.__name__}')
        self.baseclass = baseclass
        self.componentmethodname = componentmethodname

class MappedMethodNotSync(TypeError):
    def __init__(self, baseclass, componentmethodname):
        super().__init__(f'Component method {componentmethodname} is not a plain function as defined in base class {baseclass.__name__}')
        self.baseclass = baseclass
        self.componentmethodname = componentmethodname


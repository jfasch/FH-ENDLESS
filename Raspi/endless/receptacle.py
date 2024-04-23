from .component import Component
from .errors import ReceptacleAlreadyConnected


class receptacle:
    def __init__(self, name, basetype):
        self.receptacle_name = name
        self.receptacle_basetype = basetype

    def __call__(self, component_class):
        if not issubclass(component_class, Component):
            raise TypeError(f'{component_class.__name__} must be derived from {Component.__name__}')

        def receptacle_public_getter(self_component):
            return self._receptacle_public_accessor(
                receptacle_name=self.receptacle_name, 
                component=self_component, 
                required_type=self.receptacle_basetype)

        setattr(component_class, self.receptacle_name, property(receptacle_public_getter))

        def receptacle_private_getter(self_component):
            return self._receptacle_private_accessor(
                receptacle_name=self.receptacle_name, 
                component=self_component)

        setattr(component_class, '_'+self.receptacle_name, property(receptacle_private_getter))

        return component_class

    class _receptacle_public_accessor:
        def __init__(self, receptacle_name, component, required_type):
            self.receptacle_name = receptacle_name
            self.component = component
            self.required_type = required_type
        def connect(self, obj):
            if not isinstance(obj, self.required_type):
                raise TypeError(f'{obj} must be derived from {self.required_type.__name__}')
            connected_object = self.component._receptacles.get(self.receptacle_name)
            if connected_object is not None:
                raise ReceptacleAlreadyConnected(f'Receptacle {self.receptacle_name} is already connected (connected object: {connected_object})')
            self.component._receptacles[self.receptacle_name] = obj

    class _receptacle_private_accessor:
        def __init__(self, receptacle_name, component):
            self.receptacle_name = receptacle_name
            self.component = component
        def __getattr__(self, attrname):
            return getattr(self.component._receptacles[self.receptacle_name], attrname)


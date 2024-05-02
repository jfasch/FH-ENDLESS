from .component import Component
from .errors import \
    ReceptacleAlreadyConnected, \
    ReceptacleNotConnected, \
    ReceptacleMultiReturnsValue, \
    ReceptacleAttributeNotInBasetype, \
    ReceptacleAttributeNotMethod

import inspect


(ONE,
 ONE_OR_MANY,
) = range(2)

class receptacle:
    def __init__(self, name, basetype, multiplicity):
        self.receptacle_name = name
        self.receptacle_basetype = basetype
        self.receptacle_multiplicity = multiplicity

    def __call__(self, component_class):
        if not issubclass(component_class, Component):
            raise TypeError(f'{component_class.__name__} must be derived from {Component.__name__}')

        def receptacle_public_getter(self_component):
            return self._receptacle_public_accessor(
                receptacle_name=self.receptacle_name, 
                component=self_component, 
                required_type=self.receptacle_basetype,
                multiplicity=self.receptacle_multiplicity,
            )

        setattr(component_class, self.receptacle_name, property(receptacle_public_getter))

        def receptacle_private_getter(self_component):
            return self._receptacle_private_accessor(
                receptacle_name=self.receptacle_name, 
                component=self_component,
                required_type=self.receptacle_basetype,
                multiplicity=self.receptacle_multiplicity,
            )

        setattr(component_class, '_'+self.receptacle_name, property(receptacle_private_getter))

        return component_class

    class _receptacle_public_accessor:
        def __init__(self, receptacle_name, component, required_type, multiplicity):
            self.receptacle_name = receptacle_name
            self.component = component
            self.required_type = required_type
            self.multiplicity = multiplicity

        def connect(self, obj):
            if not isinstance(obj, self.required_type):
                raise TypeError(f'{obj} must be derived from {self.required_type.__name__}')

            connected_objects = self.component._receptacles.get(self.receptacle_name)
            if connected_objects is None:
                connected_objects = []
                self.component._receptacles[self.receptacle_name] = connected_objects

            if self.multiplicity == ONE:
                if len(connected_objects) != 0:
                    raise ReceptacleAlreadyConnected(f'Receptacle {self.receptacle_name} is already connected (connected object: {connected_objects[0]})')
            elif self.multiplicity == ONE_OR_MANY:
                pass

            connected_objects.append(obj)

    class _receptacle_private_accessor:
        def __init__(self, receptacle_name, component, required_type, multiplicity):
            self.receptacle_name = receptacle_name
            self.component = component
            self.required_type = required_type
            self.multiplicity = multiplicity

        def __getattr__(self, attrname):
            try:
                basemethod = getattr(self.required_type, attrname)
            except AttributeError:
                raise ReceptacleAttributeNotInBasetype(f"Receptacle {self.receptacle_name}'s base type {self.required_type} has no attribute {attrname}")

            if not inspect.isfunction(basemethod):
                raise ReceptacleAttributeNotMethod(f"Receptacle {self.receptacle_name}'s attribute {attrname} is not defined as method in {self.required_type}")

            connected_objects = self.component._receptacles.get(self.receptacle_name)
            if connected_objects is None:
                connected_objects = []
                self.component._receptacles[self.receptacle_name] = connected_objects

            if self.multiplicity == ONE:
                if len(connected_objects) == 0:
                    raise ReceptacleNotConnected(f'Receptacle {self.receptacle_name} is not connected')
                return getattr(connected_objects[0], attrname)
            elif self.multiplicity == ONE_OR_MANY:
                if len(connected_objects) == 0:
                    raise ReceptacleNotConnected(f'Receptacle {self.receptacle_name} is not connected')

                # note that we create the trampoline *every time*
                # a multi-receptacle is used -> subject to
                # performance optimization.
                if inspect.iscoroutinefunction(basemethod):
                    async def multi_trampoline_async(*args, **kwargs):
                        for obj in connected_objects:
                            func = getattr(obj, attrname)
                            coro = func(*args, **kwargs)
                            retval = await coro
                            if retval is not None:
                                raise ReceptacleMultiReturnsValue(f'Receptacle {self.receptacle_name} is multi, but {obj} returned a value')

                    return multi_trampoline_async
                else:
                    def multi_trampoline_sync(*args, **kwargs):
                        for obj in connected_objects:
                            func = getattr(obj, attrname)
                            retval = func(*args, **kwargs)
                            if retval is not None:
                                raise ReceptacleMultiReturnsValue(f'Receptacle {self.receptacle_name} is multi, but {obj} returned a value')

                    return multi_trampoline_sync

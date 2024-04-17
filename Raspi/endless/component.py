from .errorhandler import ErrorHandler
from .errors import ReceptacleAlreadyConnected

import abc
import inspect


class Component:
    def __init__(self):
        self.errorhandler = None
        self._facets = {}
        self._receptacles = {}

    def errors_to(self, errorhandler):
        assert self.errorhandler is None
        assert isinstance(errorhandler, ErrorHandler), errorhandler
        self.errorhandler = errorhandler

class LifetimeComponent(Component):
    def __init__(self, func):
        super().__init__()
        self.func = func
        self.task = None
    def start(self, taskgroup):
        assert self.task is None
        self.task = taskgroup.create_task(self.func())
    def stop(self):
        assert self.task is not None
        self.task.cancel()
        self.task = None

class facet:
    def __init__(self, name, basetype, methodspec):
        self.facet_name = name
        self.facet_basetype = basetype
        self.facet_methodspec = methodspec

    def __call__(self, component_class):
        if not issubclass(component_class, Component):
            raise TypeError(f'{component_class.__name__} must be derived from {Component.__name__}')

        facet_class = self._create_facet_class(component_class)

        def facet_getter(self_component):
            facet_obj = self_component._facets.get(self.facet_name)
            if facet_obj is None:
                facet_obj = facet_class()
                facet_obj.component = self_component
                self_component._facets[self.facet_name] = facet_obj
            return facet_obj

        setattr(component_class, self.facet_name, property(facet_getter))

        return component_class

    def _create_facet_class(self, component_class):
        facet_clsname = f'{self.facet_basetype.__name__}_{self.facet_name}'
        facet_clsattrs = {}
        for facet_methodname, component_methodname in self.facet_methodspec:
            facet_clsattrs[facet_methodname] = self._create_trampoline_method(facet_methodname, component_methodname, component_class)
        return type(facet_clsname, (self.facet_basetype,), facet_clsattrs)

    def _create_trampoline_method(self, facet_methodname, component_methodname, component_class):
        # require facet method to be defined in base type
        try:
            getattr(self.facet_basetype, facet_methodname)
        except AttributeError:
            raise TypeError(f'Facet method "{facet_methodname}()" is not defined in base type {self.facet_basetype.__name__}')

        # require component method to be defined in component
        try:
            component_method = getattr(component_class, component_methodname)
        except AttributeError:
            raise TypeError(f'Method "{component_methodname}()" is not defined in {component_class.__name__}')

        # create trampoline. 

        # args[0] is the facet instance (self). compmethod is a method
        # called on the component instance, but with the same
        # signature otherwise.

        # exchange facet-self with component-self, and call the
        # component method.
        if inspect.iscoroutinefunction(component_method):
            async def trampoline(*args, **kwargs):
                newargs = (args[0].component,) + args[1:]
                return await component_method(*newargs, **kwargs)
        else:
            def trampoline(*args, **kwargs):
                newargs = (args[0].component,) + args[1:]
                return component_method(*newargs, **kwargs)

        return trampoline

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


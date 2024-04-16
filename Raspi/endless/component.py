from .errorhandler import ErrorHandler

import functools


class Component:
    def __init__(self):
        self.errorhandler = None
        self._facets = {}

    def errors_to(self, errorhandler):
        assert self.errorhandler is None
        assert isinstance(errorhandler, ErrorHandler)
        self.errorhandler = errorhandler

class facet:
    def __init__(self, name, basetype, methodspec):
        self.facet_name = name
        self.facet_basetype = basetype
        self.facet_methodspec = methodspec

    def __call__(self, cls):
        if not issubclass(cls, Component):
            raise TypeError(f'{cls.__name__} must be derived from {Component.__name__}')

        facet_class = self._create_facet_class(cls)

        def facet_getter(self_component):
            facet_obj = self_component._facets.get(self.facet_name)
            if facet_obj is None:
                facet_obj = facet_class()
                facet_obj.component = self_component
                self_component._facets[self.facet_name] = facet_obj
            return facet_obj

        setattr(cls, self.facet_name, property(facet_getter))

        return cls

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
            
        def trampoline(*args, **kwargs):
            # args[0] is the facet instance (self). compmethod is a
            # method called on the component instance, but with the
            # same signature otherwise.

            # exchange facet-self with component-self, and call the
            # component method.

            newargs = (args[0].component,) + args[1:]
            return component_method(*newargs, **kwargs)

        return trampoline

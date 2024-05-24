from .component import Component
from .errors import MappedMethodNotAsync, MappedMethodNotSync

import functools
import inspect


class facet:
    '''Class decorator for component classes.

    .. code-block:: python

       @facet('facetname', FacetInterface, (('method1', '_implementation_method1'), ('method2', '_implementation_method2')))
       class MyComponent(Component):
           def _implementation_method1(self, ...):
               # do something
               pass
           def _implementation_method2(self, ...):
               # do something
               pass

    This creates a property ``facetname`` on ``MyComponent``
    instances, of base type
    ``FacetInterface``. ``FacetInterface.method1`` is implemented as a
    simple trampoline that calls into the associated component
    object's ``_implementation_method1``.

    With this, the component can be used as follows,

    .. code-block:: python

       my_comp = MyComponent()
       my_comp.facetname.method1('blah')

    '''


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
            base_method = getattr(self.facet_basetype, facet_methodname)
        except AttributeError:
            raise TypeError(f'Facet method "{facet_methodname}()" is not defined in base type {self.facet_basetype.__name__}')

        # require component method to be defined in component
        try:
            component_method = getattr(component_class, component_methodname)
        except AttributeError:
            raise TypeError(f'Method "{component_methodname}()" is not defined in {component_class.__name__}')

        # verify that no function/coro mismatch exists
        if inspect.iscoroutinefunction(base_method) and not inspect.iscoroutinefunction(component_method):
            raise MappedMethodNotAsync(baseclass=self.facet_basetype, componentmethodname=component_methodname)
        if inspect.iscoroutinefunction(component_method) and not inspect.iscoroutinefunction(base_method):
            raise MappedMethodNotSync(baseclass=self.facet_basetype, componentmethodname=component_methodname)

        # create trampoline. 

        # args[0] is the facet instance (self). compmethod is a method
        # called on the component instance, but with the same
        # signature otherwise.

        # exchange facet-self with component-self, and call the
        # component method.
        if inspect.iscoroutinefunction(component_method):
            @functools.wraps(component_method)
            async def trampoline(*args, **kwargs):
                newargs = (args[0].component,) + args[1:]
                return await component_method(*newargs, **kwargs)
        else:
            @functools.wraps(component_method)
            def trampoline(*args, **kwargs):
                newargs = (args[0].component,) + args[1:]
                return component_method(*newargs, **kwargs)

        return trampoline

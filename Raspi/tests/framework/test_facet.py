from endless.framework.component import Component
from endless.framework.errors import MappedMethodNotAsync, MappedMethodNotSync
from endless.framework.facet import facet

import pytest
import inspect


def test_manual_facet():
    import abc
    class SomeFunctionality(abc.ABC):
        @abc.abstractmethod
        def invoke_aspect1(self):
            raise NotImplementedError
        @abc.abstractmethod
        def invoke_aspect2(self):
            raise NotImplementedError

    class SomeFunctionality_MyComponent:
        def __init__(self, component):
            self.component = component
        def invoke_aspect1(self):
            self.component._some_functionality_aspect1()
        def invoke_aspect2(self):
            self.component._some_functionality_aspect2()

    class MyComponent(Component):
        def __init__(self):
            self.some_functionality = SomeFunctionality_MyComponent(self)
        def _some_functionality_aspect1(self):
            self.aspect1_called = True
        def _some_functionality_aspect2(self):
            self.aspect2_called = True

    comp = MyComponent()
    comp.some_functionality.invoke_aspect1()
    comp.some_functionality.invoke_aspect2()

    assert comp.aspect1_called
    assert comp.aspect2_called

def test_facet_instantiation_by_decorator():
    import abc
    class SomeFunctionality(abc.ABC):
        @abc.abstractmethod
        def invoke_aspect1(self):
            raise NotImplementedError
        @abc.abstractmethod
        def invoke_aspect2(self):
            raise NotImplementedError

    class SomeFunctionality_MyComponent:
        def __init__(self, component):
            self.component = component
        def invoke_aspect1(self):
            self.component._some_functionality_aspect1()
        def invoke_aspect2(self):
            self.component._some_functionality_aspect2()

    @facet(name='some_functionality',
           basetype=SomeFunctionality,
           methodspec=(('invoke_aspect1', '_some_functionality_aspect1'),
                       ('invoke_aspect2', '_some_functionality_aspect2'),
                       )
           )
    class MyComponent(Component):
        def _some_functionality_aspect1(self):
            self.aspect1_called = True
        def _some_functionality_aspect2(self):
            self.aspect2_called = True

    comp = MyComponent()

    # retrieve facet object from component, and invoke facet methods
    facet_obj = comp.some_functionality
    facet_obj.invoke_aspect1()
    facet_obj.invoke_aspect2()

    # facet methods must have called into component via specified
    # methods
    assert comp.aspect1_called
    assert comp.aspect2_called

def test_facet_on_non_component():
    class FacetBaseType: 
        def facetmethod(self): pass
    
    with pytest.raises(TypeError):
        @facet('facetname', FacetBaseType, (('facetmethod', 'componentmethod'),))
        class NonComponent: 
            def componentmethod(self): pass

def test_methodspec__facetmethod_not_a_basetype_method():
    class FacetBaseType: 
        def facetmethod(self): pass
    
    with pytest.raises(TypeError):
        @facet('facetname', FacetBaseType, (('facetmethod_bad', # not defined in basetype
                                             'componentmethod'),))
        class MyComponent(Component): 
            def componentmethod(self): pass

def test_methodspec__componentmethod_not_defined_in_component():
    class FacetBaseType: 
        def facetmethod(self): pass
    
    with pytest.raises(TypeError):
        @facet('facetname', FacetBaseType, (('facetmethod',
                                             'componentmethod_bad' # not defined in component
                                             ),))
        class MyComponent(Component): 
            def componentmethod(self): pass

def test_async_methods():
    class FacetBaseType:
        def regular_function(self): pass
        async def coroutine_function(self): pass

    @facet('facetname', FacetBaseType, (('regular_function', '_regular_function'), 
                                        ('coroutine_function', '_coroutine_function'),
                                        ))
    class MyComponent(Component):
        def _regular_function(self): pass
        async def _coroutine_function(self): pass

    comp = MyComponent()

    assert inspect.iscoroutinefunction(comp.facetname.coroutine_function)

    # inspect.ismethod() qualifies coroutine function as functions. I
    # put this here just to remember, and to make that clear.
    assert inspect.ismethod(comp.facetname.coroutine_function)

    assert not inspect.iscoroutinefunction(comp.facetname.regular_function)
    assert inspect.ismethod(comp.facetname.regular_function)

def test_connect__sync_async_mismatch__interface_coro__component_func():
    class Interface:
        async def func(self):                 # async
            pass

    with pytest.raises(MappedMethodNotAsync) as excinfo:
        @facet('interface', Interface, (('func', '_func_impl'),))
        class MyComponent(Component):
            def _func_impl(self):             # sync
                pass
        
    assert excinfo.value.baseclass == Interface
    assert excinfo.value.componentmethodname == '_func_impl'

def test_connect__sync_async_mismatch__interface_func__component_coro():
    class Interface:
        def func(self):                       # sync
            pass

    with pytest.raises(MappedMethodNotSync) as excinfo:
        @facet('interface', Interface, (('func', '_func_impl'),))
        class MyComponent(Component):
            async def _func_impl(self):       # async
                pass

    assert excinfo.value.baseclass == Interface
    assert excinfo.value.componentmethodname == '_func_impl'

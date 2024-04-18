from endless.component import Component, receptacle, MappedMethodNotAsync
from endless.errors import ReceptacleAlreadyConnected

import pytest


def test_sunny():
    class Interface:
        def method(self): pass

    class Implementation(Interface):
        def method(self):
            self.called = True

    @receptacle('receptaclename', basetype=Interface)
    class MyComponent(Component):
        def do_something(self):
            self._receptaclename.method()

    comp = MyComponent()
    impl = Implementation()
    comp.receptaclename.connect(impl)

    comp.do_something()

    assert impl.called

def test_already_connected():
    class Interface: pass
    class Implementation(Interface): pass

    @receptacle('receptaclename', basetype=Interface)
    class MyComponent(Component): pass

    comp = MyComponent()
    comp.receptaclename.connect(Implementation())

    with pytest.raises(ReceptacleAlreadyConnected):
        comp.receptaclename.connect(Implementation())

def test_connect_wrong_type():
    class Interface:
        def method(self): pass
    class Implementation:    # not derived from Interface
        pass      

    @receptacle('receptaclename', basetype=Interface)
    class MyComponent(Component): pass

    comp = MyComponent()
    
    with pytest.raises(TypeError):
        comp.receptaclename.connect(Implementation())

def test_receptacle_on_non_component():
    class Interface: pass
    class Implementation(Interface): pass

    with pytest.raises(TypeError):
        @receptacle('receptaclename', basetype=Interface)
        class MyComponent: pass     # not a Component

from endless.component import Component
from endless.errors import MappedMethodNotAsync
from endless.receptacle import receptacle, ONE, ONE_OR_MANY
from endless.errors import \
    ReceptacleAlreadyConnected, \
    ReceptacleNotConnected, \
    ReceptacleMultiReturnsValue, \
    ReceptacleAttributeNotMethod, \
    ReceptacleAttributeNotInBasetype

import pytest


def test_ONE_sunny():
    class Interface:
        def method(self): pass

    class Implementation(Interface):
        def method(self):
            self.called = True

    @receptacle('receptaclename', basetype=Interface, multiplicity=ONE)
    class MyComponent(Component):
        def call_out(self):
            self._receptaclename.method()

    comp = MyComponent()
    impl = Implementation()
    comp.receptaclename.connect(impl)

    comp.call_out()

    assert impl.called

def test_receptacle_on_non_component():
    class Interface: pass
    class Implementation(Interface): pass

    with pytest.raises(TypeError):
        @receptacle('receptaclename', basetype=Interface, multiplicity=ONE)
        class MyComponent: pass     # not a Component

def test_access_non_existing_attribute():
    class Interface: pass
    class Implementation(Interface): pass

    @receptacle('receptaclename', basetype=Interface, multiplicity=ONE)
    class MyComponent(Component):
        def call_out(self):
            self._receptaclename.no_exist()    # <--- not defined in basetype

    impl = Implementation()
    comp = MyComponent()
    comp.receptaclename.connect(impl)

    with pytest.raises(ReceptacleAttributeNotInBasetype):
        comp.call_out()

def test_attribute_access_only_method():
    '''Receptacle attribute access only possible on methods'''

    class Interface:
        class_attr = 666
    class Implementation(Interface):
        def __init__(self):
            super().__init__()

    @receptacle('receptaclename', Interface, multiplicity=ONE)
    class MyComponent(Component):
        def call_out(self):
            value = self._receptaclename.class_attr     # <--- accessing non-method

    impl = Implementation()
    comp = MyComponent()
    comp.receptaclename.connect(impl)

    with pytest.raises(ReceptacleAttributeNotMethod):
        comp.call_out()

def test_ONE_permits_return_value():
    class ReturnsValue:
        def method(self): return 42
        
    @receptacle('receptaclename', basetype=ReturnsValue, multiplicity=ONE)
    class MyComponent(Component):
        def call_out(self):
            return self._receptaclename.method()

    comp = MyComponent()
    comp.receptaclename.connect(ReturnsValue())

    value = comp.call_out()

    assert value == 42

def test_ONE_already_connected():
    class Interface: pass
    class Implementation(Interface): pass

    @receptacle('receptaclename', basetype=Interface, multiplicity=ONE)
    class MyComponent(Component): pass

    comp = MyComponent()
    comp.receptaclename.connect(Implementation())

    with pytest.raises(ReceptacleAlreadyConnected):
        comp.receptaclename.connect(Implementation())

def test_ONE_not_connected():
    class Interface: 
        def method(self): pass
    class Implementation(Interface): pass

    @receptacle('receptaclename', basetype=Interface, multiplicity=ONE)
    class MyComponent(Component): 
        def use_receptacle(self):
            self._receptaclename.method()

    comp = MyComponent()

    with pytest.raises(ReceptacleNotConnected):
        comp.use_receptacle()

def test_ONE_connect_wrong_type():
    class Interface:
        def method(self): pass
    class Implementation:    # not derived from Interface
        pass      

    @receptacle('receptaclename', basetype=Interface, multiplicity=ONE)
    class MyComponent(Component): pass

    comp = MyComponent()
    
    with pytest.raises(TypeError):
        comp.receptaclename.connect(Implementation())

def test_multiplicity_ONE_OR_MANY__sunny_sync():
    class Interface:
        def method(self): pass
    class Implementation(Interface):
        def method(self):
            self.called = True

    @receptacle('receptaclename', Interface, multiplicity=ONE_OR_MANY)
    class AComponent(Component):
        def call_out(self):
            self._receptaclename.method()

    impl1 = Implementation()
    impl2 = Implementation()
    component = AComponent()

    component.receptaclename.connect(impl1)
    component.receptaclename.connect(impl2)

    component.call_out()

    assert impl1.called
    assert impl2.called

@pytest.mark.asyncio
async def test_multiplicity_ONE_OR_MANY__sunny_async():
    class Interface:
        async def method(self): pass
    class Implementation(Interface):
        async def method(self):
            self.called = True

    @receptacle('receptaclename', Interface, multiplicity=ONE_OR_MANY)
    class AComponent(Component):
        async def call_out(self):
            await self._receptaclename.method()

    impl1 = Implementation()
    impl2 = Implementation()
    component = AComponent()

    component.receptaclename.connect(impl1)
    component.receptaclename.connect(impl2)

    await component.call_out()

    assert impl1.called
    assert impl2.called

def test_multiplicity_ONE_OR_MANY__not_connected():
    class Interface: 
        def method(self): pass
    @receptacle('receptaclename', Interface, multiplicity=ONE_OR_MANY)
    class AComponent(Component):
        def call_out(self):
            self._receptaclename.method()

    with pytest.raises(ReceptacleNotConnected):
        AComponent().call_out()

def test_multiplicity_ONE_OR_MANY__does_not_permit_return_value__sync():
    class ReturnsValue:
        def method(self): return 42
        
    @receptacle('receptaclename', basetype=ReturnsValue, multiplicity=ONE_OR_MANY)
    class MyComponent(Component):
        def call_out(self):
            return self._receptaclename.method()

    comp = MyComponent()
    comp.receptaclename.connect(ReturnsValue())

    with pytest.raises(ReceptacleMultiReturnsValue):
        comp.call_out()

@pytest.mark.asyncio
async def test_multiplicity_ONE_OR_MANY__does_not_permit_return_value__async():
    class ReturnsValue:
        async def method(self): return 42
        
    @receptacle('receptaclename', basetype=ReturnsValue, multiplicity=ONE_OR_MANY)
    class MyComponent(Component):
        async def call_out(self):
            return await self._receptaclename.method()

    comp = MyComponent()
    comp.receptaclename.connect(ReturnsValue())

    with pytest.raises(ReceptacleMultiReturnsValue):
        await comp.call_out()

    

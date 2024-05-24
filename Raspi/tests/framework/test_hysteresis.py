from endless.framework.interfaces import Switch
from endless.framework.hysteresis import Hysteresis
from endless.framework.sample import Sample

import pytest
from datetime import datetime

class MySwitch(Switch):
    def __init__(self):
        self.state = None
    async def set_state(self, state: bool):
        assert type(state) is bool
        self.state = state

@pytest.mark.asyncio
async def test_basic():
    my_switch = MySwitch()
    hysteresis = Hysteresis(low=36.2, high=37.3)

    hysteresis.switch.connect(my_switch)

    # below low
    await hysteresis.control.adapt(timestamp=datetime(2024, 4, 18, 17, 0), value=35)
    assert my_switch.state is True

    # between low and high -> no change
    await hysteresis.control.adapt(timestamp=datetime(2024, 4, 18, 17, 1), value=37.1)
    assert my_switch.state is True

    # above high
    await hysteresis.control.adapt(timestamp=datetime(2024, 4, 18, 17, 2), value=38.5)
    assert my_switch.state is False

@pytest.mark.asyncio
async def test_set_hi_lo():
    my_switch = MySwitch()
    hysteresis = Hysteresis(low=20, high=40)

    hysteresis.switch.connect(my_switch)

    await hysteresis.control.adapt(timestamp=datetime(2024, 5, 24, 13, 41), value=21)
    assert my_switch.state is None    # None: switch still unused by hysteresis
    
    await hysteresis.config.set_low(22)

    await hysteresis.control.adapt(timestamp=datetime(2024, 5, 24, 13, 42), value=21)
    assert my_switch.state is True
    
    await hysteresis.control.adapt(timestamp=datetime(2024, 5, 24, 13, 43), value=39)
    assert my_switch.state is True
    
    await hysteresis.config.set_high(38)

    await hysteresis.control.adapt(timestamp=datetime(2024, 5, 24, 13, 44), value=39)
    assert my_switch.state is False

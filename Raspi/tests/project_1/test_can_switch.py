from endless.project_1.can_switch import CANSwitch

from endless.framework.interfaces import CANOutputHandler

import pytest
from datetime import datetime
import struct


@pytest.mark.asyncio
async def test_can_protocol():
    switch = CANSwitch(can_id=42, number=2)

    class MyFrameSink(CANOutputHandler):
        def __init__(self):
            self.can_id = None
        async def write_frame(self, can_id, payload):
            assert self.can_id is None
            self.can_id = can_id
            self.payload = payload

    frame_sink = MyFrameSink()
    switch.frame_out.connect(frame_sink)

    await switch.switch.set_state(True)

    assert frame_sink.can_id == 42

    sw0, sw1, sw2, sw3 = struct.unpack('????', frame_sink.payload)
    assert sw0 is False
    assert sw1 is False
    assert sw2 is True
    assert sw3 is False

@pytest.mark.asyncio
async def test_counter():
    switch = CANSwitch(can_id=42, number=2)

    class MyFrameDump(CANOutputHandler):
        async def write_frame(self, can_id, payload): 
            pass
    dump = MyFrameDump()
    switch.frame_out.connect(dump)

    await switch.switch.set_state(True)
    await switch.switch.set_state(False)
    await switch.switch.set_state(True)

    assert await switch.counter.get_count() == 3

    # although we do not change state, this counts as switch-action
    await switch.switch.set_state(True)

    assert await switch.counter.get_count() == 4

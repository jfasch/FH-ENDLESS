from endless.interfaces import CANInputHandler
from endless.can_reader import CANReader
from endless.runner import Runner, StopRunning
from endless import can_util

import pytest
import socket
import struct
import asyncio


@pytest.mark.asyncio
async def test_basic(monkeypatch):
    left, right = socket.socketpair()
    left.setblocking(False)

    def my_create_can_socket(self):
        return left
    monkeypatch.setattr(can_util, 'create_socket', my_create_can_socket)

    # inject frame
    data = b'hello'
    frame = struct.pack("=IB3x8s", 42, len(data), data)
    right.send(frame)

    class MyCANInputHandler(CANInputHandler):
        def __init__(self):
            self.frame_ready = asyncio.get_running_loop().create_future()
        async def handle_frame(self, can_id, payload):
            self.frame_ready.set_result((can_id, payload))

    handler = MyCANInputHandler()

    rdr = CANReader(can_iface='blah')
    rdr.frame_out.connect(handler)

    async with Runner((rdr,)) as runner:
        await handler.frame_ready
        raise StopRunning

    assert handler.frame_ready.result() == (42, b'hello')

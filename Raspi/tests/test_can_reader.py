from endless.sink_mock import MockSink, have_n_samples
from endless.can_reader import CANReader
from endless.sample import Sample
from endless.runner import Runner, StopRunning
from endless import async_util
from endless import can_util

import pytest
import socket
import struct
from datetime import datetime, timedelta


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

    have_1, cond = have_n_samples(1)
    sink = MockSink(cond)
    source = CANReader(name='a-name', can_iface='blah', can_id=42,
                       timestamps=async_util.mock_timestamps_sync(start=datetime(2024, 4, 3, 9, 4), interval=timedelta(seconds=1)))
    source.outlet.connect(sink.inlet)

    async with Runner((source, sink)) as runner:
        await have_1
        raise StopRunning

    assert sink.collected_samples[0].name == 'a-name'
    assert sink.collected_samples[0].timestamp == datetime(2024, 4, 3, 9, 4)
    assert sink.collected_samples[0].data.can_id == 42
    assert sink.collected_samples[0].data.payload == b'hello'

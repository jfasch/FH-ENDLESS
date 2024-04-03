from endless.sink_mock import MockSink, have_n_samples
from endless.source_can import CANSource
from endless.sample import Sample
from endless.runner import Runner
from endless import async_util

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

    monkeypatch.setattr(CANSource, '_create_socket', my_create_can_socket)

    # inject frame
    data =  struct.pack("<Ii", 42, 37500)
    frame = struct.pack("=IB3x8s", 42, len(data), data)
    right.send(frame)

    have_1, cond = have_n_samples(1)
    sink = MockSink(cond)
    source = CANSource(name='a-name', can_iface='blah', can_id=42, 
                       timestamps=async_util.mock_timestamps_sync(start=datetime(2024, 4, 3, 9, 4), interval=timedelta(seconds=1)))
    source.connect(sink)

    async with Runner(sources=[source], sinks=[sink]) as runner:
        await have_1
        runner.stop()

    assert sink.samples[0] == Sample(name='a-name', timestamp=datetime(2024, 4, 3, 9, 4), temperature=pytest.approx(37.5))

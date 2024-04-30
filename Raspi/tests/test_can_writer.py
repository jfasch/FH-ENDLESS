from endless.source_mock import MockSource
from endless.can_writer import CANWriter
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
        return right
    monkeypatch.setattr(can_util, 'create_socket', my_create_can_socket)

    writer = CANWriter(can_iface='the-iface')
    await writer.inlet.consume_sample(
        Sample(tag='some-tag',
               timestamp=datetime(2024, 4, 23, 14, 54),
               data=can_util.CANFrame(
                   can_id=0x42,
                   payload=b'hello'))
    )

    frame = left.recv(1024)

    can_id, can_dlc, can_payload = struct.unpack("=IB3x8s", frame)
    can_payload = can_payload[:can_dlc]

    assert can_id == 0x42
    assert can_dlc == 5
    assert can_payload == b'hello'

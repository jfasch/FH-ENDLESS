from .component import LifetimeComponent
from .receptacle import receptacle
from .interfaces import SampleInlet
from .sample import Sample
from .async_util import wallclock_timestamps_nosleep
from . import can_util

import socket
import struct
import sys
import asyncio
from datetime import datetime


@receptacle('outlet', SampleInlet)
class CANReader(LifetimeComponent):
    def __init__(self, tag, can_iface, can_id, timestamps=None):
        super().__init__(self._run)

        self.tag = tag
        self.can_iface = can_iface
        self.can_id = can_id

        if timestamps is None:
            self.timestamps = wallclock_timestamps_nosleep()
        else:
            self.timestamps = timestamps

    async def _run(self):
        can_socket = can_util.create_socket(self.can_iface)

        while True:
            frame = await asyncio.get_running_loop().sock_recv(can_socket, can_util.FRAME_SIZE)
            frame_can_id, frame_can_dlc, frame_data = struct.unpack(can_util.FRAME_LAYOUT, frame)

            if frame_can_id != self.can_id: # ignore foreign frames
                continue

            timestamp = next(self.timestamps)

            await self._outlet.consume_sample(Sample(
                tag=self.tag,
                timestamp=timestamp, 
                data=can_util.CANFrame(
                    can_id=frame_can_id, 
                    payload=frame_data[:frame_can_dlc],
                ),
            ))

from .sample import Sample
from .source import Source
from .async_util import wallclock_timestamps_nosleep

import socket
import struct
import sys
import asyncio
from datetime import datetime


_FRAME_LAYOUT = "=IB3x8s"
_FRAME_SIZE = struct.calcsize(_FRAME_LAYOUT)


class CANSource(Source):
    def __init__(self, name, can_iface, can_id, parsedata, timestamps=None):
        super().__init__(name)

        self.name = name
        self.can_iface = can_iface
        self.can_id = can_id
        self.parsedata = parsedata

        if timestamps is None:
            self.timestamps = wallclock_timestamps_nosleep()
        else:
            self.timestamps = timestamps

    async def _run(self):
        can_socket = self._create_socket()

        while True:
            # cannot mix endiannesses in one single struct, so I have
            # to decompose the "data" part separately: (timestamp,
            # temperature) as little endian uint32

            frame = await asyncio.get_running_loop().sock_recv(can_socket, _FRAME_SIZE)
            frame_can_id, frame_can_dlc, frame_data = struct.unpack(_FRAME_LAYOUT, frame)

            if frame_can_id != self.can_id: # ignore foreign frames
                continue

            data = self.parsedata(frame_data[:frame_can_dlc])
            timestamp = next(self.timestamps)

            await self.sink.put(Sample(name=self.name, timestamp=timestamp, data=data))

    def _create_socket(self):
        s = socket.socket(socket.PF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
        s.bind((self.can_iface,))
        s.setblocking(False)
        
        return s

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
_DATA_LAYOUT = "<Ii"


class CANSource(Source):
    def __init__(self, name, can_iface, can_id, timestamps=None):
        super().__init__(name)

        self.name = name
        self.can_iface = can_iface
        self.can_id = can_id

        if timestamps is None:
            self.timestamps = wallclock_timestamps_nosleep
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

            timestamp_ms, temperature = struct.unpack(_DATA_LAYOUT, frame_data)
            temperature /= 1000

            # FIXME: we are overriding the timestamps from the
            # controller with the wall clock time that *we* see.
            my_own_timestamp = next(self.timestamps)

            await self.sink.put(Sample(name=self.name, timestamp=my_own_timestamp, temperature=temperature))

    def _create_socket(self):
        s = socket.socket(socket.PF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
        s.bind((self.can_iface,))
        s.setblocking(False)
        
        return s

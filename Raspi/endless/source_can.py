from .component import LifetimeComponent, receptacle
from .interfaces import Inlet
from .sample import Sample
from .async_util import wallclock_timestamps_nosleep

import socket
import struct
import sys
import asyncio
from datetime import datetime
from dataclasses import dataclass


_FRAME_LAYOUT = "=IB3x8s"
_FRAME_SIZE = struct.calcsize(_FRAME_LAYOUT)


@dataclass
class CANFrame:
    can_id: int
    payload: bytes

@receptacle('outlet', Inlet)
class CANSource(LifetimeComponent):
    def __init__(self, name, can_iface, can_id, timestamps=None):
        super().__init__(self._run)

        self.name = name
        self.can_iface = can_iface
        self.can_id = can_id

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

            timestamp = next(self.timestamps)

            await self._outlet.consume_sample(Sample(
                name=self.name,
                timestamp=timestamp, 
                data=CANFrame(
                    can_id=frame_can_id, 
                    payload=frame_data[:frame_can_dlc],
                ),
            ))

    def _create_socket(self):
        s = socket.socket(socket.PF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
        s.bind((self.can_iface,))
        s.setblocking(False)
        
        return s

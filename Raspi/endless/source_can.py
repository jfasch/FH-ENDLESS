from .sample import Sample

import asyncio
import socket
import struct
import sys


_FRAME_LAYOUT = "=IB3x8s"
_FRAME_SIZE = struct.calcsize(_FRAME_LAYOUT)
_DATA_LAYOUT = "<Ii"


class CANSource:
    def __init__(self, name, can_iface, can_id):
        self.name = name
        self.can_iface = can_iface
        self.can_id = can_id

        self.sink = None

    def start(self, sink, taskgroup):
        self.sink = sink
        taskgroup.create_task(self._run())

    async def _run(self):
        try:
            can_socket = socket.socket(socket.PF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
            can_socket.bind((self.can_iface,))
            can_socket.setblocking(False)

            while True:
                # cannot mix endiannesses in one single struct, so I have
                # to decompose the "data" part separately: (timestamp,
                # temperature) as little endian uint32

                frame = await asyncio.get_running_loop().sock_recv(can_socket, _FRAME_SIZE)
                frame_can_id, frame_can_dlc, frame_data = struct.unpack(_FRAME_LAYOUT, frame)

                if frame_can_id != self.can_id: # ignore foreign frames
                    continue

                timestamp_ms, temperature = struct.unpack(_DATA_LAYOUT, frame_data)

                await self.sink.put(Sample(name=self.name, timestamp_ms=timestamp_ms, temperature=temperature))

        except Exception as e:
            print(type(e), e, file=sys.stderr)    # jjj fix that: task exception handling!!!

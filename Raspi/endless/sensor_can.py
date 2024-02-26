import asyncio
import socket
import struct


class CANSensor:
    FRAME_LAYOUT = "=IB3x8s"
    FRAME_SIZE = struct.calcsize(FRAME_LAYOUT)

    DATA_LAYOUT = "<Ii"

    assert struct.calcsize(FRAME_LAYOUT) == 16
    assert struct.calcsize(DATA_LAYOUT) == 8

    def __init__(self, can_iface, can_id):
        self.can_socket = socket.socket(socket.PF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
        self.can_socket.bind((can_iface,))
        self.can_socket.setblocking(False)

        self.can_id = can_id

    async def iter(self):
        while True:
            # cannot mix endiannesses in one single struct, so I have
            # to decompose the "data" part separately: (timestamp,
            # temperature) as little endian uint32

            frame = await asyncio.get_running_loop().sock_recv(self.can_socket, self.FRAME_SIZE)
            can_id, can_dlc, data = struct.unpack(self.FRAME_LAYOUT, frame)

            if can_id != self.can_id: # ignore foreign frames
                continue

            timestamp, temperature = struct.unpack(self.DATA_LAYOUT, data)

            yield timestamp, temperature

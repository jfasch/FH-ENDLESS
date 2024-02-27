import asyncio
import socket
import struct


_FRAME_LAYOUT = "=IB3x8s"
_FRAME_SIZE = struct.calcsize(_FRAME_LAYOUT)
_DATA_LAYOUT = "<Ii"


async def source_can(queue, name, can_iface, can_id):
    can_socket = socket.socket(socket.PF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
    can_socket.bind((can_iface,))
    can_socket.setblocking(False)

    while True:
        # cannot mix endiannesses in one single struct, so I have
        # to decompose the "data" part separately: (timestamp,
        # temperature) as little endian uint32

        frame = await asyncio.get_running_loop().sock_recv(can_socket, _FRAME_SIZE)
        frame_can_id, frame_can_dlc, frame_data = struct.unpack(_FRAME_LAYOUT, frame)

        if frame_can_id != can_id: # ignore foreign frames
            continue

        timestamp_ms, temperature = struct.unpack(_DATA_LAYOUT, frame_data)

        await queue.put((name, timestamp_ms, temperature))

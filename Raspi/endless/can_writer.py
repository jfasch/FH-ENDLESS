from .component import Component
from .facet import facet
from .interfaces import CANOutputHandler
from . import can_util

import struct
import asyncio


@facet('frame_in', CANOutputHandler, (('write_frame', '_write_frame'),))
class CANWriter(Component):
    def __init__(self, can_iface):
        super().__init__()
        self.sock = can_util.create_socket(can_iface)

    async def _write_frame(self, can_id, payload):
        frame = struct.pack(can_util.FRAME_LAYOUT, can_id, len(payload), payload)
        await asyncio.get_running_loop().sock_sendall(self.sock, frame)

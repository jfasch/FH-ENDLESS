from .component import Component
from .facet import facet
from .interfaces import SampleInlet
from . import can_util

import struct
import asyncio


@facet('inlet', SampleInlet, (('consume_sample', '_write_frame'),))
class CANWriter(Component):
    def __init__(self, can_iface):
        super().__init__()
        self.sock = can_util.create_socket(can_iface)

    async def _write_frame(self, sample):
        frame = struct.pack(can_util.FRAME_LAYOUT, 
                            sample.data.can_id, len(sample.data.payload), sample.data.payload)
        await asyncio.get_running_loop().sock_sendall(self.sock, frame)

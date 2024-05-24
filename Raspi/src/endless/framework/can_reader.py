from .component import LifetimeComponent
from .receptacle import receptacle, ONE_OR_MANY
from .interfaces import CANInputHandler
from . import can_util

import socket
import struct
import sys
import asyncio
from datetime import datetime


@receptacle('frame_out', CANInputHandler, multiplicity=ONE_OR_MANY)
class CANReader(LifetimeComponent):
    def __init__(self, can_iface):
        super().__init__(self._run)
        self.can_iface = can_iface

    async def _run(self):
        can_socket = can_util.create_socket(self.can_iface)

        while True:
            frame = await asyncio.get_running_loop().sock_recv(can_socket, can_util.FRAME_SIZE)
            frame_can_id, frame_can_dlc, frame_data = struct.unpack(can_util.FRAME_LAYOUT, frame)

            await self._frame_out.handle_frame(frame_can_id, frame_data[:frame_can_dlc])

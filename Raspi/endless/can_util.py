from dataclasses import dataclass
import struct
import socket


FRAME_LAYOUT = "=IB3x8s"
FRAME_SIZE = struct.calcsize(FRAME_LAYOUT)

@dataclass
class CANFrame:
    can_id: int
    payload: bytes

def create_socket(can_iface):
    s = socket.socket(socket.PF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
    s.bind((can_iface,))
    s.setblocking(False)
    return s

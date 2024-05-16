from endless.facet import facet
from endless.receptacle import receptacle, ONE
from endless.component import Component
from endless.interfaces import Switch, Counter, CANOutputHandler

import struct


@facet('switch', Switch, (('set_state', '_set_state'),))
@facet('counter', Counter, (('get_count', '_get_counter'),))
@receptacle('frame_out', CANOutputHandler, multiplicity=ONE)
class CANSwitch(Component):
    '''Translates ``Switch`` operations into CAN frames.

    Facets:

    * ``switch`` to connect it to someone who might want to switch
      something
    * ``counter`` to see how often the switch has been operated
    
    Receptacles:

    * ``frame_out`` to send CAN frames to a CAN-writing component.

    '''
    DATA_LAYOUT = "????"      # 4 bytes/bools, 4 switches

    def __init__(self, can_id, number):
        super().__init__()
        self.can_id = can_id
        self.number = number
        self.switch_counter = 0

    async def _set_state(self, state):
        states = [0,0,0,0]
        states[self.number] = state

        payload = struct.pack(self.DATA_LAYOUT, *states)

        await self._frame_out.write_frame(
            can_id=self.can_id, 
            payload=struct.pack(self.DATA_LAYOUT, *states))

        self.switch_counter += 1

    async def _get_counter(self):
        return self.switch_counter

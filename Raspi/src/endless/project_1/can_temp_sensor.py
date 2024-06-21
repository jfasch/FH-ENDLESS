from endless.framework.component import Component
from endless.framework.facet import facet
from endless.framework.receptacle import receptacle, ONE
from endless.framework.interfaces import CANInputHandler, SampleInlet, Control
from endless.framework.sample import Sample
from endless.framework.async_util import wallclock_timestamps_nosleep

import struct


@facet('can_in', CANInputHandler, (('handle_frame', '_handle_frame'),))
@receptacle('sample_out', SampleInlet, multiplicity=ONE)
class CAN_TemperatureSensor(Component):
    PAYLOAD_FORMAT = '<q'

    def __init__(self, can_id, tag, timestamps=None):
        super().__init__()
        self.can_id = can_id
        self.tag = tag
        if timestamps is None:
            self.timestamps = iter(wallclock_timestamps_nosleep())
        else:
            self.timestamps = iter(timestamps)

    async def _handle_frame(self, can_id, payload):
        if can_id != self.can_id:
            return

        temperature, = struct.unpack(self.PAYLOAD_FORMAT, payload)
        timestamp = next(self.timestamps)

        await self._sample_out.consume_sample(
            Sample(
                tag=self.tag, 
                timestamp=timestamp,
                data=temperature/1000))


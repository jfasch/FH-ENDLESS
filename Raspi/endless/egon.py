from .component import Component
from .facet import facet
from .receptacle import receptacle, ONE
from .interfaces import CANInputHandler, SampleInlet, Switch, Control
from .sample import Sample
from .can_util import CANFrame
from .async_util import wallclock_timestamps_nosleep

from dataclasses import dataclass
from datetime import datetime
import struct
import json


@dataclass
class HumidityTemperature:
    humidity: float
    temperature: float

@facet('can_in', CANInputHandler, (('handle_frame', '_handle_frame'),))
@receptacle('sample_out', SampleInlet, multiplicity=ONE)
class HumidityTemperatureSensor(Component):
    PAYLOAD_FORMAT = '<iI'

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

        temperature, humidity = struct.unpack(self.PAYLOAD_FORMAT, payload)
        timestamp = next(self.timestamps)

        await self._sample_out.consume_sample(
            Sample(
                tag=self.tag, 
                timestamp=timestamp,
                data=HumidityTemperature(
                    temperature=temperature/10, 
                    humidity=humidity/10,
                )))

def transform_hum_temp_to_json(sample):
    json_pydict = {
        'humidity': sample.data.humidity,
        'temperature': sample.data.temperature,
    }
    json_str = json.dumps(json_pydict)
    json_bytes = bytes(json_str, encoding='ascii')

    return Sample(tag=sample.tag,
                  timestamp=sample.timestamp,
                  data=json_bytes
                  )

@facet('sample_in', SampleInlet, (('consume_sample', '_consume_sample'),))
@receptacle('control', Control, multiplicity=ONE)
class HumidityTemperature2Control(Component):
    async def _consume_sample(self, sample):
        await self._control.adapt(timestamp=sample.timestamp, value=sample.data.temperature)

def transform_hum_temp_to_temp(sample):
    return Sample(tag=sample.tag,
                  timestamp=sample.timestamp,
                  data=sample.data.temperature,
                  )

@facet('switch', Switch, (('set_state', '_set_state'),))
@receptacle('sample_out', SampleInlet, multiplicity=ONE)
class CANSwitch(Component):
    DATA_LAYOUT = "<II"  # (le uint32_t number, le uint32_t state)

    def __init__(self, can_id, number):
        super().__init__()
        self.can_id = can_id
        self.number = number

    async def _set_state(self, state):
        frame = CANFrame(can_id = self.can_id, payload = struct.pack(self.DATA_LAYOUT, self.number, state))
        await self._sample_out.consume_sample(
            Sample(tag='irrelevant', # crap: https://www.faschingbauer.me/trainings/material/soup/cxx-design-patterns/oo-principles.html#interface-segregation
                   timestamp=datetime.now(), # crap: https://www.faschingbauer.me/trainings/material/soup/cxx-design-patterns/oo-principles.html#interface-segregation
                   data=frame,
                   )
        )

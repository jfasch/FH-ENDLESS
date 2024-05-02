from .component import Component
from .facet import facet
from .receptacle import receptacle, ONE
from .interfaces import SampleInlet, Switch
from .sample import Sample
from .can_util import CANFrame

from dataclasses import dataclass
from datetime import datetime
import struct
import json


@dataclass
class HumidityTemperature:
    humidity: float
    temperature: float

def transform_can_frame_to_hum_temp(sample):
    _FORMAT = '<iI'
    temperature, humidity = struct.unpack(_FORMAT, sample.data.payload)

    return Sample(
        tag=sample.tag, 
        timestamp=sample.timestamp, 
        data=HumidityTemperature(
            temperature=temperature/10, 
            humidity=humidity/10,
        )
    )

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

def transform_hum_temp_to_temp(sample):
    return Sample(tag=sample.tag,
                  timestamp=sample.timestamp,
                  data=sample.data.temperature,
                  )

@facet('switch', Switch, (('set_state', '_set_state'),))
@receptacle('outlet', SampleInlet, multiplicity=ONE)
class CANSwitch(Component):
    DATA_LAYOUT = "<II"  # (le uint32_t number, le uint32_t state)

    def __init__(self, can_id, number):
        super().__init__()
        self.can_id = can_id
        self.number = number

    async def _set_state(self, state):
        frame = CANFrame(can_id = self.can_id, payload = struct.pack(self.DATA_LAYOUT, self.number, state))
        await self._outlet.consume_sample(
            Sample(tag='irrelevant', # crap: https://www.faschingbauer.me/trainings/material/soup/cxx-design-patterns/oo-principles.html#interface-segregation
                   timestamp=datetime.now(), # crap: https://www.faschingbauer.me/trainings/material/soup/cxx-design-patterns/oo-principles.html#interface-segregation
                   data=frame,
                   )
        )

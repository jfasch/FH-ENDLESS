from endless.component import Component
from endless.facet import facet
from endless.receptacle import receptacle, ONE
from endless.interfaces import CANInputHandler, CANOutputHandler, SampleInlet, Switch, Control, Counter
from endless.sample import Sample
from endless.can_util import CANFrame
from endless.async_util import wallclock_timestamps_nosleep

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
@facet('counter', Counter, (('get_count', '_get_counter'),))
@receptacle('frame_out', CANOutputHandler, multiplicity=ONE)
class CANSwitch(Component):
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

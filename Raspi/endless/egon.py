from .component import Component, facet, receptacle
from .interfaces import Inlet
from .sample import Sample

from dataclasses import dataclass
import struct
import json


@dataclass
class HumidityTemperature:
    humidity: float
    temperature: float

@facet('inlet', Inlet, (('consume_sample', '_transform_can_frame_to_hum_temp'),))
@receptacle('outlet', Inlet)
class CANFrameToHumidityTemperatureConverter(Component):
    async def _transform_can_frame_to_hum_temp(self, sample: Sample):
        _FORMAT = '<iI'
        temperature, humidity = struct.unpack(_FORMAT, sample.data.payload)

        await self._outlet.consume_sample(
            Sample(
                name=sample.name, 
                timestamp=sample.timestamp, 
                data=HumidityTemperature(
                    temperature=temperature/10, 
                    humidity=humidity/10,
                )
            )
        )

@facet('inlet', Inlet, (('consume_sample', '_transform_hum_temp_to_json'),))
@receptacle('outlet', Inlet)
class HumidityTemperatureToJSonConverter(Component):
    async def _transform_hum_temp_to_json(self, sample: Sample):
        json_pydict = {
            'humidity': sample.data.humidity,
            'temperature': sample.data.temperature,
        }
        json_str = json.dumps(json_pydict)
        json_bytes = bytes(json_str, encoding='ascii')

        await self._outlet.consume_sample(
            Sample(name=sample.name,
                   timestamp=sample.timestamp,
                   data=json_bytes
                   )
        )

@facet('inlet', Inlet, (('consume_sample', '_transform_hum_temp_to_temp'),))
@receptacle('outlet', Inlet)
class HumidityTemperatureToTemperatureConverter(Component):
    async def _transform_hum_temp_to_temp(self, sample: Sample):
        await self._outlet.consume_sample(
            Sample(name=sample.name,
                   timestamp=sample.timestamp,
                   data=sample.data.temperature,
                   )
        )


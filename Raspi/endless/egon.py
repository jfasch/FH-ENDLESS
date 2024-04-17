from .component import Component, facet, receptacle
from .interfaces import Inlet
from .sample import Sample

from dataclasses import dataclass
import struct
import json


@facet('can_input', Inlet, (('consume_sample', '_transform_can_frame_to_hum_temp'),))
@facet('hum_temp_input', Inlet, (('consume_sample', '_transform_hum_temp_to_json'),))
@receptacle('hum_temp_output', Inlet)
@receptacle('json_output', Inlet)
class Egon(Component):
    @dataclass
    class HumidityTemperature:
        humidity: float
        temperature: float

    async def _transform_can_frame_to_hum_temp(self, sample: Sample):
        _FORMAT = '<iI'
        temperature, humidity = struct.unpack(_FORMAT, sample.data.payload)

        await self._hum_temp_output.consume_sample(
            Sample(
                name=sample.name, 
                timestamp=sample.timestamp, 
                data=self.HumidityTemperature(
                    temperature=temperature/10, 
                    humidity=humidity/10,
                )
            )
        )

    async def _transform_hum_temp_to_json(self, sample: Sample):
        json_pydict = {
            'humidity': sample.data.humidity,
            'temperature': sample.data.temperature,
        }
        json_str = json.dumps(json_pydict)
        json_bytes = bytes(json_str, encoding='ascii')

        await self._json_output.consume_sample(
            Sample(name=sample.name,
                   timestamp=sample.timestamp,
                   data=json_bytes
                   )
        )

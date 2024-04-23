from .component import Component
from .facet import facet
from .receptacle import receptacle
from .interfaces import Inlet
from .sample import Sample

from dataclasses import dataclass
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
        name=sample.name, 
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

    return Sample(name=sample.name,
                  timestamp=sample.timestamp,
                  data=json_bytes
                  )

def transform_hum_temp_to_temp(sample):
    return Sample(name=sample.name,
                  timestamp=sample.timestamp,
                  data=sample.data.temperature,
                  )


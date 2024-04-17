from endless.egon import Egon
from endless.sample import Sample
from endless.source_can import CANFrame
from endless.interfaces import Inlet

import pytest
from datetime import datetime
import struct
import json


@pytest.mark.asyncio
async def test_egons_canframe_to_egons_humidity_temperature():
    class MySampleConsumer(Inlet):
        async def consume_sample(self, sample: Sample):
            self.sample = sample

    consumer = MySampleConsumer()
    egon = Egon()

    egon.hum_temp_output.connect(consumer)

    # inject can-frame sample, as if produced by the raw CAN reader
    await egon.can_input.consume_sample(
        Sample(
            name='name', 
            timestamp=datetime(2024, 4, 17, 16, 5), 
            data=CANFrame(
                can_id=0x42, 
                payload=struct.pack('<iI', 
                                    425, # 42.5
                                    714, # 71.4
                                    ),
            ),
        )
    )

    assert consumer.sample.name == 'name'
    assert consumer.sample.timestamp == datetime(2024, 4, 17, 16, 5)
    assert consumer.sample.data.temperature == pytest.approx(42.5)
    assert consumer.sample.data.humidity == pytest.approx(71.4)

@pytest.mark.asyncio
async def test_egons_humidity_temperature_to_egons_mqtt_payload():
    class MySampleConsumer(Inlet):
        async def consume_sample(self, sample):
            self.sample = sample

    consumer = MySampleConsumer()
    egon = Egon()
    
    egon.json_output.connect(consumer)

    # inject a humidity/temperature sample
    await egon.hum_temp_input.consume_sample(
        Sample(
            name='name',
            timestamp=datetime(2024, 4, 17, 17, 6),
            data=Egon.HumidityTemperature(
                humidity=23.3,
                temperature=37.5,
            ),
        )
    )

    assert consumer.sample.name == 'name'
    assert consumer.sample.timestamp == datetime(2024, 4, 17, 17, 6)
    assert type(consumer.sample.data) is bytes

    json_structure = json.loads(consumer.sample.data)
    assert len(json_structure) == 2
    assert json_structure['humidity'] == pytest.approx(23.3)
    assert json_structure['temperature'] == pytest.approx(37.5)

from endless import egon
from endless.sample import Sample
from endless.sample_converter import SampleConverter
from endless.can_util import CANFrame
from endless.interfaces import Inlet

import pytest
from datetime import datetime
import struct
import json


@pytest.mark.asyncio
async def test_canframe_to_humtemp():
    class MySampleConsumer(Inlet):
        async def consume_sample(self, sample: Sample):
            self.sample = sample

    humtemp_consumer = MySampleConsumer()
    can2humtemp = SampleConverter(egon.transform_can_frame_to_hum_temp)

    can2humtemp.outlet.connect(humtemp_consumer)

    # inject can-frame sample, as if produced by the raw CAN reader
    await can2humtemp.inlet.consume_sample(
        Sample(
            tag='name', 
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

    assert humtemp_consumer.sample.tag == 'name'
    assert humtemp_consumer.sample.timestamp == datetime(2024, 4, 17, 16, 5)
    assert humtemp_consumer.sample.data.temperature == pytest.approx(42.5)
    assert humtemp_consumer.sample.data.humidity == pytest.approx(71.4)

@pytest.mark.asyncio
async def test_humtemp_to_json():
    class MyJSONConsumer(Inlet):
        async def consume_sample(self, sample):
            self.sample = sample

    json_consumer = MyJSONConsumer()
    humtemp2json = SampleConverter(egon.transform_hum_temp_to_json)
    
    humtemp2json.outlet.connect(json_consumer)

    # inject a humidity/temperature sample
    await humtemp2json.inlet.consume_sample(
        Sample(
            tag='name',
            timestamp=datetime(2024, 4, 17, 17, 6),
            data=egon.HumidityTemperature(
                humidity=23.3,
                temperature=37.5,
            ),
        )
    )

    assert json_consumer.sample.tag == 'name'
    assert json_consumer.sample.timestamp == datetime(2024, 4, 17, 17, 6)
    assert type(json_consumer.sample.data) is bytes

    json_structure = json.loads(json_consumer.sample.data)
    assert len(json_structure) == 2
    assert json_structure['humidity'] == pytest.approx(23.3)
    assert json_structure['temperature'] == pytest.approx(37.5)

@pytest.mark.asyncio
async def test_humtemp_to_temp():
    class MyTemperatureConsumer(Inlet):
        async def consume_sample(self, sample):
            self.sample = sample

    temp_consumer = MyTemperatureConsumer()
    humtemp2temp = SampleConverter(egon.transform_hum_temp_to_temp)
    
    humtemp2temp.outlet.connect(temp_consumer)

    # inject a humidity/temperature sample
    await humtemp2temp.inlet.consume_sample(
        Sample(
            tag='name',
            timestamp=datetime(2024, 4, 17, 17, 6),
            data=egon.HumidityTemperature(
                humidity=23.3,
                temperature=37.5,
            ),
        )
    )

    assert temp_consumer.sample.tag == 'name'
    assert temp_consumer.sample.timestamp == datetime(2024, 4, 17, 17, 6)
    assert temp_consumer.sample.data == pytest.approx(37.5)

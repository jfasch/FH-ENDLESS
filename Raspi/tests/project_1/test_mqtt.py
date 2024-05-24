from endless.project_1.mqtt_helper import transform_hum_temp_to_json
from endless.project_1.types import HumidityTemperature

from endless.framework.interfaces import SampleInlet
from endless.framework.sample_filter import SampleFilter
from endless.framework.sample import Sample

import pytest
from datetime import datetime
import json


@pytest.mark.asyncio
async def test_humtemp_to_json():
    class MyJSONConsumer(SampleInlet):
        async def consume_sample(self, sample):
            self.sample = sample

    json_consumer = MyJSONConsumer()
    humtemp2json = SampleFilter(transform_hum_temp_to_json)
    
    humtemp2json.sample_out.connect(json_consumer)

    # inject a humidity/temperature sample
    await humtemp2json.sample_in.consume_sample(
        Sample(
            tag='name',
            timestamp=datetime(2024, 4, 17, 17, 6),
            data=HumidityTemperature(
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

from endless.sample_converter import SampleConverter
from endless.sample import Sample
from endless.interfaces import Inlet

import pytest
from datetime import datetime, timedelta


@pytest.mark.asyncio
async def test_basic():
    def funky_convert(sample):
        return Sample(
            name = 'newname',
            timestamp = sample.timestamp + timedelta(seconds=1),
            data = sample.data + 1
        )
    converter = SampleConverter(funky_convert)

    class MyConsumer(Inlet):
        async def consume_sample(self, sample):
            self.sample = sample

    consumer = MyConsumer()
    converter.outlet.connect(consumer)

    await converter.inlet.consume_sample(
        Sample(name='name',
               timestamp=datetime(2024, 4, 23, 8, 20),
               data=42
               )
    )

    assert consumer.sample.name == 'newname'
    assert consumer.sample.timestamp == datetime(2024, 4, 23, 8, 20, 1)
    assert consumer.sample.data == 43
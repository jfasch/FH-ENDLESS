from endless.sample_converter import SampleConverter
from endless.sample import Sample
from endless.interfaces import SampleInlet

import pytest
from datetime import datetime, timedelta


@pytest.mark.asyncio
async def test_basic():
    def funky_convert(sample):
        return Sample(
            tag = 'newname',
            timestamp = sample.timestamp + timedelta(seconds=1),
            data = sample.data + 1
        )
    converter = SampleConverter(funky_convert)

    class MyConsumer(SampleInlet):
        async def consume_sample(self, sample):
            self.sample = sample

    consumer = MyConsumer()
    converter.sample_out.connect(consumer)

    await converter.sample_in.consume_sample(
        Sample(tag='name',
               timestamp=datetime(2024, 4, 23, 8, 20),
               data=42
               )
    )

    assert consumer.sample.tag == 'newname'
    assert consumer.sample.timestamp == datetime(2024, 4, 23, 8, 20, 1)
    assert consumer.sample.data == 43

from endless.sample_filter import SampleFilter
from endless.sample import Sample
from endless.interfaces import SampleInlet

import pytest
from datetime import datetime, timedelta


@pytest.mark.asyncio
async def test_drop_and_accept():
    class MyConsumer(SampleInlet):
        async def consume_sample(self, sample):
            self.sample = sample

    consumer = MyConsumer()

    def accept_good(sample):
        if sample.tag == 'tag-good':
            return sample    # <--- accept
        return None          # <--- drop

    flt = SampleFilter(accept_good)
    flt.sample_out.connect(consumer)

    await flt.sample_in.consume_sample(
        Sample(
            tag='tag-good',
            timestamp=datetime(2024, 4, 18, 18, 52),
            data=42))

    assert consumer.sample.tag == 'tag-good'
    assert consumer.sample.timestamp == datetime(2024, 4, 18, 18, 52)
    assert consumer.sample.data == 42

    consumer.sample = None

    await flt.sample_in.consume_sample(
        Sample(
            tag='tag-bad',
            timestamp=datetime(2024, 4, 18, 18, 52),
            data=42))

    assert consumer.sample is None

@pytest.mark.asyncio
async def test_convert():
    def funky_convert(sample):
        return Sample(
            tag = 'newname',
            timestamp = sample.timestamp + timedelta(seconds=1),
            data = sample.data + 1
        )
    converter = SampleFilter(funky_convert)

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

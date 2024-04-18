from endless.filter import TagFilter
from endless.sample import Sample
from endless.interfaces import Inlet

import pytest
from datetime import datetime


@pytest.mark.asyncio
async def test_basic():
    class MyConsumer(Inlet):
        async def consume_sample(self, sample):
            self.sample = sample

    consumer = MyConsumer()
    filter = TagFilter('tag-good')

    filter.outlet.connect(consumer)

    await filter.inlet.consume_sample(
        Sample(
            name='tag-good',
            timestamp=datetime(2024, 4, 18, 18, 52),
            data=42))

    assert consumer.sample.name == 'tag-good'
    assert consumer.sample.timestamp == datetime(2024, 4, 18, 18, 52)
    assert consumer.sample.data == 42

    consumer.sample = None

    await filter.inlet.consume_sample(
        Sample(
            name='tag-bad',
            timestamp=datetime(2024, 4, 18, 18, 52),
            data=42))

    assert consumer.sample is None

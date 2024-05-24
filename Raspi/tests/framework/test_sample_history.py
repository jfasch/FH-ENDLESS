from endless.framework.sample_history import SampleHistory
from endless.framework.sample import Sample
from endless.framework.interfaces import SampleInlet

import pytest
from datetime import datetime, timedelta


@pytest.mark.asyncio
async def test_basic():
    class MyConsumer(SampleInlet):
        def __init__(self):
            self.samples = []
        async def consume_sample(self, sample):
            self.samples.append(sample)

    hist = SampleHistory(size=2)
    consumer = MyConsumer()
    hist.sample_out.connect(consumer)

    await hist.sample_in.consume_sample(
        Sample(
            tag='some-tag',
            timestamp=datetime(2024, 5, 24, 9, 47),
            data=42))
    await hist.sample_in.consume_sample(
        Sample(
            tag='some-other-tag',
            timestamp=datetime(2024, 5, 24, 9, 48),
            data=666))

    hist_samples = await hist.sample_list.get_samples()
    assert len(hist_samples) == 2
    assert hist_samples[0].tag == 'some-tag'
    assert hist_samples[0].timestamp == datetime(2024, 5, 24, 9, 47)
    assert hist_samples[0].data == 42
    assert hist_samples[1].tag == 'some-other-tag'
    assert hist_samples[1].timestamp == datetime(2024, 5, 24, 9, 48)
    assert hist_samples[1].data == 666

    assert len(consumer.samples) == 2
    assert consumer.samples[0].tag == 'some-tag'
    assert consumer.samples[0].timestamp == datetime(2024, 5, 24, 9, 47)
    assert consumer.samples[0].data == 42
    assert consumer.samples[1].tag == 'some-other-tag'
    assert consumer.samples[1].timestamp == datetime(2024, 5, 24, 9, 48)
    assert consumer.samples[1].data == 666


    # add 3rd sample. hist.size is 2, so [0] is shifted out.

    await hist.sample_in.consume_sample(
        Sample(
            tag='yet-another-tag',
            timestamp=datetime(2024, 5, 24, 9, 51),
            data=7))

    assert len(hist.samples) == 2
    assert hist.samples[0].tag == 'some-other-tag'
    assert hist.samples[0].timestamp == datetime(2024, 5, 24, 9, 48)
    assert hist.samples[0].data == 666
    assert hist.samples[1].tag == 'yet-another-tag'
    assert hist.samples[1].timestamp == datetime(2024, 5, 24, 9, 51)
    assert hist.samples[1].data == 7

    assert len(consumer.samples) == 3
    assert consumer.samples[0].tag == 'some-tag'
    assert consumer.samples[0].timestamp == datetime(2024, 5, 24, 9, 47)
    assert consumer.samples[0].data == 42
    assert consumer.samples[1].tag == 'some-other-tag'
    assert consumer.samples[1].timestamp == datetime(2024, 5, 24, 9, 48)
    assert consumer.samples[1].data == 666
    assert consumer.samples[2].tag == 'yet-another-tag'
    assert consumer.samples[2].timestamp == datetime(2024, 5, 24, 9, 51)
    assert consumer.samples[2].data == 7


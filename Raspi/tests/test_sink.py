from endless.sink import Sink
from endless.sink_mock import MockSink, have_n_samples
from endless.sample import Sample
from endless.runner import Runner

import pytest
from datetime import datetime


@pytest.mark.asyncio
async def test_basic():
    have_2, cond = have_n_samples(2)
    sink = MockSink(cond)

    async with Runner(sources=(), sinks=[sink]) as runner:
        await sink.put(Sample(name='name1', timestamp=datetime(2024, 3, 14, 8, 46), data=42.666))
        await sink.put(Sample(name='name2', timestamp=datetime(2024, 3, 14, 8, 47), data=-273.15))

        await have_2
        runner.stop()

    assert sink.samples[0].name == 'name1'
    assert sink.samples[0].timestamp == datetime(2024, 3, 14, 8, 46)
    assert sink.samples[0].data == pytest.approx(42.666)

    assert sink.samples[1].name == 'name2'
    assert sink.samples[1].timestamp == datetime(2024, 3, 14, 8, 47)
    assert sink.samples[1].data == pytest.approx(-273.15)

def test_is_a_sink():
    assert issubclass(MockSink, Sink)


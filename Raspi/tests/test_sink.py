from endless.sink import Sink
from endless.sink_mock import MockSink, have_n_samples
from endless.sample import Sample

import pytest
import asyncio
from datetime import datetime


@pytest.mark.asyncio
async def test_basic():
    async with asyncio.TaskGroup() as tg:
        have_2, cond = have_n_samples(2)
        sink = MockSink(cond)
        sink.start(tg)

        await sink.put(Sample(name='name1', timestamp=datetime(2024, 3, 14, 8, 46), temperature=42.666))
        await sink.put(Sample(name='name2', timestamp=datetime(2024, 3, 14, 8, 47), temperature=-273.15))

        await have_2

        assert sink.samples[0] == Sample('name1', datetime(2024, 3, 14, 8, 46), pytest.approx(42.666))
        assert sink.samples[1] == Sample('name2', datetime(2024, 3, 14, 8, 47), pytest.approx(-273.15))

        sink.stop()


def test_is_a_sink():
    assert issubclass(MockSink, Sink)


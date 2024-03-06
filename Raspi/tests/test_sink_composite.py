from endless.sink_mock import MockSink, have_n_samples
from endless.sink_composite import CompositeSink
from endless.sample import Sample

import pytest
import asyncio


@pytest.mark.asyncio
async def test_basic():
    async with asyncio.TaskGroup() as tg:
        (have_1_1, cond1), (have_1_2, cond2) = have_n_samples(1), have_n_samples(1)

        sink1, sink2 = MockSink(cond1), MockSink(cond2)
        compsink = CompositeSink([sink1, sink2])
        compsink.start(tg)

        await compsink.put(Sample(name='name', timestamp_ms=200, temperature=42.666))

        await have_1_1
        await have_1_2

        assert sink1.samples[0] == Sample(name='name', timestamp_ms=200, temperature=pytest.approx(42.666))
        assert sink2.samples[0] == Sample(name='name', timestamp_ms=200, temperature=pytest.approx(42.666))

        compsink.stop()

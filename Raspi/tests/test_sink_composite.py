from endless.sink_mock import MockSink, have_n_samples
from endless.sink_composite import CompositeSink
from endless.sample import Sample
from endless.runner import Runner

import pytest
from datetime import datetime


@pytest.mark.asyncio
async def test_basic():
    (have_1_1, cond1), (have_1_2, cond2) = have_n_samples(1), have_n_samples(1)

    sink1, sink2 = MockSink(cond1), MockSink(cond2)
    compsink = CompositeSink([sink1, sink2])

    async with Runner(sources=(), sinks=[compsink]) as runner:
        await compsink.put(Sample(name='name', timestamp=datetime(2024, 3, 14, 8, 46), data=42.666))

        await have_1_1
        await have_1_2

        runner.stop()

    assert sink1.samples[0].name == 'name'
    assert sink1.samples[0].timestamp == datetime(2024, 3, 14, 8, 46)
    assert sink1.samples[0].data == pytest.approx(42.666)

    assert sink2.samples[0].name == 'name'
    assert sink2.samples[0].timestamp == datetime(2024, 3, 14, 8, 46)
    assert sink2.samples[0].data == pytest.approx(42.666)

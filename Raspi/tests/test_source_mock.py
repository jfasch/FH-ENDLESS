from endless.sample import Sample
from endless.source_mock import MockSource
from endless.sink_mock import MockSink, have_n_samples
from endless.runner import Runner
from endless import async_util

import pytest
from datetime import datetime, timedelta


@pytest.mark.asyncio
async def test_basic():
    have_5, cond = have_n_samples(5)
    sink = MockSink(cond)
    source = MockSource(
        'mock',
        timestamps=async_util.mock_timestamps_async(start=datetime(2024, 3, 14, 8, 46), interval=timedelta(milliseconds=10)), 
        temperature=37.5)
    source.connect(sink)

    async with Runner(sources=[source], sinks=[sink]) as runner:
        await have_5
        runner.stop()

    assert sink.samples[0] == Sample(name="mock",
                                     timestamp=datetime(2024, 3, 14, 8, 46)+timedelta(milliseconds=0*10),
                                     temperature=pytest.approx(37.5))
    assert sink.samples[1] == Sample(name="mock", 
                                     timestamp=datetime(2024, 3, 14, 8, 46)+timedelta(milliseconds=1*10), 
                                     temperature=pytest.approx(37.5))
    assert sink.samples[2] == Sample(name="mock", 
                                     timestamp=datetime(2024, 3, 14, 8, 46)+timedelta(milliseconds=2*10), 
                                     temperature=pytest.approx(37.5))
    assert sink.samples[3] == Sample(name="mock", 
                                     timestamp=datetime(2024, 3, 14, 8, 46)+timedelta(milliseconds=3*10), 
                                     temperature=pytest.approx(37.5))
    assert sink.samples[4] == Sample(name="mock", 
                                     timestamp=datetime(2024, 3, 14, 8, 46)+timedelta(milliseconds=4*10), 
                                     temperature=pytest.approx(37.5))

@pytest.mark.asyncio
async def test_value_is_function_of_timestamp():
    import math
    def myfunc(ts): 
        return math.sin(ts.timestamp())

    have_1, cond = have_n_samples(1)
    sink = MockSink(cond)
    source = MockSource('mock',
                        timestamps=async_util.mock_timestamps_async(start=datetime(2024, 3, 14, 8, 46), interval=timedelta(milliseconds=10)), 
                        temperature=myfunc)
    source.connect(sink)

    async with Runner(sources=[source], sinks=[sink]) as runner:
        await have_1
        runner.stop()

    assert sink.samples[0] == Sample(name="mock",
                                     timestamp=datetime(2024, 3, 14, 8, 46),
                                     temperature=pytest.approx(math.sin(datetime(2024, 3, 14, 8, 46).timestamp())),
                                     )

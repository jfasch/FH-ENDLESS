from endless.framework.sample import Sample
from endless.framework.source_mock import MockSource
from endless.framework.sample_receiver import SampleReceiver, have_n_samples
from endless.framework.runner import Runner, StopRunning
from endless.framework import async_util

import pytest
from datetime import datetime, timedelta


@pytest.mark.asyncio
async def test_basic():
    have_5, cond = have_n_samples(5)
    sink = SampleReceiver(cond)
    source = MockSource(
        'mock',
        timestamps=async_util.mock_timestamps_async(start=datetime(2024, 3, 14, 8, 46), interval=timedelta(milliseconds=10)), 
        data=37.5)
    source.sample_out.connect(sink.sample_in)

    async with Runner((source,sink)) as runner:
        await have_5
        raise StopRunning

    assert sink.collected_samples[0].tag == "mock"
    assert sink.collected_samples[0].timestamp == datetime(2024, 3, 14, 8, 46)+timedelta(milliseconds=0*10)
    assert sink.collected_samples[0].data == pytest.approx(37.5)

    assert sink.collected_samples[1].tag == "mock"
    assert sink.collected_samples[1].timestamp == datetime(2024, 3, 14, 8, 46)+timedelta(milliseconds=1*10)
    assert sink.collected_samples[1].data == pytest.approx(37.5)

    assert sink.collected_samples[2].tag == "mock"
    assert sink.collected_samples[2].timestamp == datetime(2024, 3, 14, 8, 46)+timedelta(milliseconds=2*10)
    assert sink.collected_samples[2].data == pytest.approx(37.5)

    assert sink.collected_samples[3].tag == "mock"
    assert sink.collected_samples[3].timestamp == datetime(2024, 3, 14, 8, 46)+timedelta(milliseconds=3*10)
    assert sink.collected_samples[3].data == pytest.approx(37.5)

    assert sink.collected_samples[4].tag == "mock"
    assert sink.collected_samples[4].timestamp == datetime(2024, 3, 14, 8, 46)+timedelta(milliseconds=4*10)
    assert sink.collected_samples[4].data == pytest.approx(37.5)

@pytest.mark.asyncio
async def test_data_is_function_of_timestamp():
    import math
    def myfunc(ts): 
        return math.sin(ts.timestamp())

    have_1, cond = have_n_samples(1)
    sink = SampleReceiver(cond)
    source = MockSource('mock',
                        timestamps=async_util.mock_timestamps_async(start=datetime(2024, 3, 14, 8, 46), interval=timedelta(milliseconds=10)), 
                        data=myfunc)
    source.sample_out.connect(sink.sample_in)

    async with Runner((source, sink)) as runner:
        await have_1
        raise StopRunning

    assert sink.collected_samples[0].tag == "mock"
    assert sink.collected_samples[0].timestamp == datetime(2024, 3, 14, 8, 46)
    assert sink.collected_samples[0].data == pytest.approx(math.sin(datetime(2024, 3, 14, 8, 46).timestamp()))

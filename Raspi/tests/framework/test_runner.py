from endless.framework.source_mock import MockSource
from endless.framework.sample_receiver import SampleReceiver, have_n_samples
from endless.framework.runner import Runner, StopRunning
from endless.framework.async_util import mock_timestamps_async
from endless.framework.sample import Sample

import pytest
import asyncio
from datetime import datetime, timedelta


@pytest.mark.asyncio
async def test_basic():
    source = MockSource(
        tag='source', 
        timestamps=mock_timestamps_async(start=datetime(2024, 3, 20, 10, 56), interval=timedelta(seconds=3)), 
        data=36.5)

    have_1, cond = have_n_samples(1)
    sink = SampleReceiver(cond=cond)

    source.sample_out.connect(sink.sample_in)

    async with Runner((source,sink)):
        await have_1
        raise StopRunning

    assert sink.collected_samples[0].tag == 'source'
    assert sink.collected_samples[0].timestamp == datetime(2024, 3, 20, 10, 56)
    assert sink.collected_samples[0].data == pytest.approx(36.5)

@pytest.mark.asyncio
async def test_m_to_n():
    source1 = MockSource(
        tag='source1', 
        timestamps=mock_timestamps_async(start=datetime(2024, 3, 20, 12, 51), interval=timedelta(seconds=3)), 
        data=36.5)
    have1_1, cond1 = have_n_samples(1)
    sink1 = SampleReceiver(cond=cond1)
    source1.sample_out.connect(sink1.sample_in)

    source2 = MockSource(
        tag='source2', 
        timestamps=mock_timestamps_async(start=datetime(2024, 3, 20, 12, 52), interval=timedelta(seconds=3)), 
        data=0.5)
    have2_1, cond2 = have_n_samples(1)
    sink2 = SampleReceiver(cond=cond2)
    source2.sample_out.connect(sink2.sample_in)
    
    async with Runner((source1, source2, sink1, sink2),):
        await have1_1
        await have2_1
        raise StopRunning

    assert sink1.collected_samples[0].tag == 'source1'
    assert sink1.collected_samples[0].timestamp == datetime(2024, 3, 20, 12, 51)
    assert sink1.collected_samples[0].data == pytest.approx(36.5)

    assert sink2.collected_samples[0].tag == 'source2'
    assert sink2.collected_samples[0].timestamp == datetime(2024, 3, 20, 12, 52)
    assert sink2.collected_samples[0].data == pytest.approx(0.5)


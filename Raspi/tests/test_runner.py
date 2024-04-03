from endless.source_mock import MockSource
from endless.sink_mock import MockSink, have_n_samples
from endless.runner import Runner, SourceNotConnected
from endless.async_util import mock_timestamps_async
from endless.sample import Sample

import pytest
import asyncio
from datetime import datetime, timedelta


@pytest.mark.asyncio
async def test_basic():
    source = MockSource(
        name='source', 
        timestamps=mock_timestamps_async(start=datetime(2024, 3, 20, 10, 56), interval=timedelta(seconds=3)), 
        data=36.5)

    have_1, cond = have_n_samples(1)
    sink = MockSink(cond=cond)

    source.connect(sink)

    async with Runner(sources=[source], sinks=[sink]) as runner:
        await have_1
        runner.stop()

    assert source.task is None
    assert sink.task is None

    assert sink.samples[0].name == 'source'
    assert sink.samples[0].timestamp == datetime(2024, 3, 20, 10, 56)
    assert sink.samples[0].data == pytest.approx(36.5)

@pytest.mark.asyncio
async def test_m_to_n():
    source1 = MockSource(
        name='source1', 
        timestamps=mock_timestamps_async(start=datetime(2024, 3, 20, 12, 51), interval=timedelta(seconds=3)), 
        data=36.5)
    have1_1, cond1 = have_n_samples(1)
    sink1 = MockSink(cond=cond1)
    source1.connect(sink1)

    source2 = MockSource(
        name='source2', 
        timestamps=mock_timestamps_async(start=datetime(2024, 3, 20, 12, 52), interval=timedelta(seconds=3)), 
        data=0.5)
    have2_1, cond2 = have_n_samples(1)
    sink2 = MockSink(cond=cond2)
    source2.connect(sink2)
    
    async with Runner(sources=(source1, source2), sinks=(sink1, sink2)) as runner:
        await have1_1
        await have2_1
        runner.stop()

    assert sink1.samples[0].name == 'source1'
    assert sink1.samples[0].timestamp == datetime(2024, 3, 20, 12, 51)
    assert sink1.samples[0].data == pytest.approx(36.5)

    assert sink2.samples[0].name == 'source2'
    assert sink2.samples[0].timestamp == datetime(2024, 3, 20, 12, 52)
    assert sink2.samples[0].data == pytest.approx(0.5)

@pytest.mark.asyncio
async def test_source_not_connected():
    source = MockSource(
        name='source', 
        timestamps=mock_timestamps_async(start=datetime(2024, 3, 20, 12, 51), interval=timedelta(seconds=3)), 
        data=36.5)

    with pytest.raises(SourceNotConnected):
        async with Runner(sources=(source,), sinks=()):
            pass

from endless.source_mock import MockSource
from endless.sink_mock import MockSink, have_n_samples
from endless.runner import Runner
from endless.async_util import mock_timestamps_async

import pytest
from datetime import datetime, timedelta


@pytest.mark.asyncio
async def test_basic():
    source = MockSource(
        name='source', 
        timestamps=mock_timestamps_async(start=datetime(2024, 4, 12, 9, 19), interval=timedelta(seconds=3)), 
        data=36.5)

    have_1, cond = have_n_samples(1)
    sink = MockSink(cond=cond)

    source.outlet.connect(sink.inlet)

    async with Runner((source,)) as runner:
        await have_1
        runner.stop()

    assert source.lifetime.task is None

    assert sink.collected_samples[0].name == 'source'
    assert sink.collected_samples[0].timestamp == datetime(2024, 4, 12, 9, 19)
    assert sink.collected_samples[0].data == pytest.approx(36.5)

@pytest.mark.asyncio
async def test_errorhandler_nolifetime():
    assert False

@pytest.mark.asyncio
async def test_errorhandler_lifetime():
    assert False

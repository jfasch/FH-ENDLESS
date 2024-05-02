from endless.sample_broadcaster import SampleBroadcaster
from endless.source_mock import MockSource
from endless.sink_mock import MockSink, have_n_samples
from endless.runner import Runner, StopRunning
from endless.async_util import mock_timestamps_async

import pytest
from datetime import datetime, timedelta


@pytest.mark.asyncio
async def test_basic():
    source = MockSource(
        tag='source', 
        timestamps=mock_timestamps_async(start=datetime(2024, 4, 16, 14, 48), interval=timedelta(seconds=3)), 
        data=42)

    have_1, cond_1 = have_n_samples(1)
    sink_1 = MockSink(cond=cond_1)

    have_2, cond_2 = have_n_samples(1)
    sink_2 = MockSink(cond=cond_2)

    broadcaster = SampleBroadcaster()

    source.sample_out.connect(broadcaster.sample_in)
    broadcaster.sample_out.connect(sink_1.sample_in)
    broadcaster.sample_out.connect(sink_2.sample_in)

    async with Runner((source, sink_1, sink_2, broadcaster)):
        await have_1
        await have_2
        raise StopRunning

    assert sink_1.collected_samples[0].tag == 'source'
    assert sink_1.collected_samples[0].timestamp == datetime(2024, 4, 16, 14, 48)
    assert sink_1.collected_samples[0].data == pytest.approx(42)

    assert sink_1.collected_samples[0].tag == 'source'
    assert sink_1.collected_samples[0].timestamp == datetime(2024, 4, 16, 14, 48)
    assert sink_1.collected_samples[0].data == pytest.approx(42)

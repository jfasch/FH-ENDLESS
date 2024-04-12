from endless.source_mock import MockSource
from endless.sink_mock import MockSink, have_n_samples
from endless.sink_composite import CompositeSink
from endless.sample import Sample
from endless.runner import Runner
from endless.async_util import mock_timestamps_async

import pytest
from datetime import datetime, timedelta


@pytest.mark.asyncio
async def test_outlet_connect_multi():
    source = MockSource(
        name='source', 
        timestamps=mock_timestamps_async(start=datetime(2024, 4, 12, 10, 24), interval=timedelta(seconds=3)), 
        data=42)

    (have_1_1, cond1), (have_1_2, cond2) = have_n_samples(1), have_n_samples(1)
    sink1, sink2 = MockSink(cond1), MockSink(cond2)
    
    source.outlet.connect(sink1.inlet)
    source.outlet.connect(sink2.inlet)

    async with Runner((source,)) as runner:
        await have_1_1
        await have_1_2

        runner.stop()

    assert sink1.collected_samples[0].name == 'source'
    assert sink1.collected_samples[0].timestamp == datetime(2024, 4, 12, 10, 24)
    assert sink1.collected_samples[0].data == 42

    assert sink2.collected_samples[0].name == 'source'
    assert sink2.collected_samples[0].timestamp == datetime(2024, 4, 12, 10, 24)
    assert sink2.collected_samples[0].data == 42

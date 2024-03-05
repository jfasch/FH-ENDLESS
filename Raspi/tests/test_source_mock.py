from endless.sample import Sample
from endless.source_mock import MockSource
from endless.sink_mock import MockSink, have_n_samples
from endless import async_util

import pytest
import asyncio


@pytest.mark.asyncio
async def test_basic():
    have_5, cond = have_n_samples(5)
    sink = MockSink(cond)
    source = MockSource('mock', async_util.mock_timestamps(start_time_ms=100, interval_ms=10), temperature=37.5)

    async with asyncio.TaskGroup() as tg:
        sink.start(tg)
        source.start(tg, sink)

        await have_5

        assert sink.samples[0] == Sample(name="mock", timestamp_ms=100, temperature=pytest.approx(37.5))
        assert sink.samples[1] == Sample(name="mock", timestamp_ms=110, temperature=pytest.approx(37.5))
        assert sink.samples[2] == Sample(name="mock", timestamp_ms=120, temperature=pytest.approx(37.5))
        assert sink.samples[3] == Sample(name="mock", timestamp_ms=130, temperature=pytest.approx(37.5))
        assert sink.samples[4] == Sample(name="mock", timestamp_ms=140, temperature=pytest.approx(37.5))

        source.stop()
        sink.stop()

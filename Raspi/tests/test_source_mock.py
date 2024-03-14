from endless.sample import Sample
from endless.source_mock import MockSource
from endless.sink_mock import MockSink, have_n_samples
from endless import async_util

import pytest
import asyncio
from datetime import datetime, timedelta


@pytest.mark.asyncio
async def test_basic():
    have_5, cond = have_n_samples(5)
    sink = MockSink(cond)
    source = MockSource('mock',
                        timestamps=async_util.mock_timestamps(start=datetime(2024, 3, 14, 8, 46), interval=timedelta(milliseconds=10)), 
                        temperature=37.5)

    async with asyncio.TaskGroup() as tg:
        sink.start(tg)
        source.start(tg, sink)

        await have_5

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

        source.stop()
        sink.stop()

from endless.source_mock import MockSource
from endless.sink_mock import MockSink, have_n_samples
from endless.runner import Runner
from endless.async_util import mock_timestamps
from endless.sample import Sample

import pytest
import asyncio
from datetime import datetime, timedelta


@pytest.mark.asyncio
async def test_basic():
    source = MockSource(name='source', timestamps=mock_timestamps(start=datetime(2024, 3, 20, 10, 56), interval=timedelta(seconds=3)), temperature=36.5)

    have_1, cond = have_n_samples(1)
    sink = MockSink(cond=cond)

    async with Runner(sources=[source], sink=sink) as runner:
        await have_1
        runner.stop()

    assert source.task is None
    assert sink.task is None
    assert sink.samples[0] == Sample('source', datetime(2024, 3, 20, 10, 56), pytest.approx(36.5))

from endless.sample import Sample
from endless.source_mock import MockSource
from endless import async_util

import pytest
import asyncio


@pytest.mark.asyncio
async def test_basic():
    queue = asyncio.Queue()

    async with asyncio.TaskGroup() as tg:
        producer = tg.create_task(
            source_mock(
                queue = queue,
                name = "mock",
                timestamps = async_util.mock_timestamps(start_time_ms = 100, interval_ms = 10),
                temperature = 37.5
            ))

        assert await queue.get() == Sample(name="mock", timestamp_ms=100, temperature=pytest.approx(37.5))
        assert await queue.get() == Sample(name="mock", timestamp_ms=110, temperature=pytest.approx(37.5))
        assert await queue.get() == Sample(name="mock", timestamp_ms=120, temperature=pytest.approx(37.5))
        assert await queue.get() == Sample(name="mock", timestamp_ms=130, temperature=pytest.approx(37.5))
        assert await queue.get() == Sample(name="mock", timestamp_ms=140, temperature=pytest.approx(37.5))

        producer.cancel()


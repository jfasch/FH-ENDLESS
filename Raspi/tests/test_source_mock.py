from endless.source_mock import source_mock
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

        assert await queue.get() == ("mock", 100, pytest.approx(37.5))
        assert await queue.get() == ("mock", 110, pytest.approx(37.5))
        assert await queue.get() == ("mock", 120, pytest.approx(37.5))
        assert await queue.get() == ("mock", 130, pytest.approx(37.5))
        assert await queue.get() == ("mock", 140, pytest.approx(37.5))

        producer.cancel()


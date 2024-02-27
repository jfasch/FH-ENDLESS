from endless.sink_mock import sink_mock

import pytest
import asyncio


@pytest.mark.asyncio
async def test_basic():
    samples = []

    queue = asyncio.Queue()

    sink = asyncio.create_task(sink_mock(queue, samples))

    await queue.put(('name1', 100, 42.666))
    await queue.put(('name2', 200, -273.15))

    while len(samples) < 2: # argh. polling.
        await asyncio.sleep(0.01)
    sink.cancel()

    assert samples[0] == ('name1', 100, pytest.approx(42.666))
    assert samples[1] == ('name2', 200, pytest.approx(-273.15))



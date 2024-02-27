from endless.sink_mock import MockSink

import pytest


@pytest.mark.asyncio
async def test_basic():
    sink = MockSink()
    await sink.put(timestamp_ms = 100, temperature = 42.666)
    await sink.put(timestamp_ms = 200, temperature = -273.15)

    assert sink.samples[0] == (100, pytest.approx(42.666))
    assert sink.samples[1] == (200, pytest.approx(-273.15))

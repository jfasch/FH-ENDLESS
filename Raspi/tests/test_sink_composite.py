from endless.sink_mock import MockSink
from endless.sink_composite import CompositeSink
from endless.sample import Sample

import pytest
import asyncio


@pytest.mark.asyncio
async def test_basic():
    sink1, sink2 = MockSink(), MockSink()
    comp = CompositeSink([sink1, sink2])
    comp.start()

    await comp.put(Sample(name='name', timestamp_ms=200, temperature=42.666))

    while len(sink1.samples) < 1:
        await asyncio.sleep(0.01)

    assert sink1.samples[0] == Sample(name='name', timestamp_ms=200, temperature=pytest.approx(42.666))
    assert sink2.samples[0] == Sample(name='name', timestamp_ms=200, temperature=pytest.approx(42.666))

    comp.stop()

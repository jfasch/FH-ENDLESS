from endless.sensor_mock import MockSensor
from endless import async_util

import pytest


@pytest.mark.asyncio
async def test_iter():
    sensor = MockSensor(
        temperature = 37.5, 
        timestamps = async_util.mock_timestamps(start_time_ms = 100, interval_ms = 10),
    )

    samples = []
    async for sampleno, sample in async_util.enumerate(sensor.iter()):
        samples.append(sample)
        if sampleno == 5:
            break

    assert samples[0] == (100, pytest.approx(37.5))
    assert samples[1] == (110, pytest.approx(37.5))
    assert samples[2] == (120, pytest.approx(37.5))
    assert samples[3] == (130, pytest.approx(37.5))
    assert samples[4] == (140, pytest.approx(37.5))

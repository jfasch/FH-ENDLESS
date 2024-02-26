from endless.sensor_mock import MockSensor
from endless import async_util

import pytest


@pytest.mark.asyncio
async def test_get_one():
    sensor = MockSensor(
        temperature = 37.5,
        initial_time = 666,
        interval = 1, # unused
    )
    timestamp, temperature = await sensor.get_one()

    assert timestamp == 666
    assert temperature == pytest.approx(37.5)

@pytest.mark.asyncio
async def test_iter():
    sensor = MockSensor(
        temperature = 37.5, 
        initial_time = 100,
        interval = 10)
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

@pytest.mark.asyncio
async def test_set_time():
    sensor = MockSensor(
        temperature = 37.5, 
        initial_time = 100,
        interval = 10)

    timestamp, _ = await sensor.get_one()
    assert timestamp == 100

    sensor.set_time(200)
    
    timestamp, _ = await sensor.get_one()
    assert timestamp == 200

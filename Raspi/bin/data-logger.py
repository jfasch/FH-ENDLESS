#!/usr/bin/env python

from endless.sensor_mock import MockSensor
from endless import async_util

import asyncio


sensors = {
    'links-oben': MockSensor(
        temperature = -273.15, 
        timestamps = async_util.wall_timestamps(start_time_ns=0, interval_ns=500*1000*1000),
    ),
    'rechts-unten': MockSensor(
        temperature = 42.6,
        timestamps = async_util.wall_timestamps(start_time_ns=0, interval_ns=400*1000*1000),
    ),
}

async def measure(name, sensor):
    async for timestamp_ns, temperature in sensor.iter():
        print(name, timestamp_ns, temperature)

async def main():
    async with asyncio.TaskGroup() as tg:
        for name, sensor in sensors.items():
            tg.create_task(measure(name, sensor))

asyncio.run(main())

#!/usr/bin/env python

from endless.sensor_mock import MockSensor
from endless.sensor_can import CANSensor
from endless import async_util

import asyncio


# sensors = {
#     'links-oben': MockSensor(
#         temperature = -273.15, 
#         timestamps = async_util.wall_timestamps(start_time_ms=0, interval_ms=500),
#     ),
#     'rechts-unten': MockSensor(
#         temperature = 42.6,
#         timestamps = async_util.wall_timestamps(start_time_ms=0, interval_ms=400),
#     ),
# }

sensors = {
    'CAN#42': CANSensor(can_iface = 'mein-test-can', can_id=42),
    'CAN#43': CANSensor(can_iface = 'mein-test-can', can_id=43),
}

async def measure(name, sensor):
    async for timestamp_ms, temperature in sensor.iter():
        print(name, timestamp_ms, temperature)

async def main():
    async with asyncio.TaskGroup() as tg:
        for name, sensor in sensors.items():
            tg.create_task(measure(name, sensor))

asyncio.run(main())

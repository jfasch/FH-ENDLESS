import asyncio
from datetime import datetime


async def enumerate(aiterable, start=0):
    async for item in aiterable:
        yield start, item
        start += 1

async def wallclock_timestamps(interval):
    while True:
        yield datetime.now()
        await asyncio.sleep(interval.microseconds / 1_000_000)

async def mock_timestamps(start, interval):
    while True:
        yield start
        start += interval

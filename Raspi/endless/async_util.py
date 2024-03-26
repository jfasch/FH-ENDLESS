import asyncio
from datetime import datetime


async def iter_queue_blocking(q):
    while True:
        yield await q.get()

async def wallclock_timestamps(interval):
    while True:
        yield datetime.now()
        await asyncio.sleep(interval.microseconds / 1_000_000)

async def mock_timestamps(start, interval):
    while True:
        yield start
        start += interval

import asyncio


async def enumerate(aiterable, start=0):
    async for item in aiterable:
        yield start, item
        start += 1

async def wall_timestamps(start_time_ms, interval_ms):
    interval_s = interval_ms / 1000
    while True:
        yield start_time_ms
        await asyncio.sleep(interval_s)
        start_time_ms += interval_ms

async def mock_timestamps(start_time_ms, interval_ms):
    while True:
        yield start_time_ms
        start_time_ms += interval_ms

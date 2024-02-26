import asyncio


async def enumerate(aiterable, start=0):
    async for item in aiterable:
        yield start, item
        start += 1

async def wall_timestamps(start_time_ns, interval_ns):
    interval_s = interval_ns / 1_000_000_000
    while True:
        yield start_time_ns
        await asyncio.sleep(interval_s)
        start_time_ns += interval_ns

async def mock_timestamps(start_time_ns, interval_ns):
    while True:
        yield start_time_ns
        start_time_ns += interval_ns

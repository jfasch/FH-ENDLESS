import asyncio
import datetime
import math


async def async_iter_queue(q):
    while True:
        yield await q.get()

async def wallclock_timestamps_sleep(interval):
    while True:
        yield datetime.datetime.now()
        await asyncio.sleep(interval.microseconds / 1_000_000)

def wallclock_timestamps_nosleep():
    while True:
        yield datetime.datetime.now()

async def mock_timestamps_async(start, interval):
    while True:
        yield start
        start += interval

def mock_timestamps_sync(start, interval):
    while True:
        yield start
        start += interval

def yet_another_sin(timestamp: datetime.datetime, amplitude, hz, phase_shift, vertical_shift):
    x = timestamp.timestamp()     # seconds (in float) since epoch
    return amplitude * math.sin(hz*(x+phase_shift)) + vertical_shift

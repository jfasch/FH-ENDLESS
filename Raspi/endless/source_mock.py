from .sample import Sample

import asyncio


async def source_mock(queue, name, timestamps, temperature):
    async for ts in timestamps:
        await queue.put(Sample(name=name, timestamp_ms=ts, temperature=temperature))

        # if queue is unbounded (and timestamps are of the
        # quick-rush-through variant), then queue.put() wont schedule
        # and the entire program will hang. add a manual scheduling
        # point.
        await asyncio.sleep(0)

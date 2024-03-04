from .sample import Sample
from .source import Source

import asyncio


class MockSource(Source):
    def __init__(self, name, timestamps, temperature):
        super().__init__(name)
        self.timestamps = timestamps
        self.temperature = temperature

    async def _run(self):
        async for ts in self.timestamps:
            await self.sink.put(Sample(name=self.name, timestamp_ms=ts, temperature=self.temperature))

            # if queue is unbounded (and timestamps are of the
            # quick-rush-through variant), then queue.put() wont
            # schedule and the entire program will hang. add a manual
            # scheduling point.
            await asyncio.sleep(0)

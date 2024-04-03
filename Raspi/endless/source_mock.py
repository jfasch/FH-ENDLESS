from .sample import Sample
from .source import Source
from .errorhandler import ErrorHandler, ErrorReporter

import asyncio


class MockSource(Source):
    def __init__(self, name, timestamps, data):
        super().__init__(name)
        self.timestamps = timestamps
        self.data = data

    async def _run(self):
        async for ts in self.timestamps:
            if callable(self.data):
                async with ErrorReporter(self.errorhandler):
                    data = self.data(ts)
            else:
                data = self.data

            await self.sink.put(Sample(name=self.name, timestamp=ts, data=data))


            # if queue is unbounded (and timestamps are of the
            # quick-rush-through variant, without any real delay),
            # then queue.put() wont schedule and the entire program
            # will hang. add a manual scheduling point.
            await asyncio.sleep(0)

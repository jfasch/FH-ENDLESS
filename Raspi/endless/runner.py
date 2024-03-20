from contextlib import asynccontextmanager
from asyncio import TaskGroup


class Runner:
    def __init__(self, sources, sink):
        self.sources = sources
        self.sink = sink
        
        self._task_group = None

    async def __aenter__(self):
        self._task_group = TaskGroup()
        await self._task_group.__aenter__()
        self.sink.start(self._task_group)
        for source in self.sources:
            source.start(self._task_group, self.sink)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self._task_group.__aexit__(exc_type, exc_value, traceback)

    def stop(self):
        for s in self.sources:
            s.stop()
        self.sink.stop()

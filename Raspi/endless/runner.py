from contextlib import asynccontextmanager
from asyncio import TaskGroup


class Runner:
    class NotConnected(Exception): pass

    def __init__(self, sources, sinks):
        for source in sources:
            if source.sink is None:
                raise self.NotConnected(f'source "{source.name}" is not connected')

        self.sources = sources
        self.sinks = sinks
        
        self._task_group = None

    async def __aenter__(self):
        self._task_group = TaskGroup()
        await self._task_group.__aenter__()

        for sink in self.sinks:
            sink.start(self._task_group)
        for source in self.sources:
            source.start(self._task_group)

        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self._task_group.__aexit__(exc_type, exc_value, traceback)

    def stop(self):
        for source in self.sources:
            source.stop()
        for sink in self.sinks:
            sink.stop()

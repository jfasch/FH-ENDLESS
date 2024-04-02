from .errorhandler import ErrorHandler

from contextlib import asynccontextmanager
from asyncio import TaskGroup


class SourceNotConnected(Exception): pass
class NullErrorHandler(ErrorHandler):
    async def _handle_error(self, error): pass

class Runner:
    def __init__(self, sources, sinks, errorhandler=None):
        for source in sources:
            if source.sink is None:
                raise SourceNotConnected(f'source "{source.name}" is not connected')

        self.sources = sources
        self.sinks = sinks
        
        if errorhandler is None:
            self.errorhandler = NullErrorHandler()
        else:
            self.errorhandler = errorhandler
        
        self._task_group = None

    async def __aenter__(self):
        self.errorhandler.start()

        self._task_group = TaskGroup()
        await self._task_group.__aenter__()

        for sink in self.sinks:
            sink.start(self._task_group)
        for source in self.sources:
            source.errors_to(self.errorhandler)
            source.start(self._task_group)

        return self

    async def __aexit__(self, exc_type, exc_value, exc_traceback):
        try:
            await self._task_group.__aexit__(exc_type, exc_value, exc_traceback)
        finally:
            await self.errorhandler.stop()

    def stop(self):
        for source in self.sources:
            source.stop()
        for sink in self.sinks:
            sink.stop()

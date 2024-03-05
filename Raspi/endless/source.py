import asyncio
import abc
import sys


class Source(abc.ABC):
    def __init__(self, name):
        self.name = name
        self.task = None
        self.sink = None

    def start(self, tg, sink):
        self.sink = sink
        self.task = tg.create_task(self._run())
        
    def stop(self):
        assert self.task is not None
        self.task.cancel()

    @abc.abstractmethod
    async def _run(self):
        '''Use self.sink to get rid of data that we constantly
        produce'''
        pass

import asyncio
import abc
import sys


class Source(abc.ABC):
    def __init__(self, name):
        self.name = name
        self.task = None
        self.sink = None

    def connect(self, sink):
        assert self.sink is None
        self.sink = sink

    def start(self, tg):
        self.task = tg.create_task(self._run())
        
    def stop(self):
        assert self.task is not None
        self.task.cancel()
        self.task = None

    @abc.abstractmethod
    async def _run(self):
        '''Use self.sink to get rid of data that we constantly
        produce'''
        pass

import asyncio
import abc
import sys


class Source(abc.ABC):
    def __init__(self, name):
        self.name = name
        self.task = None
        self.sink = None

    def start(self, sink):
        self.sink = sink
        self.task = asyncio.create_task(self._do_run())
        return [self.task]

    async def _do_run(self):
        try:
            await self._run()
        except asyncio.CancelledError:
            print(self.name, 'cancelled', file=sys.stderr)
        except Exception as e:
            print(self.name, 'exception', type(e), e)

    @abc.abstractmethod
    async def _run(self):
        '''Use self.sink to get rid of data that we constantly
        produce'''
        pass

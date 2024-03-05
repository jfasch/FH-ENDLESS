import asyncio
import abc
import sys


class Sink(abc.ABC):
    def __init__(self):
        self.task = None
        self.queue = asyncio.Queue()

    def start(self, tg):
        self.task = tg.create_task(self._run())

    def stop(self):
        assert self.task is not None
        self.task.cancel()

    async def put(self, sample):
        await self.queue.put(sample)

    async def _run(self):
        try:
            while True:
                sample = await self.queue.get()
                await self.handle_put(sample)
        except Exception as e:
            print(type(e), e, file=sys.stderr)
            raise

    @abc.abstractmethod
    async def handle_put(self, sample):
        # do something with sample
        pass
        

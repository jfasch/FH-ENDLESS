import asyncio
import abc
import sys


class Sink(abc.ABC):
    def __init__(self):
        self.task = None
        self.queue = asyncio.Queue()

    def start(self, taskgroup):
        return taskgroup.create_task(self._run())

    async def put(self, sample):
        await self.queue.put(sample)

    async def _run(self):
        try:
            while True:
                sample = await self.queue.get()
                await self.handle_put(sample)
        except Exception as e:
            print(type(e), e, file=sys.stderr)    # jjj fix that: task exception handling!!!

    @abc.abstractmethod
    async def handle_put(self, sample):
        # do something with sample
        pass
        

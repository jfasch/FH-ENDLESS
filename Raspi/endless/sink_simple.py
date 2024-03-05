from .sink import Sink

import abc


class SimpleSink(Sink):
    async def _run(self):
        while True:
            sample = await self.queue.get()
            await self._handle_put(sample)

    @abc.abstractmethod
    async def _handle_put(self, sample):
        '''Derived class implement this to handle the sample

        :param sample: a Sample object

        '''

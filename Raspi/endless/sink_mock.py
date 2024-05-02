from .interfaces import SampleInlet
from .component import LifetimeComponent
from .facet import facet

import asyncio


def have_n_samples(n):
    future = asyncio.get_running_loop().create_future()
    def cond(mocksink):
        if len(mocksink.collected_samples) == n:
            future.set_result(True)
    return future, cond

@facet('sample_in', basetype=SampleInlet, methodspec=(('consume_sample', '_incoming_sample'),))
class MockSink(LifetimeComponent):
    def __init__(self, cond=None):
        super().__init__(self._run)
        self.collected_samples = []
        self.cond = cond

        self.queue = asyncio.Queue()

    async def _incoming_sample(self, sample):
        await self.queue.put(sample)

        await asyncio.sleep(0)

    async def _run(self):
        while True:
            sample = await self.queue.get()
            self.collected_samples.append(sample)

            if self.cond is not None:
                self.cond(self)

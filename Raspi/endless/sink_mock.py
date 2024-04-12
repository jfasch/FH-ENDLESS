from .inlet import Inlet
from .component import Component

import asyncio


def have_n_samples(n):
    future = asyncio.get_running_loop().create_future()
    def cond(mocksink):
        if len(mocksink.collected_samples) == n:
            future.set_result(True)
    return future, cond

class MockSink(Component):
    def __init__(self, cond=None):
        super().__init__()
        self.collected_samples = []
        self.cond = cond

        self.inlet = Inlet(self._incoming_sample)

    async def _incoming_sample(self, sample):
        self.collected_samples.append(sample)

        if self.cond is not None:
            self.cond(self)

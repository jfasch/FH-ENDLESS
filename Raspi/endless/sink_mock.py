from .sink import Sink

import asyncio


def have_n_samples(n):
    future = asyncio.get_running_loop().create_future()
    def cond(mocksink):
        if len(mocksink.samples) == n:
            future.set_result(True)
    return future, cond

class MockSink(Sink):
    def __init__(self, cond=None):
        super().__init__()
        self.samples = []
        self.cond = cond

    async def handle_put(self, sample):
        self.samples.append(sample)

        if self.cond is not None:
            self.cond(self)

from .sink import Sink


class MockSink(Sink):
    def __init__(self):
        super().__init__()
        self.samples = []

    async def handle_put(self, sample):
        self.samples.append(sample)

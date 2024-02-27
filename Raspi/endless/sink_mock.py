class MockSink:
    def __init__(self):
        self.samples = []

    async def put(self, timestamp_ms, temperature):
        self.samples.append((timestamp_ms, temperature))

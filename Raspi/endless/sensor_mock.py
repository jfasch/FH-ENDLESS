class MockSensor:
    def __init__(self, timestamps, temperature):
        self.timestamps = timestamps
        self.temperature = temperature

    async def iter(self):
        async for ts in self.timestamps:
            yield ts, self.temperature

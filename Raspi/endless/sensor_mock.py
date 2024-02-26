class MockSensor:
    def __init__(self, initial_timestamp, temperature, interval):
        self.timestamp = initial_timestamp
        self.temperature = temperature
        self.interval = interval

    async def get_one(self):
        return self.timestamp, self.temperature

    async def iter(self):
        while True:
            yield self.timestamp, self.temperature
            self.timestamp += self.interval

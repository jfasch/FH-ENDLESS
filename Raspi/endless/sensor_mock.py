class MockSensor:
    def __init__(self, initial_time, temperature, interval):
        self.time = initial_time
        self.temperature = temperature
        self.interval = interval

    async def get_one(self):
        return self.time, self.temperature

    async def iter(self):
        while True:
            yield self.time, self.temperature
            self.time += self.interval

    def set_time(self, time):
        self.time = time

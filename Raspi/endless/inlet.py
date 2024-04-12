class Inlet:
    def __init__(self, func):
        self.func = func
        
    async def consume_sample(self, sample):
        await self.func(sample)

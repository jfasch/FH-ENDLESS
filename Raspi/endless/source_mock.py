from .component import Component
from .sample import Sample
from .outlet import Outlet
from .lifetime import Lifetime
from .error_strategy import ErrorStrategy

import asyncio


class MockSource(Component):
    def __init__(self, name, timestamps, data):
        super().__init__()

        self.name = name
        self.timestamps = timestamps
        self.data = data

        self.outlet = Outlet()
        self.lifetime = Lifetime(self._run)

    async def _run(self):
        async for ts in self.timestamps:
            produced_data = None
            if callable(self.data):
                async with ErrorStrategy(self.errors_to):
                    produced_data = self.data(ts)
            else:
                produced_data = self.data

            if produced_data is not None:
                await self.outlet.produce_sample(
                    Sample(name=self.name, timestamp=ts, data=produced_data))

from .component import LifetimeComponent
from .receptacle import receptacle, ONE
from .sample import Sample
from .interfaces import SampleInlet
from .error_strategy import ErrorStrategy

import asyncio


@receptacle('sample_out', SampleInlet, multiplicity=ONE)
class MockSource(LifetimeComponent):
    def __init__(self, tag, timestamps, data):
        super().__init__(self._run)

        self.tag = tag
        self.timestamps = timestamps
        self.data = data

    async def _run(self):
        async for ts in self.timestamps:
            produced_data = None
            if callable(self.data):
                async with ErrorStrategy(self):
                    produced_data = self.data(ts)
            else:
                produced_data = self.data

            if produced_data is not None:
                await self._sample_out.consume_sample(Sample(tag=self.tag, timestamp=ts, data=produced_data))

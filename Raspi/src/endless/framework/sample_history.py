from .component import Component
from .receptacle import receptacle, ONE
from .facet import facet
from .interfaces import SampleInlet, SampleList

from collections import deque


@facet('sample_in', SampleInlet, (('consume_sample', '_consume_sample'),))
@facet('sample_list', SampleList, (('get_samples', '_get_samples'),))
@receptacle('sample_out', SampleInlet, multiplicity=ONE)
class SampleHistory(Component):
    def __init__(self, size):
        super().__init__()
        self.samples = deque(maxlen=size)

    async def _consume_sample(self, sample):
        self.samples.append(sample)
        await self._sample_out.consume_sample(sample)

    async def _get_samples(self):
        return self.samples

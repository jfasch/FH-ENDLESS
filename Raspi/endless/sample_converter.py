from .component import Component
from .facet import facet
from .receptacle import receptacle, ONE
from .interfaces import SampleInlet


@facet('sample_in', SampleInlet, (('consume_sample', '_convert'),))
@receptacle('sample_out', SampleInlet, multiplicity=ONE)
class SampleConverter(Component):
    def __init__(self, func):
        super().__init__()
        self.func = func

    async def _convert(self, sample):
        converted = self.func(sample)
        await self._sample_out.consume_sample(converted)

from .component import Component
from .receptacle import receptacle, ONE
from .facet import facet
from .interfaces import SampleInlet


@facet('sample_in', SampleInlet, (('consume_sample', '_convert'),))
@receptacle('sample_out', SampleInlet, multiplicity=ONE)
class SampleConverter(Component):
    def __init__(self, func):
        super().__init__()
        self.func = func

    async def _convert(self, sample):
        converted = self.func(sample)
        if converted is not None:
            await self._sample_out.consume_sample(converted)

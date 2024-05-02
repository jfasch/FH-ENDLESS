from .component import Component
from .facet import facet
from .receptacle import receptacle, ONE
from .interfaces import SampleInlet


@facet('inlet', SampleInlet, (('consume_sample', '_convert'),))
@receptacle('outlet', SampleInlet, multiplicity=ONE)
class SampleConverter(Component):
    def __init__(self, func):
        super().__init__()
        self.func = func

    async def _convert(self, sample):
        converted = self.func(sample)
        await self._outlet.consume_sample(converted)

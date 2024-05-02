from .component import Component
from .receptacle import receptacle, ONE
from .facet import facet
from .interfaces import SampleInlet


@facet('inlet', SampleInlet, (('consume_sample', '_handle_sample'),))
@receptacle('outlet', SampleInlet, multiplicity=ONE)
class TagFilter(Component):
    def __init__(self, tag):
        super().__init__()
        self.tag = tag
    async def _handle_sample(self, sample):
        if sample.tag == self.tag:
            await self._outlet.consume_sample(sample)

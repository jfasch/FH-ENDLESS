from .component import Component
from .facet import facet
from .receptacle import receptacle, ONE_OR_MANY
from .interfaces import SampleInlet


@facet('sample_in', SampleInlet, (('consume_sample', '_put_sample'),))
@receptacle('sample_out', SampleInlet, multiplicity=ONE_OR_MANY)
class SampleBroadcaster(Component):
    async def _put_sample(self, sample):
        await self._sample_out.consume_sample(sample)

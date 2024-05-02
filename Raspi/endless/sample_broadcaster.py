from .component import Component
from .facet import facet
from .interfaces import SampleInlet


@facet('sample_in', SampleInlet, (('consume_sample', '_put_sample'),))
class SampleBroadcaster(Component):
    def __init__(self):
        super().__init__()
        self._sample_out = self._multi_outlet()
        self.sample_out = self._sample_out

    async def _put_sample(self, sample):
        await self._sample_out.consume_sample(sample)

    class _multi_outlet:
        def __init__(self):
            self.targets = []
        def connect(self, target):
            assert isinstance(target, SampleInlet)
            self.targets.append(target)
        async def consume_sample(self, sample):
            for target in self.targets:
                retval = await target.consume_sample(sample)
                assert retval is None

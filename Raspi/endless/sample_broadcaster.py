from .component import Component
from .facet import facet
from .interfaces import SampleInlet


@facet('inlet', SampleInlet, (('consume_sample', '_put_sample'),))
class SampleBroadcaster(Component):
    def __init__(self):
        super().__init__()
        self._outlet = self._multi_outlet()
        self.outlet = self._outlet

    async def _put_sample(self, sample):
        await self._outlet.consume_sample(sample)

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

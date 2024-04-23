from .component import Component
from .facet import facet
from .interfaces import Inlet


@facet('inlet', Inlet, (('consume_sample', '_put_sample'),))
class Tee(Component):
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
            assert isinstance(target, Inlet)
            self.targets.append(target)
        async def consume_sample(self, sample):
            for target in self.targets:
                retval = await target.consume_sample(sample)
                assert retval is None

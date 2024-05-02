from .component import Component
from .facet import facet
from .receptacle import receptacle, ONE
from .interfaces import SampleInlet, Switch


@facet('sample_in', SampleInlet, (('consume_sample', '_new_value'),))
@receptacle('switch', Switch, multiplicity=ONE)
class Hysteresis(Component):
    def __init__(self, low, high):
        super().__init__()
        self.low = low
        self.high = high

    async def _new_value(self, sample):
        if sample.data < self.low:
            await self._switch.set_state(True)
        elif sample.data > self.high:
            await self._switch.set_state(False)
        else:
            pass

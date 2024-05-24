from .component import Component
from .facet import facet
from .receptacle import receptacle, ONE
from .interfaces import Control, Switch, HighLowConfig


@facet('control', Control, (('adapt', '_new_value'),))
@facet('config', HighLowConfig, (('set_high', '_set_hi'), ('set_low', '_set_lo'), ('show', '_show')))
@receptacle('switch', Switch, multiplicity=ONE)
class Hysteresis(Component):
    def __init__(self, low, high):
        super().__init__()
        self.low = low
        self.high = high

    async def _new_value(self, timestamp, value):
        if value < self.low:
            await self._switch.set_state(True)
        elif value > self.high:
            await self._switch.set_state(False)
        else:
            pass

    async def _set_hi(self, value):
        self.high = value
    async def _set_lo(self, value):
        self.low = value
    async def _show(self):
        return self.low, self.high

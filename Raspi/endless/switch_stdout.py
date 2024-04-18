from .component import Component, facet
from .interfaces import Switch


@facet('switch', Switch, (('set_state', '_set_state'),))
class StdoutSwitch(Component):
    def __init__(self, prefix):
        super().__init__()
        self.prefix = prefix
    async def _set_state(self, state):
        print(self.prefix, state)

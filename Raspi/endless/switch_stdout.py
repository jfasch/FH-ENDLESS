from .component import Component
from .facet import facet
from .interfaces import Switch


@facet('switch', Switch, (('set_state', '_set_state'),))
class StdoutSwitch(Component):
    def __init__(self, prefix):
        super().__init__()
        self.prefix = prefix
        self.state = False
    async def _set_state(self, state):
        if self.state != state:
            print(self.prefix, state)
            self.state = state

from .component import Component, facet
from .interfaces import Inlet


@facet('inlet', Inlet, (('consume_sample', '_handle_put'),))
class StdoutSink(Component):
    async def _handle_put(self, sample):
        print(f'{sample.name};{sample.timestamp};{sample.data}')
        

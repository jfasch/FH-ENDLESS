from .component import Component
from .facet import facet
from .interfaces import SampleInlet


@facet('inlet', SampleInlet, (('consume_sample', '_handle_put'),))
class StdoutSink(Component):
    def __init__(self, prefix):
        super().__init__()
        self.prefix = prefix
    async def _handle_put(self, sample):
        print(f'{self.prefix}:{sample.tag};{sample.timestamp};{sample.data}')


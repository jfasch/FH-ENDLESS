from .sink_simple import SimpleSink


class CompositeSink(SimpleSink):
    '''Distributes incoming samples to other sinks'''

    def __init__(self, sinks):
        super().__init__()
        self.sinks = sinks

    def start(self, tg):
        for sink in self.sinks:
            sink.start(tg)
        super().start(tg)

    def stop(self):
        super().stop()
        for sink in self.sinks:
            sink.stop()
        
    async def _handle_put(self, sample):
        for sink in self.sinks:
            await sink.put(sample)

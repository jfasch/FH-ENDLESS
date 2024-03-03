from .sink import Sink


class CompositeSink(Sink):
    def __init__(self, sinks):
        super().__init__()
        self.sinks = sinks

    def start(self):
        for sink in self.sinks:
            sink.start()
        super().start()

    def stop(self):
        super().stop()
        for sink in self.sinks:
            sink.stop()
        
    async def handle_put(self, sample):
        for sink in self.sinks:
            await sink.put(sample)

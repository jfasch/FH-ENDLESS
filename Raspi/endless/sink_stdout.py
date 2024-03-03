from .sink import Sink


class StdoutSink(Sink):
    async def handle_put(self, sample):
        print(sample.name, sample.timestamp_ms, sample.temperature)

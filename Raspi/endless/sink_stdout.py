from .sink_simple import SimpleSink


class StdoutSink(SimpleSink):
    async def _handle_put(self, sample):
        print(sample.name, sample.timestamp_ms, sample.temperature)

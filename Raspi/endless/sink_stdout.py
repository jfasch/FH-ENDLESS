from .sink_simple import SimpleSink


class StdoutSink(SimpleSink):
    async def _handle_put(self, sample):
        print(f'{sample.name};{sample.timestamp};{sample.temperature}')
        

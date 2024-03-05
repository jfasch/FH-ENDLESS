from .sink import Sink

import aiomqtt
import json


class MQTTSink(Sink):
    def __init__(self, host, topics, port = 1883):
        super().__init__()

        self.host = host
        self.port = port
        self.topics = topics

    async def _run(self):
        async with aiomqtt.Client(hostname=self.host, port=self.port) as client:
            while True:
                sample = await self.queue.get()
                topic = self.topics[sample.name]
                payload = self._make_payload(sample)
                await client.publish(topic, payload=payload)

    def _make_payload(self, sample):
        return json.dumps({
            'timestamp_ms': sample.timestamp_ms,
            'temperature': sample.temperature,
        })

    def handle_put(self, sample):
        assert False

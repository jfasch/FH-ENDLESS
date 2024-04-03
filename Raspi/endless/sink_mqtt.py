from .sink import Sink

import aiomqtt
import json


class MQTTSink(Sink):
    def __init__(self, host, topics, port = 1883):
        ''':param host: MQTT broker to establish a connection to
        :param port: optional, defaults to 1883
        :param topics: mapping of incoming sample names to MQTT topics

        '''

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
            'timestamp': sample.timestamp.isoformat(),
            'data': sample.data,
        })

from .source import Source
from .sample import Sample

import json
import aiomqtt
from datetime import datetime


class MQTTSource(Source):
    def __init__(self, name, host, topic, port = 1883):
        super().__init__(name)

        self.host = host
        self.port = port
        self.topic = topic

    async def _run(self):
        async with aiomqtt.Client(hostname=self.host, port=self.port) as client:
            await client.subscribe(self.topic)
            async for message in client.messages:
                sample = self._make_sample(message.payload)
                await self.sink.put(sample)

    def _make_sample(self, payload):
        mqtt_sample = json.loads(payload)
        if len(mqtt_sample) != 2:
            raise RuntimeError(f'Invalid sample (#entries=={len(mqtt_sample)}):', payload)
        return Sample(
            name = self.name,
            timestamp = datetime.fromisoformat(mqtt_sample['timestamp']),
            temperature = mqtt_sample['temperature'],
        )

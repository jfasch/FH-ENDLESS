from .component import LifetimeComponent
from .receptacle import receptacle, ONE
from .interfaces import SampleInlet
from .sample import Sample

import json
import aiomqtt
from datetime import datetime


@receptacle('sample_out', SampleInlet, multiplicity=ONE)
class MQTTSource(LifetimeComponent):
    def __init__(self, tag, host, topic, port = 1883):
        super().__init__(self._run)

        self.host = host
        self.port = port
        self.topic = topic

        self.tag = tag

    async def _run(self):
        async with aiomqtt.Client(hostname=self.host, port=self.port) as client:
            await client.subscribe(self.topic)
            async for message in client.messages:
                sample = self._make_sample(message.payload)
                await self._sample_out.consume_sample(sample)

    def _make_sample(self, payload):
        mqtt_sample = json.loads(payload)
        if len(mqtt_sample) != 2:
            raise RuntimeError(f'Invalid sample (#entries=={len(mqtt_sample)}):', payload)
        return Sample(
            tag = self.tag,
            timestamp = datetime.fromisoformat(mqtt_sample['timestamp']),
            data = mqtt_sample['data'],
        )

from .component import Component, LifetimeComponent
from .facet import facet
from .receptacle import receptacle, ONE
from .interfaces import SampleInlet, Publisher

import aiomqtt
import asyncio
import abc
from dataclasses import dataclass


@facet('publisher', Publisher, (('publish', '_publish'),))
class MQTTClient(LifetimeComponent):
    def __init__(self, host, port = 1883):
        super().__init__(self._run)

        self.host = host
        self.port = port

        self.queue = asyncio.Queue()

    async def _publish(self, topic, message):
        await self.queue.put(self._PublishRequest(topic=topic, message=message))
        await asyncio.sleep(0)

    async def _run(self):
        async with aiomqtt.Client(hostname=self.host, port=self.port) as client:
            while True:
                publish_request = await self.queue.get()
                await client.publish(topic=publish_request.topic, payload=publish_request.message)

    @dataclass
    class _PublishRequest:
        topic: str
        message: bytes

@facet('sample_in', SampleInlet, (('consume_sample', '_publish_sample_by_tag'),))
@receptacle('publisher', Publisher, multiplicity=ONE)
class MQTT_PublishSampleTagToTopic(Component):
    def __init__(self, tag2topic):
        super().__init__()
        self.tag2topic = tag2topic
    async def _publish_sample_by_tag(self, sample):
        assert type(sample.data) is bytes
        await self._publisher.publish(topic=self.tag2topic[sample.tag], message=sample.data)

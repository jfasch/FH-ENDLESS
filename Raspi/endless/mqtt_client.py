from .sink import Sink
from .component import LifetimeComponent, facet
from .interfaces import Inlet

import aiomqtt
import asyncio
import abc
from dataclasses import dataclass


class Publisher(abc.ABC):
    @abc.abstractmethod
    async def publish(self, topic, message):
        raise NotImplementedError

@facet('publisher', Publisher, (('publish', '_publish'),))
class MQTTClient(LifetimeComponent):
    def __init__(self, host, port = 1883):
        super().__init__(self._run)

        self.host = host
        self.port = port

        self.queue = asyncio.Queue()

    async def _publish(self, topic, message):
        await self.queue.put(_PublishRequest(topic=topic, message=message))
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


from .sink import Sink
from .component import LifetimeComponent, facet
from .interfaces import Inlet

import aiomqtt
import asyncio


@facet('inlet', Inlet, (('consume_sample', '_consume_sample'),))
class MQTTSink(LifetimeComponent):
    def __init__(self, host, topics, payloadfunc, port = 1883):
        ''':param host: MQTT broker to establish a connection to
        :param payloadfunc: function that takes a Sample and converts it to a bytes object (the MQTT payload that is published)
        :param port: optional, defaults to 1883
        :param topics: mapping of incoming sample names to MQTT topics

        '''

        super().__init__(self._run)

        self.host = host
        self.port = port
        self.topics = topics
        self.payloadfunc = payloadfunc

        self.queue = asyncio.Queue()

    async def _consume_sample(self, sample):
        await self.queue.put(sample)
        await asyncio.sleep(0)

    async def _run(self):
        async with aiomqtt.Client(hostname=self.host, port=self.port) as client:
            while True:
                sample = await self.queue.get()
                topic = self.topics[sample.name]
                payload = self.payloadfunc(sample)
                await client.publish(topic, payload=payload)

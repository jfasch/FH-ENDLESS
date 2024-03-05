from endless.sink_mock import MockSink, have_n_samples
from endless.source_mqtt import MQTTSource
from endless.sample import Sample

from dataclasses import dataclass
import pytest
import aiomqtt
import asyncio


@pytest.mark.asyncio
async def test_basic(monkeypatch):
    @dataclass 
    class Message:
        payload: str

    class MyClient:  # aiomqtt.Client replacement
        def __init__(self, hostname, port):
            self.host = hostname
            self.port = port
            self._messages = [Message(payload='{"timestamp_ms": 100, "temperature": 37.5}'),
                             Message(payload='{"timestamp_ms": 200, "temperature": 38.3}'),
                             ]

        @property
        async def messages(self):
            for m in self._messages:
                yield m

        async def subscribe(self, topic):
            self.topic = topic

        async def __aenter__(self): return self
        async def __aexit__(self, exc_type, exc, tb): pass        

    monkeypatch.setattr(aiomqtt, 'Client', MyClient)

    async with asyncio.TaskGroup() as tg:
        have_2, cond = have_n_samples(2)
        sink = MockSink(cond)
        source = MQTTSource(name='a-name', host='blah.com', port=6666, topic='a-topic')

        sink.start(tg)
        source.start(tg, sink=sink)

        await have_2

        assert sink.samples[0] == Sample(name='a-name', timestamp_ms=100, temperature=pytest.approx(37.5))
        assert sink.samples[1] == Sample(name='a-name', timestamp_ms=200, temperature=pytest.approx(38.3))

        sink.stop()
        source.stop()

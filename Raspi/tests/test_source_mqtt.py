from endless.sink_mock import MockSink, have_n_samples
from endless.source_mqtt import MQTTSource
from endless.sample import Sample
from endless.runner import Runner

from dataclasses import dataclass
import pytest
import aiomqtt
from datetime import datetime


@pytest.mark.asyncio
async def test_basic(monkeypatch):
    @dataclass 
    class Message:
        payload: str

    ts1 = datetime(2024, 3, 14, 8, 46)
    ts2 = datetime(2024, 3, 14, 8, 47)

    class MyClient:  # aiomqtt.Client replacement
        def __init__(self, hostname, port):
            self.host = hostname
            self.port = port
            self._messages = [Message(payload='{"timestamp": "'+ts1.isoformat()+'", "temperature": 37.5}'),
                              Message(payload='{"timestamp": "'+ts2.isoformat()+'", "temperature": 38.3}'),
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

    have_2, cond = have_n_samples(2)
    sink = MockSink(cond)
    source = MQTTSource(name='a-name', host='blah.com', port=6666, topic='a-topic')
    source.connect(sink)

    async with Runner(sources=[source], sinks=[sink]) as runner:
        await have_2
        runner.stop()

    assert sink.samples[0] == Sample(name='a-name', timestamp=ts1, temperature=pytest.approx(37.5))
    assert sink.samples[1] == Sample(name='a-name', timestamp=ts2, temperature=pytest.approx(38.3))

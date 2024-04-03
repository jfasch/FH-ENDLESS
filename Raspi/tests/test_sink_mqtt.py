from endless.sink_mqtt import MQTTSink
from endless.sample import Sample
from endless.runner import Runner


import pytest
import aiomqtt
import asyncio
import json
from datetime import datetime


@pytest.mark.asyncio
async def test_basic(monkeypatch):
    out_host = out_port = out_topic = out_payload = None
    has_published = None

    class MyClient:  # aiomqtt.Client replacement
        def __init__(self, hostname, port):
            nonlocal out_host, out_port
            out_host = hostname
            out_port = port

        async def publish(self, topic, payload):
            nonlocal out_topic, out_payload
            out_topic = topic
            out_payload = payload

            has_published.set_result(True)

        async def __aenter__(self): return self
        async def __aexit__(self, exc_type, exc, tb): pass        

    monkeypatch.setattr(aiomqtt, 'Client', MyClient)

    def make_payload(sample):
        return json.dumps({
            'timestamp': sample.timestamp.isoformat(),
            'data': sample.data,
        })


    sink = MQTTSink(host='blah.com', port=6666, 
                    topics={
                        'sensor-1': 'topic-1',
                        'sensor-2': 'topic-2',
                    },
                    payloadfunc=make_payload)

    async with Runner(sources=(), sinks=[sink]) as runner:
        # first sample
        has_published = asyncio.get_running_loop().create_future()
        await sink.put(Sample(name='sensor-1', timestamp=datetime(2024, 3, 14, 8, 46), data=37.5))
        await has_published

        assert out_host == 'blah.com'
        assert out_port == 6666
        assert out_topic == 'topic-1' # remapped from 'sensor-1'

        py_payload = json.loads(out_payload)
        assert len(py_payload) == 2
        assert py_payload['timestamp'] == datetime(2024, 3, 14, 8, 46).isoformat()
        assert py_payload['data'] == pytest.approx(37.5)

        # second sample
        has_published = asyncio.get_running_loop().create_future()
        await sink.put(Sample(name='sensor-2', timestamp=datetime(2024, 3, 14, 8, 47), data=38.5))
        await has_published
        assert out_topic == 'topic-2'
        py_payload = json.loads(out_payload)
        assert len(py_payload) == 2
        assert py_payload['timestamp'] == datetime(2024, 3, 14, 8, 47).isoformat()
        assert py_payload['data'] == pytest.approx(38.5)

        runner.stop()

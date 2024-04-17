from endless.mqtt_client import MQTTClient
from endless.sample import Sample
from endless.runner import Runner, StopRunning


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

    mqtt_client = MQTTClient(host='blah.com', port=6666)

    async with Runner((mqtt_client,)):
        # first message
        has_published = asyncio.get_running_loop().create_future()
        await mqtt_client.publisher.publish(topic='topic1', message=b'message1')

        await has_published
        assert out_topic == 'topic1'
        assert out_payload == b'message1'

        # second message
        has_published = asyncio.get_running_loop().create_future()
        await mqtt_client.publisher.publish(topic='topic2', message=b'message2')

        await has_published
        assert out_topic == 'topic2'
        assert out_payload == b'message2'

        # I guess aiomqtt make connections on-demand, so it is
        # probably safest to check connection parameters at the very
        # end.
        assert out_host == 'blah.com'
        assert out_port == 6666

        raise StopRunning

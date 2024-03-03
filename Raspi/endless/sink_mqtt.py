import asyncio_mqtt as aiomqtt
import json


def _serialize(name, timestamp_ms, temperature):
    return json.dumps({
        'name': name,
        'timestamp_ms': timestamp_ms,
        'temperature': temperature,
    })

async def sink_to_mqtt(queue, host, port, topic):
    async with aiomqtt.Client(host, port) as client:
        while True:
            name, timestamp_ms, temperature = await queue.get()
            await client.publish(topic, _serialize(name, timestamp_ms, temperature))

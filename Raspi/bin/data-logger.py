#!/usr/bin/env python

from endless.source_can import CANSource
from endless.source_mqtt import MQTTSource
from endless.source_mock import MockSource
from endless.sink_composite import CompositeSink
from endless.sink_stdout import StdoutSink
from endless.sink_mqtt import MQTTSink
from endless import async_util

import asyncio


sources = [
    CANSource(name='CAN#42', can_iface='mein-test-can', can_id=42),
    CANSource(name='CAN#01', can_iface='mein-test-can', can_id=1),
#    MockSource(name='MOCK', timestamps = async_util.wall_timestamps(400, 400), temperature=37.5),
    MQTTSource(name='MQTT.egon', host='localhost', topic='egon'),
]

sink = CompositeSink(
    (StdoutSink(),
     MQTTSink(host='localhost',
              topics={
                  'CAN#42': 'can-42',
                  'CAN#01': 'can-01',
                  'MOCK': 'mock',
                  'MQTT.egon': 'mqtt-egon',
              })
     ))

async def main():
    async with asyncio.TaskGroup() as tg:
        sink.start(tg)

        for source in sources:
            source.start(tg, sink)

asyncio.run(main())

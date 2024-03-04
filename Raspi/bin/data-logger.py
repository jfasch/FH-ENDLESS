#!/usr/bin/env python

from endless.source_can import CANSource
from endless.sink_stdout import StdoutSink

import asyncio


sources = [
    CANSource(name='CAN#42', can_iface='mein-test-can', can_id=42),
    CANSource(name='CAN#01', can_iface='mein-test-can', can_id=1),
]

sink = StdoutSink()

async def main():
    tasks = []

    tasks += sink.start()

    for source in sources:
        tasks += source.start(sink)

    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        for t in tasks:
            t.cancel()

asyncio.run(main())

#!/usr/bin/env python

from endless.source_can import source_can
from endless.sink_stdout import sink_stdout

import asyncio


queue = asyncio.Queue()

sources = [
    source_can(name='CAN#42', can_iface = 'mein-test-can', can_id=42, queue=queue),
    source_can(name='CAN#01', can_iface = 'mein-test-can', can_id=1, queue=queue),
]

sink = sink_stdout(queue)

async def main():
    async with asyncio.TaskGroup() as tg:
        for source in sources:
            tg.create_task(source)
        tg.create_task(sink)

asyncio.run(main())

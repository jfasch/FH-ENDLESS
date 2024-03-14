#!/usr/bin/env python

import argparse
import asyncio


parser = argparse.ArgumentParser()
parser.add_argument('--configfile', type=str, required=True)
args = parser.parse_args()

config = open(args.configfile).read()
context = {}
exec(config, context)

sources = context['SOURCES']
sink = context['SINK']

async def main():
    async with asyncio.TaskGroup() as tg:
        sink.start(tg)

        for source in sources:
            source.start(tg, sink)

asyncio.run(main())

#!/usr/bin/env python

from endless.runner import Runner

import argparse
import asyncio


parser = argparse.ArgumentParser()
parser.add_argument('--configfile', type=str, required=True)
args = parser.parse_args()

config = open(args.configfile).read()
context = {}
exec(config, context)

sources = context['SOURCES']
sinks = context['SINKS']

async def main():
    async with Runner(sources=sources, sinks=sinks) as runner:
        pass

try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass

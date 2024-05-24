#!/usr/bin/env python

from endless.framework.runner import Runner

import argparse
import asyncio


parser = argparse.ArgumentParser()
parser.add_argument('--configfile', type=str, required=True)
args = parser.parse_args()

config = open(args.configfile).read()
context = {}
exec(config, context)

components = context['COMPONENTS']

async def main():
    async with Runner(components):
        pass

try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass

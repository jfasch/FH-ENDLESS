from .inlet import Inlet

import asyncio


class Outlet:
    def __init__(self):
        self.inlets = []

    def connect(self, inlet):
        assert isinstance(inlet, Inlet)
        self.inlets.append(inlet)

    async def produce_sample(self, sample):
        for inlet in self.inlets:
            await inlet.consume_sample(sample)

        # if sink's queue is unbounded (and timestamps are of the
        # quick-rush-through variant, without any real delay), then
        # queue.put() wont schedule and the entire program will
        # hang. add a manual scheduling point.

        # fixme: what if sink has no queue? isn't scheduling the
        # sink's responsibility?
        await asyncio.sleep(0)


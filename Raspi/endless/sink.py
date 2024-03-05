import asyncio
import abc
import sys


class Sink(abc.ABC):
    '''Base class for all classes that sink samples to somewhere.

    Sink objects employ a :doc:`python:library/asyncio-queue` that
    clients put samples into, and an internal task that pops elements
    off that queue.

    '''

    def __init__(self):
        self.task = None
        self.queue = asyncio.Queue()

    def start(self, tg):
        '''Start the object's own task and begin to handle incoming
        samples.

        :param tg: :doc:`asyncio.TaskGroup
                    <python:library/asyncio-task>` into which the
                    internal task is created

        '''
        self.task = tg.create_task(self._run())

    def stop(self):
        '''Cancel the object's task'''
        assert self.task is not None
        self.task.cancel()

    async def put(self, sample):
        '''Put a sample onto the object's queue. The object's task
        will pop it off the queue and handle it.

        '''
        await self.queue.put(sample)

    @abc.abstractmethod
    async def _run(self):
        '''Derived classes implement this to retrieve samples from the
        queue and handle them.

        '''
        pass

from .async_util import async_iter_queue
import asyncio


class _Lifetime:
    def __init__(self, mock_eh):
        self.eh = mock_eh
    def start(self):
        self.eh.start()
    async def stop(self):
        await self.eh.stop()

class _ErrorSink:
    def __init__(self, mock_eh):
        self.eh = mock_eh
    async def report_error(self, error):
        await self.eh.report_error(error)

class MockErrorHandler_Lifetime:
    def __init__(self):
        super().__init__()
        self.collected_errors = []

        self.task = None
        self.queue = asyncio.Queue()
        self.lifetime = _Lifetime(self)
        self.errors = _ErrorSink(self)

    async def report_error(self, error):
        await self.queue.put(error)

    def start(self):
        assert self.task is None
        self.task = asyncio.create_task(self._run())

    async def stop(self):
        self.task.cancel()
        await self.task
        self.task = None

    async def _run(self):
        try:
            async for error in async_iter_queue(self.queue):
                if error is None:       # shutdown requested
                    break
                self.collected_errors.append(error)
        except asyncio.CancelledError:
            # intercept cancellation and consume remaining errors
            while True:
                try:
                    error = self.queue.get_nowait()
                    self.collected_errors.append(error)
                except asyncio.QueueEmpty:
                    return

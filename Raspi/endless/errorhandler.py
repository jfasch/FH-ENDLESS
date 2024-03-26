import abc
import asyncio
from .async_util import iter_queue_blocking


class Error:
    '''Error object that is reported to an ErrorHandler.

    Currently exception information is the only error context that is
    reported. The idea is to define error handling semantics in terms
    of exception type (for example, FatalError, TransientError (num
    retries? backoff?), ...). The ``logging`` module sure has
    readymade solutions, but lets see.

    '''
    def __init__(self, exc_type, exc_value, exc_traceback):
        self.exc_type = exc_type
        self.exc_value = exc_value
        self.exc_traceback = exc_traceback

class ErrorReporter:
    '''Async context manager, used to report exceptions to an
    ErrorHandler object.

    Suggested usage:

    .. code-block:: python

       async with ErrorReporter(errorhandler):
           temperature = self.temperature(ts)

    '''
    def __init__(self, errorhandler):
        self.errorhandler = errorhandler
    async def __aenter__(self):
        return self
    async def __aexit__(self, exc_type, exc_value, exc_traceback):
        if exc_type is not None:
            assert exc_value is not None
            assert exc_traceback is not None
            await self.errorhandler.put(Error(exc_type=exc_type, exc_value=exc_value, exc_traceback=exc_traceback))

class ErrorHandler(abc.ABC):
    def __init__(self):
        self.task = None
        self.queue = asyncio.Queue()

    def start(self):
        self.task = asyncio.create_task(self._run())
    
    async def stop(self):
        assert self.task is not None
        self.stopped = asyncio.get_running_loop().create_future()
        await self.queue.put(None)   # None -> request shotdown
        await self.stopped

    async def put(self, error):
        await self.queue.put(error)

    async def _run(self):
        async for error in iter_queue_blocking(self.queue):
            if error is None:       # shutdown requested
                break
            await self._handle_error(error)

        while not self.queue.empty():
            error = self.queue.get_nowait()
            await self._handle_error(error)

        self.stopped.set_result(True)

    @abc.abstractmethod
    async def _handle_error(self, error):
        pass

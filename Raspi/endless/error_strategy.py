from .errorhandler import Error
from .errors import EndlessException


class ErrorStrategy:
    '''Async context manager, used to report exceptions.

    Suggested usage inside a ``Component`` subclass:

    .. code-block:: python

       async with ErrorStrategy(self.errors_to):
           temperature = self.temperature(ts)

    '''
    def __init__(self, errors_to):
        self.errors_to = errors_to
    async def __aenter__(self):
        return self
    async def __aexit__(self, exc_type, exc_value, exc_traceback):
        if exc_type is not None:
            assert exc_value is not None
            assert exc_traceback is not None
            await self.errors_to.report_error(Error(exc_type=exc_type, exc_value=exc_value, exc_traceback=exc_traceback))

            if issubclass(exc_type, EndlessException):
                return True

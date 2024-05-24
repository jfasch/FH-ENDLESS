from .errors import EndlessException

from contextlib import asynccontextmanager
import sys


@asynccontextmanager
async def ErrorStrategy(component):
    '''Async context manager, used to report exceptions inside
    components.

    Suggested usage (where ``self`` is the component):

    .. code-block:: python

       async with ErrorStrategy(self):
           temperature = self.temperature(ts)

    '''

    try:
        yield
    except:
        # this is new in 3.11. see python doc for sys.exception(), and
        # https://peps.python.org/pep-3134/
        exception = sys.exception()

        # should probably try/except around this, and terminate after
        # failure
        await component.errorhandler.report_exception(exception)

        if not isinstance(exception, EndlessException):
            raise

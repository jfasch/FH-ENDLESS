from .component import Component, LifetimeComponent
from .errorhandler import ErrorHandler

import asyncio
from contextlib import asynccontextmanager


class _NullErrorHandler(ErrorHandler):
    def report_exception(self, e):
        pass

class StopRunning(Exception): pass

@asynccontextmanager
async def Runner(components, errorhandler=None):
    for component in components:
        assert isinstance(component, Component), component

    if errorhandler is None:
        errorhandler = _NullErrorHandler()

    for component in components:
        component.errors_to(errorhandler)

    async with asyncio.TaskGroup() as tg:
        if hasattr(errorhandler, 'lifetime'):
            errorhandler.lifetime.start()

        for component in components:
            if isinstance(component, LifetimeComponent):
                component.start(tg)

        try:
            yield
        except StopRunning:
            for component in components:
                if isinstance(component, LifetimeComponent):
                    component.stop()
        finally:
            if hasattr(errorhandler, 'lifetime'):
                await errorhandler.lifetime.stop()

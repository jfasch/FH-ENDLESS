from .component import Component
from .errorhandler import ErrorHandler

from asyncio import TaskGroup


class _NullErrorHandler(ErrorHandler):
    def report_exception(self, e):
        pass

class Runner:
    def __init__(self, components, errorhandler=None):
        for component in components:

            assert isinstance(component, Component), component

        self.components = components
        if errorhandler is not None:
            self.errorhandler = errorhandler
        else:
            self.errorhandler = _NullErrorHandler()

        for component in self.components:
            component.errors_to(self.errorhandler)

        self.task_group = None

    async def __aenter__(self):
        if hasattr(self.errorhandler, 'lifetime'):
            self.errorhandler.lifetime.start()

        self.task_group = TaskGroup()
        await self.task_group.__aenter__()

        for component in self.components:
            if hasattr(component, "lifetime"):
                component.lifetime.start(self.task_group)

        return self

    async def __aexit__(self, exc_type, exc_value, exc_traceback):
        try:
            await self.task_group.__aexit__(exc_type, exc_value, exc_traceback)
        finally:
            if hasattr(self.errorhandler, 'lifetime'):
                await self.errorhandler.lifetime.stop()

    def stop(self):
        for component in self.components:
            if hasattr(component, "lifetime"):
                component.lifetime.stop()

from .errorhandler import ErrorHandler

import abc


class Component:
    def __init__(self):
        self.errorhandler = None
        self._facets = {}
        self._receptacles = {}

    def errors_to(self, errorhandler):
        assert self.errorhandler is None
        assert isinstance(errorhandler, ErrorHandler), errorhandler
        self.errorhandler = errorhandler

class LifetimeComponent(Component):
    def __init__(self, func):
        super().__init__()
        self.func = func
        self.task = None
    def start(self, taskgroup):
        assert self.task is None
        self.task = taskgroup.create_task(self.func())
    def stop(self):
        assert self.task is not None
        self.task.cancel()
        self.task = None


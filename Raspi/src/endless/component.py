from .errorhandler import ErrorHandler

import abc


class Component:
    '''Base class for components.

    Provides basic functionality that components inherit.

    * Components are guaranteed to have an errorhandler, via the
      :attr:`errorhandler` property
    * Components usually have :class:`facets <endless.facet.facet>` 
      and :class:`receptacles <endless.facet.facet>`

    '''

    def __init__(self):
        self.errorhandler = None
        self._facets = {}
        self._receptacles = {}

    def errors_to(self, errorhandler):
        assert self.errorhandler is None
        assert isinstance(errorhandler, ErrorHandler), errorhandler
        self.errorhandler = errorhandler

class LifetimeComponent(Component):
    '''Base class for components whose lifetime needs to be managed.'''

    def __init__(self, func):
        super().__init__()
        self.func = func
        self.task = None
    def start(self, taskgroup):
        '''Create task'''
        assert self.task is None
        self.task = taskgroup.create_task(self.func())
    def stop(self):
        '''Cancel task'''
        assert self.task is not None
        self.task.cancel()
        self.task = None

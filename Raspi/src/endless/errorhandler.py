from .errors import EndlessException

import abc


class ErrorHandler(abc.ABC):
    '''Abstract base class for error handlers'''
    @abc.abstractmethod
    async def report_exception(self, exc):
        '''Report an exception

        :param exc: Exception
        '''
        raise NotImplementedError

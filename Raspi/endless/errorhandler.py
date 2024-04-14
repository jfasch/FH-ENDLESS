from .errors import EndlessException

import abc


class ErrorHandler(abc.ABC):
    @abc.abstractmethod
    async def report_exception(self, e):
        raise NotImplementedError

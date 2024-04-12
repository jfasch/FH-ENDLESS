import asyncio
import abc
import sys


class Source(abc.ABC):
    def __init__(self, name):
        self.name = name
        self.errorhandler = None

    def errors_to(self, errorhandler):
        self.errorhandler = errorhandler

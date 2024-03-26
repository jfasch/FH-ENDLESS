from .errorhandler import ErrorHandler

import sys


class MockErrorHandler(ErrorHandler):
    def __init__(self):
        super().__init__()
        self.errors = []

    async def _handle_error(self, error):
        self.errors.append(error)

        

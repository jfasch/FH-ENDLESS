from .errorhandler import ErrorHandler


class Component:
    def __init__(self):
        self.errorhandler = None

    def errors_to(self, errorhandler):
        assert self.errorhandler is None
        assert isinstance(errorhandler, ErrorHandler)
        self.errorhandler = errorhandler

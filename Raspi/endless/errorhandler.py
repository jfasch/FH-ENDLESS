from .errors import EndlessException


class Error:
    '''Error object that is reported to an ErrorHandler.

    Currently exception information is the only error context that is
    reported. The idea is to define error handling semantics in terms
    of exception type (for example, FatalError, TransientError (num
    retries? backoff?), ...). The ``logging`` module sure has
    readymade solutions, but lets see.

    '''
    def __init__(self, exc_type, exc_value, exc_traceback):
        self.exc_type = exc_type
        self.exc_value = exc_value
        self.exc_traceback = exc_traceback


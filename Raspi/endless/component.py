class Errors:
    def __init__(self):
        self.errorhandler = None
    def connect(self, errorhandler):
        assert self.errorhandler is None
        self.errorhandler = errorhandler
    async def report_error(self, error):
        await self.errorhandler.report_error(error)

class Component:
    def __init__(self):
        self.errors_to = Errors()
